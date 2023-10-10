from pymodbus.client import ModbusSerialClient

# Define the serial port (ttyUSB0) and baudrate
ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

# Ensure the client is connected
if not ser.connect():
    print("Failed to connect to the Modbus device.")
else:
    try:
        # Specify the slave ID (address)
        slave_id = 15  # Replace with the actual slave ID of your device

        # Specify the Modbus register to read (e.g., register number 0)
        register_address = 0x1811

        #Specify the number of coils to read
        count = 1

        # Specify the value you want to write
        value_to_write = 5  #when writing miltpiple vales, the fiest digit is the multiplier

        # Read a single holding register
        #response = ser.read_holding_registers(register_address, count, slave_id)
        
        # Write to a single holding register
        response = ser.write_register(register_address, value_to_write, slave_id)
        

        if response.isError():
            print(f"Error response: {response}") 
        else:
            # Extract the value from the response
            print(f"Successfully wrote {value_to_write} to register {register_address}")
            print(f"Raw response: {response}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the Modbus connection
        ser.close()
