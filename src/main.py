#!/usr/bin/env python3
"""
Golf Cart CarPlay System - Main Application
"""

import sys
import os
import json
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

# Import UI modules
from ui.home_screen import HomeScreen
from ui.music_player import MusicPlayer
from ui.gps_navigation import GPSNavigation
from ui.settings_screen import SettingsScreen
from carplay.carplay_manager import CarPlayManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GolfCartSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_settings()
        self.init_carplay()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Golf Cart Entertainment System")
        self.setGeometry(0, 0, 800, 480)  # Standard 7" touchscreen resolution
        
        # Enable fullscreen for production
        if not os.environ.get('DEBUG'):
            self.showFullScreen()
            
        # Create stacked widget for multiple screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize screens
        self.home_screen = HomeScreen(self)
        self.music_player = MusicPlayer(self)
        self.gps_navigation = GPSNavigation(self)
        self.settings_screen = SettingsScreen(self)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.music_player)
        self.stacked_widget.addWidget(self.gps_navigation)
        self.stacked_widget.addWidget(self.settings_screen)
        
        # Set home screen as default
        self.stacked_widget.setCurrentWidget(self.home_screen)
        
        # Apply dark theme for better visibility
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: 2px solid #3d3d3d;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #3d3d3d;
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)
        
    def load_settings(self):
        """Load application settings from config file"""
        settings_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config', 'settings.json'
        )
        
        try:
            with open(settings_path, 'r') as f:
                self.settings = json.load(f)
                logger.info("Settings loaded successfully")
        except FileNotFoundError:
            logger.warning("Settings file not found, using defaults")
            self.settings = self.get_default_settings()
            self.save_settings()
            
    def get_default_settings(self):
        """Return default settings"""
        return {
            "audio": {
                "volume": 70,
                "output_device": "default"
            },
            "display": {
                "brightness": 80,
                "auto_dim": True,
                "timeout_seconds": 300
            },
            "carplay": {
                "enabled": True,
                "auto_launch": True
            },
            "gps": {
                "enabled": True,
                "update_interval": 1
            }
        }
        
    def save_settings(self):
        """Save current settings to config file"""
        settings_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config', 'settings.json'
        )
        
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        
        with open(settings_path, 'w') as f:
            json.dump(self.settings, f, indent=2)
            
    def init_carplay(self):
        """Initialize CarPlay manager"""
        if self.settings.get('carplay', {}).get('enabled', True):
            self.carplay_manager = CarPlayManager(self)
            self.carplay_manager.device_connected.connect(self.on_carplay_connected)
            self.carplay_manager.device_disconnected.connect(self.on_carplay_disconnected)
            self.carplay_manager.start_monitoring()
            
    def on_carplay_connected(self):
        """Handle CarPlay device connection"""
        logger.info("CarPlay device connected")
        if self.settings.get('carplay', {}).get('auto_launch', True):
            self.carplay_manager.launch_carplay()
            
    def on_carplay_disconnected(self):
        """Handle CarPlay device disconnection"""
        logger.info("CarPlay device disconnected")
        self.show_screen('home')
        
    def show_screen(self, screen_name):
        """Switch to a different screen"""
        screens = {
            'home': self.home_screen,
            'music': self.music_player,
            'gps': self.gps_navigation,
            'settings': self.settings_screen
        }
        
        if screen_name in screens:
            self.stacked_widget.setCurrentWidget(screens[screen_name])
            logger.info(f"Switched to {screen_name} screen")
            
    def closeEvent(self, event):
        """Handle application close event"""
        self.save_settings()
        if hasattr(self, 'carplay_manager'):
            self.carplay_manager.stop_monitoring()
        event.accept()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Golf Cart System")
    
    # Set application icon if available
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Create and show main window
    window = GolfCartSystem()
    window.show()
    
    # Start application event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()