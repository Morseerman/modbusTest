import serial

def process_gps_data(data):
    # Split the string into separate lines
    lines = data.split('\n')
    result = {
        "Latitude": "Unknown",
        "Longitude": "Unknown",
        "Altitude": "Unknown",
        "Signal Quality": "Unknown"
    }
    
    for line in lines:
        # Process $KSXT data for latitude, longitude, and altitude
        if '$KSXT' in line:
            parts = line.split(',')
            result["Latitude"] = parts[2]
            result["Longitude"] = parts[3]
            result["Altitude"] = parts[4] + " meters"
        
        # Process #UNIHEADINGA data for signal quality
        if '#UNIHEADINGA' in line:
            parts = line.split(',')
            sol_status = parts[1]
            pos_type = parts[2] + ', ' + parts[3]
            result["Signal Quality"] = f"Solution Status: {sol_status}, Position Type: {pos_type}"

    return result

serial_port = '/dev/ttyUSB1'
baud_rate = 921600  

try:
    # Open the serial port
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        while True:
            # Read a line of data from the serial port
            data = ser.readline().decode('utf-8').strip()
            
            # Update the latest compass reading
            print(process_gps_data(process_gps_data(data)))

except KeyboardInterrupt:
    print("Serial communication stopped.")
except Exception as e:
    print(f"Error: {str(e)}")