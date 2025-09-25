#!/bin/sh
# RijanOS Assistant Root Wrapper
# Script untuk menjalankan RijanOS Assistant sebagai root saat autostart

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    # Try to run with sudo
    exec sudo -E "$0" "$@"
fi

# Function to find the current user's display
find_display() {
    # Try to find the active display
    for display in :0 :1 :2; do
        display_num=$(echo "$display" | cut -c2-)
        if [ -S "/tmp/.X11-unix/X$display_num" ]; then
            echo "$display"
            return 0
        fi
    done
    echo ":0"  # Default fallback
}

# Function to find XAUTHORITY
find_xauthority() {
    # Try different possible locations
    if [ -n "$SUDO_USER" ]; then
        # Check user's home directory
        if [ -f "/home/$SUDO_USER/.Xauthority" ]; then
            echo "/home/$SUDO_USER/.Xauthority"
            return 0
        fi
        
        # Check user's gdm directory
        user_id=$(id -u "$SUDO_USER" 2>/dev/null)
        if [ -n "$user_id" ] && [ -f "/run/user/$user_id/gdm/Xauthority" ]; then
            echo "/run/user/$user_id/gdm/Xauthority"
            return 0
        fi
    fi
    
    # Check system XAUTHORITY files
    if [ -f "/var/lib/gdm3/.Xauthority" ]; then
        echo "/var/lib/gdm3/.Xauthority"
        return 0
    fi
    
    if [ -f "/var/lib/gdm/.Xauthority" ]; then
        echo "/var/lib/gdm/.Xauthority"
        return 0
    fi
    
    # If no XAUTHORITY found, try to create one
    if [ -n "$SUDO_USER" ]; then
        user_home="/home/$SUDO_USER"
        xauth_file="$user_home/.Xauthority"
        
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
        # Run xhost as the original user
        su - "$SUDO_USER" -c "xhost +local:root" >/dev/null 2>&1 || true
        su - "$SUDO_USER" -c "xhost +SI:localuser:root" >/dev/null 2>&1 || true
        su - "$SUDO_USER" -c "xhost +local:" >/dev/null 2>&1 || true
    fi
    
    # Test again
    if ! xset q >/dev/null 2>&1; then
        echo "Warning: Still cannot connect to display. GUI may not work properly."
        echo "Please run: sudo /opt/rijanos-assistant/fix-x11-permissions.sh"
    else
        echo "X11 permissions fixed successfully!"
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
