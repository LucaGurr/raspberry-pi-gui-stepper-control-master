import os
import sys
import pytest
from PyQt5.QtWidgets import QApplication

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='session')
def qapp():
    """Create the QApplication instance"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app

@pytest.fixture
def qtbot(qapp):
    """Create QtBot instance for testing"""
    from pytestqt.qtbot import QtBot
    return QtBot(qapp)