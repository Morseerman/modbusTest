# import flaskApplication
# from devices.radio import radio_slave
import microwave_dish

target_gps = {
    'lat' : -1.883196,
    "long": 51.773461,
    "alt": 162
}

current_gps = {
    'lat': -1.88363343,
    'long': 51.77374322,
    'alt': 161.6077
}
   
print("bearing...")
microwave = microwave_dish.MicrowaveDish("master")

# microwave.align_azimuth(current_gps, target_gps)


h_distance = microwave.calculate_horizontal_distance(current_gps, target_gps)
microwave.align_elevation(target_gps, current_gps, h_distance)

