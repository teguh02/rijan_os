#!/bin/bash
# RijanOS Assistant Root Wrapper
# Script untuk menjalankan RijanOS Assistant sebagai root saat autostart

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    # Try to run with sudo
    exec sudo -E "$0" "$@"
fi

# Function to find the current user's display
find_display() {
    # Try to find the active display
    for display in :0 :1 :2; do
        if [ -S "/tmp/.X11-unix/X${display#:}" ]; then
            echo "$display"
            return 0
        fi
    done
    echo ":0"  # Default fallback
}

# Function to find XAUTHORITY
find_xauthority() {
    # Try different possible locations
    local possible_paths=(
        "/home/$SUDO_USER/.Xauthority"
        "/home/$SUDO_USER/.X0-lock"
        "/run/user/$(id -u "$SUDO_USER")/gdm/Xauthority"
        "/var/lib/gdm3/.Xauthority"
        "/var/lib/gdm/.Xauthority"
    )
    
    for path in "${possible_paths[@]}"; do
        if [ -f "$path" ]; then
            echo "$path"
            return 0
        fi
    done
    
    # If no XAUTHORITY found, try to create one
    if [ -n "$SUDO_USER" ]; then
        local user_home="/home/$SUDO_USER"
        local xauth_file="$user_home/.Xauthority"
        
        # Try to copy from system XAUTHORITY
        if [ -f "/var/lib/gdm3/.Xauthority" ]; then
            cp "/var/lib/gdm3/.Xauthority" "$xauth_file" 2>/dev/null
            chown "$SUDO_USER:$SUDO_USER" "$xauth_file" 2>/dev/null
            if [ -f "$xauth_file" ]; then
                echo "$xauth_file"
                return 0
            fi
        fi
    fi
    
    echo ""
}

# Set display environment for GUI
export DISPLAY=$(find_display)

# Find and set XAUTHORITY
XAUTH_FILE=$(find_xauthority)
if [ -n "$XAUTH_FILE" ]; then
    export XAUTHORITY="$XAUTH_FILE"
    echo "Using XAUTHORITY: $XAUTHORITY"
else
    echo "Warning: Could not find XAUTHORITY, GUI may not work properly"
fi

# Set additional environment variables for GUI
export QT_QPA_PLATFORM=xcb
export QT_X11_NO_MITSHM=1

# Check if display is accessible
if ! xset q >/dev/null 2>&1; then
    echo "Error: Cannot connect to display $DISPLAY"
    echo "Trying to fix X11 permissions..."
    
    # Try to fix X11 permissions
    if [ -n "$SUDO_USER" ]; then
        xhost +local:root >/dev/null 2>&1
        xhost +SI:localuser:root >/dev/null 2>&1
    fi
fi

# Run RijanOS Assistant
cd /opt/rijanos-assistant

# Check if virtual environment exists
if [ ! -f "./venv/bin/python" ]; then
    echo "Error: Virtual environment not found at /opt/rijanos-assistant/venv/"
    echo "Please run install-or-update.sh first"
    exit 1
fi

echo "Starting RijanOS Assistant as root..."
echo "Display: $DISPLAY"
echo "XAUTHORITY: $XAUTHORITY"

exec ./venv/bin/python main.py "$@"
