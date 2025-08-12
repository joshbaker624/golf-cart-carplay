#!/bin/bash

# Golf Cart CarPlay System Installation Script
# For Raspberry Pi running Raspberry Pi OS

set -e

echo "======================================"
echo "Golf Cart CarPlay System Installer"
echo "======================================"

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install system dependencies
echo "Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    cmake \
    build-essential \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    python3-pyqt5 \
    python3-pyqt5.qtmultimedia \
    python3-pyqt5.qtwebengine \
    libqt5multimedia5 \
    libqt5multimedia5-plugins \
    libqt5multimediawidgets5 \
    pulseaudio \
    bluetooth \
    bluez \
    bluez-tools \
    gpsd \
    gpsd-clients \
    python3-gps \
    vlc \
    python3-vlc

# Install touchscreen support
echo "Installing touchscreen support..."
sudo apt install -y \
    xserver-xorg-input-evdev \
    xinput-calibrator \
    raspberrypi-touchscreen-calibrator

# Create virtual environment
echo "Creating Python virtual environment..."
cd /home/pi/carplay
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Configure audio
echo "Configuring audio..."
# Set USB audio as default if available
if lsusb | grep -q "Audio"; then
    sudo tee /etc/asound.conf > /dev/null <<EOF
pcm.!default {
    type hw
    card 1
}
ctl.!default {
    type hw
    card 1
}
EOF
fi

# Enable and start PulseAudio
systemctl --user enable pulseaudio
systemctl --user start pulseaudio

# Configure GPS
echo "Configuring GPS..."
# Enable GPS daemon
sudo systemctl enable gpsd
sudo systemctl start gpsd

# Configure display
echo "Configuring display..."
# Rotate display if needed (for landscape mode)
if ! grep -q "lcd_rotate" /boot/config.txt; then
    echo "lcd_rotate=0" | sudo tee -a /boot/config.txt
fi

# Enable touch screen
if ! grep -q "dtoverlay=rpi-ft5406" /boot/config.txt; then
    echo "dtoverlay=rpi-ft5406" | sudo tee -a /boot/config.txt
fi

# Create autostart entry
echo "Setting up autostart..."
mkdir -p /home/pi/.config/autostart

cat > /home/pi/.config/autostart/carplay.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Golf Cart CarPlay
Exec=/home/pi/carplay/scripts/autostart.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

# Create autostart script
cat > /home/pi/carplay/scripts/autostart.sh <<EOF
#!/bin/bash
cd /home/pi/carplay
source venv/bin/activate
python3 src/main.py
EOF

chmod +x /home/pi/carplay/scripts/autostart.sh

# Create config directory
mkdir -p /home/pi/carplay/config

# Create default settings
cat > /home/pi/carplay/config/settings.json <<EOF
{
  "audio": {
    "volume": 70,
    "output_device": "default"
  },
  "display": {
    "brightness": 80,
    "auto_dim": true,
    "timeout_seconds": 300
  },
  "carplay": {
    "enabled": true,
    "auto_launch": true
  },
  "gps": {
    "enabled": true,
    "update_interval": 1
  }
}
EOF

# Set permissions
chmod -R 755 /home/pi/carplay
chown -R pi:pi /home/pi/carplay

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Reboot your Raspberry Pi: sudo reboot"
echo "2. The CarPlay system will start automatically"
echo "3. Connect your iPhone via USB to use CarPlay"
echo ""
echo "For OpenAuto Pro (recommended for full CarPlay support):"
echo "Visit: https://bluewavestudio.io/shop/openauto-pro-car-head-unit-solution/"
echo ""
echo "Manual start command:"
echo "cd /home/pi/carplay && source venv/bin/activate && python3 src/main.py"
echo ""