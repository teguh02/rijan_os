#!/bin/bash
# RijanOS Assistant User Wrapper
# Script untuk menjalankan RijanOS Assistant sebagai user biasa dengan sudo permissions

# Check if not running as root
if [ "$EUID" -eq 0 ]; then
    echo "Error: This script should not be run as root directly"
    echo "Use: ./rijanos-assistant-user.sh"
    exit 1
fi

# Set display environment for GUI
export DISPLAY=${DISPLAY:-:0}

# Set additional environment variables for GUI
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1

# Check if virtual environment exists
if [ ! -f "/opt/rijanos-assistant/venv/bin/python" ]; then
    echo "Error: Virtual environment not found at /opt/rijanos-assistant/venv/"
    echo "Please run: sudo /opt/rijanos-assistant/install-or-update.sh"
    exit 1
fi

# Check if user has sudo permissions
if ! sudo -n true 2>/dev/null; then
    echo "Warning: Sudo permissions not configured for passwordless access"
    echo "Some features may require password input"
    echo "To fix this, run: sudo /opt/rijanos-assistant/fix-sudo-permissions.sh"
fi

echo "Starting RijanOS Assistant as user: $USER"
echo "Display: $DISPLAY"

# Run RijanOS Assistant
cd /opt/rijanos-assistant
exec ./venv/bin/python main.py "$@"
