import threading
import time
import flaskApplication
from devices import compass, motor_controller
import devices.Inclinometer.WitProtocol.chs.inclinometer as inclinometer
import microwave_dish


class MicrowaveDishFSM:
    def __init__(self):
        self.state = 'Start'
        self.next_state()

    def get_state(self):
        return self.state
    
    
    def next_state(self):
        time.sleep(3)
        if self.state == 'Start':
            self.state = 'Read Devices'
            self.read_devices()
            self.next_state()
        elif self.state == 'Read Devices':
            self.state = 'Web Server'
            self.web_server()
            self.next_state()
        elif self.state == 'Web Server':
            self.state = 'Initial Alignment'
            self.initial_alignment()
        elif self.state == 'Initial Alignment':
            self.state = 'Fine Alignment'
            self.fine_alignment()
        elif self.state == 'Fine Alignment':
            self.state = 'Connected'
        elif self.state == 'Error':
            self.state = 'Error'
            

    # Note to self: Will eventually have all devices here! Also might not need to use multi threading
    def read_devices(self):
        # Start compass reading in a separate thread
        compass_thread = threading.Thread(target=compass.read_compass)
        compass_thread.start()

        inclinometer_thread = threading.Thread(target=inclinometer.start_inclinometer)
        inclinometer_thread.start()

    def web_server(self):
        thread = threading.Thread(target=flaskApplication.start_web_server)
        thread.start()

    def initial_alignment(self):
        microwave = microwave_dish.MicrowaveDish("master")

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

        microwave.align_azimuth(current_gps, target_gps)

        # h_distance = microwave.calculate_horizontal_distance(current_gps, target_gps)
        # elevation_angle  = microwave.align_elevation(current_gps, target_gps, h_distance)

    def fine_alignment(self):
        max_position = motor_controller.scan_matrix_columns()
        time.sleep(2) 
        motor_controller.move_motor(max_position[0], 14)
        motor_controller.move_motor(max_position[1], 15)
