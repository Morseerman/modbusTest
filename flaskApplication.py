from flask import Flask, request, jsonify, render_template
from pymodbus.client import ModbusSerialClient
import motor_controller
import read

app = Flask(__name__)
app.static_folder = 'static'

ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=5.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_position')
def get_position():  
    response = read.read_motor_position

    if not response.isError():        
        return jsonify(position=response.registers[0] / 100)   
    else:
        return jsonify(error=f"Error reading register {0x1803}")

@app.route('/set_position', methods=['POST'])
def set_position():
    try:
        # Get the 'position' field from the posted form data
        angle = float(request.form.get('position'))

        motor_controller.move_motor(angle, 14)
        
        return jsonify(status="success", message=f"Set motor angle to {angle} degrees")

    except Exception as e:
        return jsonify(status="error", message=str(e))

    finally:
        # Close the Modbus connection
        ser.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
