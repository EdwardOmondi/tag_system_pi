#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess
import time
import requests


def get_serial_number():
    # Run the command and get the output
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True).stdout

    # Find the line with the serial number
    for line in cpuinfo.split('\n'):
        if line.startswith('Serial'):
            return line.split(':')[1].strip()

# Set the scannerId to the serial number
scannerId = get_serial_number()
reader = SimpleMFRC522()
waitTime=10
print("Started")
print("Use ctrl+c to exit program")

try:
    last_submissions = {}
    while True:
        id, text = reader.read()
        if id is not None:
            timestamp = int(time.time() * 1000)
            if id in last_submissions and timestamp - last_submissions[id] < waitTime*1000:
                print("Submission for this ID must be at least",waitTime," seconds apart.",id)
            else:
                last_submissions[id] = timestamp
                formData = {
                'bracelet_id':1,
                'scanner_id': 1,
                }
                response = requests.post('https://mobileappstarter.com/dashboards/kidzquad/apitest/user/scan_bracelet', data=formData)
                print(response.text)
            print(id)
            print(text)
            # write to a file
            with open('/var/www/html/bracelet_id.txt','w') as f:
                f.write(str(id))
except KeyboardInterrupt:
    print("Ended by user")
finally:
    GPIO.cleanup()