import pytest
from PyQt5.QtWidgets import QApplication
from src.app import App  # Update import path
from src.gui.main_window import MainWindow
from src.utils.serial_connection import SerialConnection

@pytest.fixture(scope='function')
def app(qtbot):
    """Create a fresh app instance for each test"""
    test_app = App()
    qtbot.addWidget(test_app.main_window)
    yield test_app
    test_app.main_window.close()
    del test_app

@pytest.mark.gui
def test_app_initialization(app, qtbot):
    """Test if the application initializes correctly"""
    assert isinstance(app.app, QApplication)
    assert isinstance(app.main_window, MainWindow)

@pytest.mark.gui
def test_main_window_title(app, qtbot):
    """Test if the main window has correct title"""
    assert app.main_window.windowTitle() == "Main Window"

@pytest.mark.gui
def test_serial_connection(app, qtbot):
    """Test if serial connection is properly initialized"""
    assert isinstance(app.main_window.serial_connection, SerialConnection)

@pytest.mark.gui
def test_motor_controls(app, qtbot):
    """Test if motor controls are properly initialized"""
    assert hasattr(app.main_window, 'motor_controls')
    assert isinstance(app.main_window.motor_controls, list)