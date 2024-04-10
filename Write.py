#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
print("Started")
print("Use ctrl+c to exit program")

try:
    while True:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
except KeyboardInterrupt:
    print("Ended by user")
finally:
    GPIO.cleanup()