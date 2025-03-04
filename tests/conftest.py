import os
import sys
import pytest
import platform
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure Qt doesn't use platform-specific features that might cause issues
def pytest_configure(config):
    """Configure pytest with GUI marker"""
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    config.addinivalue_line("markers", "gui: mark test as GUI test")

def pytest_runtest_setup(item):
    """Skip hardware tests when not on Raspberry Pi"""
    if 'hardware' in item.keywords and platform.system() != 'Linux':
        pytest.skip('Hardware tests can only run on Raspberry Pi')

@pytest.fixture(scope="session", autouse=True)
def qapp_auto():
    """Ensure QApplication exists and is properly torn down"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def qtbot(qapp_auto, request):
    """Provide a QtBot instance with proper cleanup"""
    from pytestqt.plugin import QtBot
    bot = QtBot(qapp_auto)
    return bot

def cleanup_qt():
    """Clean up Qt widgets"""
    QApplication.instance().processEvents()