#!/usr/bin/env python

import asyncio
import websockets
import requests
import subprocess
import logging
import json

connected = set()
logging.basicConfig(level=logging.INFO)

def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()


async def handler(websocket):
    logging.info('\nConnected: %s\n', websocket.remote_address)
    scannerId = get_serial_number()
    logging.info('\nScanner ID: %s\n', scannerId)
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            body={'scanner_id': scannerId, 
                  'bracelet_id': message,
                  'status': 'INITIAL_SCAN',
                  'response': None
                  }
            logging.info('\nbody: %s\n', body)
            # Broadcast a message to all connected clients.
            websockets.broadcast(connected, json.dumps(body))
            if message != '-1':
                formData = {
                        'bracelet_id':message,
                        'scanner_id': scannerId,
                }
                response = requests.post('https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet', data=formData)
                body={'scanner_id': scannerId, 
                      'bracelet_id': message,
                      'status': 'SCAN_COMPLETE',
                      'response': json.dumps(response.json())
                      }
                logging.info('\nbody: %s\n', body)
                # Broadcast a message to all connected clients.
                websockets.broadcast(connected, json.dumps(body))
            else:
                logging.info('\nbody: %s\n', body)
    finally:
        # Unregister.
        connected.remove(websocket)
async def main():
    try:
        logging.info("Starting server")
        async with websockets.serve(handler, "", 8765):
            await asyncio.Future()  # run forever
    except KeyboardInterrupt:
        logging.info("Server stopped")

if __name__ == "__main__":
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    asyncio.run(main())