#!/usr/bin/env python

import asyncio
import websockets
from mfrc522 import SimpleMFRC522
import logging
import RPi.GPIO as GPIO


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        reader = SimpleMFRC522()
        try:
            while True:
                id, text = reader.read()
                logging.debug(f"ID: {id}")

                await websocket.send(str(id))
                logging.debug(f">>> {id}")

                greeting = await websocket.recv()
                logging.debug(f"<<< {greeting}")
        except KeyboardInterrupt:
            logging.debug("Ended by user")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    asyncio.run(hello())