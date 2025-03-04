from unittest.mock import MagicMock

class MockSerialConnection:
    def __init__(self, port='COM3', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.is_connected = False
        self.mock_responses = {
            'motor0 rotate cw 90 degrees': 'OK',
            'motor0 rotate ccw 90 degrees': 'OK',
            'motor1 rotate cw 180 degrees': 'OK',
            'motor1 rotate ccw 180 degrees': 'OK'
        }

    def connect(self):
        self.is_connected = True
        return True

    def disconnect(self):
        self.is_connected = False
        return True

    def send_command(self, command):
        if not self.is_connected:
            raise ConnectionError("Not connected")
        return self.mock_responses.get(command, 'ERROR')

class MockI2CDevice:
    def __init__(self, address):
        self.address = address
        self.position = 0
        self.direction = 'cw'

    def step(self, steps, direction):
        self.direction = direction
        if direction == 'cw':
            self.position += steps
        else:
            self.position -= steps
        return True