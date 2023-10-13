from pymodbus.client import ModbusSerialClient


def setup_serial_connection():

    # Create a Modbus serial client
 
    client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

    # Connect to the Modbus device
    if client.connect():
        print("Connected Succesfully")
    else:
        print("Failed to connect to the Modbus device.")

    return client

def read_register(client, register_address):

    # Read from the register
    response = client.read_holding_registers(register_address, 1, 15)

    # Check if the read operation was successful
    base_address = 0
    if not response.isError():
        for register in response.registers:

            
            print(f"Register Address: {register_address} (+{base_address}),   Value: {register}")
            register_address = register_address + 1
            base_address = base_address + 1

        #value = (response.registers[0] << 16) | response.registers[1]
        #print(f"r0: {response.registers[0]} r1: {response.registers[1]} val: {value}")
    else:
        print(f"Error reading register {register_address}")
    client.close()
    
    # Close the Modbus connection


read_register(setup_serial_connection(), 0x1803)