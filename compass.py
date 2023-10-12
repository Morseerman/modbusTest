import serial

serial_port = '/dev/ttyUSB1'
baud_rate = 4800  

try:
    # Open the serial port
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        while True:
            # Read a line of data from the serial port
            data = ser.readline().decode('utf-8').strip()
            
            # Process and display the data (replace this with your processing logic)
            print(f"Compass Data: {data}")

except KeyboardInterrupt:
    print("Serial communication stopped.")
except Exception as e:
    print(f"Error: {str(e)}")
