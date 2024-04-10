#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
print("Started")
print("Use ctrl+c to exit program")

try:
    while True:
        id, text = reader.read()
        print(id)
        print(text)
except KeyboardInterrupt:
    print("Ended by user")
finally:
    GPIO.cleanup()