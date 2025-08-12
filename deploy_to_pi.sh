#!/bin/bash

# Deploy to Raspberry Pi Script
# Usage: ./deploy_to_pi.sh pi@192.168.1.100

if [ $# -eq 0 ]; then
    echo "Usage: $0 pi@<raspberry-pi-ip>"
    echo "Example: $0 pi@192.168.1.100"
    exit 1
fi

PI_HOST=$1
PROJECT_NAME="golf-cart-carplay"

echo "========================================"
echo "Deploying Golf Cart UI to Raspberry Pi"
echo "Target: $PI_HOST"
echo "========================================"

# Check if we can connect
echo "Testing connection..."
ssh -o ConnectTimeout=5 $PI_HOST "echo 'Connection successful!'" || {
    echo "Error: Cannot connect to $PI_HOST"
    echo "Make sure:"
    echo "  1. Raspberry Pi is powered on"
    echo "  2. SSH is enabled"
    echo "  3. You're on the same network"
    exit 1
}

# Option 1: Deploy via Git (Recommended)
echo ""
echo "Choose deployment method:"
echo "1) Clone from GitHub (recommended)"
echo "2) Copy files directly via SCP"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    # Git deployment
    echo "Deploying via Git..."
    ssh $PI_HOST << 'ENDSSH'
    cd ~
    if [ -d "golf-cart-carplay" ]; then
        echo "Updating existing installation..."
        cd golf-cart-carplay
        git pull
    else
        echo "Cloning repository..."
        git clone https://github.com/joshbaker624/golf-cart-carplay.git
        cd golf-cart-carplay
    fi
    
    echo "Running installation..."
    chmod +x scripts/install.sh
    ./scripts/install.sh
ENDSSH

else
    # Direct file copy
    echo "Copying files..."
    
    # Create temp archive
    TEMP_FILE="/tmp/${PROJECT_NAME}.tar.gz"
    tar -czf $TEMP_FILE \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='*.pyc' \
        .
    
    # Copy to Pi
    scp $TEMP_FILE $PI_HOST:~/
    
    # Extract and install on Pi
    ssh $PI_HOST << ENDSSH
    cd ~
    mkdir -p $PROJECT_NAME
    tar -xzf ${PROJECT_NAME}.tar.gz -C $PROJECT_NAME
    cd $PROJECT_NAME
    chmod +x scripts/install.sh
    ./scripts/install.sh
    rm ~/${PROJECT_NAME}.tar.gz
ENDSSH
    
    # Clean up
    rm $TEMP_FILE
fi

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. SSH into Pi: ssh $PI_HOST"
echo "2. Test manually: cd ~/$PROJECT_NAME && ./run_mac.py"
echo "3. Reboot to test auto-start: sudo reboot"
echo ""
echo "The UI should start automatically on boot!"
echo "To view logs: journalctl -u golf-cart-ui -f"