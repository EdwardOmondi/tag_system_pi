#!/usr/bin/env python

import asyncio
import websockets
import json
import time
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess

def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()

async def handle_rfid_scan(websocket, path):
    scanner_id = get_serial_number()
    print("Scanner ID:", scanner_id)
    reader = SimpleMFRC522()
    last_submissions = {}
    while True:
        id, text = reader.read()
        if id is not None:
            timestamp = int(time.time() * 1000)
            if id in last_submissions and timestamp - last_submissions[id] < waitTime*1000:
                print("Submission for this ID must be at least", waitTime, " seconds apart.", id)
            else:
                last_submissions[id] = timestamp
                formData = {
                    'bracelet_id': 2,
                    'scanner_id': 2,
                    # 'bracelet_id':id,
                    # 'scanner_id': scanner_id,
                }
                response = requests.post('https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet', data=formData)
                if response.status_code == 200:
                    print('response: ', response, '\n')
                    await websocket.send(json.dumps(response.json()))
                else:
                    print('response: ', response.content, '\n')
                    await websocket.send(json.dumps({'Message': 'Failed to submit data'}))

async def main():
    try:
        print("Starting server")
        async with websockets.serve(handle_rfid_scan, "", 8765):
            await asyncio.Future()
    except KeyboardInterrupt:
        print("Ended by user")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed Ok")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    waitTime = 10  # Define waitTime here
    asyncio.run(main())
