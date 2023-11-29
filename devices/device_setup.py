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

def create_udev_rule(name, idVendor, idProduct, use_kernel=False):
    if use_kernel:
        rule = f'KERNEL=="ttyUSB*", ATTRS{{idVendor}}=="{idVendor}", ATTRS{{idProduct}}=="{idProduct}", SYMLINK+="{name}"\n'
    else:
        rule = f'SUBSYSTEM=="tty", ATTRS{{idVendor}}=="{idVendor}", ATTRS{{idProduct}}=="{idProduct}", SYMLINK+="{name}"\n'
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

    seen_combinations = set()
    udev_rules = []

    for name, attributes in DEVICES_INFO.items():
        combo = (attributes['idVendor'], attributes['idProduct'])
        use_kernel = combo in seen_combinations
        seen_combinations.add(combo)

        rule = create_udev_rule(name, **attributes, use_kernel=use_kernel)
        udev_rules.append(rule)

    write_udev_rules(udev_rules)
    reload_udev_rules()
    print("Udev rules created and loaded successfully.")

if __name__ == '__main__':
    main()
