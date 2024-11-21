from flask import Flask, render_template
from flask_socketio import SocketIO

# Create Flask app and initialize SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
