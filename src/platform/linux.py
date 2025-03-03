import os

def get_serial_port():
    """Return the default serial port for Linux."""
    return '/dev/ttyUSB0'

def check_dependencies():
    """Check if required dependencies are installed for Linux."""
    try:
        import serial
        import adafruit_motorkit
        import adafruit_motor
    except ImportError as e:
        print(f"Missing dependency: {e.name}. Please install it using pip.")

def clear_console():
    """Clear the console for Linux."""
    os.system('clear')