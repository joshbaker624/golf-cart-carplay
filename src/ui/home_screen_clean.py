"""
Clean Modern Home Screen UI for Golf Cart System
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QBrush, QColor, QPen
from datetime import datetime

class CleanCard(QFrame):
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self._hover = False
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
        
    def enterEvent(self, event):
        self._hover = True
        self.update()
        
    def leaveEvent(self, event):
        self._hover = False
        self.update()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 16, 16)
        
        color = QColor("#2a3447")
        if self._hover:
            color = color.lighter(110)
            
        painter.fillPath(path, QBrush(color))

class IconButton(QPushButton):
    def __init__(self, icon, name, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.name = name
        self.setFixedSize(64, 64)
        self.setCursor(Qt.PointingHandCursor)
        self._active = False
        
    def set_active(self, active):
        self._active = active
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background circle
        if self._active:
            painter.setBrush(QBrush(QColor("#4a9eff")))
        else:
            painter.setBrush(QBrush(QColor("#3a4556")))
            
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(8, 8, 48, 48)
        
        # Icon
        painter.setPen(Qt.white if self._active else QColor("#8a95aa"))
        font = QFont("Arial", 24)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, self.icon)

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_timers()
        
    def init_ui(self):
        """Initialize the clean modern UI"""
        self.setStyleSheet("background-color: #1e2537;")
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Content area
        content = QHBoxLayout()
        content.setSpacing(20)
        
        # Left column
        left_col = QVBoxLayout()
        left_col.setSpacing(20)
        
        # Weather widget
        weather = self.create_weather_widget()
        left_col.addWidget(weather)
        
        # Music widget
        music = self.create_music_widget()
        left_col.addWidget(music)
        
        left_col.addStretch()
        
        # Right column - Navigation
        nav_widget = self.create_navigation_widget()
        
        content.addLayout(left_col, 1)
        content.addWidget(nav_widget, 1)
        
        layout.addLayout(content)
        
        # Bottom navigation
        nav_bar = self.create_nav_bar()
        layout.addWidget(nav_bar)
        
        self.setLayout(layout)
        
    def create_header(self):
        """Create minimal header"""
        header = QFrame()
        header.setFixedHeight(40)
        header.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: 500;
        """)
        layout.addWidget(self.time_label)
        
        layout.addStretch()
        
        # Status icons
        status_layout = QHBoxLayout()
        status_layout.setSpacing(16)
        
        # Network
        network = QLabel("•••")
        network.setStyleSheet("color: #8a95aa; font-size: 14px;")
        status_layout.addWidget(network)
        
        # Battery
        battery = QLabel("100%")
        battery.setStyleSheet("color: #8a95aa; font-size: 14px;")
        status_layout.addWidget(battery)
        
        layout.addLayout(status_layout)
        
        header.setLayout(layout)
        return header
        
    def create_weather_widget(self):
        """Create clean weather widget"""
        widget = CleanCard()
        widget.setFixedHeight(120)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Weather icon area
        icon_frame = QFrame()
        icon_frame.setFixedSize(72, 72)
        icon_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #ffd89b, stop:1 #faa245);
            border-radius: 16px;
        """)
        
        # Icon
        icon_layout = QVBoxLayout()
        icon_layout.setContentsMargins(0, 0, 0, 0)
        weather_icon = QLabel("☀")
        weather_icon.setAlignment(Qt.AlignCenter)
        weather_icon.setStyleSheet("""
            color: white;
            font-size: 36px;
        """)
        icon_layout.addWidget(weather_icon)
        icon_frame.setLayout(icon_layout)
        
        layout.addWidget(icon_frame)
        
        # Weather info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        temp = QLabel("30°C")
        temp.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: 600;
        """)
        info_layout.addWidget(temp)
        
        condition = QLabel("Sunny")
        condition.setStyleSheet("""
            color: #8a95aa;
            font-size: 16px;
        """)
        info_layout.addWidget(condition)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        widget.clicked.connect(lambda: print("Weather clicked"))
        return widget
        
    def create_music_widget(self):
        """Create clean music widget"""
        widget = CleanCard()
        widget.setFixedHeight(180)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Album art and info
        top_layout = QHBoxLayout()
        top_layout.setSpacing(16)
        
        # Album art
        album = QFrame()
        album.setFixedSize(64, 64)
        album.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
            border-radius: 12px;
        """)
        top_layout.addWidget(album)
        
        # Song info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        song = QLabel("Yuri on Ice")
        song.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: 600;
        """)
        info_layout.addWidget(song)
        
        artist = QLabel("Taro Umebayashi")
        artist.setStyleSheet("""
            color: #8a95aa;
            font-size: 14px;
        """)
        info_layout.addWidget(artist)
        
        top_layout.addLayout(info_layout)
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # Controls
        controls = QHBoxLayout()
        controls.setSpacing(12)
        
        for icon in ["⏮", "⏸", "⏭"]:
            btn = QPushButton(icon)
            btn.setFixedSize(44, 44)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: #3a4556;
                    color: white;
                    border: none;
                    border-radius: 22px;
                    font-size: 18px;
                }
                QPushButton:hover {
                    background: #4a5566;
                }
                QPushButton:pressed {
                    background: #2a3546;
                }
            """)
            controls.addWidget(btn)
            
        controls.addStretch()
        layout.addLayout(controls)
        
        widget.setLayout(layout)
        widget.clicked.connect(lambda: self.parent.show_screen('music'))
        return widget
        
    def create_navigation_widget(self):
        """Create clean navigation widget"""
        widget = CleanCard()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Navigation header
        nav_header = QFrame()
        nav_header.setFixedHeight(80)
        nav_header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4a9eff, stop:1 #3b85ff);
            border-radius: 12px;
        """)
        
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(20, 20, 20, 20)
        
        # Turn icon
        turn_icon = QLabel("←")
        turn_icon.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: bold;
        """)
        turn_icon.setFixedWidth(40)
        nav_layout.addWidget(turn_icon)
        
        # Direction info
        dir_layout = QVBoxLayout()
        dir_layout.setSpacing(2)
        
        distance = QLabel("500 m")
        distance.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: 600;
        """)
        dir_layout.addWidget(distance)
        
        street = QLabel("Turn left towards M G Road")
        street.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
        """)
        dir_layout.addWidget(street)
        
        nav_layout.addLayout(dir_layout)
        nav_layout.addStretch()
        
        nav_header.setLayout(nav_layout)
        layout.addWidget(nav_header)
        
        # Map placeholder
        map_frame = QFrame()
        map_frame.setStyleSheet("""
            background: #1a2332;
            border-radius: 12px;
        """)
        
        map_layout = QVBoxLayout()
        map_label = QLabel("Map View")
        map_label.setAlignment(Qt.AlignCenter)
        map_label.setStyleSheet("""
            color: #4a5566;
            font-size: 18px;
        """)
        map_layout.addWidget(map_label)
        map_frame.setLayout(map_layout)
        
        layout.addWidget(map_frame)
        
        widget.setLayout(layout)
        widget.clicked.connect(lambda: self.parent.show_screen('gps'))
        return widget
        
    def create_nav_bar(self):
        """Create clean bottom navigation"""
        nav_bar = QFrame()
        nav_bar.setFixedHeight(80)
        nav_bar.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout()
        layout.setSpacing(0)
        
        # Center the buttons
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(24)
        
        buttons = [
            ("⌂", "home", self.show_home),
            ("♫", "music", self.show_music),
            ("📞", "phone", self.show_phone),
            ("📍", "nav", self.show_nav),
            ("⚙", "settings", self.show_settings),
        ]
        
        self.nav_buttons = {}
        for icon, name, callback in buttons:
            btn = IconButton(icon, name)
            btn.clicked.connect(callback)
            if name == "home":
                btn.set_active(True)
            self.nav_buttons[name] = btn
            button_layout.addWidget(btn)
            
        layout.addLayout(button_layout)
        layout.addStretch()
        
        nav_bar.setLayout(layout)
        return nav_bar
        
    def setup_timers(self):
        """Setup update timers"""
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()
        
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.time_label.setText(current_time)
        
    def show_home(self):
        """Already on home"""
        pass
        
    def show_music(self):
        """Show music screen"""
        self.parent.show_screen('music')
        
    def show_phone(self):
        """Show phone/CarPlay"""
        try:
            if hasattr(self.parent, 'carplay_manager'):
                self.parent.carplay_manager.launch_carplay()
            else:
                print("CarPlay manager not available")
        except Exception as e:
            print(f"Error launching CarPlay: {e}")
            import traceback
            traceback.print_exc()
            
    def show_nav(self):
        """Show navigation"""
        self.parent.show_screen('gps')
        
    def show_settings(self):
        """Show settings"""
        self.parent.show_screen('settings')