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
    response = client.read_holding_registers(register_address, 40, 15)

    # Check if the read operation was successful
    if not response.isError():
        for register in response.registers:

            #register_value = response.registers[0]
            #print(f"Value in register {register_address} = {register}")
            register_address = register_address + 1
            print(f"Register Adress: {register_address},   Value: {register}")

        value = (response.registers[0] << 16) | response.registers[1]
        #print(f"r0: {response.registers[0]} r1: {response.registers[1]} val: {value}")
    else:
        print(f"Error reading register {register_address}")
    return value
    # Close the Modbus connection
    client.close()


read_register(setup_serial_connection(), 0x1800)