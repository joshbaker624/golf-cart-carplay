# Raspberry Pi Installation Guide

## What You'll Need

### Hardware
- **Raspberry Pi 4** (4GB or 8GB recommended)
- **MicroSD Card** (32GB minimum, Class 10)
- **Power Supply** (Official 5V/3A USB-C)
- **Display** (Official 7" touchscreen or HDMI)
- **Case** (with cooling fan recommended)
- **USB-C to Lightning cable** (for iPhone/CarPlay)

### Optional
- USB sound card (for better audio)
- GPS USB dongle
- Keyboard/mouse (for initial setup)

## Step 1: Prepare the SD Card

### On your Mac:
1. Download **Raspberry Pi Imager**: https://www.raspberrypi.com/software/
2. Insert SD card into your Mac
3. Open Raspberry Pi Imager
4. Choose:
   - **OS**: Raspberry Pi OS (64-bit) with desktop
   - **Storage**: Select your SD card
5. Click the ⚙️ (Advanced options):
   - Set hostname: `golfcart`
   - Enable SSH
   - Set username: `pi`
   - Set password: (choose secure password)
   - Configure WiFi (optional)
   - Set locale: en_US.UTF-8
6. Write the image

## Step 2: First Boot

1. Insert SD card into Raspberry Pi
2. Connect display, keyboard, mouse
3. Power on
4. Wait for first boot (2-3 minutes)

## Step 3: Initial Setup

### Via Desktop (if you have display attached):
Open Terminal and run:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Enable VNC (for remote access)
sudo raspi-config
# Select: Interface Options > VNC > Enable
```

### Via SSH (headless):
From your Mac:
```bash
# Connect (replace with your Pi's IP)
ssh pi@golfcart.local
# or
ssh pi@192.168.1.XXX
```

## Step 4: Install Golf Cart UI

### Option A: Automated Installation

```bash
# Clone the repository
cd ~
git clone https://github.com/joshbaker624/golf-cart-carplay.git
cd golf-cart-carplay

# Run installer
chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

### Option B: Manual Installation

```bash
# Install system dependencies
sudo apt update
sudo apt install -y \
    python3-pip python3-venv \
    python3-pyqt5 python3-pyqt5.qtwebengine \
    git build-essential \
    pulseaudio bluetooth bluez

# Clone repository
cd ~
git clone https://github.com/joshbaker624/golf-cart-carplay.git
cd golf-cart-carplay

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Test run
python src/main.py
```

## Step 5: Configure Auto-Start

### Create systemd service:
```bash
sudo nano /etc/systemd/system/golfcart-ui.service
```

Add this content:
```ini
[Unit]
Description=Golf Cart CarPlay UI
After=graphical.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/golf-cart-carplay
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/pi/.Xauthority"
ExecStart=/home/pi/golf-cart-carplay/venv/bin/python /home/pi/golf-cart-carplay/src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=graphical.target
```

Enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable golfcart-ui.service
sudo systemctl start golfcart-ui.service

# Check status
sudo systemctl status golfcart-ui.service
```

## Step 6: Display Configuration

### For Official 7" Touchscreen:
```bash
# Rotate if needed (0, 90, 180, 270)
echo "lcd_rotate=0" | sudo tee -a /boot/config.txt

# Adjust brightness
echo 100 | sudo tee /sys/class/backlight/rpi_backlight/brightness
```

### For HDMI Display:
```bash
sudo nano /boot/config.txt

# Add these lines:
hdmi_force_hotplug=1
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
hdmi_group=2
```

## Step 7: Audio Setup

```bash
# List audio devices
aplay -l

# Set default audio output
sudo raspi-config
# Select: System Options > Audio > Choose output

# Test audio
speaker-test -t wav -c 2
```

## Step 8: Performance Optimization

```bash
sudo nano /boot/config.txt

# Add for better performance:
gpu_mem=256
over_voltage=4
arm_freq=1800

# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable cups
```

## Step 9: Test Everything

1. **Reboot**: `sudo reboot`
2. **UI should start automatically**
3. **Test touchscreen**: Touch navigation buttons
4. **Test audio**: Play music
5. **Test CarPlay**: Connect iPhone via USB

## Troubleshooting

### UI doesn't start:
```bash
# Check logs
journalctl -u golfcart-ui -f

# Run manually to see errors
cd ~/golf-cart-carplay
source venv/bin/activate
python src/main.py
```

### Touch not working:
```bash
# Calibrate touchscreen
sudo apt install xinput-calibrator
xinput_calibrator
```

### No audio:
```bash
# Check audio devices
aplay -l
# Select correct output
alsamixer
```

### Performance issues:
```bash
# Check temperature
vcgencmd measure_temp
# Should be under 80°C
```

## Remote Access

### VNC (Graphical):
1. On Mac: Download VNC Viewer
2. Connect to: `golfcart.local:5900`

### SSH (Terminal):
```bash
ssh pi@golfcart.local
```

### Web-based (future):
Access at: `http://golfcart.local:8080`

## Next Steps

1. **Mount in golf cart** with proper ventilation
2. **Connect power** through DC-DC converter
3. **Test with iPhone** for CarPlay
4. **Configure GPS** if you have USB GPS module
5. **Customize settings** in the app

## Quick Commands Reference

```bash
# Start UI manually
cd ~/golf-cart-carplay && source venv/bin/activate && python src/main.py

# View logs
journalctl -u golfcart-ui -f

# Restart UI
sudo systemctl restart golfcart-ui

# Update software
cd ~/golf-cart-carplay && git pull && sudo systemctl restart golfcart-ui

# Check system info
vcgencmd measure_temp
free -h
df -h
```

## Safety Notes

⚠️ **For Golf Cart Installation**:
- Use proper fuses (5A) on power connection
- Ensure good ventilation for Pi
- Mount display securely
- Keep away from moisture
- Don't operate while driving on public roads