from pymodbus.client import ModbusSerialClient

# Create a Modbus serial client
client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600)

# Connect to the Modbus device
if client.connect():
    # Specify the register address to read from
    register_address = 0x0384

    # Read from the register
    response = client.read_holding_registers(register_address, 1, 15)

    # Check if the read operation was successful
    if not response.isError():
        register_value = response.registers[0]
        print(f"Value in register {register_address}: {register_value}")

    # Close the Modbus connection
    client.close()
else:
    print("Failed to connect to the Modbus device.")
