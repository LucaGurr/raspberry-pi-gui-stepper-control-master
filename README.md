# Raspberry Pi GUI Stepper Motor Control

A PyQt5-based GUI application for controlling stepper motors via a Raspberry Pi Zero, featuring a modern dark mode interface.

## Features

- Modern dark mode interface
- Serial connection management for Raspberry Pi Zero
- Multiple stepper motor control support
- Real-time motor position feedback
- Cross-platform support (Windows/Linux)
- Comprehensive test suite

## Project Structure

```
raspberry-pi-gui-stepper-control/
├── src/
│   ├── app.py
│   ├── gui/
│   │   └── main_window.py
│   └── utils/
│       └── serial_connection.py
├── tests/
│   └── test_app.py
├── requirements.txt
└── pytest.ini
```

## Requirements

- Python 3.10 or higher
- PyQt5
- pyserial
- Adafruit CircuitPython MotorKit
- pytest (for testing)

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

## Usage

Run the application:
```bash
python src/app.py
```

## Development

Run tests:
```bash
python -m pytest
```

## Testing

The project uses pytest with pytest-qt for GUI testing. To run tests:

```bash
python -m pytest -v
```

## License

None

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
