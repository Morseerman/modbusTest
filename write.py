import time
from pymodbus.client import ModbusSerialClient

def write_to_register(register_address, value_to_write, motor_id):
        
        # Write to a single holding register
        response = ser.write_register(register_address, value_to_write, motor_id)

        if response.isError():
            print(f"Error response: {response}") 
        else:
            # Extract the value from the response
            print(f"Successfully wrote {value_to_write} to register {register_address}")
           

def close_server():
    ser.close

#-----------------------------------------------------------------------------------------------------------
#                                               Setup

# Define the serial port (ttyUSB0) and baudrate
# ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

# # Connect to the Modbus device
# if ser.connect():
#     print("Connected Succesfully")
# else:
#     print("Failed to connect to the Modbus device.")
