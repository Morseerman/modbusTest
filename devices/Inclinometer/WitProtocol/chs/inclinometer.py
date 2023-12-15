# coding:UTF-8
"""
    Test file
"""
import time
import datetime
import platform

if __name__ == '__main__':
    pass
else:
    import Inclinometer.WitProtocol.chs.lib.device_model as deviceModel
    from Inclinometer.WitProtocol.chs.lib.data_processor.roles.jy901s_dataProcessor import JY901SDataProcessor
    from Inclinometer.WitProtocol.chs.lib.protocol_resolver.roles.wit_protocol_resolver import WitProtocolResolver

welcome = """
Welcome to the Wit-Motion sample program
"""
_writeF = None                    # Write file
_IsWriteF = False                 # Write file identification
def readConfig(device):
    """
    Example of reading configuration information
    :param device: Device model
    :return:
    """
    tVals = device.readReg(0x02,3)  # Read data content, return rate, communication rate
    if (len(tVals)>0):
        print("Returned Result:" + str(tVals))
    else:
        print("No Return")
    tVals = device.readReg(0x23,2)  # Read the installation direction and algorithm
    if (len(tVals)>0):
        print("Returned Result:" + str(tVals))
    else:
        print("No Return")

def setConfig(device):
    """
    Example setting configuration information
    :param device: Device model
    :return:
    """
    device.unlock()                # Unlock
    time.sleep(0.1)                # Sleep 100ms
    device.writeReg(0x03, 6)       # Set the return rate to 10HZ
    time.sleep(0.1)                # Sleep 100ms
    device.writeReg(0x23, 0)       # Set the installation direction: horizontal and vertical
    time.sleep(0.1)                # Sleep 100ms
    device.writeReg(0x24, 0)       # Set the installation direction: nine axis, six axis
    time.sleep(0.1)                # Sleep 100ms
    device.save()                  # Save

def AccelerationCalibration(device):
    """
    Acceleration calibration
    :param device: Device model
    :return:
    """
    device.AccelerationCalibration()                 # Acceleration calibration
    print("Acceleration Calibration Completed")

def FieldCalibration(device):
    """
    Magnetic field calibration
    :param device: Device model
    :return:
    """
    device.BeginFieldCalibration()                   # Starting field calibration
    if input("Please rotate slowly around XYZ axes one circle each, once completed with the rotations on all axes, end calibration (Y/N)?").lower()=="y":
        device.EndFieldCalibration()                 # End field calibration
        print("Magnetic Field Calibration Ended")

