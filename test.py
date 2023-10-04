from pymodbus.client import ModbusSerialClient

# Define the serial port (ttyUSB0) and baudrate
ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

# Ensure the client is connected
if not ser.connect():
    print("Failed to connect to the Modbus device.")
else:
    try:
        # Specify the slave ID (address)
        slave_id = 16  # Replace with the actual slave ID of your device

        # Specify the Modbus register to read (e.g., register number 0)
        register_address = 3

        # Read a single holding register
        response = ser.read_holding_registers(register_address, 1, unit=slave_id)

        if response.isError():
            print(f"Error response: {response}")
        else:
            # Extract the value from the response
            value = response.registers[0]
            print(f"Register {register_address}: {value}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the Modbus connection
        ser.close()
