import pytest
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow

@pytest.fixture(scope="module")
def qapp():
    """Create the QApplication instance"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

@pytest.fixture
def main_window(qapp, qtbot_instance):
    """Create the main window for testing"""
    window = MainWindow()
    qtbot_instance.add_widget(window)
    return window

def test_app_initialization(qapp):
    """Test if QApplication initializes correctly"""
    assert QApplication.instance() is not None

@pytest.mark.gui
def test_main_window_title(main_window):
    """Test if main window has correct title"""
    assert main_window.windowTitle() == "Stepper Motor Control"

@pytest.mark.hardware
def test_serial_connection(main_window, qtbot):
    """Test serial connection functionality"""
    with qtbot.waitSignal(main_window.connection_status_changed, timeout=1000):
        main_window.connect_to_device()