#!/usr/bin/env python

import asyncio
import websockets
from mfrc522 import SimpleMFRC522
import logging
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.INFO)


async def handler():
    uri = "ws://0.0.0.0:8765"
    async with websockets.connect(uri) as websocket:
        reader = SimpleMFRC522()
        try:
            while True:
                logging.debug("\nWaiting for RFID read...\n")
                id, text = reader.read()
                logging.info("\nID: {id}\n")

                await websocket.send(str(id))
                logging.info("\n>>> {id}\n")
        except KeyboardInterrupt:
            logging.debug("\nEnded by user\n")
        except websockets.exceptions.ConnectionClosedError:
            logging.debug("\nConnection closed unexpectedly\n")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    asyncio.run(handler())