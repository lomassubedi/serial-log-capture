import serial
import time
from serial.tools.list_ports import comports
import zmq  
import sys
import signal

# Define global variables
BAUD_RATE = 115200
LOG_FILE_PATH = "serial_data.txt"

stop_reading = False

def signal_handler(sig, frame):
    global stop_reading
    print('Caught SIGINT (Ctrl+C), exiting...')
    # Perform any cleanup tasks before exiting
    stop_reading = True

signal.signal(signal.SIGINT, signal_handler)

def find_serial_port():
    # Get a list of available serial ports
    ports = comports()

    # Iterate through the list of ports and select the first one
    for port in ports:
        if port.device.startswith('/dev/ttyUSB') or port.device.startswith('/dev/ttyACM'):
            return port.device

    # If no suitable port is found
    raise RuntimeError("No suitable serial port found")


def read_serial_and_send_data():
    port = find_serial_port()
    print("Using port : " + str(port))

    context = zmq.Context() 
    socket = context.socket(zmq.PUB) # Using PUB for publishing messages 
    socket.bind("tcp://localhost:5555") # Bind to a port

    try:
        # Open serial port
        # ser = serial.Serial(port, BAUD_RATE)

        # Open log file in append mode
        with open(LOG_FILE_PATH, 'a') as log_file, serial.Serial(port, BAUD_RATE) as ser:
            while not stop_reading:
                # Read data from serial port
                try:
                    data = ser.readline().decode()
                    if data:
                        # Send data to WebSocket clients
                        print("Data saved to file:", data)  # Debug message
                        # Log data to file
                        log_file.write(data + '\n')
                        socket.send_string(data)
                except:
                    pass
                finally:
                    time.sleep(0.01)  # Adjust sleep time as needed
            print("stop reading")
    except Exception as e:
        print(f"Error reading from serial port: {e}. Restarting...")
        time.sleep(1)
    context.term()


if __name__ == "__main__":
    read_serial_and_send_data()
