# import time

# id = 1
# print ("Start...")
# try:
#     with open('/dev/tty0', 'r') as tty:
#         while True:
#             rfid = tty.readline()
#             time.sleep(0.5)
#             if rfid:
#                 rfid = str(rfid)[:10]
#                 msg = rfid
#                 print (msg)
#             time.sleep(0.5)
# except KeyboardInterrupt:
#     print("Ended by user")

# import serial

# serialPort = serial.Serial("/dev/tty0", 9600, timeout=0.5)

# try:
#     while True:
#         command = serialPort.read_until('\0', size=None)
#         commandString = command.decode('utf-8')

#         if len(commandString) > 0:
#             print(commandString)

# except KeyboardInterrupt:
#     print("Program terminated")

from evdev import InputDevice, categorize, ecodes

# Change /dev/input/eventX to the correct path for your device.
dev = InputDevice('/dev/input/eventX')

print("Starting to read from RFID reader...")

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))