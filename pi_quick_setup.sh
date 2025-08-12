#!/bin/bash

# Quick Setup Script for Raspberry Pi
# Run this after cloning the repository

echo "======================================"
echo "Golf Cart UI - Quick Setup for Pi"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    echo -e "${RED}Warning: This doesn't appear to be a Raspberry Pi${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo -e "${GREEN}Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo -e "${GREEN}Installing system dependencies...${NC}"
sudo apt install -y \
    python3-pip python3-venv python3-dev \
    python3-pyqt5 python3-pyqt5.qtwebengine python3-pyqt5.qtmultimedia \
    git build-essential \
    xinput-calibrator \
    pulseaudio pavucontrol \
    gpsd gpsd-clients \
    bluetooth bluez bluez-tools

# Create virtual environment
echo -e "${GREEN}Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo -e "${GREEN}Installing Python packages...${NC}"
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt || {
    echo -e "${RED}Some packages failed to install. Installing minimal set...${NC}"
    pip install PyQt5 PyQtWebEngine Pillow requests
}

# Create autostart directory
mkdir -p ~/.config/autostart

# Create desktop entry for autostart
cat > ~/.config/autostart/golfcart-ui.desktop << EOF
[Desktop Entry]
Type=Application
Name=Golf Cart UI
Comment=Golf Cart CarPlay System
Exec=/home/pi/golf-cart-carplay/venv/bin/python /home/pi/golf-cart-carplay/src/main.py
Path=/home/pi/golf-cart-carplay
Terminal=false
X-GNOME-Autostart-enabled=true
EOF

# Create systemd service
echo -e "${GREEN}Creating systemd service...${NC}"
sudo tee /etc/systemd/system/golfcart-ui.service > /dev/null << EOF
[Unit]
Description=Golf Cart CarPlay UI
After=graphical.target

[Service]
Type=simple
User=pi
WorkingDirectory=$PWD
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/pi/.Xauthority"
Environment="QT_QPA_PLATFORM=xcb"
ExecStart=$PWD/venv/bin/python $PWD/src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=graphical.target
EOF

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable golfcart-ui.service

# Configure display settings
echo -e "${GREEN}Configuring display...${NC}"
if [ -e /sys/class/backlight/rpi_backlight/brightness ]; then
    echo "Official touchscreen detected"
    echo 100 | sudo tee /sys/class/backlight/rpi_backlight/brightness
fi

# Create launch script
cat > ~/Desktop/GolfCartUI.desktop << EOF
[Desktop Entry]
Type=Application
Name=Golf Cart UI
Comment=Launch Golf Cart UI
Icon=/home/pi/golf-cart-carplay/icon.png
Exec=/home/pi/golf-cart-carplay/venv/bin/python /home/pi/golf-cart-carplay/src/main.py
Path=/home/pi/golf-cart-carplay
Terminal=false
Categories=Utility;
EOF
chmod +x ~/Desktop/GolfCartUI.desktop

# Performance tweaks
echo -e "${GREEN}Applying performance optimizations...${NC}"
if ! grep -q "gpu_mem=" /boot/config.txt; then
    echo "gpu_mem=256" | sudo tee -a /boot/config.txt
fi

# Create update script
cat > update.sh << 'EOF'
#!/bin/bash
echo "Updating Golf Cart UI..."
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart golfcart-ui
echo "Update complete!"
EOF
chmod +x update.sh

echo ""
echo -e "${GREEN}======================================"
echo "Setup Complete!"
echo "======================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test now: source venv/bin/activate && python src/main.py"
echo "2. Or reboot to test auto-start: sudo reboot"
echo "3. Check logs: journalctl -u golfcart-ui -f"
echo ""
echo "The UI will start automatically on boot!"
echo "You can also launch it from the desktop icon."
echo ""
echo "To update in the future, run: ./update.sh"