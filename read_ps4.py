import random
import sys
from flask import Flask, render_template
from flask_socketio import SocketIO
import pygame
import threading
import time

DEBUG = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')


# Initialize pygame and the joystick

pygame.init()
pygame.joystick.init()


# Check for joysticks
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joysticks detected")
    sys.exit() 

joystick = pygame.joystick.Joystick(0)
joystick.init()

print('Initialized Joystick : %s' % joystick.get_name())



def test_socket():
    rand_num = random.randint(1, 100)
    socketio.emit('controller_data', {'l2': rand_num, 'r2': rand_num})

def read_joystick():
    print('Joystick thread started')
    while True:
        pygame.event.pump()  # Process event queue
        l2_x = joystick.get_axis(1)  # Axis number for L2 might differ
        l2_y = joystick.get_axis(2)  # Axis number for R2 might differ

        print('L2 X: %s, L2 Y: %s' % (l2_x, l2_y))
        #Send the joystick values to the client
        socketio.emit('controller_data', {'l2_x': l2_x, 'l2_y': l2_y})

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
    threading.Thread(target=read_joystick).start()

if __name__ == '__main__': 
    socketio.run(app)