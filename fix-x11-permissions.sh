#!/bin/bash
# Fix X11 Permissions for RijanOS Assistant
# Script untuk memperbaiki masalah X11 authorization

set -e

echo "🔧 RijanOS Assistant - Fix X11 Permissions"
echo "==========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Script ini harus dijalankan dengan sudo!"
    echo "Gunakan: sudo bash fix-x11-permissions.sh"
    exit 1
fi

print_header "1. Checking X11 setup..."

# Check if X11 is running
if ! pgrep -x "Xorg\|Xwayland" > /dev/null; then
    print_warning "X11 server tidak berjalan. Pastikan desktop environment aktif."
fi

# Check display
DISPLAY=${DISPLAY:-:0}
print_status "Using display: $DISPLAY"

print_header "2. Setting up X11 permissions..."

# Allow root to connect to X11
if command -v xhost >/dev/null 2>&1; then
    print_status "Configuring xhost permissions..."
    xhost +local:root 2>/dev/null || true
    xhost +SI:localuser:root 2>/dev/null || true
    print_success "X11 permissions configured"
else
    print_warning "xhost not found, skipping X11 permission setup"
fi

print_header "3. Setting up XAUTHORITY..."

# Find the current user's XAUTHORITY
CURRENT_USER=${SUDO_USER:-$(logname 2>/dev/null || echo "root")}
USER_HOME="/home/$CURRENT_USER"

if [ -d "$USER_HOME" ]; then
    # Try to copy XAUTHORITY from user to root
    if [ -f "$USER_HOME/.Xauthority" ]; then
        print_status "Copying XAUTHORITY from user $CURRENT_USER..."
        cp "$USER_HOME/.Xauthority" "/root/.Xauthority" 2>/dev/null || true
        chown root:root "/root/.Xauthority" 2>/dev/null || true
        print_success "XAUTHORITY copied to root"
    else
        print_warning "User XAUTHORITY not found at $USER_HOME/.Xauthority"
    fi
else
    print_warning "User home directory not found: $USER_HOME"
fi

print_header "4. Testing X11 connection..."

# Test X11 connection
if xset q >/dev/null 2>&1; then
    print_success "X11 connection successful!"
else
    print_error "X11 connection failed!"
    print_warning "You may need to run this script from a desktop session"
fi

print_header "5. Creating desktop entry for manual execution..."

# Create a desktop entry for manual launch
cat > /usr/share/applications/rijanos-assistant.desktop << 'EOF'
[Desktop Entry]
Type=Application
Exec=/opt/rijanos-assistant/rijanos-assistant-root.sh
Hidden=false
NoDisplay=false
Name=RijanOS Assistant
Comment=Start RijanOS Assistant
Icon=/opt/rijanos-assistant/assets/logo.png
Categories=System;Utility;
Keywords=assistant;system;management;rijanos;
StartupNotify=true
EOF

chmod 644 /usr/share/applications/rijanos-assistant.desktop
print_success "Desktop entry created for manual execution"

print_header "6. Fix X11 permissions completed!"
echo "================================================"
print_success "X11 permissions have been configured!"
print_status "You can now run RijanOS Assistant using:"
echo "  • As root: sudo /opt/rijanos-assistant/rijanos-assistant-root.sh"
echo "  • From menu: RijanOS Assistant"
echo "  • Autostart: Will run automatically on login"
echo
print_status "If you still have issues, try running from a desktop session"
