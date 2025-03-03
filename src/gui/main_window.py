from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QComboBox, QLineEdit, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from utils.serial_connection import SerialConnection
from gui.motor_control import MotorControl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)
        
        # Force dark mode
        self.set_dark_theme()

        self.serial_connection = SerialConnection()

        # Haupt-Widget und Layout erstellen
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Button zum Verbinden mit dem Raspberry Pi Zero
        self.connect_button = QPushButton("Connect to PI Zero")
        self.connect_button.clicked.connect(self.connect_to_pi)
        layout.addWidget(self.connect_button)

        # Debug-Informationen
        self.debug_info = QLabel("Debug Information")
        self.debug_info.setAlignment(Qt.AlignTop)
        layout.addWidget(self.debug_info)

        # Motorsteuerung
        self.motor_controls = []
        self.add_motor_control(layout)

        # Button zum Hinzufügen weiterer Motorsteuerungen
        self.add_motor_button = QPushButton("Add Motor Control")
        self.add_motor_button.clicked.connect(lambda: self.add_motor_control(layout))
        layout.addWidget(self.add_motor_button)

        # Layout dem zentralen Widget zuweisen
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def connect_to_pi(self):
        if self.serial_connection.open_connection():
            self.debug_info.setText("Connected to PI Zero")
        else:
            self.debug_info.setText("Failed to connect to PI Zero")

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