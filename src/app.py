import sys
import os
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui.main_window import MainWindow

# Force X11 on Linux
if sys.platform.startswith('linux'):
    os.environ["QT_QPA_PLATFORM"] = "xcb"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        # Auto-connect to USB-Serial on startup
        self.connect_serial()

    def connect_serial(self):
        """Auto-connect to the first available USB-Serial port"""
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "USB" in port.description:
                try:
                    self.serial = serial.Serial(
                        port=port.device,
                        baudrate=115200,
                        timeout=1
                    )
                    self.main_window.status_label.setText(f"Connected to {port.device}")
                    return True
                except serial.SerialException as e:
                    self.main_window.status_label.setText(f"Failed to connect: {str(e)}")
                    return False
        self.main_window.status_label.setText("No USB-Serial device found")
        return False

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = App()
    app.run()