def onUpdateAll(deviceModel):
    """
    Data update event
    :param deviceModel: Device model
    :return:
    """
    print("Chip time:" + str(deviceModel.getDeviceData("Chiptime"))
         , " Temperature:" + str(deviceModel.getDeviceData("temperature"))
         , " Acceleration:" + str(deviceModel.getDeviceData("accX")) +","+  str(deviceModel.getDeviceData("accY")) +","+ str(deviceModel.getDeviceData("accZ"))
         ,  " Angular velocity:" + str(deviceModel.getDeviceData("gyroX")) +","+ str(deviceModel.getDeviceData("gyroY")) +","+ str(deviceModel.getDeviceData("gyroZ"))
         , " Angle:" + str(deviceModel.getDeviceData("angleX")) +","+ str(deviceModel.getDeviceData("angleY")) +","+ str(deviceModel.getDeviceData("angleZ"))
        , " Magnetic field:" + str(deviceModel.getDeviceData("magX")) +","+ str(deviceModel.getDeviceData("magY"))+","+ str(deviceModel.getDeviceData("magZ"))
        , " Longitude:" + str(deviceModel.getDeviceData("lon")) + " Latitude:" + str(deviceModel.getDeviceData("lat"))
        , " Yaw angle:" + str(deviceModel.getDeviceData("Yaw")) + " Ground speed:" + str(deviceModel.getDeviceData("Speed"))
         , " Quaternion:" + str(deviceModel.getDeviceData("q1")) + "," + str(deviceModel.getDeviceData("q2")) + "," + str(deviceModel.getDeviceData("q3"))+ "," + str(deviceModel.getDeviceData("q4"))
          )
    if (_IsWriteF):    # Record data
        Tempstr = " " + str(deviceModel.getDeviceData("Chiptime"))
        Tempstr += "\t"+str(deviceModel.getDeviceData("accX")) + "\t"+str(deviceModel.getDeviceData("accY"))+"\t"+ str(deviceModel.getDeviceData("accZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("gyroX")) +"\t"+ str(deviceModel.getDeviceData("gyroY")) +"\t"+ str(deviceModel.getDeviceData("gyroZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("angleX")) +"\t" + str(deviceModel.getDeviceData("angleY")) +"\t"+ str(deviceModel.getDeviceData("angleZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("temperature"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("magX")) +"\t" + str(deviceModel.getDeviceData("magY")) +"\t"+ str(deviceModel.getDeviceData("magZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("lon")) + "\t" + str(deviceModel.getDeviceData("lat"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("Yaw")) + "\t" + str(deviceModel.getDeviceData("Speed"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("q1")) + "\t" + str(deviceModel.getDeviceData("q2"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("q3")) + "\t" + str(deviceModel.getDeviceData("q4"))
        Tempstr += "\r\n"
        _writeF.write(Tempstr)

angle_data = {'x': None, 'y': None, 'z': None}
modified_angle_data = {'x': None, 'y': None, 'z': None}
pressure = None

def set_zero_data():
    global zero_x
    global zero_y
    global zero_z
    zero_x = round(angle_data['x'] * -1, 2)
    zero_y = round(angle_data['y'] * -1, 2)
    zero_z = round(angle_data['z'] * -1, 2)

zero_x = 0
zero_y = 0
zero_z = 0
def zero_angle_data():
    modified_angle_data['x'] = round(angle_data['x'] + zero_x, 2)
    modified_angle_data['y'] = round(angle_data['y'] + zero_y, 2)
    modified_angle_data['z'] = round(angle_data['z'] + zero_z, 2)

def get_angle_data():
    return modified_angle_data

def get_compass_once():

    compass_value = (angle_data['z'])
    compass_value = float(compass_value)
    # Adjusting the compass value to be in the range of 0 to 360
    if compass_value < 0:
        compass_value += 360
    return compass_value


def get_angle_data_string():
    global modified_angle_data
    total = str(round(modified_angle_data['x'] + modified_angle_data['y'] + modified_angle_data['z'], 2))
    print("--------->" + str(modified_angle_data['x']) + " ~~~~ "  + str(modified_angle_data['y']) + " ~~~~ " + str(modified_angle_data['z']) + "  Pressure: " + str(pressure))
    return "-X: " + str(modified_angle_data['x']) + "   -Y: "  + str(modified_angle_data['y']) + "   -Z: " + str(modified_angle_data['z']) + "   -Total: " + total

def get_pressure():
    global pressure
    return str(pressure)


def calculate_altitude(temperature, pressure=get_pressure()):

    import math

    # Constants
    PRESSURE_SEA_LEVEL = 1013.25 # average sea level pressure in hPa

    """
    Calculate altitude from air pressure.
    :param pressure: Air pressure in hPa
    :param temperature: Temperature in Celsius
    :return: Altitude in meters
    """
    # Convert temperature to Kelvin
    temperature += 273.15

    # Barometric formula
    altitude = (temperature / 0.0065) * ((pressure / PRESSURE_SEA_LEVEL) ** (-0.0065 * 287.05 / 9.80665) - 1)

    return altitude


def onUpdate(deviceModel):
    """
    Data update event for angle
    :param deviceModel: Device model
    :return:
    """
    global angle_data
    angle_data = {
        'x': deviceModel.getDeviceData("angleX"),
        'y': deviceModel.getDeviceData("angleY"),
        'z': deviceModel.getDeviceData("angleZ")
    }
    zero_angle_data()

    global pressure
    pressure = deviceModel.getDeviceData("pressure")
   

def startRecord():
    """
    Start recording data
    :return:
    """
    global _writeF
    global _IsWriteF
    
    if _IsWriteF:
        _writeF = open("inclinometer/data_files/" + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".txt", "w")  # Create a new file in specified directory
        _IsWriteF = True                                                    # Mark write identification
        Tempstr = "Chiptime"
        Tempstr +=  "\tax(g)\tay(g)\taz(g)"
        Tempstr += "\twx(deg/s)\twy(deg/s)\twz(deg/s)"
        Tempstr += "\tAngleX(deg)\tAngleY(deg)\tAngleZ(deg)"
        Tempstr += "\tT(°)"
        Tempstr += "\tmagx\tmagy\tmagz"
        Tempstr += "\tlon\tlat"
        Tempstr += "\tYaw\tSpeed"
        Tempstr += "\tq1\tq2\tq3\tq4"
        Tempstr += "\r\n"
        _writeF.write(Tempstr)
        print("Start recording data")

def endRecord():
    """
    End recording data
    :return:
    """
    global _writeF
    global _IsWriteF
    _IsWriteF = False             # Mark non-writable identification
    _writeF.close()               # Close file
    print("End recording data")

def start_inclinometer():
    print(welcome)
    """
    Initialize a device model
    """
    device = deviceModel.DeviceModel(
        "MyJY901",
        WitProtocolResolver(),
        JY901SDataProcessor(),
        "51_0"
    )
    try:
        if (platform.system().lower() == 'linux'):
            device.serialConfig.portName = "/dev/inclinometer"   # Set serial port
        else:
            device.serialConfig.portName = "COM5"          # Set serial port
        device.serialConfig.baud = 9600                     # Set baud rate
        device.openDevice()                                 # Open serial port
        readConfig(device)                                  # Read configuration information
        device.dataProcessor.onVarChanged.append(onUpdate)  # Data update event
    except Exception as e:
        print(f"An error occurred: {e}")
    startRecord()                                       # Start recording data
    input()

    device.closeDevice()
    endRecord()                                         # End recording data

if __name__ == '__main__':

    start_inclinometer()
