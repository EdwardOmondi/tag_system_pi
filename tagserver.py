#!/usr/bin/env python

import asyncio
import websockets
import requests
import subprocess
import logging
import json
import time

connected = set()
logging.basicConfig(level=logging.DEBUG)
waitTime = 10  # Define waitTime here
last_submissions = {}

def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()


async def handler(websocket):
    logging.debug('\nConnected: %s\n', websocket.remote_address)
    scannerId = get_serial_number()
    logging.info('\nScanner ID: %s\n', scannerId)
    # Register.
    connected.add(websocket)
    body={
        'scanner_id': scannerId, 
        'bracelet_id': None,
        'status': 'INITIAL_CONNECTION',
        'response': None
    }
    websockets.broadcast(connected, json.dumps(body))
    try:
        async for message in websocket:
            body={
                'scanner_id': scannerId, 
                'bracelet_id': message,
                'status': 'INITIAL_SCAN',
                'response': None
            }
            logging.info('\nbody: %s\n', body)
            # Broadcast a message to all connected clients.
            websockets.broadcast(connected, json.dumps(body))
            timestamp = int(time.time() * 1000)
            logging.debug('\nMessage: %s\n', message)
            logging.debug('\nLast submissions: %s\n', last_submissions)
            logging.debug('\nTimestamp: %s\n', timestamp)
            logging.debug('\nTime Difference: %s\n', timestamp - last_submissions.get(message,0))
            if message in last_submissions and timestamp - last_submissions.get(message,0) < waitTime*1000:
                body={
                    'scanner_id': scannerId, 
                    'bracelet_id': message,
                    'status': 'TOO_SOON',
                    'response': None
                }
                logging.info('\nbody: %s\n', body)
                websockets.broadcast(connected, json.dumps(body))                
            else:
                last_submissions[message] = timestamp
                formData = {
                        'bracelet_id':message,
                        'scanner_id': scannerId,
                }
                liveUrl='https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet'
                testUrl='https://httpbin.org/post'
                response = requests.post(liveUrl, data=formData)
                body={
                    'scanner_id': scannerId, 
                    'bracelet_id': message,
                    'status': 'SCAN_COMPLETE',
                    'response': json.dumps(response.text)
                }
                logging.info('\nbody: %s\n', body)
                # Broadcast a message to all connected clients.
                websockets.broadcast(connected, json.dumps(body))

    except websockets.ConnectionClosed:
        logging.debug("\nConnection closed\n")
    except websockets.exceptions.ConnectionClosedOK:
        logging.debug("\nConnection closed OK\n")
    except websockets.exceptions.ConnectionClosedError:
        logging.debug("\nConnection closed unexpectedly\n")
    finally:
        # Unregister.
        connected.remove(websocket)

async def main():
    try:
        logging.info("\nStarting server\n")
        async with websockets.serve(handler, "", 8765):
            await asyncio.Future()  # run forever
    except KeyboardInterrupt:
        logging.info("\nServer stopped\n")

if __name__ == "__main__":
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.debug("\nEnded by user\n")