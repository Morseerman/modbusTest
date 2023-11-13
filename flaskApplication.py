from flask import Flask, request, jsonify, render_template
from pymodbus.client import ModbusSerialClient
from devices import motor_controller
from devices import read
import threading
from devices import compass
import devices.Inclinometer.WitProtocol.chs.inclinometer as inclinometer

app = Flask(__name__)
app.static_folder = 'static'

# ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_position')
def get_position():  
    response_14 = motor_controller.get_motor_angle(14)
    response_15 = motor_controller.get_motor_angle(15)

    if response_14 is None or response_15 is None:
        return jsonify(error="Error reading from one or both motors"), 500

    return jsonify(motor_14_position=response_14, motor_15_position=response_15)    

@app.route('/set_position', methods=['POST'])
def set_position():
    try:
        angle = float(request.form.get('position'))
        motor_id = int(request.form.get('motor_id'))

        if motor_id not in [14, 15]:
            return jsonify(status="error", message="Invalid motor ID")

        motor_controller.move_motor(angle, motor_id)
        
        return jsonify(status="success", message=f"Set motor {motor_id} angle to {angle} degrees")

    except Exception as e:
        return jsonify(status="error", message=str(e))

@app.route('/get_compass_data')
def get_compass_data():
    data = compass.get_latest_compass_data()

    return jsonify(compass_data=data)

@app.route('/get_inclinometer_data')
def get_inclinometer_data():
    # Assume get_inclinometer_data is a function that returns a dict with x, y, and z values
    angle_data = inclinometer.get_angle_data()
    air_pressure_data = inclinometer.get_pressure()
    print(angle_data + "<------")
    return jsonify(inclinometer_angle_data=angle_data, inclinometer_air_pressure_data=air_pressure_data)


# Start compass reading in a separate thread
compass_thread = threading.Thread(target=compass.read_compass)
compass_thread.start()

inclinometer_thread = threading.Thread(target=inclinometer.start_inclinometer)
inclinometer_thread.start()

#Start Flask application
app.run(host='0.0.0.0', port=5000)

