# Raspberry Pi GUI Stepper Motor Control

A PyQt5-based GUI application for controlling stepper motors via a Raspberry Pi Zero, featuring a modern dark mode interface.

## Features

- Modern dark mode interface
- Serial connection management for Raspberry Pi Zero
- Multiple stepper motor control support
- Real-time motor position feedback
- Cross-platform support (Windows/Linux)
- Comprehensive test suite

## Technical Overview

### Architecture

The application follows a modular architecture:

1. **GUI Layer** (`src/gui/`)
   - `main_window.py`: Primary window implementing dark theme and layout management
   - `motor_control.py`: Individual motor control widgets with direction and degree inputs

2. **Hardware Communication** (`src/utils/`)
   - `serial_connection.py`: Handles serial communication with Raspberry Pi
   - Supports multiple baudrates (default: 9600)
   - Implements connection pooling and error handling

3. **Platform Abstraction** (`src/platform/`)
   - `windows.py` & `linux.py`: Platform-specific implementations
   - Automatic serial port detection
   - OS-specific optimizations

### Motor Control System

The stepper motor control system utilizes:

- **I2C Communication**
  - Two MotorHAT boards (addresses: 0x60 and 0x61)
  - Each board controls 2 stepper motors
  - Total support for 4 independent motors

- **Stepper Motor Specifications**
  - 200 steps per revolution
  - Supports both clockwise (CW) and counter-clockwise (CCW) rotation
  - Precision control down to individual steps

### Command Protocol

Serial commands follow the format:

```text
motor<id> rotate <direction> <degrees> degrees
```

Example:
```text
motor0 rotate cw 90 degrees
```

## Project Structure

```text
raspberry-pi-gui-stepper-control/
├── src/
│   ├── app.py                 # Application entry point
│   ├── i2c.py                # I2C communication layer
│   ├── gui/
│   │   ├── main_window.py    # Main GUI window
│   │   └── motor_control.py  # Motor control widget
│   ├── platform/
│   │   ├── windows.py        # Windows-specific code
│   │   └── linux.py         # Linux-specific code
│   └── utils/
│       ├── serial_connection.py  # Serial communication
│       └── platform_check.py    # Platform detection
├── tests/
│   ├── conftest.py           # pytest configuration
│   └── test_app.py          # Application tests
├── requirements.txt
└── pytest.ini
```

## Requirements

- Python 3.10 or higher
- PyQt5 for GUI implementation
- pyserial for communication
- Adafruit CircuitPython MotorKit
- pytest and related packages for testing

## Hardware Requirements

- Raspberry Pi Zero (or compatible)
- 2x Adafruit DC & Stepper Motor HAT
- Up to 4 stepper motors
- 12V power supply for motors
- USB-to-Serial converter (if using USB connection)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/raspberry-pi-gui-stepper-control.git
cd raspberry-pi-gui-stepper-control
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. For development/testing, install additional requirements:
```bash
pip install pytest pytest-qt pytest-mock pytest-cov
```

## Configuration

### Serial Connection
- Windows: Usually `COM3` (configurable in `platform/windows.py`)
- Linux: Usually `/dev/ttyUSB0` (configurable in `platform/linux.py`)
- Baudrate: 9600 (configurable in `utils/serial_connection.py`)

### I2C Setup
1. Enable I2C on Raspberry Pi:
```bash
sudo raspi-config
# Navigate to Interface Options -> I2C -> Enable
```

2. Verify I2C devices:
```bash
i2cdetect -y 1
```

## Usage

1. Run the application:
```bash
python src/app.py
```

2. Connect to Raspberry Pi using the "Connect to PI Zero" button
3. Add motor controls as needed
4. Control motors using the interface:
   - Select motor (0-3)
   - Choose direction (CW/CCW)
   - Enter degrees
   - Click "Rotate Motor"

## Development

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run GUI-specific tests
python -m pytest -v -m gui
```

### Debug Mode
Set environment variable for debug output:
```bash
export DEBUG=1  # Linux/Mac
set DEBUG=1     # Windows
```

## Troubleshooting

1. **Serial Connection Issues**
   - Check USB connection
   - Verify correct port in platform settings
   - Ensure proper permissions on Linux

2. **Motor Control Issues**
   - Verify I2C addresses (0x60 and 0x61)
   - Check power supply connection
   - Verify motor wiring sequence

## License

None

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a new Pull Request

## Acknowledgments

- PyQt5 for the GUI framework
- Adafruit for the MotorHAT library
- Contributors and testers
