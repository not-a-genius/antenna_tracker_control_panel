import random
import sys
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time

DEBUG = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')



def test_socket():
    rand_num = random.randint(1, 100)
    socketio.emit('controller_data', {'l2': rand_num, 'r2': rand_num})

def send_data():
    print('Joystick thread started')
    while True:
    
        if DEBUG:
            print('Sending random data')
            test_socket()

        time.sleep(0.5)  # Adjust the frequency of updates


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')
    
    socketio.emit('welcome', {'data': 'ACK from server'});

    # Start the background thread
    threading.Thread(target=send_data).start()

if __name__ == '__main__': 
    socketio.run(app)