import os
import serial
import time
import platform
from devices import compass
from devices import motor_controller
from devices.VoltMeter import volt_meter
from devices.Inclinometer.WitProtocol.chs import inclinometer

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

try:
    print("Listening for incoming data...")

    while True:
        if ser.in_waiting > 0:
            # Read the incoming data. ser.readline() assumes that the incoming message ends with a newline character (\n).
            incoming_data = ser.readline().decode('utf-8').rstrip().upper()
            print(f"Received data: {incoming_data}")

            response = None

            # Command is handled here
            if incoming_data == "GET COMPASS":
                response = compass.read_compass_once()
            elif incoming_data == "ALIGN":
                max_strength, max_position = motor_controller.scan_matrix(start_x_angle=0, start_y_angle=90)
                response = f"Strongest signal at position: {max_position} with strength: {max_strength}"
            elif incoming_data == "GET VOLTAGE":
                response = volt_meter.get_voltage_once()
            elif incoming_data == "GET INCLINOMETER":
                response = inclinometer.get_angle_data()
            elif incoming_data == "GET AIR PRESSURE":
                response = inclinometer.get_pressure()
            else:
                response = "Invalid Command"

            # Incoming Response
            time.sleep(1.5)
            ser.write(("[SLAVE]: " + response + '\n').encode('utf-8'))
            print(f"--->{response.strip()}")

            


except KeyboardInterrupt:
    print("Receiver terminated by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the serial connection.
    ser.close()
