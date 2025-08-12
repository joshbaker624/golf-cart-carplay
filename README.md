# Golf Cart CarPlay System

A Raspberry Pi-based touchscreen interface for golf carts with Apple CarPlay support, music playback, and GPS navigation.

## Hardware Requirements

### Essential Components
- **Raspberry Pi 4B** (4GB or 8GB RAM recommended)
- **Official Raspberry Pi 7" Touchscreen** or compatible HDMI touchscreen
- **USB Sound Card** (for better audio quality)
- **MicroSD Card** (32GB minimum, Class 10)
- **Power Supply** (5V 3A minimum, consider 12V to 5V converter for golf cart)
- **USB-C Cable** for iPhone connection
- **Speakers** (waterproof recommended for outdoor use)

### Optional Components
- **GPS Module** (USB or GPIO-based)
- **Cooling Fan** for Raspberry Pi
- **Weatherproof Case**
- **Amplifier** for better sound output

## Software Stack

### Core Software
- **Raspberry Pi OS** (64-bit recommended)
- **OpenAuto Pro** (Commercial CarPlay implementation) or alternative
- **Python 3.9+** for custom UI components
- **Qt5/PyQt5** or **Kivy** for touchscreen interface

### Features
1. **Apple CarPlay Integration**
   - Wired connection support
   - Full CarPlay functionality
   - Automatic iPhone detection

2. **Custom UI Mode**
   - Music player with local file support
   - GPS navigation (when not using CarPlay)
   - System settings and controls

3. **Golf Cart Optimizations**
   - Large touch targets for use while driving
   - Outdoor-readable display settings
   - Power management for battery operation

## Installation Steps

### 1. Prepare Raspberry Pi
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-dev git cmake build-essential
sudo apt install -y libqt5multimedia5 libqt5multimedia5-plugins
sudo apt install -y pulseaudio bluetooth bluez
```

### 2. Install Display Drivers
```bash
# For official Raspberry Pi touchscreen
sudo apt install -y raspberrypi-touchscreen-calibrator

# Enable touchscreen rotation if needed
echo "lcd_rotate=2" | sudo tee -a /boot/config.txt
```

### 3. Audio Setup
```bash
# Configure audio output
sudo raspi-config
# Select: System Options > Audio > Choose your audio device

# Test audio
speaker-test -t wav -c 2
```

### 4. Install CarPlay Software
For OpenAuto Pro (commercial option):
- Purchase license from https://bluewavestudio.io/shop/openauto-pro-car-head-unit-solution/
- Follow their installation guide

For open-source alternatives, we'll implement a custom solution.

## Project Structure
```
carplay/
├── src/
│   ├── main.py           # Main application entry
│   ├── ui/               # UI components
│   ├── carplay/          # CarPlay integration
│   ├── music/            # Music player module
│   └── gps/              # GPS navigation module
├── config/
│   ├── settings.json     # Application settings
│   └── audio.conf        # Audio configuration
├── scripts/
│   ├── install.sh        # Installation script
│   └── autostart.sh      # Auto-start configuration
└── docs/
    └── wiring-diagram.md # Hardware connection guide
```

## Quick Start

1. Clone this repository
2. Run the installation script: `./scripts/install.sh`
3. Configure your settings in `config/settings.json`
4. Start the application: `python3 src/main.py`

## Safety Notice
- Mount the display at a safe viewing angle
- Ensure all connections are secure and weatherproofed
- Use appropriate fuses for power connections
- Do not operate while driving on public roads