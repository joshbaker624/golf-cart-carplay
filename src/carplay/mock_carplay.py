"""
Mock CarPlay Interface for Testing
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QFont, QLinearGradient, QBrush, QPainterPath

class CarPlayApp(QPushButton):
    def __init__(self, name, icon, color, parent=None):
        super().__init__(parent)
        self.name = name
        self.icon = icon
        self.color = QColor(color)
        self.setFixedSize(100, 120)
        self.setCursor(Qt.PointingHandCursor)
        
        # Animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        # Scale up on hover
        current = self.geometry()
        self.animation.setStartValue(current)
        self.animation.setEndValue(current.adjusted(-5, -5, 5, 5))
        self.animation.start()
        
    def leaveEvent(self, event):
        # Scale back down
        current = self.geometry()
        self.animation.setStartValue(current)
        self.animation.setEndValue(current.adjusted(5, 5, -5, -5))
        self.animation.start()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw rounded rectangle background
        path = QPainterPath()
        path.addRoundedRect(10, 10, 80, 80, 20, 20)
        
        # Gradient background
        gradient = QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0, self.color.lighter(120))
        gradient.setColorAt(1, self.color)
        painter.fillPath(path, QBrush(gradient))
        
        # Draw icon
        painter.setPen(Qt.white)
        icon_font = QFont("Arial", 36)
        painter.setFont(icon_font)
        painter.drawText(10, 10, 80, 80, Qt.AlignCenter, self.icon)
        
        # Draw label
        painter.setPen(Qt.white)
        label_font = QFont("Arial", 12)
        painter.setFont(label_font)
        painter.drawText(0, 95, 100, 25, Qt.AlignCenter, self.name)

class MockCarPlay(QWidget):
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("CarPlay")
        self.setFixedSize(800, 480)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Black background with subtle gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a1a, stop:1 #000000);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Status bar
        status_bar = self.create_status_bar()
        layout.addWidget(status_bar)
        
        # App grid
        app_grid = self.create_app_grid()
        layout.addWidget(app_grid)
        
        # Dock
        dock = self.create_dock()
        layout.addWidget(dock)
        
        self.setLayout(layout)
        
    def create_status_bar(self):
        status = QFrame()
        status.setFixedHeight(30)
        status.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Signal strength
        signal = QLabel("●●●●●")
        signal.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(signal)
        
        # Carrier
        carrier = QLabel("CarPlay")
        carrier.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(carrier)
        
        layout.addStretch()
        
        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.time_label)
        
        # Update time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        
        status.setLayout(layout)
        return status
        
    def create_app_grid(self):
        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        
        grid = QGridLayout()
        grid.setSpacing(30)
        
        # CarPlay apps
        apps = [
            ("Phone", "☎", "#30D158"),
            ("Music", "♫", "#FC3C44"),
            ("Maps", "🗺", "#007AFF"),
            ("Messages", "💬", "#30D158"),
            ("Now Playing", "▶", "#FF9500"),
            ("Podcasts", "🎙", "#9B59B6"),
            ("Audiobooks", "📚", "#FF6B35"),
            ("Settings", "⚙", "#8E8E93"),
        ]
        
        positions = [(i, j) for i in range(2) for j in range(4)]
        
        for position, (name, icon, color) in zip(positions, apps):
            app = CarPlayApp(name, icon, color)
            app.clicked.connect(lambda checked, n=name: self.launch_app(n))
            grid.addWidget(app, *position)
            
        grid_widget.setLayout(grid)
        return grid_widget
        
    def create_dock(self):
        dock = QFrame()
        dock.setFixedHeight(80)
        dock.setStyleSheet("""
            QFrame {
                background: rgba(50, 50, 50, 0.8);
                border-radius: 20px;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Home button
        home_btn = QPushButton("Home")
        home_btn.setFixedSize(100, 60)
        home_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        home_btn.clicked.connect(self.close_carplay)
        
        layout.addStretch()
        layout.addWidget(home_btn)
        layout.addStretch()
        
        dock.setLayout(layout)
        return dock
        
    def update_time(self):
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        self.time_label.setText(current_time)
        
    def launch_app(self, app_name):
        print(f"Launching {app_name}")
        # Here you could launch specific app views
        if app_name == "Music":
            self.close()
            if self.parent() and hasattr(self.parent(), 'show_screen'):
                self.parent().show_screen('music')
        elif app_name == "Maps":
            self.close()
            if self.parent() and hasattr(self.parent(), 'show_screen'):
                self.parent().show_screen('gps')
        elif app_name == "Settings":
            self.close()
            if self.parent() and hasattr(self.parent(), 'show_screen'):
                self.parent().show_screen('settings')
                
    def close_carplay(self):
        self.close()
        self.closed.emit()
        if self.parent():
            self.parent().show()
            
    def mousePressEvent(self, event):
        # Allow dragging the window
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'dragPos'):
            self.move(event.globalPos() - self.dragPos)
            event.accept()