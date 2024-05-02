#!/usr/bin/env python

import asyncio
import websockets
from mfrc522 import SimpleMFRC522
import logging
import RPi.GPIO as GPIO

logging.basicConfig(level=logging.INFO)

async def handler():
    uri = "ws://0.0.0.0:8765"
    async for websocket in websockets.connect(uri):
        logger.info("\nConnected to server\n")
        try:
            reader = SimpleMFRC522()
            logging.debug("\nWaiting for RFID read...\n")
            id, text = reader.read()
            logging.info("\nID: %s\n", id)
            await websocket.send(str(id))
        except websockets.ConnectionClosed:
            logging.debug("\nConnection closed\n")
            continue
        except websockets.exceptions.ConnectionClosedOK:
            logging.debug("\nConnection closed OK\n")
            continue
        except websockets.exceptions.ConnectionClosedError:
            logging.debug("\nConnection closed unexpectedly\n")
            continue
        except KeyboardInterrupt:
            logging.debug("\nEnded by user\n")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    asyncio.run(handler())