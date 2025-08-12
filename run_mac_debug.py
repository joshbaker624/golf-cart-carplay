#!/usr/bin/env python3
"""
Mac-compatible launcher with debug mode for Golf Cart CarPlay System
"""

import os
import sys
import traceback

# Set debug mode
os.environ['DEBUG'] = '1'

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Mock RPi.GPIO
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

def main():
    print("Starting Golf Cart CarPlay System (Debug Mode)")
    print("=" * 50)
    
    try:
        # Import QtWebEngine first (required for WebEngine to work properly)
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import qInstallMessageHandler, QtInfoMsg, QtWarningMsg, QtCriticalMsg, QtFatalMsg, Qt
        
        # Set shared OpenGL contexts
        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        
        # Qt message handler for debugging
        def qt_message_handler(mode, context, message):
            if mode == QtInfoMsg:
                mode_str = 'INFO'
            elif mode == QtWarningMsg:
                mode_str = 'WARNING'
            elif mode == QtCriticalMsg:
                mode_str = 'CRITICAL'
            elif mode == QtFatalMsg:
                mode_str = 'FATAL'
            else:
                mode_str = 'DEBUG'
            
            print(f"Qt {mode_str}: {message}")
            
            # Print context info for critical/fatal
            if mode in (QtCriticalMsg, QtFatalMsg):
                if context.file:
                    print(f"  File: {context.file}:{context.line}")
                if context.function:
                    print(f"  Function: {context.function}")
        
        qInstallMessageHandler(qt_message_handler)
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Golf Cart System")
        
        # Import main window
        from main import GolfCartSystem
        
        print("Creating main window...")
        window = GolfCartSystem()
        
        print("Showing window...")
        window.show()
        
        print("Starting event loop...")
        print("=" * 50)
        
        # Run event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        print("\n" + "=" * 50)
        print("CRASH DETECTED!")
        print("=" * 50)
        print(f"Error: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        print("=" * 50)
        
        # Try to show error in GUI if possible
        try:
            from PyQt5.QtWidgets import QMessageBox
            if 'app' in locals():
                QMessageBox.critical(None, "Application Crash", 
                                   f"The application crashed with error:\n\n{str(e)}\n\n"
                                   "Check terminal for full details.")
        except:
            pass

if __name__ == '__main__':
    main()