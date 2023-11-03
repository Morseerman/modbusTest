import serial
import time

# Define the serial port and baud rate.
# Ensure the '/dev/radio' is the correct path for your radio device.
ser = serial.Serial('/dev/radio', 19600)

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
            incoming_data = ser.readline().decode('utf-8').rstrip()

            # Do something with the incoming data. For now, we'll just print it.
            print(f"Received data: {incoming_data}")

            # You could include some condition to break the loop if necessary.
            # For example, if incoming_data == "quit":
            #     break

except KeyboardInterrupt:
    print("Receiver terminated by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the serial connection.
    ser.close()
