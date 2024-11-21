from flask import Flask, render_template
from flask_socketio import SocketIO
import zmq
import threading
import sys
import signal

run_read_thread = True
context = zmq.Context() 
socket = context.socket(zmq.SUB) 
socket.connect("tcp://localhost:5555") 
socket.setsockopt_string(zmq.SUBSCRIBE, "") # Subscribe to all messages

# Create Flask app and initialize SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

def zmq_listener(): 
    while run_read_thread: 
        try:
            message = socket.recv_string() 
            print(f"Received message: {message}") 
            socketio.emit('serial_data', {'data': message}) # Emit message to websocket clients
        except:
            pass

# Handle WebSocket connection event
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.emit('message', "Welcome to the WebSocket server!")

# Handle messages sent by the client
@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")

# Handle WebSocket disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@app.route('/')
def index():
    return render_template("index.html")

def signal_handler(sig, frame): 
    global run_read_thread 
    run_read_thread = False 
    print('Shutting down...') 
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler) # Register the signal handler 
    thread = threading.Thread(target=zmq_listener) 
    thread.daemon = True 
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
