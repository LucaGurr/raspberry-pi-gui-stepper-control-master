# Raspberry Pi GUI Stepper Motor Control

A PyQt5-based GUI application for controlling stepper motors via a Raspberry Pi Zero, featuring a modern dark mode interface.

## Features

- Modern dark mode interface
- Serial connection management for Raspberry Pi Zero
- Multiple stepper motor control support
- Real-time motor position feedback
- Cross-platform support (Windows(COM3)/Linux(/dev/ttyUSB0))
- Comprehensive test suite

## Technical Overview

### Under the Hood

#### GUI Architecture
- **Event-Driven Design**: PyQt5 signal/slot mechanism for asynchronous operations
- **Dark Mode Implementation**: Custom stylesheet system with configurable themes
- **Widget Hierarchy**:
  ```
  MainWindow
  └── MotorControlWidget (Multiple instances)
      ├── DirectionSelector (ComboBox)
      ├── DegreeInput (SpinBox)
      └── ControlButtons
  ```

#### Hardware Communication
- **Serial Protocol**: 9600 baud, 8-N-1 configuration
- **Command Buffer**: FIFO queue for motor commands
- **Error Handling**: Automatic reconnection and command retry
- **Platform Detection**: Auto-configuration for Windows/Linux

#### Motor Control
- **Stepping Modes**: Full-step (200 steps/rev), Half-step (400 steps/rev)
- **Position Tracking**: Real-time degree and step counting
- **Emergency Stop**: Immediate motor halt capability
- **Power Management**: Auto-shutdown on inactivity

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

### Testing Framework

The project uses pytest with several specialized fixtures and mock objects for hardware simulation.

#### Test Structure
```text
tests/
├── conftest.py           # Shared fixtures and configuration
├── test_app.py          # Core application tests
├── mock_hardware.py     # Hardware simulation classes
└── test_mock_hardware.py # Hardware simulation tests
```

#### Mock Hardware Components
```python
# Serial Connection Mock
class MockSerialConnection:
    def __init__(self, port='COM3', baudrate=9600):
        self.is_connected = False
        self.mock_responses = {
            'motor0 rotate cw 90 degrees': 'OK',
            'motor0 rotate ccw 90 degrees': 'OK'
        }

# I2C Device Mock
class MockI2CDevice:
    def __init__(self, address):
        self.position = 0
        self.direction = 'cw'
```

#### Test Categories
1. **Hardware Mock Tests** - `test_mock_hardware.py`
   ```python
   def test_serial_connection(mock_serial):
       # Tests basic serial connectivity
       assert not mock_serial.is_connected
       mock_serial.connect()
       assert mock_serial.is_connected

   def test_motor_rotation(mock_serial):
       # Tests motor rotation commands
       mock_serial.connect()
       response = mock_serial.send_command('motor0 rotate cw 90 degrees')
       assert response == 'OK'

   def test_i2c_device(mock_i2c):
       # Tests stepper motor positioning
       initial_position = mock_i2c.position
       mock_i2c.step(100, 'cw')
       assert mock_i2c.position == initial_position + 100
   ```

2. **Basic Application Tests** - `test_app.py`
   ```python
   @pytest.mark.gui
   def test_app_initialization(qapp):
       # Tests QApplication setup
       assert QApplication.instance() is not None

   @pytest.mark.hardware
   def test_serial_connection(main_window, qtbot):
       # Tests hardware communication (skipped on non-Pi)
       ...
   ```

#### Test Results
When running on a development machine:
```bash
$ python -m pytest -v
============= test session starts =============
collected 7 items

test_app.py::test_app_initialization PASSED                 [ 14%]
test_app.py::test_main_window_title ERROR                  [ 28%]
test_app.py::test_serial_connection SKIPPED                [ 42%]
test_mock_hardware.py::test_serial_connection PASSED       [ 57%]
test_mock_hardware.py::test_motor_rotation PASSED          [ 71%]
test_mock_hardware.py::test_i2c_device PASSED             [ 85%]
test_mock_hardware.py::test_main_window_with_mocks ERROR  [100%]
```

- ✅ All hardware mock tests pass
- ✅ Basic application initialization works
- ⏭️ Hardware tests automatically skipped
- ❌ GUI tests require display setup

#### Running Tests
```bash
# Run only mock hardware tests
python -m pytest -v -k "mock"

# Run non-GUI tests
python -m pytest -v -m "not gui"

# Run with coverage report
python -m pytest --cov=src tests/
```

### Mock Testing
The project includes comprehensive hardware mocking:

```python
# Example mock usage
@pytest.fixture
def mock_motor():
    with patch('src.hardware.motor.MotorController') as mock:
        yield mock
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run GUI-specific tests
python -m pytest -v -m gui

# Run with detailed output
python -m pytest -v --capture=no
```

### Debug Mode
Set environment variable for debug output:
```bash
# Windows
set DEBUG=1

# Linux/Mac
export DEBUG=1
```

### Logging Levels
```python
# Available debug levels
DEBUG_LEVELS = {
    'OFF': 0,
    'ERROR': 1,
    'WARN': 2,
    'INFO': 3,
    'DEBUG': 4,
    'TRACE': 5
}
```

## Troubleshooting

### Common Issues

1. **Serial Connection Issues**
   - Check USB connection
   - Verify correct port in platform settings
   - Ensure proper permissions on Linux
   ```bash
   # Linux permission fix
   sudo usermod -a -G dialout $USER
   ```

2. **Motor Control Issues**
   - Verify I2C addresses (0x60 and 0x61)
   - Check power supply connection
   - Verify motor wiring sequence
   ```bash
   # I2C address verification
   i2cdetect -y 1
   ```

3. **GUI Issues**
   - Check Qt version compatibility
   - Verify display settings
   - Enable debug logging
   ```bash
   set DEBUG=4  # Windows
   export DEBUG=4  # Linux/Mac
   ```

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
