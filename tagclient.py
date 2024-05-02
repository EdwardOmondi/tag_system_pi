#!/usr/bin/env python

import asyncio
import websockets
from mfrc522 import SimpleMFRC522
import logging
import RPi.GPIO as GPIO
from evdev import InputDevice, categorize, ecodes

logging.basicConfig(level=logging.INFO)

async def mfrc522Scanner(websocket):
    reader = SimpleMFRC522()
    logging.debug("\nWaiting for RFID read...\n")
    id, text = reader.read()
    logging.info("\nID: %s\n", id)
    await websocket.send(str(id))

async def usbScanner(websocket):
    dev = InputDevice('/dev/input/event0')
    logging.debug("\nWaiting for RFID read...\n")
    rfid_id = ""
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                if key_event.keycode == "KEY_ENTER":
                    logging.info("\nID: %s\n", rfid_id)
                    await websocket.send(rfid_id)
                    rfid_id = ""
                else:
                    rfid_id += key_event.keycode[-1]

async def handler():
    uri = "ws://0.0.0.0:8765"
    async for websocket in websockets.connect(uri):
        logger.info("\nConnected to server\n")
        try:
            await usbScanner(websocket)
        except websockets.ConnectionClosed:
            logging.debug("\nConnection closed\n")
            continue
        except websockets.exceptions.ConnectionClosedOK:
            logging.debug("\nConnection closed OK\n")
            continue
        except websockets.exceptions.ConnectionClosedError:
            logging.debug("\nConnection closed unexpectedly\n")
            continue

if __name__ == "__main__":
    logger = logging.getLogger('websockets')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    try:
        asyncio.run(handler())
    except KeyboardInterrupt:
        logging.debug("\nEnded by user\n")
    finally:
        GPIO.cleanup()