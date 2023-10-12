from flask import Flask, render_template, jsonify
from pymodbus.client import ModbusSerialClient

app = Flask(__name__)

client = ModbusSerialClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='E', stopbits=1, bytesize=8, timeout=5.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_position')
def get_position():
    if not client.connect():
        return jsonify(error="Failed to connect to the Modbus device.")

    register_address = 0x01803
    response = client.read_holding_registers(register_address, 1, 15)

    if not response.isError():
        return jsonify(position=response.registers[0])
    else:
        return jsonify(error=f"Error reading register {register_address}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
