# CarPlay Simulation Guide

## Option 1: CarPlay Simulator (macOS - Recommended)

If you have Xcode installed, Apple provides an official CarPlay Simulator:

1. **Open Xcode** and go to Xcode → Open Developer Tool → Simulator
2. In Simulator, go to Device → External Displays → CarPlay
3. A CarPlay window will appear
4. Connect a simulated iPhone to test CarPlay apps

**Note**: This only works for apps you're developing with CarPlay entitlements.

## Option 2: React-CarPlay (Web-based Mock)

For testing our UI with a CarPlay-like interface:

```bash
# Install react-carplay globally
npm install -g react-carplay

# Run the CarPlay simulator
carplay-simulator --port 8080
```

Then modify our app to display in an iframe or integrate with the simulator.

## Option 3: Mock CarPlay Interface in Our App

I can create a mock CarPlay interface within our PyQt5 app. This would simulate the CarPlay experience without needing actual CarPlay.

### Quick Implementation:

Create `src/carplay/mock_carplay.py`:

```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont

class MockCarPlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout()
        
        # CarPlay Header
        header = QLabel("CarPlay")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
        """)
        layout.addWidget(header)
        
        # App Grid
        grid_layout = QHBoxLayout()
        
        apps = [
            ("Phone", "#007AFF"),
            ("Music", "#FC3C44"),
            ("Maps", "#4CD964"),
            ("Messages", "#007AFF"),
            ("Now Playing", "#FF9500"),
            ("Settings", "#8E8E93")
        ]
        
        for app_name, color in apps:
            app_btn = QPushButton(app_name)
            app_btn.setFixedSize(120, 120)
            app_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 25px;
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:pressed {{
                    background-color: {color}cc;
                }}
            """)
            grid_layout.addWidget(app_btn)
            
        layout.addLayout(grid_layout)
        layout.addStretch()
        
        self.setLayout(layout)
```

## Option 4: OpenCarPlay (Open Source Alternative)

An open-source CarPlay implementation that works on Linux/Mac:

```bash
# Clone the repository
git clone https://github.com/opencardev/crankshaft
cd crankshaft

# Build and run
./build.sh
./run.sh
```

## Option 5: Dongles and Hardware

Physical CarPlay dongles that convert video output:
- **Carlinkit**: Wireless CarPlay adapter
- **AAWireless**: Android Auto/CarPlay adapter
- **CPlay2Air**: Wireless adapter

These connect to your Mac via USB and can display CarPlay.

## Integrating with Our App

To add mock CarPlay to our current app, update the CarPlay manager:

```python
def launch_carplay(self):
    """Launch CarPlay interface"""
    if self.openauto_path:
        self.launch_openauto()
    else:
        # Launch mock CarPlay for testing
        from carplay.mock_carplay import MockCarPlay
        self.carplay_widget = MockCarPlay(self.parent)
        self.carplay_widget.show()
```

## Testing iPhone Connection

On macOS, you can test iPhone detection:

```bash
# List connected iOS devices
system_profiler SPUSBDataType | grep -A 10 -i "iPhone\|iPad"

# Using libimobiledevice (install via brew)
brew install libimobiledevice
idevice_id -l
```

## Recommended Approach

For your golf cart project:
1. Use the mock CarPlay interface for UI development
2. Test with real iPhone connection detection
3. For production, use OpenAuto Pro on Raspberry Pi
4. Consider a wireless CarPlay adapter for easier connectivity