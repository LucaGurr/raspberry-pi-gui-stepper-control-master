# Raspberry Pi GUI Project

This project provides a graphical user interface (GUI) for controlling stepper motors connected to a Raspberry Pi via USB serial. The application allows users to interface with the motors, view debug information, and manage connections to the Raspberry Pi.

## Project Structure

```
raspberry-pi-gui
├── src
│   ├── app.py               # Entry point of the application
│   ├── i2c.py               # Logic for controlling stepper motors
│   ├── gui
│   │   ├── main_window.py    # Main GUI window definition
│   │   └── motor_control.py   # Motor control interface
│   ├── platform
│   │   ├── __init__.py       # Marks the directory as a Python package
│   │   ├── base.py           # Base functionality for platform-specific implementations
│   │   ├── linux.py          # Linux-specific implementations
│   │   └── windows.py        # Windows-specific implementations
│   └── utils
│       └── serial_connection.py # USB serial connection handling
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd raspberry-pi-gui
   ```

2. **Install dependencies**:
   Ensure you have Python 3 installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Connect the Raspberry Pi**:
   Connect your Raspberry Pi to your computer via USB.

4. **Run the application**:
   Execute the following command to start the GUI:
   ```
   python src/app.py
   ```

## Usage Guidelines

- **Connecting to the Raspberry Pi**: Use the connection options in the main window to establish a link with the Raspberry Pi.
- **Motor Control**: Navigate to the motor control interface to select motors, specify rotation direction, and set degrees of rotation.
- **Debug Information**: View real-time debug information in the main window to monitor the status of the connection and motor operations.

## Features

- User-friendly GUI for easy interaction with stepper motors.
- Real-time debug information display.
- Ability to control multiple motors grouped by HAT.
- Local execution on the user's machine with USB serial communication.

## Compatibility

This project is designed to work on both Windows and Linux platforms. The platform-specific implementations are handled in the `src/platform` directory.
