import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  - 1 = +/-4.096V
#  - 2 = +/-2.048V
#  - 4 = +/-1.024V
#  - 8 = +/-0.512V
#  - 16 = +/-0.256V
GAIN = 1

# Read the voltage on channel 0 (check your voltmeter's documentation to find the correct channel)
voltage = adc.read_adc(0, gain=GAIN)

# Convert the raw ADC value to voltage
# This conversion factor will depend on the gain chosen above
conversion_factor = 4.096 / 32768
voltage_volts = voltage * conversion_factor

# Print the voltage
print(f'Voltage: {voltage_volts} V')