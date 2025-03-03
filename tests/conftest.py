import os
import sys
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure Qt doesn't use platform-specific features that might cause issues
def pytest_configure(config):
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

@pytest.fixture(scope='session')
def qapp():
    """Create a Qt application for the entire test session"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

@pytest.fixture
def qtbot(qapp, request):
    """Provide a QtBot instance with proper cleanup"""
    from pytestqt.plugin import QtBot
    bot = QtBot(qapp)
    return bot

def cleanup_qt():
    """Clean up Qt widgets"""
    QApplication.instance().processEvents()