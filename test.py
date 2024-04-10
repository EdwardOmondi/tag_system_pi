from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522

app = Flask(__name__)
socketio = SocketIO(app)

# reader = SimpleMFRC522()

@app.route('/')
def index():
    return {'text': 'working'}  # Serve the client-side application

@socketio.on('read')
def handle_read():
    try:
        while True:
            # id, text = reader.read()
            # emit('rfid_read', {'id': id, 'text': text})
            emit('rfid_read', {'id': 'testId', 'text': 'testText'})
    except KeyboardInterrupt:
        print("Ended by user")
    finally:
        # GPIO.cleanup()
        pass

@socketio.on('write')
def handle_write(text):
    try:
        while True:
            # reader.write(text)
            # emit('rfid_write', {'text': text})
            emit('rfid_write', {'text': 'testText'})
    except KeyboardInterrupt:
        print("Ended by user")
    finally:
        # GPIO.cleanup()
        pass


if __name__ == '__main__':
    socketio.run(app)