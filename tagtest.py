import asyncio
import websockets
# from evdev import InputDevice, categorize, ecodes
import logging
import subprocess
import requests
import json
import time
import random
import string

connected = set()
loggerLevel = logging.INFO
logging.basicConfig(level=loggerLevel)
waitTime = 10
last_submissions = {}

def get_serial_number():
    return '0'

def generate_random_id(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def getTimeDifference(braceletId:str):
    logging.debug('\nGetting time difference\n')
    timestamp = int(time.time() * 1000)
    timeDifference = (timestamp - last_submissions.get(braceletId,timestamp))/1000
    logging.debug('\nMessage: %s\n', braceletId)
    logging.debug('\nLast submissions: %s\n', last_submissions)
    logging.debug('\nTimestamp: %s\n', timestamp)
    logging.debug('\nTime Difference: %s seconds\n', timeDifference)
    logging.debug('\nWait Time: %s seconds\n', waitTime)
    return timestamp,timeDifference

def sendToConnectedClients(scannerId, braceletId,status, response):
    logging.debug('\nSending to connected clients\n')
    logging.info('\Connected Clients: %s\n', connected)
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
    logging.info('\nbody: %s\n', body)
    websockets.broadcast(connected, json.dumps(body))

def sendToDb(scannerId:str, braceletId:str, timestamp:int):
    last_submissions[braceletId] = timestamp
    formData = {
                'bracelet_id': braceletId,
                'scanner_id': scannerId,
    }
    liveUrl='https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet'
    testUrl='https://httpbin.org/post'
    response = requests.post(liveUrl, data=formData)
    return response
       
async def usbScanner(scannerId:str):
    dev = InputDevice('/dev/input/event0')
    logging.debug("\nWaiting for RFID read...\n")
    braceletId = ""
    for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                    if key_event.keycode == "KEY_ENTER":
                        logging.info("\nID: %s\n", braceletId)
                        sendToConnectedClients(scannerId, braceletId,'INITIAL_SCAN', None)
                        timestamp, timeDifference = getTimeDifference(braceletId)
                        if braceletId in last_submissions and timeDifference < waitTime:
                            sendToConnectedClients(scannerId, braceletId,'TOO_SOON', None)
                        else:
                            response = sendToDb(scannerId, braceletId, timestamp)
                            sendToConnectedClients(scannerId, braceletId,'SCAN_COMPLETE', response)                                           
                        braceletId = ""
                    else:
                        braceletId += key_event.keycode[-1]


async def testEnv(scannerId:str):
    logging.debug("\nGenerating random IDs...\n")
    while True:
        braceletId = generate_random_id()
        logging.info("\nID: %s\n", braceletId)
        sendToConnectedClients(scannerId, braceletId,'INITIAL_SCAN', None)
        timestamp, timeDifference = getTimeDifference(braceletId)
        if braceletId in last_submissions and timeDifference < waitTime:
            sendToConnectedClients(scannerId, braceletId,'TOO_SOON', None)
        else:
            response = sendToDb(scannerId, braceletId, timestamp)
            sendToConnectedClients(scannerId, braceletId,'SCAN_COMPLETE', response)
        await asyncio.sleep(15)  # wait for 1 second before generating the next ID

async def handler(websocket):
    try:
        scannerId = get_serial_number()
        logging.debug('\nConnected: %s\n', websocket.remote_address)
        logging.info('\nScanner ID: %s\n', scannerId)
        connected.add(websocket)
        sendToConnectedClients(scannerId, None, 'INITIAL_CONNECTION', None)
        await testEnv(scannerId)
    finally:
        connected.remove(websocket)
        sendToConnectedClients(scannerId, None, 'DISCONNECTED', None)

async def main():
    try:
        logging.info("\nStarting server\n")
        async with websockets.serve(handler, "", 8765):
            await asyncio.Future()  # run forever
    except websockets.ConnectionClosed:
        logging.debug("\nConnection closed\n")
    except websockets.exceptions.ConnectionClosedOK:
        logging.debug("\nConnection closed OK\n")
    except websockets.exceptions.ConnectionClosedError:
        logging.debug("\nConnection closed unexpectedly\n")

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
        logging.info("\nEnded by user\n")