#!/usr/bin/env python

import asyncio
import websockets
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess
import requests
import json
import logging
import threading

connected = set()
reader = SimpleMFRC522()


def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()
        
async def producer():
    logging.debug('\nproducer')
    scannerId = get_serial_number()
    logging.info('\nScanner ID: %s', scannerId)
    # Start a new thread to read the RFID tag
    id, text = reader.read()
    logging.debug('\nid: %s', id)
    if id is not None:
        logging.info('\nRFID detected: %s', id)
        formData = {
            'bracelet_id':id,
            'scanner_id': scannerId,
        }
        liveUrl='https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet'
        testUrl='https://httpbin.org/post'
        response = requests.post(testUrl, data=formData)
        body = {'piId': scannerId, 'braceletId': id, 'response': response.json()}
        logging.info('\nbody: %s', body) 
        id = None
        return json.dumps(body)
    else:
        logging.debug('\nNo RFID detected')

async def producer_handler(websocket):
    logging.debug('\nproducer_handler')
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
    try:
        logging.info('\nStarting server')
        async with websockets.serve(handler, "", 8765):
            await asyncio.Future()
    except KeyboardInterrupt:
        logging.info('\nServer stopped by keyboard interrupt')
    except websockets.exceptions.ConnectionClosed:
        logging.info('\nConnection closed')
    except Exception as e:
        logging.error('\nError: %s', e)
    finally:
        logging.info('\nCleaning up GPIO')
        GPIO.cleanup()
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())