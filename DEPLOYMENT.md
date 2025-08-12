# Deployment Guide - Golf Cart CarPlay System

## Option 1: Deploy to Raspberry Pi (Recommended)

### Prerequisites
- Raspberry Pi 4 (4GB or 8GB RAM)
- MicroSD card (32GB minimum)
- Official 7" touchscreen or HDMI display
- Power supply (5V 3A)

### Step 1: Prepare Raspberry Pi OS

1. Download Raspberry Pi Imager: https://www.raspberrypi.com/software/
2. Flash Raspberry Pi OS (64-bit) to SD card
3. Enable SSH and WiFi (optional) before first boot

### Step 2: Transfer Project to Pi

```bash
# From your Mac, push to GitHub first
cd /Users/joshbaker/Desktop/claude/carplay
git add -A
git commit -m "Ready for deployment"
git push origin main

# On Raspberry Pi
git clone https://github.com/joshbaker624/golf-cart-carplay.git
cd golf-cart-carplay
```

### Step 3: Install on Raspberry Pi

```bash
# Run the installation script
chmod +x scripts/install.sh
sudo ./scripts/install.sh

# The script will:
# - Install all dependencies
# - Configure touchscreen
# - Set up auto-start
# - Configure audio/GPS
```

### Step 4: Configure Auto-Start

The installer creates an autostart entry, but you can also manually configure:

```bash
# Create systemd service
sudo nano /etc/systemd/system/golf-cart-ui.service
```

Add:
```ini
[Unit]
Description=Golf Cart CarPlay UI
After=graphical.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/golf-cart-carplay
Environment="DISPLAY=:0"
ExecStart=/home/pi/golf-cart-carplay/venv/bin/python /home/pi/golf-cart-carplay/src/main.py
Restart=always

[Install]
WantedBy=default.target
```

Enable service:
```bash
sudo systemctl enable golf-cart-ui.service
sudo systemctl start golf-cart-ui.service
```

## Option 2: Package as Standalone App

### For Raspberry Pi (AppImage)

Create `build_appimage.sh`:
```bash
#!/bin/bash
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-aarch64.AppImage
chmod +x appimagetool-aarch64.AppImage

# Create AppDir structure
mkdir -p GolfCartUI.AppDir/usr/bin
mkdir -p GolfCartUI.AppDir/usr/lib/python3.9

# Copy application
cp -r src venv requirements.txt GolfCartUI.AppDir/usr/

# Create AppRun
cat > GolfCartUI.AppDir/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3.9:${PYTHONPATH}"
exec "${HERE}/usr/bin/python3" "${HERE}/usr/src/main.py" "$@"
EOF

chmod +x GolfCartUI.AppDir/AppRun

# Create desktop entry
cat > GolfCartUI.AppDir/golfcart.desktop << EOF
[Desktop Entry]
Name=Golf Cart UI
Exec=AppRun
Icon=golfcart
Type=Application
Categories=Utility;
EOF

# Build AppImage
./appimagetool-aarch64.AppImage GolfCartUI.AppDir
```

### For macOS (Testing)

Create a macOS app bundle:

```bash
# Install py2app
pip install py2app

# Create setup.py
cat > setup.py << EOF
from setuptools import setup

APP = ['src/main.py']
DATA_FILES = ['config', 'src']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5', 'PyQtWebEngine'],
    'iconfile': 'icon.icns',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
EOF

# Build app
python setup.py py2app
```

## Option 3: Deploy to Golf Cart

### Hardware Installation

1. **Mount Raspberry Pi**
   - Use vibration-dampening mounts
   - Ensure good ventilation
   - Protect from moisture

2. **Power Connection**
   ```
   Golf Cart Battery → Fuse (5A) → DC-DC Converter → Raspberry Pi
   ```

3. **Display Mounting**
   - Mount at driver's eye level
   - Use sun shade/hood for visibility
   - Secure cables

### Software Configuration

1. **Network Setup** (Optional)
   ```bash
   # Configure WiFi for updates
   sudo raspi-config
   # Select: System Options → Wireless LAN
   ```

2. **Performance Optimization**
   ```bash
   # Overclock for better performance
   sudo nano /boot/config.txt
   
   # Add:
   over_voltage=6
   arm_freq=2000
   gpu_freq=750
   ```

3. **Boot Optimization**
   ```bash
   # Disable unnecessary services
   sudo systemctl disable bluetooth
   sudo systemctl disable avahi-daemon
   
   # Fast boot
   sudo nano /boot/cmdline.txt
   # Add: quiet splash
   ```

## Option 4: Web-Based Deployment

Convert to web app for any device:

1. **Create FastAPI backend**
   ```python
   # api_server.py
   from fastapi import FastAPI
   from fastapi.staticfiles import StaticFiles
   
   app = FastAPI()
   app.mount("/", StaticFiles(directory="web", html=True))
   ```

2. **Use WebAssembly** (Pyodide)
   - Convert PyQt5 UI to HTML/JS
   - Run Python in browser

## Quick Deployment Checklist

- [ ] Test on target device
- [ ] Configure auto-start
- [ ] Set up power management
- [ ] Test touchscreen calibration
- [ ] Verify GPS reception
- [ ] Test audio output
- [ ] Configure network (if needed)
- [ ] Create backup image

## Remote Management

### SSH Access
```bash
# Enable SSH
sudo systemctl enable ssh

# Connect from Mac
ssh pi@golfcart.local
```

### VNC Access
```bash
# Install VNC
sudo apt install realvnc-vnc-server
sudo systemctl enable vncserver-x11-serviced

# Connect from Mac using VNC Viewer
```

### Over-the-Air Updates
```bash
# Create update script
cat > update.sh << 'EOF'
#!/bin/bash
cd /home/pi/golf-cart-carplay
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart golf-cart-ui
EOF
```

## Troubleshooting

### Display Issues
```bash
# Rotate display
echo "lcd_rotate=2" | sudo tee -a /boot/config.txt

# Adjust resolution
echo "hdmi_mode=87" | sudo tee -a /boot/config.txt
echo "hdmi_cvt=800 480 60 6 0 0 0" | sudo tee -a /boot/config.txt
```

### Performance Issues
```bash
# Check temperature
vcgencmd measure_temp

# Monitor resources
htop
```

### Touch Calibration
```bash
sudo apt install xinput-calibrator
xinput_calibrator
```

## Production Considerations

1. **Weatherproofing**
   - Use IP65 rated enclosure
   - Seal all cable entries
   - Add ventilation

2. **Vibration**
   - Use rubber dampeners
   - Secure all connections
   - Use thread locker on screws

3. **Temperature**
   - Add cooling fan for hot climates
   - Use heatsinks on Pi
   - Monitor CPU temperature

4. **Power**
   - Add capacitor for voltage spikes
   - Use automotive-grade DC-DC converter
   - Include reverse polarity protection

5. **Safety**
   - Mount display away from airbags
   - Use breakaway mounts
   - Ensure no sharp edges