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

def read_registers(client, register_address):

    # Read from the register
    response = client.read_holding_registers(register_address, 1, 15)

    # Check if the read operation was successful
    base_address = 0
    if not response.isError():
        for register in response.registers:

            
            print(f"Register Address: {register_address} (+{base_address}),   Value: {register}")
            register_address = register_address + 1
            base_address = base_address + 1

    else:
        print(f"Error reading register {register_address}")
    client.close()
    
def read_motor_position(client):
      # Read from the register
    response = client.read_holding_registers(0x1803, 1, 15)

    # Check if the read operation was successful
    if not response.isError():           
        print(f"Position: {response.register[0]}")

    else:
        print(f"Error reading register {0x1803}")
    client.close()
    return response.register[0]


read_registers(setup_serial_connection(), 0x1803)