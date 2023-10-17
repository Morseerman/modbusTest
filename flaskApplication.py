from flask import Flask, request, jsonify, render_template
from pymodbus.client import ModbusSerialClient
import motor_controller
import read

app = Flask(__name__)
app.static_folder = 'static'

ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytestize=8, timeout=5.0)

# Connect to the Modbus device
if ser.connect():
    print("Connected Succesfully")
else:
    print("Failed to connect to the Modbus device.")

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_position')
def get_position():  
    response_14 = read.read_motor_position(14)
    response_15 = read.read_motor_position(15)

    if response_14 is None or response_15 is None:
        return jsonify(error="Error reading from one or both motors"), 500

    return jsonify(motor_14_position=response_14 / 100, motor_15_position=response_15 / 100)    

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

