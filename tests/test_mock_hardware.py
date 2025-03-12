import pytest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
import paramiko

# Mock Adafruit dependencies before importing our modules
adafruit_mock = MagicMock()
board_mock = MagicMock()

with patch.dict('sys.modules', {
    'adafruit_motorkit': adafruit_mock,
    'board': board_mock,
    'adafruit_motor': MagicMock()
}):
    from mock_hardware import MockSerialConnection, MockI2CDevice
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
def main_window(qapp, qtbot_instance, mock_serial, mock_i2c):
    with patch('src.utils.serial_connection.SerialConnection', return_value=mock_serial):
        with patch('src.i2c.I2CDevice', return_value=mock_i2c):
            window = MainWindow()
            qtbot_instance.add_widget(window)
            return window

@pytest.fixture
def main_window_mock(qapp, qtbot_fix, mock_serial, mock_i2c):
    """Create main window with mocked hardware"""
    with patch('src.utils.serial_connection.SerialConnection', return_value=mock_serial):
        with patch('src.hardware.i2c.I2CDevice', return_value=mock_i2c):
            window = MainWindow()
            qtbot_fix.addWidget(window)
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
def test_main_window_with_mocks(main_window, qtbot_instance):
    assert main_window.windowTitle() == "Stepper Motor Control"
    qtbot_instance.waitExposed(main_window)

def test_main_window_with_mocks(main_window_mock):
    """Test main window with mocked hardware"""
    assert main_window_mock.windowTitle() == "Stepper Motor Control"

def test_ssh_connection(main_window, qtbot_instance):
    """Test SSH connection setup"""
    with patch.object(paramiko.SSHClient, 'connect', return_value=None) as mock_connect:
        main_window.ssh_ip_input.setText("192.168.7.2")
        main_window.ssh_password_input.setText("raspberry")
        main_window.connect_button.click()
        mock_connect.assert_called_once_with("192.168.7.2", username='pi', password='raspberry')
        assert main_window.debug_info.text() == "Connected to PI Zero via SSH"