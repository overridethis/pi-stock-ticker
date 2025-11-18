#!/bin/bash

# Install script for pi-stock-ticker service on Raspberry Pi

set -e

echo "Installing pi-stock-ticker as a systemd service..."

# Get the current directory (project root)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER=$(whoami)
VENV_PYTHON="$PROJECT_DIR/venv/bin/python3"

# Check if virtual environment exists, create if not
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Virtual environment not found. Creating one now..."
    python3 -m venv "$PROJECT_DIR/venv"

    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo "Make sure python3-venv is installed:"
        echo "  sudo apt-get install python3-venv"
        exit 1
    fi

    echo "Virtual environment created successfully."
    echo "Installing project dependencies..."

    "$PROJECT_DIR/venv/bin/pip3" install --upgrade pip
    "$PROJECT_DIR/venv/bin/pip3" install --prefer-binary -e "$PROJECT_DIR"

    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi

    echo "Dependencies installed successfully."
else
    echo "Virtual environment found at $PROJECT_DIR/venv"
fi

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/pi-stock-ticker.service"

echo "Creating service file at $SERVICE_FILE..."

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Pi Stock Ticker E-Paper Display
After=network-online.target sysinit.target
Wants=network-online.target
Requires=sysinit.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
ExecStartPre=/bin/sleep 5
ExecStart=$VENV_PYTHON $PROJECT_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "Service file created successfully."

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling service to start on boot..."
sudo systemctl enable pi-stock-ticker.service

echo ""
echo "Installation complete!"
echo ""
echo "Available commands:"
echo "  Start service:   sudo systemctl start pi-stock-ticker"
echo "  Stop service:    sudo systemctl stop pi-stock-ticker"
echo "  Restart service: sudo systemctl restart pi-stock-ticker"
echo "  View status:     sudo systemctl status pi-stock-ticker"
echo "  View logs:       sudo journalctl -u pi-stock-ticker -f"
echo "  Disable service: sudo systemctl disable pi-stock-ticker"
echo ""
echo "To start the service now, run:"
echo "  sudo systemctl start pi-stock-ticker"
