import serial

# This variable will store the latest compass reading
latest_compass_data = None

def extract_value_from_data(data):
    data_parts = data.split(',')

    if len(data_parts) > 1:
        return data_parts[1]
    else:
        return None

def read_compass():
    global latest_compass_data

    serial_port = '/dev/ttyUSB1'
    baud_rate = 4800  

    try:
        # Open the serial port
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            while True:
                # Read a line of data from the serial port
                data = ser.readline().decode('utf-8').strip()
                
                # Update the latest compass reading
                latest_compass_data = extract_value_from_data(data)

    except KeyboardInterrupt:
        print("Serial communication stopped.")
    except Exception as e:
        print(f"Error: {str(e)}")

def get_latest_compass_data():
    return latest_compass_data
