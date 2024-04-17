#!/usr/bin/env python

import asyncio
import websockets
import json
import time


import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

async def handler(websocket):
    message = {'operation': None, 'userId': None, 'braceletId': None,'timestamp': int(time.time() * 1000)}
    while True:
        id, text = reader.read()
        if id is not None:
            print(text)
            print(id)
            await websocket.send(json.dumps(text))
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