import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

print('Press Ctrl-C to quit...')
while True:
    value = adc.read_adc_difference(0, gain=GAIN)
    # Convert raw value to voltage
    voltage = value * (4.096 / 32768)
    print('Channel 0 minus 1: {0} V'.format(voltage))
    time.sleep(0.5)
