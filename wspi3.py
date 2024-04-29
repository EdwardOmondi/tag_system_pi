#!/usr/bin/env python

import asyncio
import websockets
import json
import time
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from localMFRC522 import MFRC522
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

# reader = MFRC522()


def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()
        
# def read(trailer_block, key, block_addrs):
#     (status, TagType) = reader.Request(reader.PICC_REQIDL)
#     if status != reader.MI_OK:
#         return None, None
#     (status, uid) = reader.Anticoll()
#     if status != reader.MI_OK:
#         return None, None
#     id = uid
#     reader.SelectTag(uid)
#     status = reader.Authenticate(
#         reader.PICC_AUTHENT1A, trailer_block , key, uid)
#     data = []
#     text_read = ''
#     if status == reader.MI_OK:
#         for block_num in block_addrs:
#             block = reader.ReadTag(block_num)
#             if block:
#                 data += block
#         if data:
#             text_read = ''.join(chr(i) for i in data)
#     reader.StopAuth()
#     return id, text_read

async def handle_rfid_scan(websocket, path):
    scanner_id = get_serial_number()
    logging.info("Scanner ID: %s", scanner_id)    
    await websocket.send(json.dumps({'Result': -3,'Message': scanner_id}))
    reader = SimpleMFRC522()
    last_submissions = {}
    while True:
        # id, text = read(7, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], [8])
        id, text = reader.read()
        if id is not None:
            timestamp = int(time.time() * 1000)
            if id in last_submissions and timestamp - last_submissions[id] < waitTime*1000:
                errorMessage="Please wait at least "+str(waitTime)+" seconds before you try scanning again."
                logging.warning("%s %s", errorMessage, id)
                await websocket.send(json.dumps({'Result': -2,'Message': errorMessage}))
            else:
                last_submissions[id] = timestamp
                await websocket.send(json.dumps({'Result': -1,'Message': 'Bracelet scanned. Analyzing data...'}))
                formData = {
                    'bracelet_id': 2,
                    'scanner_id': 2,
                    # 'bracelet_id':id,
                    # 'scanner_id': scanner_id,
                }
                response = requests.post('https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet', data=formData)
                if response.status_code == 200:
                    logging.info('response: %s', response.json())
                    await websocket.send(json.dumps(response.json()))
                else:
                    logging.error('response: %s', response.content)
                    await websocket.send(json.dumps({'Message': 'Failed to submit data'}))

async def main():
    try:
        logging.info("Starting server")
        async with websockets.serve(handle_rfid_scan, "", 8765):
            await asyncio.Future()
    except KeyboardInterrupt:
        logging.info("Ended by user")
    except websockets.exceptions.ConnectionClosed:
        logging.info("Connection closed Ok")
    finally:
        logging.info("Cleaning up GPIO")
        GPIO.cleanup()

if __name__ == "__main__":
    waitTime = 10  # Define waitTime here
    asyncio.run(main())
