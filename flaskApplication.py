from flask import Flask, request, jsonify, render_template
from pymodbus.client import ModbusSerialClient
import time

app = Flask(__name__)

ser = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=5.0)

def write(register_address, value_to_write):
    response = ser.write_register(register_address, value_to_write, 15)
    if response.isError():
        print(f"Error response: {response}")
    else:
        print(f"Successfully wrote {value_to_write} to register {register_address}")

def degrees_to_steps(degrees):
    return round(degrees * 100)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_position')
def get_position():
    if not ser.connect():
        return jsonify(error="Failed to connect to the Modbus device.")

    register_address = 0x01803
    response = ser.read_holding_registers(register_address, 1, 15)

    if not response.isError():
        return jsonify(position=response.registers[0])
    else:
        return jsonify(error=f"Error reading register {register_address}")

@app.route('/set_position', methods=['POST'])
def set_position():
    try:
        # Get the 'position' field from the posted form data
        degrees = float(request.form.get('position'))
        
        if not ser.connect():
            return jsonify(status="error", message="Failed to connect to the Modbus device.")

        # Write the provided angle and execute the START command
        write(0x1803, degrees_to_steps(degrees))
        write(0x79, 8) # This is the START command
        
        return jsonify(status="success", message=f"Set motor angle to {degrees} degrees")

    except Exception as e:
        return jsonify(status="error", message=str(e))

    finally:
        # Close the Modbus connection
        ser.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
