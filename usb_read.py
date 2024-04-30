import serial
import time

# Define the USB port
usb_port = '/dev/ttyAMA1'  # Use the appropriate USB port

# Create a serial object
ser = serial.Serial(usb_port, baudrate=9600, timeout=1)

try:
    while True:
        # Read data from the RF DR-300
        data = ser.readline().decode().strip()
        if data:
            print("RFID Tag ID:", data)
        time.sleep(0.1)  # Add a small delay to avoid high CPU usage
except KeyboardInterrupt:
    ser.close()
