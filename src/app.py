import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui.main_window import MainWindow

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = App()
    app.run()