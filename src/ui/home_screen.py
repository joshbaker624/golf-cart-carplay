"""
Home Screen UI for Golf Cart System
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from datetime import datetime

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_clock()
        
    def init_ui(self):
        """Initialize the home screen UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Header with clock and status
        header = self.create_header()
        layout.addWidget(header)
        
        # Main buttons grid
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Row 1: CarPlay and Music
        row1 = QHBoxLayout()
        row1.setSpacing(15)
        
        self.carplay_btn = self.create_button(
            "Apple CarPlay", 
            self.launch_carplay,
            "#007AFF"  # Apple blue
        )
        row1.addWidget(self.carplay_btn)
        
        self.music_btn = self.create_button(
            "Music Player",
            self.launch_music,
            "#1DB954"  # Spotify green
        )
        row1.addWidget(self.music_btn)
        
        buttons_layout.addLayout(row1)
        
        # Row 2: GPS and Settings
        row2 = QHBoxLayout()
        row2.setSpacing(15)
        
        self.gps_btn = self.create_button(
            "GPS Navigation",
            self.launch_gps,
            "#EA4335"  # Google red
        )
        row2.addWidget(self.gps_btn)
        
        self.settings_btn = self.create_button(
            "Settings",
            self.launch_settings,
            "#666666"  # Gray
        )
        row2.addWidget(self.settings_btn)
        
        buttons_layout.addLayout(row2)
        
        # Add buttons to main layout
        layout.addLayout(buttons_layout)
        
        # Status bar at bottom
        self.status_bar = self.create_status_bar()
        layout.addWidget(self.status_bar)
        
        self.setLayout(layout)
        
    def create_header(self):
        """Create header with clock and system info"""
        header = QFrame()
        header.setFrameStyle(QFrame.NoFrame)
        header.setFixedHeight(80)
        
        layout = QHBoxLayout()
        
        # Clock
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = QFont("Arial", 36, QFont.Bold)
        self.clock_label.setFont(font)
        self.clock_label.setStyleSheet("color: white;")
        layout.addWidget(self.clock_label)
        
        layout.addStretch()
        
        # Connection status
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_label.setStyleSheet("""
            color: #4CAF50;
            font-size: 18px;
            font-weight: bold;
            padding: 5px 10px;
            background-color: rgba(76, 175, 80, 0.2);
            border-radius: 5px;
        """)
        layout.addWidget(self.status_label)
        
        header.setLayout(layout)
        return header
        
    def create_button(self, text, callback, color="#2d2d2d"):
        """Create a styled button"""
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setMinimumHeight(120)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 24px;
                font-weight: bold;
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """)
        return button
        
    def darken_color(self, color):
        """Darken a hex color by 20%"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * 0.8) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        
    def create_status_bar(self):
        """Create status bar with system info"""
        status_bar = QFrame()
        status_bar.setFrameStyle(QFrame.NoFrame)
        status_bar.setFixedHeight(40)
        status_bar.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 5, 15, 5)
        
        # Battery/Power status
        self.power_label = QLabel("Power: Connected")
        self.power_label.setStyleSheet("color: #4CAF50; font-size: 14px;")
        layout.addWidget(self.power_label)
        
        layout.addStretch()
        
        # Temperature (if available)
        self.temp_label = QLabel("CPU: --°C")
        self.temp_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.temp_label)
        
        layout.addStretch()
        
        # GPS status
        self.gps_status_label = QLabel("GPS: Searching...")
        self.gps_status_label.setStyleSheet("color: #FFC107; font-size: 14px;")
        layout.addWidget(self.gps_status_label)
        
        status_bar.setLayout(layout)
        return status_bar
        
    def setup_clock(self):
        """Setup clock timer"""
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)  # Update every second
        self.update_clock()
        
        # System status timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_system_status)
        self.status_timer.start(5000)  # Update every 5 seconds
        
    def update_clock(self):
        """Update clock display"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.clock_label.setText(current_time)
        
    def update_system_status(self):
        """Update system status information"""
        # Update CPU temperature (Raspberry Pi specific)
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read()) / 1000
                self.temp_label.setText(f"CPU: {temp:.1f}°C")
        except:
            pass
            
    def launch_carplay(self):
        """Launch CarPlay interface"""
        if hasattr(self.parent, 'carplay_manager'):
            self.parent.carplay_manager.launch_carplay()
        else:
            self.status_label.setText("CarPlay Not Available")
            self.status_label.setStyleSheet("""
                color: #f44336;
                font-size: 18px;
                font-weight: bold;
                padding: 5px 10px;
                background-color: rgba(244, 67, 54, 0.2);
                border-radius: 5px;
            """)
            
    def launch_music(self):
        """Switch to music player"""
        self.parent.show_screen('music')
        
    def launch_gps(self):
        """Switch to GPS navigation"""
        self.parent.show_screen('gps')
        
    def launch_settings(self):
        """Switch to settings screen"""
        self.parent.show_screen('settings')
        
    def update_carplay_status(self, connected):
        """Update CarPlay connection status"""
        if connected:
            self.status_label.setText("iPhone Connected")
            self.status_label.setStyleSheet("""
                color: #4CAF50;
                font-size: 18px;
                font-weight: bold;
                padding: 5px 10px;
                background-color: rgba(76, 175, 80, 0.2);
                border-radius: 5px;
            """)
        else:
            self.status_label.setText("Ready")
            self.status_label.setStyleSheet("""
                color: #2196F3;
                font-size: 18px;
                font-weight: bold;
                padding: 5px 10px;
                background-color: rgba(33, 150, 243, 0.2);
                border-radius: 5px;
            """)