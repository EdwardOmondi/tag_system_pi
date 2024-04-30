#!/usr/bin/env python

import asyncio
import websockets
import json
import time
import requests
import subprocess
import logging

logging.basicConfig(level=logging.INFO)

def get_serial_number():
    return "1234567890"  # Mocked serial number

class SimpleMFRC522:  # Mocked class
    def read(self):
        return "1234567890", "Test text"  # Mocked ID and text

async def send_message_every_10_seconds(websocket):
    scanner_id = get_serial_number()
    while True:
        await websocket.send(json.dumps({'Result': -3,'Message': scanner_id}))
        await asyncio.sleep(10)  # pause for 10 seconds

async def handle_rfid_scan(websocket, path):
    scanner_id = get_serial_number()
    logging.info("Scanner ID: %s", scanner_id)    
    asyncio.create_task(send_message_every_10_seconds(websocket))
    reader = SimpleMFRC522()
    last_submissions = {}
    video_stopped = True  # Add a flag to track if the video has stopped
    while True:
        if not video_stopped:
            # Listen for incoming messages
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                data = json.loads(message)
                if data.get('Message') == 'Video Stopped':
                    video_stopped = True
            except asyncio.TimeoutError:
                pass
        else:
            id, text = reader.read()
            await asyncio.sleep(5)  # pause for 10 seconds
            if id is not None:
                timestamp = int(time.time() * 1000)
                if id in last_submissions and timestamp - last_submissions[id] < waitTime*1000:
                    errorMessage="Please wait at least "+str(waitTime)+" seconds before you try scanning again."
                    logging.warning("%s %s", errorMessage, id)
                    await websocket.send(json.dumps({'Result': -2,'Message': errorMessage}))
                else:
                    last_submissions[id] = timestamp
                    await websocket.send(json.dumps({'Result': -1,'Message': 'Bracelet scanned. Analyzing data...'}))
                    formData = {
                        'bracelet_id':id,
                        'scanner_id': scanner_id,
                    }
                    logging.info('formData: %s', formData)
                    # response = requests.post('https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet', data=formData)
                    # if response.status_code == 200:
                    #     logging.info('response: %s', response.json())
                    #     video_stopped = False  # Reset the flag after successful submission
                    #     await websocket.send(json.dumps(response.json()))
                    # else:
                    #     logging.error('response: %s', response.content)
                    #     await websocket.send(json.dumps({'Message': 'Failed to submit data'}))
                    await websocket.send(json.dumps({'Result': 1,'Message': 'Mocked response'}))

async def main():
    try:
        logging.info("Starting server")
        async with websockets.serve(handle_rfid_scan, "", 8765):
            await asyncio.Future()
    except KeyboardInterrupt:
        logging.info("Ended by user")
    except websockets.exceptions.ConnectionClosed:
        logging.info("Connection closed Ok")
        # await main()

if __name__ == "__main__":
    waitTime = 10  # Define waitTime here
    asyncio.run(main())