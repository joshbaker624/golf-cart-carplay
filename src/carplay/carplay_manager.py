"""
CarPlay Manager - Handles Apple CarPlay integration
"""

import os
import subprocess
import logging
from PyQt5.QtCore import QObject, QTimer, pyqtSignal, QProcess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)

class CarPlayManager(QObject):
    """Manages CarPlay connection and display"""
    
    device_connected = pyqtSignal()
    device_disconnected = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.carplay_process = None
        self.monitoring = False
        self.connected = False
        
        # Check for OpenAuto Pro installation
        self.openauto_path = self.find_openauto()
        
    def find_openauto(self):
        """Find OpenAuto Pro installation"""
        possible_paths = [
            "/usr/local/bin/openauto",
            "/opt/openauto/bin/openauto",
            "/home/pi/openauto/bin/openauto",
            os.path.expanduser("~/openauto/bin/openauto")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found OpenAuto at: {path}")
                return path
                
        logger.warning("OpenAuto Pro not found. CarPlay functionality limited.")
        return None
        
    def start_monitoring(self):
        """Start monitoring for iPhone connections"""
        self.monitoring = True
        
        # Setup USB monitoring timer
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.check_usb_devices)
        self.monitor_timer.start(2000)  # Check every 2 seconds
        
        logger.info("Started CarPlay device monitoring")
        
    def stop_monitoring(self):
        """Stop monitoring for devices"""
        self.monitoring = False
        if hasattr(self, 'monitor_timer'):
            self.monitor_timer.stop()
            
    def check_usb_devices(self):
        """Check for connected Apple devices"""
        try:
            # Use lsusb to find Apple devices
            result = subprocess.run(
                ['lsusb'], 
                capture_output=True, 
                text=True
            )
            
            # Apple vendor ID is 05ac
            apple_device_found = '05ac:' in result.stdout
            
            if apple_device_found and not self.connected:
                self.connected = True
                self.device_connected.emit()
                logger.info("Apple device connected")
                
            elif not apple_device_found and self.connected:
                self.connected = False
                self.device_disconnected.emit()
                logger.info("Apple device disconnected")
                
        except Exception as e:
            logger.error(f"Error checking USB devices: {e}")
            
    def launch_carplay(self):
        """Launch CarPlay interface"""
        if self.openauto_path:
            self.launch_openauto()
        else:
            # Launch our custom CarPlay view
            self.launch_custom_carplay()
            
    def launch_openauto(self):
        """Launch OpenAuto Pro"""
        try:
            if self.carplay_process and self.carplay_process.state() == QProcess.Running:
                logger.info("OpenAuto already running")
                return
                
            self.carplay_process = QProcess()
            self.carplay_process.finished.connect(self.on_carplay_closed)
            
            # Launch OpenAuto with appropriate parameters
            args = [
                '--fullscreen',
                '--audio-channels', '2',
                '--fps', '30',
                '--resolution', '800x480',
                '--dpi', '150'
            ]
            
            self.carplay_process.start(self.openauto_path, args)
            logger.info("Launched OpenAuto Pro")
            
        except Exception as e:
            logger.error(f"Error launching OpenAuto: {e}")
            
    def launch_custom_carplay(self):
        """Launch custom CarPlay interface (fallback)"""
        # Hide main window and show CarPlay widget
        if self.parent:
            self.parent.hide()
            
        self.carplay_widget = CarPlayWidget(self.parent)
        self.carplay_widget.show()
        
    def on_carplay_closed(self):
        """Handle CarPlay process closure"""
        logger.info("CarPlay process closed")
        if self.parent and self.parent.isHidden():
            self.parent.show()
            
    def stop_carplay(self):
        """Stop CarPlay interface"""
        if self.carplay_process and self.carplay_process.state() == QProcess.Running:
            self.carplay_process.terminate()
            
        if hasattr(self, 'carplay_widget'):
            self.carplay_widget.close()
            
            
class CarPlayWidget(QWidget):
    """Custom CarPlay widget for when OpenAuto is not available"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the CarPlay UI"""
        self.setWindowTitle("CarPlay")
        self.setGeometry(0, 0, 800, 480)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        if not os.environ.get('DEBUG'):
            self.showFullScreen()
            
        layout = QVBoxLayout()
        
        # Information label
        info_label = QLabel(
            "CarPlay Ready\n\n"
            "Please connect your iPhone via USB.\n\n"
            "Note: This is a placeholder interface.\n"
            "For full CarPlay functionality, please install OpenAuto Pro.\n\n"
            "Touch anywhere to return to main menu."
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                background-color: #000;
                padding: 20px;
            }
        """)
        
        layout.addWidget(info_label)
        self.setLayout(layout)
        
        # Set black background
        self.setStyleSheet("background-color: black;")
        
    def mousePressEvent(self, event):
        """Handle touch/click to return to main menu"""
        self.close()
        if self.parent():
            self.parent().show()