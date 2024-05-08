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
loggerLevel = logging.DEBUG
logging.basicConfig(level=loggerLevel)
waitTime = 5
last_submissions = {}

def get_serial_number():
    # return '0'
    return '100000002f692899'

def generate_random_id(length=10):
    letters = string.ascii_lowercase
    # return ''.join(random.choice(letters) for _ in range(length))
    return 2643791645

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
    logging.info('\n Connected Clients: %s\n ', connected)
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
                'scanner_id': scannerId
    }
    liveUrl='https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet'
    response = requests.post(liveUrl, data=formData)
    return response
       
async def testEnv(scannerId:str):
    logging.debug("\n Generating random IDs...\n ")
    while True:
        braceletId = generate_random_id()
        logging.info("\n ID: %s\n ", braceletId)
        sendToConnectedClients(scannerId, braceletId,'INITIAL_SCAN', None)
        timestamp, timeDifference = getTimeDifference(braceletId)
        if braceletId in last_submissions and timeDifference < waitTime:
            sendToConnectedClients(scannerId, braceletId,'TOO_SOON', None)
        else:
            response = sendToDb(scannerId, braceletId, timestamp)
            sendToConnectedClients(scannerId, braceletId,'SCAN_COMPLETE', response)
        await asyncio.sleep(10)  # wait for 1 second before generating the next ID

async def handler(websocket):
    global connected, waitTime, last_submissions
    try:
        if connected:
            logging.debug('\n Clearing connections\n ')
            connected.clear()
        scannerId = get_serial_number()
        logging.debug('\n Connected: %s\n ', websocket.remote_address)
        logging.info('\n Scanner ID: %s\n ', scannerId)
        connected.add(websocket)
        sendToConnectedClients(scannerId, None, 'INITIAL_CONNECTION', None)
        await testEnv(scannerId)
    finally:
        connected.remove(websocket)
        sendToConnectedClients(scannerId, None, 'DISCONNECTED', None)

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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("\n Ended by user\n ")