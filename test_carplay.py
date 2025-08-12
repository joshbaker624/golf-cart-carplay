#!/usr/bin/env python3
"""Test CarPlay mock interface independently"""

import sys
import os

# Set debug
os.environ['DEBUG'] = '1'

# Add src to path
sys.path.insert(0, 'src')

# Import Qt first
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Set shared OpenGL contexts
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Create app
app = QApplication(sys.argv)

# Import and test mock CarPlay
from carplay.mock_carplay import MockCarPlay

print("Creating MockCarPlay window...")
carplay = MockCarPlay()
carplay.show()

print("MockCarPlay window should be visible now")

sys.exit(app.exec_())