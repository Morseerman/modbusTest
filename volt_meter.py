import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.096V.
GAIN = 1

# Read the ADC value from channel 0
adc_value = adc.read_adc(0, gain=GAIN)

# Convert the ADC value to voltage
# Note: The conversion factor is determined by the gain setting and the voltage divider ratio.
# The formula for conversion_factor is: (4.096 / 32768) / (R2 / (R1 + R2))
conversion_factor = (4.096 / 32768) / (20 / (10 + 20))
voltage = adc_value * conversion_factor

# Since the voltage was stepped down, multiply by the inverse of the voltage divider ratio to get the original voltage
original_voltage = voltage * (10 + 20) / 20

# Print the original voltage
print(f'Battery Voltage: {original_voltage} V')
