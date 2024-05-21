import asyncio
import websockets
from evdev import InputDevice, categorize, ecodes
import logging
import subprocess
import requests
import json
import time

connected = set()
loggerLevel = logging.DEBUG
logging.basicConfig(level=loggerLevel)
waitTime = 5
last_submissions = {}

def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        logging.debug('\n Line: %s\n ', line)
        if line.startswith('Serial'):
            logging.debug('\n Serial: %s\n ', line.split(':')[1].strip())
            return line.split(':')[1].strip()
        
scannerId = get_serial_number()

def remove_old_submissions(lastSubmissions):
    logging.debug('\n Removing old submissions\n ')
    current_time = time.time() * 1000
    one_hour_in_milliseconds = 60 * 60 * 1000
    braceletIds_to_remove = []

    for bracelet_id, time_stamp in lastSubmissions.items():
        logging.debug('\n lastSubmissions: %s\n ', lastSubmissions)
        logging.debug('\n bracelet_id: %s\n ', bracelet_id)
        logging.debug('\n time_stamp: %s\n ', time_stamp)
        logging.debug('\n current_time: %s\n ', current_time)
        logging.debug('\n difference: %s\n ', current_time - time_stamp)
        if current_time - time_stamp > one_hour_in_milliseconds:
            braceletIds_to_remove.append(bracelet_id)

    for id in braceletIds_to_remove:
        item = lastSubmissions[id]
        logging.debug('\n Removed: %s\n ', item)
        del lastSubmissions[id]

def getTimeDifference(braceletId:str):
    logging.debug('\n Getting time difference\n ')
    timestamp = int(time.time() * 1000)
    timeDifference = (timestamp - last_submissions.get(braceletId,timestamp))/1000
    logging.debug('\n Message: %s\n ', braceletId)
    logging.debug('\n Last submissions: %s\n ', last_submissions)
    logging.debug('\n Timestamp: %s\n ', timestamp)
    logging.debug('\n Time Difference: %s seconds\n ', timeDifference)
    logging.debug('\n Wait Time: %s seconds\n ', waitTime)
    return timestamp,timeDifference

def sendToConnectedClients(scannerId, braceletId,status, response):
    logging.debug('\n Sending to connected clients\n ')
    logging.debug('\n Connected clients: %s\n ', connected)
    if response is None:
        body={
            'scanner_id': scannerId, 
            'bracelet_id': braceletId,
            'status': status,
            'response': None
        }
    else:
        body={
            'scanner_id': scannerId, 
            'bracelet_id': braceletId,
            'status': status,
            'response': json.dumps(response.text)
        }
    logging.info('\n body: %s\n ', body)
    websockets.broadcast(connected, json.dumps(body))

def sendToDb(scannerId:str, braceletId:str, timestamp:int):
    last_submissions[braceletId] = timestamp
    formData = {
                'bracelet_id': braceletId,
                'scanner_id': scannerId,
    }
    liveUrl='https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet'
    response = requests.post(liveUrl, data=formData)
    return response
       
async def usbScanner(scannerId:str):
    dev = InputDevice('/dev/input/event0')
    logging.debug("\n Waiting for RFID read...\n ")
    braceletId = ""
    for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                    if key_event.keycode == "KEY_ENTER":
                        logging.info("\n ID: %s\n ", braceletId)
                        sendToConnectedClients(scannerId, braceletId,'INITIAL_SCAN', None)
                        timestamp, timeDifference = getTimeDifference(braceletId)
                        if braceletId in last_submissions and timeDifference < waitTime:
                            sendToConnectedClients(scannerId, braceletId,'TOO_SOON', None)
                        else:
                            response = sendToDb(scannerId, braceletId, timestamp)
                            sendToConnectedClients(scannerId, braceletId,'SCAN_COMPLETE', response)                                           
                        break
                    else:
                        braceletId += key_event.keycode[-1]

async def handler(websocket):
    global scannerId
    try:
        if connected:
            logging.debug('\n Clearing connections\n ')
            connected.clear()
        logging.debug('\n Connected: %s\n ', websocket.remote_address)
        logging.info('\n Scanner ID: %s\n ', scannerId)
        connected.add(websocket)
        sendToConnectedClients(scannerId, None, 'INITIAL_CONNECTION', None)
        await usbScanner(scannerId)
    finally:
        timestamp = int(time.time() * 1000)
        logging.debug('\n Done: %s\n ', timestamp)
        remove_old_submissions(last_submissions)
        # connected.remove(websocket)
        # sendToConnectedClients(scannerId, None, 'DISCONNECTED', None)

async def main():
    try:
        logging.info("\n Starting server\n ")
        async with websockets.serve(handler, "", 8765):
            await asyncio.Future()  # run forever
    except websockets.ConnectionClosed:
        logging.debug("\n Connection closed\n ")
    except websockets.exceptions.ConnectionClosedOK:
        logging.debug("\n Connection closed OK\n ")
    except websockets.exceptions.ConnectionClosedError:
        logging.debug("\n Connection closed unexpectedly\n ")

if __name__ == "__main__":
    # logger1 = logging.getLogger('websockets')
    # logger1.setLevel(loggerLevel)
    # logger1.addHandler(logging.StreamHandler())
    # logger2 = logging.getLogger('evdev')
    # logger2.setLevel(loggerLevel)
    # logger2.addHandler(logging.StreamHandler())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("\n Ended by user\n ")