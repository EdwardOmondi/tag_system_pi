#!/usr/bin/env python

import asyncio
import websockets
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess
import requests
import json
import logging

connected = set()
reader = SimpleMFRC522()

def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()
        
async def producer():
    logging.info('producer')
    scannerId = get_serial_number()
    logging.info('Scanner ID: %s', scannerId)
    id, text = reader.read()
    if id is not None:
        logging.info('RFID detected: %s', id)
        formData = {
            'bracelet_id':id,
            'scanner_id': scannerId,
        }
        liveUrl='https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet'
        testUrl='https://httpbin.org/post'
        response = requests.post(testUrl, data=formData)
        body = {'piId': scannerId, 'braceletId': id, 'response': response.json()}
        logging.info('body: %s', body) 
        return json.dumps(body)
    else:
        logging.info('No RFID detected')

async def producer_handler(websocket):
    logging.info('producer_handler')
    while True:
        message = await producer()
        await websocket.send(message)

async def consumer(message):
    print(f"Received message: {message}")

async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)

async def handler(websocket):
    await asyncio.gather(
        consumer_handler(websocket),
        producer_handler(websocket),
    )

async def main():
    async with websockets.serve(producer_handler, "", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Starting server')
    asyncio.run(main())