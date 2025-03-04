import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.app import App
from src.gui.main_window import MainWindow
from src.utils.serial_connection import SerialConnection

@pytest.fixture(scope="session")
def qapp():
    """Create the QApplication instance"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def main_window(qapp, qtbot):
    """Create the main window for testing"""
    window = MainWindow()
    qtbot.addWidget(window)
    return window

def test_app_initialization(qapp):
    """Test if QApplication initializes correctly"""
    assert QApplication.instance() is not None

def test_main_window_title(main_window):
    """Test if main window has correct title"""
    assert main_window.windowTitle() == "Stepper Motor Control"

def test_serial_connection(main_window, qtbot):
    """Test serial connection functionality"""
    with qtbot.waitSignal(main_window.connection_status_changed, timeout=1000):
        main_window.connect_to_device()