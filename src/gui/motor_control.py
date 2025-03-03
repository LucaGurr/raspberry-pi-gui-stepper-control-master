from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QHBoxLayout, QInputDialog
from utils.serial_connection import SerialConnection

class MotorControl(QWidget):
    def __init__(self, serial_connection: SerialConnection):
        super().__init__()
        self.serial_connection = serial_connection
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.motor_selector = QComboBox()
        self.motor_selector.addItems(["Motor 0", "Motor 1", "Motor 2", "Motor 3"])
        layout.addWidget(QLabel("Select Motor:"))
        layout.addWidget(self.motor_selector)

        self.direction_selector = QComboBox()
        self.direction_selector.addItems(["cw", "ccw"])
        layout.addWidget(QLabel("Select Direction:"))
        layout.addWidget(self.direction_selector)

        self.degrees_input = QLineEdit()
        layout.addWidget(QLabel("Enter Degrees:"))
        layout.addWidget(self.degrees_input)

        self.rotate_button = QPushButton("Rotate Motor")
        self.rotate_button.clicked.connect(self.rotate_motor)
        layout.addWidget(self.rotate_button)

        self.debug_info = QLabel("")
        layout.addWidget(self.debug_info)

        self.setLayout(layout)

    def rotate_motor(self):
        motor_id = self.motor_selector.currentIndex()
        direction = self.direction_selector.currentText()
        degrees = self.degrees_input.text()

        if not degrees.isdigit():
            self.debug_info.setText("Please enter a valid number for degrees.")
            return

        command = f"motor{motor_id} rotate {direction} {degrees} degrees\n"
        self.serial_connection.send_data(command)
        self.debug_info.setText(f"Sent command: {command.strip()}")