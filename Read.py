import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
try:
    while True:
        id, text = reader.read()
        print(f"ID: {id}")
        print(f"Text: {text}")
except KeyboardInterrupt:
    print("Ended by user")
finally:
    GPIO.cleanup()