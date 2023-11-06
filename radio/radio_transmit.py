import os
import serial
import time
import platform

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
# Ensure the '/dev/radio' is the correct path for your radio device.
ser = serial.Serial(device_path, 19600)

# Check if the serial port is open, if not, open it.
if not ser.is_open:
    ser.open()

# Give some time for the serial port to initialize
time.sleep(2)

try:
    # Write the string 'hello world' to the radio.
    # The encode() method converts the string to bytes.
    ser.write(b'Saucey\n')

    # You might want to wait a bit for the data to be sent.
    time.sleep(1)

    print("Message sent to the radio.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the serial connection.
    ser.close()
