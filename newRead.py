import time

id = 1
print ("Start...")
try:
    with open('/dev/tty0', 'r') as tty:
        while True:
            rfid = tty.readline()
            time.sleep(0.5)
            if rfid:
                rfid = str(rfid)[:10]
                msg = rfid
                print (msg)
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Ended by user")