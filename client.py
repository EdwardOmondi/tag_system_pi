#!/usr/bin/env python

import asyncio
import websockets
from mfrc522 import SimpleMFRC522
import logging
import RPi.GPIO as GPIO


async def handler():
    uri = "ws://0.0.0.0:8765"
    async with websockets.connect(uri) as websocket:
        reader = SimpleMFRC522()
        try:
            while True:
                logging.debug("\nWaiting for RFID read...\n")
                id, text = reader.read()
                logging.debug("\nID: {id}\n")

                await websocket.send(str(id))
                logging.debug("\n>>> {id}\n")

                greeting = await websocket.recv()
                logging.debug("\n<<< {greeting}\n")
        except KeyboardInterrupt:
            logging.debug("\nEnded by user\n")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    asyncio.run(handler())