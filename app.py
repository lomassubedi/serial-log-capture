import serial
import time
from serial.tools.list_ports import comports
import socketserver
import threading
import asyncio
import websockets

# Define global variables
BAUD_RATE = 115200
LOG_FILE_PATH = "serial_data.txt"


def find_serial_port():
    # Get a list of available serial ports
    ports = comports()

    # Iterate through the list of ports and select the first one
    for port in ports:
        if port.device.startswith('/dev/ttyUSB'):
            return port.device

    # If no suitable port is found
    raise RuntimeError("No suitable serial port found")


def read_serial_and_send_data():
    port = find_serial_port()
    print("Using port : " + str(port))
    try:
        # Open serial port
        ser = serial.Serial(port, BAUD_RATE)

        # Open log file in append mode
        with open(LOG_FILE_PATH, 'a') as log_file:
            while True:
                # Read data from serial port
                try:
                    data = ser.readline().decode()
                    if data:
                        # Send data to WebSocket clients
                        # await websocket.send(data)
                        print("Data saved to file:", data)  # Debug message
                        # Log data to file
                        log_file.write(data + '\n')
                except:
                    pass
                finally:
                    time.sleep(0.01)  # Adjust sleep time as needed
    except Exception as e:
        print(f"Error reading from serial port: {e}. Restarting...")
        time.sleep(1)


# async def run_websocket_server():
#     async with websockets.serve(read_serial_and_send_data, "localhost", 8765):
#         print("WebSocket server started.")
#         await asyncio.Future()  # Keep server running indefinitely


if __name__ == "__main__":
    # asyncio.run(run_websocket_server())
    read_serial_and_send_data()
