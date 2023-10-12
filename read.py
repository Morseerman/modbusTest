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
    response = client.read_holding_registers(register_address, 2, 15)

    # Check if the read operation was successful
    if not response.isError():
        for register in response.registers:

            #register_value = response.registers[0]
            print(f"Value in register {register_address} = {register}")
            register_address = register_address + 1

        value = (response[0] << 15) | response[1]
        print(f"val: {value}")
    else:
        print(f"Error reading register {register_address}")

    # Close the Modbus connection
    client.close()
