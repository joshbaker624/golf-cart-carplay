#!/usr/bin/env python3
"""
Mac-compatible launcher for Golf Cart CarPlay System
Disables Raspberry Pi specific features
"""

import os
import sys

# Set debug mode to disable fullscreen
os.environ['DEBUG'] = '1'

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Mock RPi.GPIO for Mac
class MockGPIO:
    BCM = OUT = IN = None
    def setmode(self, *args): pass
    def setup(self, *args): pass
    def output(self, *args): pass
    def input(self, *args): return 0

sys.modules['RPi'] = type(sys)('RPi')
sys.modules['RPi.GPIO'] = MockGPIO()

# Mock gpsd
class MockGPSD:
    def connect(self): pass
    def get_current(self): 
        class Packet:
            mode = 0
            lat = 0
            lon = 0
            hspeed = 0
        return Packet()

sys.modules['gpsd'] = MockGPSD()

# Import QtWebEngine first (must be before QApplication)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Set shared OpenGL contexts
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Import and run main
from main import main

if __name__ == '__main__':
    print("Starting Golf Cart CarPlay System (Mac Mode)")
    print("Window will open at 800x480 (not fullscreen)")
    print("Hardware features (GPS, GPIO) are mocked")
    main()