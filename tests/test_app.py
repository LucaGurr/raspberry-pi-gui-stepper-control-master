import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.app import App
from src.gui.main_window import MainWindow
from src.utils.serial_connection import SerialConnection

@pytest.fixture
def app(qapp, qtbot):
    """Create a fresh app instance for each test"""
    test_app = App()
    qtbot.addWidget(test_app.main_window)
    qtbot.waitExposed(test_app.main_window)
    
    yield test_app
    
    test_app.main_window.close()
    qapp.processEvents()

@pytest.mark.gui
def test_app_initialization(app, qtbot):
    """Test if the application initializes correctly"""
    with qtbot.waitActive(app.main_window):
        assert isinstance(app.app, QApplication)
        assert isinstance(app.main_window, MainWindow)

@pytest.mark.gui
def test_main_window_title(app, qtbot):
    """Test if the main window has correct title"""
    with qtbot.waitActive(app.main_window):
        assert app.main_window.windowTitle() == "Main Window"

@pytest.mark.gui
def test_serial_connection(app, qtbot):
    """Test if serial connection is properly initialized"""
    with qtbot.waitActive(app.main_window):
        assert isinstance(app.main_window.serial_connection, SerialConnection)