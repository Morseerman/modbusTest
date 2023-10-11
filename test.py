from pymodbus.client import ModbusSerialClient

def write(register_address, value_to_write):
        
        # Write to a single holding register
        response = ser.write_register(register_address, value_to_write, 15)

        if response.isError():
            print(f"Error response: {response}") 
        else:
            # Extract the value from the response
            print(f"Successfully wrote {value_to_write} to register {register_address}")
            print(f"Raw response: {response}")

def degrees_to_steps(degrees):
    return degrees * 100

#-----------------------------------------------------------------------------------------------------------

# Define the serial port (ttyUSB0) and baudrate
ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

# Ensure the client is connected
if not ser.connect():
    print("Failed to connect to the Modbus device.")
else:
    try:
        degrees = 90

        write(0x1803, degrees_to_steps(degrees))
        write(0x79, 8) #This is the START command

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the Modbus connection
        ser.close()

