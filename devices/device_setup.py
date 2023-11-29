import os
import subprocess

# Dictionary to hold device information
DEVICES_INFO = {
    'motor': {'idVendor': '0403', 'idProduct': '6001'},
    'compass': {'idVendor': '0403', 'idProduct': '6010'},
    'radio': {'idVendor': '0403', 'idProduct': '6015'},
    'inclinometer': {'idVendor': '1a86', 'idProduct': '7523'},
    'gps': {'idVendor': '0403', 'idProduct': '6010'}
}

UDEV_RULES_PATH = '/etc/udev/rules.d/99-usb-serial.rules'

def create_udev_rule(name, idVendor, idProduct):
    rule = (
        f'SUBSYSTEM=="tty", ATTRS{{idVendor}}=="{idVendor}", ATTRS{{idProduct}}=="{idProduct}", '
        f'SYMLINK+="{name}"\n'
    )
    return rule

def write_udev_rules(rules):
    with open(UDEV_RULES_PATH, 'w') as f:
        f.writelines(rules)

def reload_udev_rules():
    subprocess.run(['sudo', 'udevadm', 'control', '--reload-rules'], check=True)
    subprocess.run(['sudo', 'udevadm', 'trigger'], check=True)

def main():
    if os.geteuid() != 0:
        exit("You need root privileges to run this script.")

    udev_rules = [create_udev_rule(name, **attributes) for name, attributes in DEVICES_INFO.items()]

    write_udev_rules(udev_rules)
    reload_udev_rules()
    print("Udev rules created and loaded successfully.")

if __name__ == '__main__':
    main()
