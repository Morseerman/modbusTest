import os
import subprocess

# Dictionary to hold device information, including the motor.
# You can add more devices later in the same format.
DEVICES_INFO = {
    'motor': {'idVendor': '0403', 'idProduct': '6001', 'serial': 'A60321EB'},
    'compass': {'idVendor': '0403', 'idProduct': '6010', 'serial': 'FTVIZSZU'},
    'inclinometer': {'idVendor': '1a86', 'idProduct': '7523', 'devpath': '1.1'}
}


UDEV_RULES_PATH = '/etc/udev/rules.d/99-usb-serial.rules'

def create_udev_rule(name, idVendor, idProduct, devpath=None, serial=None):
    # Start with the base rule
    rule = (
        f'SUBSYSTEM=="tty", ATTRS{{idVendor}}=="{idVendor}", '
        f'ATTRS{{idProduct}}=="{idProduct}"'
    )
    
    # Add the serial if available, otherwise use devpath
    if serial:
        rule += f', ATTRS{{serial}}=="{serial}"'
    elif devpath:
        rule += f', ATTRS{{devpath}}=="{devpath}"'
    else:
        raise ValueError("Either serial or devpath must be provided.")
    
    # Finish the rule with the symlink
    rule += f', SYMLINK+="{name}"\n'
    return rule


def write_udev_rules(rules):
    with open(UDEV_RULES_PATH, 'w') as f:
        f.writelines(rules)

def reload_udev_rules():
    subprocess.run(['sudo', 'udevadm', 'control', '--reload-rules'], check=True)
    subprocess.run(['sudo', 'udevadm', 'trigger'], check=True)

def main():
    # Ensure this script is running with superuser privileges
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

    # Create udev rules for all devices in the dictionary
    udev_rules = [create_udev_rule(name, **attributes) for name, attributes in DEVICES_INFO.items()]
    
    # Write the udev rules to the file
    write_udev_rules(udev_rules)

    # Reload the udev rules to apply changes
    reload_udev_rules()
    print("Udev rules created and loaded successfully.")

if __name__ == '__main__':
    main()
