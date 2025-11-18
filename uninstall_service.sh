#!/bin/bash

# Uninstall script for pi-stock-ticker service on Raspberry Pi

set -e

SERVICE_NAME="pi-stock-ticker"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "Uninstalling ${SERVICE_NAME} service..."

# Check if service exists
if [ ! -f "$SERVICE_FILE" ]; then
    echo "Service file not found at $SERVICE_FILE"
    echo "Service may not be installed."
    exit 0
fi

# Stop the service if it's running
echo "Stopping service..."
sudo systemctl stop ${SERVICE_NAME} 2>/dev/null || true

# Disable the service
echo "Disabling service..."
sudo systemctl disable ${SERVICE_NAME} 2>/dev/null || true

# Remove the service file
echo "Removing service file..."
sudo rm -f $SERVICE_FILE

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Reset failed state
sudo systemctl reset-failed 2>/dev/null || true

echo ""
echo "Uninstallation complete!"
echo ""
echo "The ${SERVICE_NAME} service has been removed."
echo "Your project files and virtual environment remain intact."
echo ""
echo "To reinstall the service, run:"
echo "  ./install_service.sh"
