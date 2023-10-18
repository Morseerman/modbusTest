import serial

# This variable will store the latest compass reading
latest_compass_data = None

def extract_value_from_data(data):
    data_parts = data.split(',')

    if len(data_parts) > 1:
        return data_parts[1]
    else:
        return None

def interpret_direction(compass_data):
    if compass_data > 337.5 or compass_data <= 22.5:
        return 'N'
    if compass_data > 22.5 and compass_data <= 67.5:
        return 'N.E'
    if compass_data > 67.5 and compass_data <= 112.5:
        return 'E'
    if compass_data > 112.5 and compass_data <= 157.5:
        return 'S.E'
    if compass_data > 157.5 and compass_data <= 202.5:
        return 'S'
    if compass_data > 202.5 and compass_data <= 247.5:
        return 'S.W'
    if compass_data > 247.5 and compass_data <= 292.5:
        return 'W'
    if compass_data > 292.5 and compass_data <= 337.5:
        return 'N.W'

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
    direction = interpret_direction(latest_compass_data)
    return latest_compass_data + f"  ({direction})"
