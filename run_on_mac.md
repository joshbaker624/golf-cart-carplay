# Running Golf Cart CarPlay on macOS

## Quick Start (Recommended)

### 1. Install Python and Dependencies

```bash
# Install Python 3.9+ if not already installed
brew install python@3.9

# Create virtual environment
cd /Users/joshbaker/Desktop/claude/carplay
python3 -m venv venv
source venv/bin/activate

# Install dependencies (excluding Raspberry Pi specific)
pip install PyQt5==5.15.7 PyQtWebEngine==5.15.6 python-vlc==3.0.18122 Pillow==10.0.0 requests==2.31.0
```

### 2. Create Mac-Compatible Main Script

Create a new file `run_mac.py`:

```python
#!/usr/bin/env python3
import os
os.environ['DEBUG'] = '1'  # Disable fullscreen
import sys
sys.path.insert(0, 'src')
from main import main

if __name__ == '__main__':
    main()
```

### 3. Run the Application

```bash
python run_mac.py
```

## Alternative: Docker Container

### 1. Create Dockerfile for Mac

Create `Dockerfile.mac`:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    python3-pyqt5.qtwebengine \
    python3-pyqt5.qtmultimedia \
    xvfb \
    x11vnc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt || true

# Run with virtual display
CMD Xvfb :99 -screen 0 800x480x24 & \
    export DISPLAY=:99 && \
    x11vnc -display :99 -forever -nopw & \
    python3 src/main.py
```

### 2. Build and Run

```bash
docker build -f Dockerfile.mac -t golf-cart-ui .
docker run -p 5900:5900 golf-cart-ui
```

Then connect with VNC Viewer to `localhost:5900`

## Best Option: Native macOS PyQt5

For the best development experience on Mac:

1. **Install dependencies**:
   ```bash
   pip install PyQt5 PyQtWebEngine
   ```

2. **Disable Pi-specific features**:
   - GPS module (gpsd)
   - RPi.GPIO
   - Temperature monitoring

3. **Run directly**:
   ```bash
   DEBUG=1 python src/main.py
   ```

## Raspberry Pi Emulation

For true Raspberry Pi emulation:

### 1. QEMU (Full System Emulation)

```bash
# Install QEMU
brew install qemu

# Download Raspberry Pi OS image
curl -O https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2023-05-03/2023-05-03-raspios-bullseye-armhf-lite.img.xz
unxz 2023-05-03-raspios-bullseye-armhf-lite.img.xz

# Run QEMU
qemu-system-arm \
  -M versatilepb \
  -cpu arm1176 \
  -m 256 \
  -drive file=2023-05-03-raspios-bullseye-armhf-lite.img,format=raw \
  -net nic -net user,hostfwd=tcp::5022-:22 \
  -dtb versatile-pb-buster-5.4.51+.dtb \
  -kernel kernel-qemu-5.4.51-buster \
  -append 'root=/dev/sda2 panic=1 rootfstype=ext4 rw' \
  -no-reboot
```

### 2. UTM (User-Friendly GUI)

1. Download UTM from https://mac.getutm.app/
2. Create new VM → Virtualize → Linux
3. Select ARM64 architecture
4. Import Raspberry Pi OS image
5. Allocate 2GB RAM, 16GB storage
6. Enable display and networking

## Recommended Approach

For development and testing on Mac, I recommend:

1. **Use native PyQt5** - Fastest and easiest
2. **Mock hardware features** - GPS, GPIO, etc.
3. **Test UI/UX** - Focus on interface development
4. **Final testing** - Use real Raspberry Pi

The application will automatically detect it's running on Mac (not Pi) and disable hardware-specific features.