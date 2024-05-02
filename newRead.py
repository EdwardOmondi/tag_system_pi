from evdev import InputDevice, categorize, ecodes

# Change /dev/input/eventX to the correct path for your device.
dev = InputDevice('/dev/input/event0')

print("Starting to read from RFID reader...")

rfid_id = ""
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        if key_event.keystate == key_event.key_down:
            if key_event.keycode == "KEY_ENTER":
                print("RFID ID: ", rfid_id)
                rfid_id = ""
            else:
                rfid_id += key_event.keycode[-1]