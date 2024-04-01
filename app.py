import argparse
import serial
import time

def read_serial_and_log(port, baud_rate, file_path):
    try:
        # Open serial port
        ser = serial.Serial(port, baud_rate)

        # Open file in append mode
        with open(file_path, 'a') as file:
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
    parser = argparse.ArgumentParser(description='Read data from serial port and log to file.')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('--baud_rate', type=int, default=115200, help='Baud rate')
    parser.add_argument('file_path', help='Path to log file')

    args = parser.parse_args()

    while True:
        read_serial_and_log(args.port, args.baud_rate, args.file_path)
