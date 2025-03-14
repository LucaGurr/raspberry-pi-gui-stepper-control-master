from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import sys
import paramiko
from utils.serial_connection import SerialConnection
from gui.motor_control import MotorControl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot Arm Control")
        self.setGeometry(100, 100, 800, 600)
        
        # Force dark theme
        self.set_dark_theme()

        self.serial_connection = SerialConnection()

        # Create main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create connection status label
        self.status_label = QLabel("Waiting for USB connection...")
        layout.addWidget(self.status_label)

        # USB connection button
        self.connect_button = QPushButton("Reconnect USB Device")
        self.connect_button.clicked.connect(self.connect_usb)
        layout.addWidget(self.connect_button)

        # Debug information
        self.debug_info = QLabel("Debug Information")
        self.debug_info.setAlignment(Qt.AlignTop)
        layout.addWidget(self.debug_info)

        # Initialize motor controls
        self.motor_controls = []
        self.add_motor_control(layout)

        self.add_motor_button = QPushButton("Add Motor Control")
        self.add_motor_button.clicked.connect(lambda: self.add_motor_control(layout))
        layout.addWidget(self.add_motor_button)

    def connect_usb(self):
        """Attempt to connect to USB-Serial device"""
        if self.serial_connection.open_connection():
            self.status_label.setText("Connected to USB device")
            return True
        self.status_label.setText("Failed to connect to USB device")
        return False

    def run_selected_test(self):
        """Execute the selected test and display results"""
        test_name = self.test_selector.currentText()
        
        test_results = {
            "Hardware Test": self.run_hardware_test,
            "Motor Rotation Test": self.run_motor_rotation_test,
            "Serial Connection Test": self.run_serial_test,
            "I2C Communication Test": self.run_i2c_test
        }
        
        if test_name in test_results:
            result = test_results[test_name]()
            self.debug_info.setText(f"Test Results: {result}")
        else:
            self.debug_info.setText("Invalid test selected")

    def run_hardware_test(self):
        """Run basic hardware connectivity test"""
        try:
            if self.serial_connection.open_connection():
                return "Hardware connection successful"
            return "Hardware connection failed"
        except Exception as e:
            return f"Hardware test error: {str(e)}"

    def run_motor_rotation_test(self):
        """Test motor rotation command"""
        try:
            if not self.serial_connection.serial:
                return "Not connected to hardware"
            cmd = "motor0 rotate cw 10 degrees\n"
            if self.serial_connection.send_data(cmd):
                return "Motor rotation command sent successfully"
            return "Failed to send motor command"
        except Exception as e:
            return f"Motor test error: {str(e)}"

    def run_serial_test(self):
        """Test serial communication"""
        try:
            if self.serial_connection.open_connection():
                self.serial_connection.close_connection()
                return "Serial connection test passed"
            return "Serial connection test failed"
        except Exception as e:
            return f"Serial test error: {str(e)}"

    def run_i2c_test(self):
        """Test I2C communication"""
        if sys.platform.startswith('win'):
            return "I2C testing is only available on Linux/Raspberry Pi systems"
            
        try:
            try:
                from smbus2 import SMBus
            except ImportError:
                return "I2C test error: smbus2 not installed. Run 'pip install smbus2'"
                
            try:
                bus = SMBus(1)  # Use I2C bus 1
                # Try to detect MotorHAT at default address
                bus.read_byte(0x60)
                bus.close()  # Clean up
                return "I2C communication successful"
            except OSError as e:
                return f"I2C hardware error: {str(e)}"
            except Exception as e:
                return f"I2C test error: {str(e)}"
        finally:
            if 'bus' in locals():
                bus.close()

    def connect_to_pi(self):
        """Auto-connect to roboterarm@roboterarm.local"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('roboterarm.local', username='roboterarm', password='1234')
            self.status_label.setText("Connected to Robot Arm")
            ssh.close()
            
            # After successful connection, attempt to open serial connection
            if self.serial_connection.open_connection():
                self.status_label.setText("Connected to Robot Arm and serial port")
            else:
                self.status_label.setText("Connected to Robot Arm but serial connection failed")
                
        except paramiko.AuthenticationException:
            self.status_label.setText("Authentication failed")
        except paramiko.SSHException as sshException:
            self.status_label.setText(f"SSH connection failed: {str(sshException)}")
        except Exception as e:
            self.status_label.setText(f"Connection error: {str(e)}")

    def add_motor_control(self, layout):
        motor_control = MotorControl(self.serial_connection)
        self.motor_controls.append(motor_control)
        layout.addWidget(motor_control)

    def set_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Pitch black background
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # Pure white text
        dark_palette.setColor(QPalette.Base, QColor(0, 0, 0))  # Pitch black background for text fields
        dark_palette.setColor(QPalette.AlternateBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))  # Pure white text
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))  # Dark grey buttons
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        self.setPalette(dark_palette)
        self.setStyleSheet("""
            * { 
                color: #ffffff;
                background-color: #000000;
            }
            QToolTip { 
                color: #ffffff; 
                background-color: #000000; 
                border: 1px solid #ffffff;
                border-radius: 4px;
            }
            QPushButton {
                color: #ffffff;
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                color: #ffffff;
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                padding: 6px;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #5d5d5d;
                background-color: #3d3d3d;
            }
            QComboBox {
                color: #ffffff;
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                padding: 6px;
                border-radius: 8px;
                min-height: 20px;
                padding-right: 20px;  /* Make room for arrow */
            }
            QComboBox:hover {
                background-color: #3d3d3d;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                margin-right: 8px;
                image: none;
                border: none;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background-color: transparent;
            }
            QComboBox::drop-down::after {
                content: "";
                position: absolute;
                top: 50%;
                right: 8px;
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QComboBox QAbstractItemView {
                color: #ffffff;
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                selection-background-color: #3d3d3d;
                padding: 4px;
            }
        """)