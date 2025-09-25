#!/bin/bash
# Fix Autostart untuk RijanOS Assistant
# Script sederhana untuk memperbaiki konfigurasi autostart

set -e

echo "🔧 RijanOS Assistant - Fix Autostart"
echo "===================================="

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

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Script ini harus dijalankan dengan sudo!"
    echo "Gunakan: sudo bash fix-autostart-simple.sh"
    exit 1
fi

print_header "1. Updating autostart configuration..."

# Update autostart file to use root script
mkdir -p /etc/xdg/autostart

cat > /etc/xdg/autostart/rijanos-assistant.desktop << 'EOF'
[Desktop Entry]
Type=Application
Exec=/opt/rijanos-assistant/rijanos-assistant-root.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=RijanOS Assistant
Comment=Start RijanOS Assistant on login
Icon=/opt/rijanos-assistant/assets/logo.png
Categories=System;Utility;
Keywords=assistant;system;management;rijanos;
StartupNotify=true
StartupWMClass=RijanOS Assistant
EOF

chmod 644 /etc/xdg/autostart/rijanos-assistant.desktop
print_success "Autostart file updated to use root script"

print_header "2. Installing desktop entry for manual launch..."

# Install desktop entry for manual launch
mkdir -p /usr/share/applications
cp /etc/xdg/autostart/rijanos-assistant.desktop /usr/share/applications/
chmod 644 /usr/share/applications/rijanos-assistant.desktop
print_success "Desktop entry installed for manual launch"

print_header "3. Making scripts executable..."

# Make scripts executable
chmod +x /opt/rijanos-assistant/rijanos-assistant-root.sh 2>/dev/null || true
chmod +x /opt/rijanos-assistant/fix-x11-permissions.sh 2>/dev/null || true
print_success "Scripts made executable"

print_header "4. Fix autostart completed!"
echo "================================================"
print_success "Autostart configuration has been fixed!"
print_status "RijanOS Assistant will now start as root on login"
print_status "If you have X11 issues, run: sudo /opt/rijanos-assistant/fix-x11-permissions.sh"
echo
print_status "To test:"
echo "  1. Logout and login again"
echo "  2. Or restart your system"
echo
print_status "To run manually:"
echo "  • As root: sudo /opt/rijanos-assistant/rijanos-assistant-root.sh"
echo "  • From menu: RijanOS Assistant"
