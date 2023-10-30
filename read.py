from pymodbus.client import ModbusSerialClient

def read_registers(register_address, number_of_registers, motor_id):

    # Read from the register
    response = ser.read_holding_registers(register_address, number_of_registers, motor_id)

    # Check if the read operation was successful
    if response.isError():
         print(f"Error reading register {register_address}")
    else:
        #Reads all registers
        for register in response.registers:
            print(f"Register Address: {register_address} Value: {register}")
            register_address = register_address + 1


    return response
    
def read_motor_position(motor_id):
    # Read from the register
    response = ser.read_holding_registers(0x1803, 1, motor_id)

    # Check if the read operation was successful
    if not response.isError():           
        print(f"Position: {response.registers[0]}")
        return response.registers[0]
    else:
        print(f"Error reading register {0x1803}")
        print(response)
        return None
    
    

#-----------------------------------------------------------------------------------------------------------
#                                               Setup

# Create a Modbus serial client
ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB2', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

# Connect to the Modbus device
if ser.connect():
    print("Connected Succesfully")
else:
    print("Failed to connect to the Modbus device.")
