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

scannerId = get_serial_number()
print("Scanner ID:", scannerId)
reader = SimpleMFRC522()
waitTime=10
async def handler(websocket):
    last_submissions = {}
    while True:
        id, text = reader.read()
        if id is not None:
            timestamp = int(time.time() * 1000)
            if id in last_submissions and timestamp - last_submissions[id] < waitTime*1000:
                print("Submission for this ID must be at least",waitTime," seconds apart.",id)
            else:
                last_submissions[id] = timestamp
                formData = {
                'bracelet_id':2,
                'scanner_id': 2,
                # 'bracelet_id':id,
                # 'scanner_id': scannerId,
                }
                response = requests.post('https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet', data=formData)
                print('response: ',response.json(),'\n')
                await websocket.send(json.dumps(response.json()))
        try:
            data = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            if data is not None:
                reader.write(data)
        except asyncio.TimeoutError:
            pass


async def main():
    async with websockets.serve(handler, "", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        print("Starting server")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Ended by user")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed Ok")
    finally:
        GPIO.cleanup()
