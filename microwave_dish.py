import math
from devices import motor_controller
from devices.radio import radio_master
from devices import compass
from devices.Inclinometer.WitProtocol.chs import inclinometer
from devices import gps
import threading

class MicrowaveDish:
    """
    Class representing a Microwave Dish, capable of aligning itself with another dish.
    """

    def __init__(self, device_type):
        """
        Initialize the Microwave Dish with a specific device type (master or slave).
        """
        self.device_type = device_type

    def send_command_to_slave(self, command):
        """
        Send a command to the slave dish if this device is a master.
        """
        if self.device_type == "master":
            radio_master.send_command(command)
        else:
            print("Only master can send commands")

    def get_slave_data(self):
        """
        Retrieve data from the slave dish.
        """
        return self.send_command_to_slave("GET DATA")

    def initial_alignment(self):
        """
        Align the microwave dish with the slave dish using azimuth and elevation adjustments.
        """
        current_data = self.collect_current_data()
        slave_data = self.get_slave_data()
        horizontal_distance = self.calculate_horizontal_distance(current_data["gps"], slave_data["gps"])

        self.align_azimuth(current_data, slave_data, horizontal_distance)
        self.align_elevation(current_data, slave_data, horizontal_distance)

    def collect_current_data(self):
        """
        Collect current compass, inclinometer, and GPS data of this dish.
        """
        return {
            "compass": compass.read_compass_once(),
            "inclinometer": inclinometer.get_angle_data(),
            "gps": gps.get_gps_data()
        }

    def align_azimuth(self, current_data, target_data):
        """
        Align the azimuth of the dish towards the target.
        """
        bearing_to_target = self.calculate_bearing(current_data, target_data)
        # print("gpscompass -> " + (str(gps.get_compass_once())) + "   -magcompass " + str(compass.read_compass_once()))
        adjustment = self.adjust_orientation(float(gps.get_compass_once()), bearing_to_target)
        adjusted_position = motor_controller.get_motor_angle(14) - adjustment
        print(f"adjustment: {adjustment}  adjusted position: {adjusted_position}  current motor position: {motor_controller.get_motor_angle(14)}")
        # motor_controller.move_motor(adjusted_position, 14)  # Adjust azimuth (x-axis)
        radio_master.send_command(f"ALIGN BEARING: {str(bearing_to_target)}")

    
    def align_azimuth_slave(self, bearing_from_master):
        """
        Align the azimuth of the dish towards the target.
        """
        bearing_to_target = 360 - bearing_from_master 
        inclinometer_thread = threading.Thread(target=inclinometer.start_inclinometer)
        inclinometer_thread.start()
        adjustment = self.adjust_orientation(inclinometer.get_compass_once(), bearing_to_target)
        adjusted_position = motor_controller.get_motor_angle(14) - adjustment
        print(f"adjustment: {adjustment}  adjusted position: {adjusted_position}  current motor position: {motor_controller.get_motor_angle(14)}")
        motor_controller.move_motor(adjusted_position, 14)  # Adjust azimuth (x-axis)

    def align_elevation(self, current_data, target_data, horizontal_distance):
        """
        Align the elevation of the dish towards the target.
        """
        elevation_angle = self.calculate_elevation_angle(current_data["gps"]["alt"], target_data["gps"]["alt"], horizontal_distance)
        motor_controller.move_motor(elevation_angle, 15)  # Adjust elevation (y-axis)

    def calculate_horizontal_distance(self, current_gps, target_gps):
        """
        Calculate the horizontal distance between the current dish and the target using the Haversine formula.
        """
        return self.haversine(current_gps["lat"], current_gps["long"], target_gps["lat"], target_gps["long"])

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points on the earth specified in decimal degrees.
        """
        R = 6371e3  # Radius of the Earth in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    def calculate_bearing(self, current_gps, target_gps):
        """
        Calculate the compass bearing from the current dish to the target.
        """
        lat1, lon1, lat2, lon2 = target_gps["lat"], target_gps["long"], current_gps["lat"], current_gps["long"]
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dLon = lon2 - lon1
        x = math.sin(dLon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dLon))
        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing

    def adjust_orientation(self, current_orientation, target_bearing):
        """
        Calculate the adjustment needed for the current orientation to align with the target bearing.
        Positive adjustment indicates a clockwise movement, and negative indicates counterclockwise.
        """
        adjustment = target_bearing - current_orientation
        if adjustment > 180:
            adjustment -= 360  # Move counterclockwise
        elif adjustment < -180:
            adjustment += 360  # Move clockwise

        return adjustment


    def calculate_elevation_angle(self, current_alt, target_alt, horizontal_distance):
        """
        Calculate the elevation angle needed to point towards the target.
        """
        elevation_difference = target_alt - current_alt
        return math.degrees(math.atan2(elevation_difference, horizontal_distance))

    def move_slave(self, angle, axis):
        """
        Send a command to move the slave dish along a specified axis by a certain angle.
        """
        if axis.upper() == 'X' or axis == 14:
            radio_master.send_command(f"MOVE X: {angle}")
        elif axis.upper() == 'Y' or axis == 15:
            radio_master.send_command(f"MOVE Y: {angle}")

