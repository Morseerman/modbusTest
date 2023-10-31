import smbus2

# Create an smbus2 object
bus = smbus2.SMBus(1)

# Replace with your voltmeter's I2C address
voltmeter_address = 0x49  

# Replace with the command to read voltage, check your voltmeter's datasheet
read_voltage_command = 0x00  

# Send the command to read voltage
bus.write_byte(voltmeter_address, read_voltage_command)

# Read the voltage data (assuming 2 bytes, check your voltmeter's datasheet)
voltage_data = bus.read_word_data(voltmeter_address, read_voltage_command)

# Convert the data to voltage, check your voltmeter's datasheet for the conversion formula
voltage = voltage_data * conversion_factor

# Print the voltage
print(f'Voltage: {voltage} V')

bus.close()
