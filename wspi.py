#!/usr/bin/env python

import asyncio
import websockets
import json
import time


import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess

def get_serial_number():
    # Run the command and get the output
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout

    # Find the line with the serial number
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()

# Set the scannerId to the serial number
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
                print(text)
                print(id)
                
                message = {'scannerId': scannerId, 'braceletId': id, 'timestamp': timestamp * 1000}
                await websocket.send(json.dumps(message))
        # print(message)
        # await websocket.send(json.dumps(message))
        # await asyncio.sleep(5)
        try:
            data = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            if data is not None:
                reader.write(data)
                # message = json.loads(data)
                # print(message)
        except asyncio.TimeoutError:
            # print("Timeout")
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
        # print("GPIO cleanup")
