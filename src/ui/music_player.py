"""
Music Player UI for Golf Cart System
"""

import os
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QSlider, QListWidget, QFrame, QFileDialog)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QIcon

class MusicPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_player()
        
    def init_ui(self):
        """Initialize the music player UI"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Header with back button
        header = self.create_header()
        layout.addWidget(header)
        
        # Now playing info
        self.now_playing_frame = self.create_now_playing()
        layout.addWidget(self.now_playing_frame)
        
        # Progress slider
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #1DB954;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: #1DB954;
                border-radius: 4px;
            }
        """)
        self.progress_slider.sliderMoved.connect(self.set_position)
        layout.addWidget(self.progress_slider)
        
        # Time labels
        time_layout = QHBoxLayout()
        self.time_current = QLabel("0:00")
        self.time_total = QLabel("0:00")
        self.time_current.setStyleSheet("color: #aaa; font-size: 14px;")
        self.time_total.setStyleSheet("color: #aaa; font-size: 14px;")
        time_layout.addWidget(self.time_current)
        time_layout.addStretch()
        time_layout.addWidget(self.time_total)
        layout.addLayout(time_layout)
        
        # Control buttons
        controls = self.create_controls()
        layout.addWidget(controls)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊")
        volume_label.setStyleSheet("color: white; font-size: 20px;")
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(200)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #333;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: white;
                border-radius: 3px;
            }
        """)
        self.volume_slider.valueChanged.connect(self.set_volume)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addStretch()
        
        layout.addLayout(volume_layout)
        
        # Playlist
        self.playlist_widget = QListWidget()
        self.playlist_widget.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                color: white;
                border: none;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #1DB954;
            }
        """)
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected)
        layout.addWidget(self.playlist_widget)
        
        # Add music button
        add_music_btn = QPushButton("Add Music Files")
        add_music_btn.clicked.connect(self.add_music_files)
        add_music_btn.setStyleSheet("""
            QPushButton {
                background-color: #1DB954;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: #169c46;
            }
        """)
        layout.addWidget(add_music_btn)
        
        self.setLayout(layout)
        
    def create_header(self):
        """Create header with back button"""
        header = QFrame()
        header.setFrameStyle(QFrame.NoFrame)
        header.setFixedHeight(60)
        
        layout = QHBoxLayout()
        
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
        
        # Title
        title = QLabel("Music Player")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        # Spacer for symmetry
        spacer = QLabel()
        spacer.setFixedWidth(back_btn.sizeHint().width())
        layout.addWidget(spacer)
        
        header.setLayout(layout)
        return header
        
    def create_now_playing(self):
        """Create now playing display"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        
        self.track_label = QLabel("No Track Playing")
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)
        layout.addWidget(self.track_label)
        
        self.artist_label = QLabel("")
        self.artist_label.setAlignment(Qt.AlignCenter)
        self.artist_label.setStyleSheet("""
            color: #aaa;
            font-size: 16px;
        """)
        layout.addWidget(self.artist_label)
        
        frame.setLayout(layout)
        return frame
        
    def create_controls(self):
        """Create playback control buttons"""
        controls = QFrame()
        controls.setFrameStyle(QFrame.NoFrame)
        
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Previous button
        self.prev_btn = QPushButton("⏮")
        self.prev_btn.clicked.connect(self.previous_track)
        self.prev_btn.setFixedSize(60, 60)
        
        # Play/Pause button
        self.play_btn = QPushButton("▶")
        self.play_btn.clicked.connect(self.toggle_playback)
        self.play_btn.setFixedSize(80, 80)
        
        # Next button
        self.next_btn = QPushButton("⏭")
        self.next_btn.clicked.connect(self.next_track)
        self.next_btn.setFixedSize(60, 60)
        
        # Style all control buttons
        for btn in [self.prev_btn, self.play_btn, self.next_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1DB954;
                    color: white;
                    border: none;
                    border-radius: 50%;
                    font-size: 24px;
                }
                QPushButton:pressed {
                    background-color: #169c46;
                }
            """)
            
        layout.addStretch()
        layout.addWidget(self.prev_btn)
        layout.addWidget(self.play_btn)
        layout.addWidget(self.next_btn)
        layout.addStretch()
        
        controls.setLayout(layout)
        return controls
        
    def setup_player(self):
        """Setup media player"""
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        
        # Connect signals
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.stateChanged.connect(self.state_changed)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        
        # Load saved playlist
        self.load_playlist()
        
    def load_playlist(self):
        """Load saved playlist from config"""
        playlist_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'config', 'playlist.json'
        )
        
        if os.path.exists(playlist_path):
            try:
                with open(playlist_path, 'r') as f:
                    playlist_data = json.load(f)
                    for track in playlist_data.get('tracks', []):
                        if os.path.exists(track['path']):
                            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(track['path'])))
                            self.playlist_widget.addItem(track['name'])
            except:
                pass
                
    def save_playlist(self):
        """Save current playlist to config"""
        playlist_data = {'tracks': []}
        
        for i in range(self.playlist.mediaCount()):
            media = self.playlist.media(i)
            if media:
                path = media.canonicalUrl().toLocalFile()
                name = os.path.basename(path)
                playlist_data['tracks'].append({'path': path, 'name': name})
                
        playlist_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'config', 'playlist.json'
        )
        
        os.makedirs(os.path.dirname(playlist_path), exist_ok=True)
        with open(playlist_path, 'w') as f:
            json.dump(playlist_data, f, indent=2)
            
    def add_music_files(self):
        """Add music files to playlist"""
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Select Music Files",
            os.path.expanduser("~/Music"),
            "Audio Files (*.mp3 *.wav *.flac *.m4a *.ogg)"
        )
        
        for file in files:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.playlist_widget.addItem(os.path.basename(file))
            
        self.save_playlist()
        
    def toggle_playback(self):
        """Toggle play/pause"""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
            
    def previous_track(self):
        """Play previous track"""
        self.playlist.previous()
        
    def next_track(self):
        """Play next track"""
        self.playlist.next()
        
    def play_selected(self):
        """Play selected track from playlist"""
        current_index = self.playlist_widget.currentRow()
        if current_index >= 0:
            self.playlist.setCurrentIndex(current_index)
            self.player.play()
            
    def set_position(self, position):
        """Set playback position"""
        self.player.setPosition(position)
        
    def set_volume(self, value):
        """Set volume level"""
        self.player.setVolume(value)
        
    def position_changed(self, position):
        """Update position slider"""
        self.progress_slider.setValue(position)
        self.time_current.setText(self.format_time(position))
        
    def duration_changed(self, duration):
        """Update duration"""
        self.progress_slider.setRange(0, duration)
        self.time_total.setText(self.format_time(duration))
        
    def state_changed(self, state):
        """Update UI based on player state"""
        if state == QMediaPlayer.PlayingState:
            self.play_btn.setText("⏸")
        else:
            self.play_btn.setText("▶")
            
    def playlist_position_changed(self, position):
        """Update now playing info"""
        if position >= 0:
            self.playlist_widget.setCurrentRow(position)
            track_name = self.playlist_widget.item(position).text()
            self.track_label.setText(track_name)
            
    def format_time(self, ms):
        """Format milliseconds to MM:SS"""
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m}:{s:02d}"