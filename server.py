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

id = None  # Initialize id to None
text = None  # Initialize text to None

def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()

def read_rfid(): 
    global id, text
    id, text = reader.read()
        
async def producer():
    logging.debug('producer')
    scannerId = get_serial_number()
    logging.info('Scanner ID: %s', scannerId)
    # Start a new thread to read the RFID tag
    threading.Thread(target=read_rfid).start()
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
        id = None
        return json.dumps(body)
    else:
        logging.debug('No RFID detected')

async def producer_handler(websocket):
    logging.debug('producer_handler')
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
        logging.info('Starting server')
        async with websockets.serve(handler, "", 8765):
            await asyncio.Future()
    except KeyboardInterrupt:
        logging.info('Server stopped by keyboard interrupt')
    except websockets.exceptions.ConnectionClosed:
        logging.info('Connection closed')
    except Exception as e:
        logging.error('Error: %s', e)
    finally:
        logging.info('Cleaning up GPIO')
        GPIO.cleanup()
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())