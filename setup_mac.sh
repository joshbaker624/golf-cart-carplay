#!/bin/bash

echo "======================================"
echo "Golf Cart CarPlay - Mac Setup"
echo "======================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it first:"
    echo "brew install python@3.9"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip

# Install only Mac-compatible dependencies
pip install PyQt5==5.15.7
pip install PyQtWebEngine==5.15.6
pip install Pillow==10.0.0
pip install requests==2.31.0

# Optional: Install VLC if available
pip install python-vlc==3.0.18122 || echo "VLC not installed, music playback may be limited"

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo "1. source venv/bin/activate"
echo "2. python run_mac.py"
echo ""
echo "Or simply: ./run_mac.py"