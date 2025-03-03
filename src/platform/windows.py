import os
import sys

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def platform_specific_setup():
    # Windows-specific setup code can be added here
    pass

def get_serial_port():
    """Return the default serial port for Windows."""
    return 'COM3'  # Adjust as necessary for your setup

def check_dependencies():
    """Check if required dependencies are installed for Windows."""
    try:
        import serial
        import adafruit_motorkit
        import adafruit_motor
    except ImportError as e:
        print(f"Missing dependency: {e.name}. Please install it using pip.")

if __name__ == "__main__":
    clear_console()
    print("Running on Windows platform.")
    platform_specific_setup()