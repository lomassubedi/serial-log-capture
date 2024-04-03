import serial
import time
from serial.tools.list_ports import comports

# Define global variables
BAUD_RATE = 115200
FILE_PATH = "log_file.log"


def find_serial_port():
    # Get a list of available serial ports
    ports = comports()

    # Iterate through the list of ports and select the first one
    for port in ports:
        if port.device.startswith('/dev/ttyUSB'):
            return port.device

    # If no suitable port is found
    raise RuntimeError("No suitable serial port found")


def read_serial_and_log():
    global FILE_PATH
    port = find_serial_port()
    try:
        # Open serial port
        ser = serial.Serial(port, BAUD_RATE)

        # Open file in append mode
        with open(FILE_PATH, 'a') as file:
            while True:
                # Read data from serial port
                data = ser.readline().decode().strip()
                if data:
                    # Append data to file
                    file.write(data + '\n')
                    print(data)  # Print data to console
    except Exception as e:
        print(f"Error: {e}. Restarting...")
        time.sleep(1)


if __name__ == "__main__":
    while True:
        read_serial_and_log()
