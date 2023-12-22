import os
import serial
import time
import platform
import json

# Check the operating system
system_name = platform.system()

# Define the baud rate
baud_rate = 19600

# Select the correct device path based on the operating system
if system_name == 'Windows':
    # Use the appropriate COM port on Windows
    device_path = 'COM7'
else:
    # Use the appropriate device path on Unix/Linux-like operating systems
    device_path = '/dev/radio'

# Define the serial port and baud rate.
ser = serial.Serial(device_path, 19600)

# Check if the serial port is open, if not, open it.
if not ser.is_open:
    ser.open()

# Give some time for the serial port to initialize
time.sleep(2)

def send_command(command):
    try:        
        command = (command + '\n').encode()
        ser.write(command)

        # You might want to wait a bit for the data to be sent.
        time.sleep(1)
        print("Message sent to the radio.")

        # Here is where we wait for a response
        print(f"awaiting response...")
        response = ser.readline().decode('utf-8').rstrip()

        try:
            # Try parsing the response as JSON
            slave_data = json.loads(response)
            # Handle the data dictionary here
        except json.JSONDecodeError:
            # If it's not JSON, just print the response as is
            print("Received response:", response)


        print(f"{response}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the serial connection.
        ser.close()

if __name__ == '__main__':
    send_command("move x: 50")
    pass