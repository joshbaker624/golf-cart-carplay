"""
Settings Screen UI for Golf Cart System
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QSlider, QFrame, QScrollArea, QCheckBox,
                             QComboBox, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal

class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        """Initialize the settings UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1a1a1a;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2a2a2a;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #4a4a4a;
                border-radius: 5px;
            }
        """)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Audio settings
        audio_group = self.create_audio_settings()
        content_layout.addWidget(audio_group)
        
        # Display settings
        display_group = self.create_display_settings()
        content_layout.addWidget(display_group)
        
        # CarPlay settings
        carplay_group = self.create_carplay_settings()
        content_layout.addWidget(carplay_group)
        
        # GPS settings
        gps_group = self.create_gps_settings()
        content_layout.addWidget(gps_group)
        
        # System settings
        system_group = self.create_system_settings()
        content_layout.addWidget(system_group)
        
        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
    def create_header(self):
        """Create header with back button"""
        header = QFrame()
        header.setFrameStyle(QFrame.NoFrame)
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #2a2a2a;")
        
        layout = QHBoxLayout()
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.save_and_return)
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
        
        # Title
        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Spacer
        spacer = QLabel()
        spacer.setFixedWidth(back_btn.sizeHint().width())
        layout.addWidget(spacer)
        
        header.setLayout(layout)
        return header
        
    def create_audio_settings(self):
        """Create audio settings group"""
        group = QGroupBox("Audio Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout()
        
        # Master volume
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Master Volume")
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.parent.settings.get('audio', {}).get('volume', 70))
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        volume_layout.addWidget(self.volume_slider)
        
        self.volume_value = QLabel(str(self.volume_slider.value()))
        self.volume_value.setFixedWidth(40)
        volume_layout.addWidget(self.volume_value)
        
        layout.addLayout(volume_layout)
        
        # Audio output device
        device_layout = QHBoxLayout()
        device_label = QLabel("Output Device")
        device_layout.addWidget(device_label)
        
        self.device_combo = QComboBox()
        self.device_combo.addItems(["Default", "USB Audio", "Bluetooth", "HDMI"])
        self.device_combo.setCurrentText(
            self.parent.settings.get('audio', {}).get('output_device', 'Default')
        )
        device_layout.addWidget(self.device_combo)
        
        layout.addLayout(device_layout)
        
        group.setLayout(layout)
        return group
        
    def create_display_settings(self):
        """Create display settings group"""
        group = QGroupBox("Display Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout()
        
        # Brightness
        brightness_layout = QHBoxLayout()
        brightness_label = QLabel("Brightness")
        brightness_layout.addWidget(brightness_label)
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(10, 100)
        self.brightness_slider.setValue(
            self.parent.settings.get('display', {}).get('brightness', 80)
        )
        self.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        brightness_layout.addWidget(self.brightness_slider)
        
        self.brightness_value = QLabel(str(self.brightness_slider.value()))
        self.brightness_value.setFixedWidth(40)
        brightness_layout.addWidget(self.brightness_value)
        
        layout.addLayout(brightness_layout)
        
        # Auto-dim
        self.auto_dim_check = QCheckBox("Auto-dim display when inactive")
        self.auto_dim_check.setChecked(
            self.parent.settings.get('display', {}).get('auto_dim', True)
        )
        layout.addWidget(self.auto_dim_check)
        
        # Screen timeout
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("Screen timeout (seconds)")
        timeout_layout.addWidget(timeout_label)
        
        self.timeout_slider = QSlider(Qt.Horizontal)
        self.timeout_slider.setRange(30, 600)
        self.timeout_slider.setSingleStep(30)
        self.timeout_slider.setValue(
            self.parent.settings.get('display', {}).get('timeout_seconds', 300)
        )
        timeout_layout.addWidget(self.timeout_slider)
        
        self.timeout_value = QLabel(str(self.timeout_slider.value()))
        self.timeout_value.setFixedWidth(40)
        timeout_layout.addWidget(self.timeout_value)
        
        layout.addLayout(timeout_layout)
        
        group.setLayout(layout)
        return group
        
    def create_carplay_settings(self):
        """Create CarPlay settings group"""
        group = QGroupBox("CarPlay Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout()
        
        # Enable CarPlay
        self.carplay_enabled_check = QCheckBox("Enable CarPlay support")
        self.carplay_enabled_check.setChecked(
            self.parent.settings.get('carplay', {}).get('enabled', True)
        )
        layout.addWidget(self.carplay_enabled_check)
        
        # Auto-launch
        self.carplay_auto_launch_check = QCheckBox("Auto-launch when iPhone connected")
        self.carplay_auto_launch_check.setChecked(
            self.parent.settings.get('carplay', {}).get('auto_launch', True)
        )
        layout.addWidget(self.carplay_auto_launch_check)
        
        group.setLayout(layout)
        return group
        
    def create_gps_settings(self):
        """Create GPS settings group"""
        group = QGroupBox("GPS Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout()
        
        # Enable GPS
        self.gps_enabled_check = QCheckBox("Enable GPS tracking")
        self.gps_enabled_check.setChecked(
            self.parent.settings.get('gps', {}).get('enabled', True)
        )
        layout.addWidget(self.gps_enabled_check)
        
        # Update interval
        interval_layout = QHBoxLayout()
        interval_label = QLabel("Update interval (seconds)")
        interval_layout.addWidget(interval_label)
        
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["1", "2", "5", "10"])
        self.interval_combo.setCurrentText(
            str(self.parent.settings.get('gps', {}).get('update_interval', 1))
        )
        interval_layout.addWidget(self.interval_combo)
        
        layout.addLayout(interval_layout)
        
        group.setLayout(layout)
        return group
        
    def create_system_settings(self):
        """Create system settings group"""
        group = QGroupBox("System Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout()
        
        # About button
        about_btn = QPushButton("About System")
        about_btn.clicked.connect(self.show_about)
        about_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:pressed {
                background-color: #4a4a4a;
            }
        """)
        layout.addWidget(about_btn)
        
        # Reset button
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_settings)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        layout.addWidget(reset_btn)
        
        group.setLayout(layout)
        return group
        
    def get_group_style(self):
        """Get consistent group box style"""
        return """
            QGroupBox {
                background-color: #2a2a2a;
                border: 2px solid #3a3a3a;
                border-radius: 10px;
                padding-top: 30px;
                font-size: 18px;
                font-weight: bold;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
            QLabel {
                color: #ccc;
                font-size: 16px;
                font-weight: normal;
            }
            QCheckBox {
                color: #ccc;
                font-size: 16px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #3a3a3a;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #1DB954;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #1DB954;
                border-radius: 3px;
            }
            QComboBox {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
                font-weight: normal;
            }
        """
        
    def on_volume_changed(self, value):
        """Handle volume slider change"""
        self.volume_value.setText(str(value))
        
    def on_brightness_changed(self, value):
        """Handle brightness slider change"""
        self.brightness_value.setText(str(value))
        # Apply brightness change to display
        # (Implementation depends on display hardware)
        
    def save_and_return(self):
        """Save settings and return to home"""
        # Update settings
        self.parent.settings['audio']['volume'] = self.volume_slider.value()
        self.parent.settings['audio']['output_device'] = self.device_combo.currentText()
        self.parent.settings['display']['brightness'] = self.brightness_slider.value()
        self.parent.settings['display']['auto_dim'] = self.auto_dim_check.isChecked()
        self.parent.settings['display']['timeout_seconds'] = self.timeout_slider.value()
        self.parent.settings['carplay']['enabled'] = self.carplay_enabled_check.isChecked()
        self.parent.settings['carplay']['auto_launch'] = self.carplay_auto_launch_check.isChecked()
        self.parent.settings['gps']['enabled'] = self.gps_enabled_check.isChecked()
        self.parent.settings['gps']['update_interval'] = int(self.interval_combo.currentText())
        
        # Save to file
        self.parent.save_settings()
        
        # Return to home
        self.parent.show_screen('home')
        
    def reset_settings(self):
        """Reset all settings to defaults"""
        self.parent.settings = self.parent.get_default_settings()
        self.parent.save_settings()
        # Refresh UI
        self.parent.show_screen('settings')
        
    def show_about(self):
        """Show about dialog"""
        # Simple about info (could be expanded to a proper dialog)
        pass