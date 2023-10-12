from pymodbus.client import ModbusSerialClient

# Create a Modbus serial client
client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

# Connect to the Modbus device
if client.connect():
    print("Connected Succesfully")

    # Specify the register address to read from
    register_address = 0x024C

    # Read from the register
    response = client.read_holding_registers(register_address, 50, 15)

    # Check if the read operation was successful
    if not response.isError():
        for x in response.registers:

            #register_value = response.registers[0]
            print(f"Value in register {register_address} = {x}")
            register_address = register_address + 1
    else:
        print(f"Error reading register {register_address}")

    # Close the Modbus connection
    client.close()
else:
    print("Failed to connect to the Modbus device.")
