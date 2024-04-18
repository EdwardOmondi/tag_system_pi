#!/usr/bin/env python

import asyncio
import websockets
import json
import time
import requests

scannerId=1
waitTime=100
async def handler(websocket):
    last_submissions = {}
    while True:
        timestamp = int(time.time() * 1000)
        if id in last_submissions and timestamp - last_submissions[id] < waitTime*1000:
            print("Submission for this ID must be at least",waitTime," seconds apart.",id)
        else:
            last_submissions[id] = timestamp
            formData = {
                'bracelet_id':2,
                'scanner_id': 2345689,
            }
            response = requests.post('https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet', data=formData)
            print('response: ',response.json(),'\n')
            await websocket.send(json.dumps(response.json()))
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
