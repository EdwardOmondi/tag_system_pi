#!/usr/bin/env python

import asyncio
import websockets
import requests
import subprocess
import logging
import json

connected = set()

def get_serial_number():
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()

async def handler(websocket):
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            # Broadcast to all connected clients.
            body={'piId': get_serial_number(), 'braceletId': message,'status': 'INITIAL_SCAN','response': None}
            logging.info('\nbody: %s\n', body)
            await asyncio.wait([ws.send(json.dumps(body)) for ws in connected])
            formData = {
                    'bracelet_id':id,
                    'scanner_id': scanner_id,
            }
            response = requests.post('https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet', data=formData)
            body['status'] = 'SCAN_COMPLETE'
            body['response'] = response.json()
            logging.info('\nbody: %s\n', body)
            await asyncio.wait([ws.send(json.dumps(body)) for ws in connected])
    finally:
        # Unregister.
        connected.remove(websocket)

async def main():
    async with websockets.serve(handler, "", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())