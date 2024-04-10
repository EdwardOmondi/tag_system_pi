import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
print("Welcome to the RFID system")
def read():
    try:
        while True:
            id, text = reader.read()
    except KeyboardInterrupt:
        print("Ended by user")
    finally:
        GPIO.cleanup()

def write(text):
    try:
        while True:
            reader.write(text)
    except KeyboardInterrupt:
        print("Ended by user")
    finally:
        GPIO.cleanup()
