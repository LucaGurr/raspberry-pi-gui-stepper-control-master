import pytest
from unittest.mock import patch
from mock_hardware import MockSerialConnection, MockI2CDevice
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow

# Create a single QApplication instance for all tests
@pytest.fixture(scope='session')
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

@pytest.fixture
def mock_serial():
    return MockSerialConnection()

@pytest.fixture
def mock_i2c():
    return MockI2CDevice(address=0x60)

@pytest.fixture
def main_window(qapp, mock_serial, mock_i2c, qtbot):
    with patch('src.utils.serial_connection.SerialConnection', return_value=mock_serial):
        with patch('src.i2c.I2CDevice', return_value=mock_i2c):
            window = MainWindow()
            qtbot.addWidget(window)
            return window

def test_serial_connection(mock_serial):
    assert not mock_serial.is_connected
    mock_serial.connect()
    assert mock_serial.is_connected
    mock_serial.disconnect()
    assert not mock_serial.is_connected

def test_motor_rotation(mock_serial):
    mock_serial.connect()
    response = mock_serial.send_command('motor0 rotate cw 90 degrees')
    assert response == 'OK'
    
    response = mock_serial.send_command('motor0 rotate ccw 90 degrees')
    assert response == 'OK'

def test_i2c_device(mock_i2c):
    initial_position = mock_i2c.position
    mock_i2c.step(100, 'cw')
    assert mock_i2c.position == initial_position + 100
    
    mock_i2c.step(50, 'ccw')
    assert mock_i2c.position == initial_position + 50

@pytest.mark.gui
def test_main_window_with_mocks(main_window, qtbot):
    assert main_window.windowTitle() == "Stepper Motor Control"
    qtbot.waitExposed(main_window)