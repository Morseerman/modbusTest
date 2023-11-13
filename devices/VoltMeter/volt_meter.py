import time
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
GAIN = 1

ADC_MAX_VALUE = 32768  # Maximum value for a 16-bit ADC
VOLTAGE_REFERENCE = 4.096  # Voltage reference for the ADS1115
CUSTOM_SCALING_FACTOR = 0.01592  # Custom scaling factor for your setup

def get_voltage():
    print('Press Ctrl-C to quit...')
    while True:
        # Read the difference between channel 0 and 1
        value = adc.read_adc_difference(0, gain=GAIN)
        
        # Convert raw value to voltage
        voltage = value * (VOLTAGE_REFERENCE / ADC_MAX_VALUE)
        
        # Apply the custom scaling factor
        voltage = voltage / CUSTOM_SCALING_FACTOR
        
        print('Channel 0 minus 1: {0} V'.format(voltage))
        time.sleep(0.5)

def get_voltage_once():
     # Read the difference between channel 0 and 1
        value = adc.read_adc_difference(0, gain=GAIN)
        
        # Convert raw value to voltage
        voltage = value * (VOLTAGE_REFERENCE / ADC_MAX_VALUE)
        
        # Apply the custom scaling factor
        voltage = voltage / CUSTOM_SCALING_FACTOR
        print(voltage)
        return (voltage)

if __name__ == '__main__':
    get_voltage()