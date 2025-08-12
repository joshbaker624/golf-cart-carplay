"""
Home Screen UI for Golf Cart System
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect,
                             QGraphicsOpacityEffect)
from PyQt5.QtCore import (Qt, QTimer, pyqtSignal, QPropertyAnimation, QRect, 
                          QEasingCurve, QSequentialAnimationGroup, QParallelAnimationGroup)
from PyQt5.QtGui import (QFont, QPainter, QPainterPath, QBrush, QColor, 
                         QLinearGradient, QRadialGradient, QPen)
from datetime import datetime

class RoundedFrame(QFrame):
    def __init__(self, radius=20, gradient=None, parent=None):
        super().__init__(parent)
        self.radius = radius
        self.gradient = gradient
        self.hover = False
        self.setMouseTracking(True)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)
        
    def enterEvent(self, event):
        self.hover = True
        self.update()
        
    def leaveEvent(self, event):
        self.hover = False
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Create path
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        
        # Background with gradient or solid color
        if self.gradient:
            painter.fillPath(path, self.gradient)
        else:
            base_color = QColor("#2a3142")
            if self.hover:
                base_color = base_color.lighter(110)
            painter.fillPath(path, QBrush(base_color))
        
        # Subtle border
        painter.setPen(QPen(QColor(255, 255, 255, 20), 1))
        painter.drawPath(path)

class ModernButton(QPushButton):
    def __init__(self, icon_text, label, parent=None):
        super().__init__(parent)
        self.icon_text = icon_text
        self.label = label
        self.setFixedSize(80, 80)
        self.setCursor(Qt.PointingHandCursor)
        self._active = False
        
    def set_active(self, active):
        self._active = active
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw circle background
        if self._active:
            painter.setBrush(QBrush(QColor(59, 127, 246)))  # Active blue
        elif self.isDown():
            painter.setBrush(QBrush(QColor(60, 60, 60)))
        else:
            painter.setBrush(QBrush(QColor(45, 45, 45)))
            
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 80, 80)
        
        # Draw icon
        if self._active:
            painter.setPen(Qt.white)
        else:
            painter.setPen(QColor(100, 150, 200))
        font = QFont("Arial", 32)  # Use Arial as fallback
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, self.icon_text)

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_clock()
        
    def init_ui(self):
        """Initialize the home screen UI"""
        # Set dark theme background
        self.setStyleSheet("background-color: #1a1f2e;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header with time and status
        header = self.create_header()
        layout.addWidget(header)
        
        # Main content area with cards
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Left column - Weather and Music
        left_column = QVBoxLayout()
        left_column.setSpacing(20)
        
        # Weather card
        self.weather_card = self.create_weather_card()
        left_column.addWidget(self.weather_card)
        
        # Music card
        self.music_card = self.create_music_card()
        left_column.addWidget(self.music_card)
        
        left_column.addStretch()
        content_layout.addLayout(left_column)
        
        # Right side - Navigation card
        self.nav_card = self.create_navigation_card()
        content_layout.addWidget(self.nav_card)
        
        layout.addLayout(content_layout)
        
        # Bottom navigation bar
        nav_bar = self.create_navigation_bar()
        layout.addWidget(nav_bar)
        
        self.setLayout(layout)
        
    def create_header(self):
        """Create header with clock and system info"""
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: transparent;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Time
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font = QFont("SF Pro Display", 20, QFont.Medium)
        self.clock_label.setFont(font)
        self.clock_label.setStyleSheet("color: white;")
        layout.addWidget(self.clock_label)
        
        layout.addStretch()
        
        # Status indicators
        status_layout = QHBoxLayout()
        status_layout.setSpacing(20)
        
        # Carrier/Connection
        self.carrier_label = QLabel("Inspired Mobile")
        self.carrier_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 16px;")
        status_layout.addWidget(self.carrier_label)
        
        # Signal strength
        self.signal_label = QLabel("●●●")
        self.signal_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px;")
        status_layout.addWidget(self.signal_label)
        
        # WiFi
        self.wifi_label = QLabel("⚡")
        self.wifi_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 18px;")
        status_layout.addWidget(self.wifi_label)
        
        # Battery
        self.battery_label = QLabel("■")
        self.battery_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 18px;")
        status_layout.addWidget(self.battery_label)
        
        layout.addLayout(status_layout)
        
        header.setLayout(layout)
        return header
        
    def create_weather_card(self):
        """Create weather information card"""
        card = RoundedFrame(20)
        card.setFixedHeight(100)
        card.setStyleSheet("""
            RoundedFrame {
                background-color: #2a3142;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Weather icon (using text as placeholder)
        weather_icon = QLabel("☀")
        weather_icon.setStyleSheet("color: #FDB813; font-size: 40px;")
        weather_icon.setFixedWidth(50)
        layout.addWidget(weather_icon)
        
        # Temperature and conditions
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        temp_label = QLabel("30°C")
        temp_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        info_layout.addWidget(temp_label)
        
        condition_label = QLabel("Sunny")
        condition_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 16px;")
        info_layout.addWidget(condition_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        card.setLayout(layout)
        return card
        
    def create_music_card(self):
        """Create now playing music card"""
        card = RoundedFrame(20)
        card.setFixedHeight(200)
        card.setStyleSheet("""
            RoundedFrame {
                background-color: #2a3142;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Album art placeholder
        album_frame = QFrame()
        album_frame.setFixedSize(60, 60)
        album_frame.setStyleSheet("""
            background-color: #6366f1;
            border-radius: 10px;
        """)
        
        # Song info
        song_layout = QVBoxLayout()
        song_layout.setSpacing(5)
        
        self.song_title = QLabel("Yuri on Ice")
        self.song_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        song_layout.addWidget(self.song_title)
        
        self.artist_label = QLabel("Taro Umebayashi")
        self.artist_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px;")
        song_layout.addWidget(self.artist_label)
        
        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)
        
        prev_btn = QPushButton("⏮")
        prev_btn.setFixedSize(50, 50)
        prev_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 20px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        
        play_btn = QPushButton("⏸")
        play_btn.setFixedSize(50, 50)
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 20px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        
        next_btn = QPushButton("⏭")
        next_btn.setFixedSize(50, 50)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 20px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        
        controls_layout.addWidget(prev_btn)
        controls_layout.addWidget(play_btn)
        controls_layout.addWidget(next_btn)
        controls_layout.addStretch()
        
        layout.addWidget(album_frame)
        layout.addLayout(song_layout)
        layout.addLayout(controls_layout)
        
        card.setLayout(layout)
        
        # Connect buttons
        prev_btn.clicked.connect(lambda: self.parent.show_screen('music'))
        play_btn.clicked.connect(lambda: self.parent.show_screen('music'))
        next_btn.clicked.connect(lambda: self.parent.show_screen('music'))
        
        return card
        
    def create_navigation_card(self):
        """Create navigation card with map preview"""
        card = RoundedFrame(20)
        card.setMinimumWidth(400)
        card.setStyleSheet("""
            RoundedFrame {
                background-color: #2a3142;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Navigation instruction
        nav_frame = RoundedFrame(15)
        nav_frame.setFixedHeight(80)
        nav_frame.setStyleSheet("""
            RoundedFrame {
                background-color: #3b7ff6;
            }
        """)
        
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(15, 15, 15, 15)
        
        # Turn arrow
        arrow_label = QLabel("↰")
        arrow_label.setStyleSheet("color: white; font-size: 32px;")
        nav_layout.addWidget(arrow_label)
        
        # Direction info
        dir_layout = QVBoxLayout()
        distance_label = QLabel("500 m")
        distance_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        dir_layout.addWidget(distance_label)
        
        street_label = QLabel("Turn left towards M G Road")
        street_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 14px;")
        dir_layout.addWidget(street_label)
        
        nav_layout.addLayout(dir_layout)
        nav_layout.addStretch()
        
        nav_frame.setLayout(nav_layout)
        layout.addWidget(nav_frame)
        
        # Map preview (placeholder)
        map_frame = QFrame()
        map_frame.setStyleSheet("""
            background-color: #1a1f2e;
            border-radius: 15px;
        """)
        map_frame.setMinimumHeight(300)
        
        # Simple map representation
        map_layout = QVBoxLayout()
        map_label = QLabel("Map Preview")
        map_label.setAlignment(Qt.AlignCenter)
        map_label.setStyleSheet("color: rgba(255, 255, 255, 0.3); font-size: 24px;")
        map_layout.addWidget(map_label)
        map_frame.setLayout(map_layout)
        
        layout.addWidget(map_frame)
        
        card.setLayout(layout)
        
        # Make clickable
        card.mousePressEvent = lambda e: self.parent.show_screen('gps')
        
        return card
        
    def create_navigation_bar(self):
        """Create bottom navigation bar"""
        nav_bar = QFrame()
        nav_bar.setFixedHeight(100)
        nav_bar.setStyleSheet("""
            QFrame {
                background-color: transparent;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(30)
        
        # Navigation buttons
        buttons = [
            ("⊞", "home", self.launch_home),
            ("♪", "music", self.launch_music),
            ("☎", "phone", self.launch_phone),
            ("▲", "nav", self.launch_gps),
            ("⚙", "settings", self.launch_settings)
        ]
        
        self.nav_buttons = {}
        for icon, name, callback in buttons:
            btn = ModernButton(icon, name)
            btn.clicked.connect(callback)
            
            if name == "home":
                # Highlight home button by default
                btn.set_active(True)
            
            self.nav_buttons[name] = btn
            layout.addWidget(btn)
        
        nav_bar.setLayout(layout)
        return nav_bar
        
    def setup_clock(self):
        """Setup clock timer"""
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)  # Update every second
        self.update_clock()
        
    def update_clock(self):
        """Update clock display"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.clock_label.setText(current_time)
        
    def launch_home(self):
        """Already on home screen"""
        pass
        
    def launch_music(self):
        """Switch to music player"""
        self.parent.show_screen('music')
        
    def launch_phone(self):
        """Launch CarPlay for phone"""
        if hasattr(self.parent, 'carplay_manager'):
            self.parent.carplay_manager.launch_carplay()
            
    def launch_gps(self):
        """Switch to GPS navigation"""
        self.parent.show_screen('gps')
        
    def launch_settings(self):
        """Switch to settings screen"""
        self.parent.show_screen('settings')