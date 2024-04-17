#!/usr/bin/env python

import asyncio
import websockets
import json
import time


# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522

# reader = SimpleMFRC522()
scannerId=1
waitTime=6
async def handler(websocket):
    last_submissions = {}
    while True:
        timestamp = int(time.time() * 1000)
        # id, text = reader.read()
        # if id is not None:
        #     await websocket.send(json.dumps(text))
        if id in last_submissions and timestamp - last_submissions[id] < waitTime*1000:
            print("Submission for this ID must be at least",waitTime," seconds apart.",id)
        else:
            last_submissions[id] = timestamp
            message = {'scannerId': scannerId, 'braceletId': 1,'timestamp': int(time.time() * 1000)}
            print(message)
            await websocket.send(json.dumps(message))
            await asyncio.sleep(5)
        try:
            data = await asyncio.wait_for(websocket.recv(), timeout=0.5)
            if data is not None:
                # reader.write(data)
                message = json.loads(data)
                print(message)
        except asyncio.TimeoutError:
            print("Timeout")
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
        # GPIO.cleanup()
        print("GPIO cleanup")
