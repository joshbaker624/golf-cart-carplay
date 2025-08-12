"""
GPS Navigation UI for Golf Cart System
"""

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QComboBox, QLineEdit)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont

class GPSNavigation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_location = None
        self.init_ui()
        self.setup_gps()
        
    def init_ui(self):
        """Initialize the GPS navigation UI"""
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with back button and search
        header = self.create_header()
        layout.addWidget(header)
        
        # Map view (using QWebEngineView for web-based maps)
        self.map_view = QWebEngineView()
        self.map_view.setUrl(QUrl("https://www.openstreetmap.org"))
        layout.addWidget(self.map_view)
        
        # GPS info bar
        self.info_bar = self.create_info_bar()
        layout.addWidget(self.info_bar)
        
        self.setLayout(layout)
        
    def create_header(self):
        """Create header with navigation controls"""
        header = QFrame()
        header.setFrameStyle(QFrame.NoFrame)
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #2a2a2a;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.parent.show_screen('home'))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:pressed {
                color: #ccc;
            }
        """)
        layout.addWidget(back_btn)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search location...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
            }
        """)
        self.search_input.returnPressed.connect(self.search_location)
        layout.addWidget(self.search_input)
        
        # Search button
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_location)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #357ae8;
            }
        """)
        layout.addWidget(search_btn)
        
        header.setLayout(layout)
        return header
        
    def create_info_bar(self):
        """Create GPS information bar"""
        info_bar = QFrame()
        info_bar.setFrameStyle(QFrame.NoFrame)
        info_bar.setFixedHeight(100)
        info_bar.setStyleSheet("background-color: #1a1a1a;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Speed display
        speed_frame = self.create_info_widget("Speed", "0", "mph")
        layout.addWidget(speed_frame)
        
        # Distance display
        distance_frame = self.create_info_widget("Distance", "0.0", "mi")
        layout.addWidget(distance_frame)
        
        # ETA display
        eta_frame = self.create_info_widget("ETA", "--:--", "")
        layout.addWidget(eta_frame)
        
        # Quick destinations
        quick_dest = QFrame()
        quick_layout = QVBoxLayout()
        
        dest_label = QLabel("Quick Destinations")
        dest_label.setStyleSheet("color: #aaa; font-size: 14px;")
        quick_layout.addWidget(dest_label)
        
        self.dest_combo = QComboBox()
        self.dest_combo.addItems([
            "Clubhouse",
            "Driving Range", 
            "Pro Shop",
            "Hole 1",
            "Hole 10",
            "Parking"
        ])
        self.dest_combo.setStyleSheet("""
            QComboBox {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
        """)
        self.dest_combo.currentTextChanged.connect(self.navigate_to_destination)
        quick_layout.addWidget(self.dest_combo)
        
        quick_dest.setLayout(quick_layout)
        layout.addWidget(quick_dest)
        
        info_bar.setLayout(layout)
        
        # Store info widgets for updates
        self.speed_label = speed_frame.findChild(QLabel, "value")
        self.distance_label = distance_frame.findChild(QLabel, "value")
        self.eta_label = eta_frame.findChild(QLabel, "value")
        
        return info_bar
        
    def create_info_widget(self, title, value, unit):
        """Create an information display widget"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #aaa; font-size: 14px;")
        layout.addWidget(title_label)
        
        value_layout = QHBoxLayout()
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        value_layout.addWidget(value_label)
        
        if unit:
            unit_label = QLabel(unit)
            unit_label.setStyleSheet("color: #aaa; font-size: 16px; margin-left: 5px;")
            value_layout.addWidget(unit_label)
            
        value_layout.addStretch()
        layout.addLayout(value_layout)
        
        frame.setLayout(layout)
        return frame
        
    def setup_gps(self):
        """Setup GPS monitoring"""
        # GPS update timer
        self.gps_timer = QTimer()
        self.gps_timer.timeout.connect(self.update_gps_data)
        self.gps_timer.start(1000)  # Update every second
        
        # Try to get GPS data
        try:
            import gpsd
            gpsd.connect()
            self.gpsd_connected = True
        except:
            self.gpsd_connected = False
            
    def update_gps_data(self):
        """Update GPS information"""
        if self.gpsd_connected:
            try:
                import gpsd
                packet = gpsd.get_current()
                
                if packet.mode >= 2:
                    # Update speed
                    speed_mph = packet.hspeed * 2.237  # Convert m/s to mph
                    self.speed_label.setText(f"{speed_mph:.0f}")
                    
                    # Store location
                    self.current_location = (packet.lat, packet.lon)
                    
                    # Update map center if significant movement
                    # (Implementation depends on map provider)
                    
            except:
                pass
                
    def search_location(self):
        """Search for a location"""
        query = self.search_input.text()
        if query:
            # For OpenStreetMap
            search_url = f"https://www.openstreetmap.org/search?query={query}"
            self.map_view.setUrl(QUrl(search_url))
            
    def navigate_to_destination(self, destination):
        """Navigate to a quick destination"""
        # Golf course destinations (example coordinates)
        destinations = {
            "Clubhouse": (35.7796, -78.6382),
            "Driving Range": (35.7810, -78.6370),
            "Pro Shop": (35.7798, -78.6385),
            "Hole 1": (35.7802, -78.6378),
            "Hole 10": (35.7825, -78.6360),
            "Parking": (35.7790, -78.6390)
        }
        
        if destination in destinations:
            lat, lon = destinations[destination]
            # Center map on destination
            map_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}"
            self.map_view.setUrl(QUrl(map_url))
            
            # Calculate distance and ETA if we have current location
            if self.current_location:
                distance = self.calculate_distance(self.current_location, (lat, lon))
                self.distance_label.setText(f"{distance:.1f}")
                
                # Estimate ETA (assuming 15 mph average golf cart speed)
                eta_minutes = (distance / 15) * 60
                self.eta_label.setText(f"{int(eta_minutes)}min")
                
    def calculate_distance(self, pos1, pos2):
        """Calculate distance between two GPS coordinates in miles"""
        from math import sin, cos, sqrt, atan2, radians
        
        lat1, lon1 = pos1
        lat2, lon2 = pos2
        
        R = 3959  # Earth radius in miles
        
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c