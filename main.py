# import flaskApplication
# from devices.radio import radio_slave
import microwave_dish

target_gps = {
    'lat' : -1.883196,
    "long": 51.773461
}

current_gps = {
    'lat': -1.88363343,
    'long': 51.77374322
}

print("bearing...")
microwave = microwave_dish.MicrowaveDish("master")

microwave.align_azimuth( target_gps)