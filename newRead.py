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

import serial

# Set up the serial port to read from the USB reader.
serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)

try:
    while True:
        # Read from the USB reader until a null character is received.
        command = serialPort.read_until('\0', size=None)
        commandString = command.decode('utf-8')

        # If a command was received, print it.
        if len(commandString) > 0:
            print(commandString)

except KeyboardInterrupt:
    print("Program terminated")