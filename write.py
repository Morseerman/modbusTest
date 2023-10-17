import time
from pymodbus.client import ModbusSerialClient

def write_to_register(register_address, value_to_write):
        
        # Write to a single holding register
        response = ser.write_register(register_address, value_to_write, 14)

        if response.isError():
            print(f"Error response: {response}") 
        else:
            # Extract the value from the response
            print(f"Successfully wrote {value_to_write} to register {register_address}")
           
def degrees_to_steps(degrees):
    return round(degrees * 100)

def close_server():
    ser.close

#-----------------------------------------------------------------------------------------------------------
#                                               Setup

# Define the serial port (ttyUSB0) and baudrate
ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

# Ensure the client is connected
if not ser.connect():
    print("Failed to connect to the Modbus device.")