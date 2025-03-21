import sys

def is_windows():
    return sys.platform.startswith('win')

def is_linux():
    return sys.platform.startswith('linux')

def get_serial_port():
    if is_windows():
        return 'COM3'  # Default Windows port
    return '/dev/ttyACM0'  # Default Linux/Raspberry Pi port for USB connection