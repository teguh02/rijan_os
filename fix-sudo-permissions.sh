#!/bin/sh
# Fix Sudo Permissions untuk RijanOS Assistant
# Script untuk memperbaiki konfigurasi sudoers agar aplikasi bisa berjalan tanpa password
# Compatible with both sh and bash

set -e  # Exit on any error

echo "🔧 RijanOS Assistant - Fix Sudo Permissions"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if running as root or with sudo
if [ "$(id -u)" -ne 0 ]; then
    print_error "Script ini harus dijalankan dengan sudo!"
    echo "Gunakan: sudo sh fix-sudo-permissions.sh"
    exit 1
fi

print_header "1. Backup existing sudoers file..."
if [ -f "/etc/sudoers.d/rijanos-assistant" ]; then
    cp /etc/sudoers.d/rijanos-assistant /etc/sudoers.d/rijanos-assistant.backup
    print_status "Backup sudoers file created"
fi

print_header "2. Create comprehensive sudoers rule..."
# Create comprehensive sudoers rule for passwordless sudo commands
cat > /etc/sudoers.d/rijanos-assistant << 'EOF'
# RijanOS Assistant - Sudoers Configuration
# Allow users to run RijanOS Assistant as root without password for autostart
%sudo ALL=(ALL) NOPASSWD: /opt/rijanos-assistant/rijanos-assistant-root.sh

# Allow passwordless sudo for common system commands used by RijanOS Assistant
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt update
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt upgrade
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt install *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt remove *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt autoremove *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt clean
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt show *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt search *
%sudo ALL=(ALL) NOPASSWD: /bin/systemctl *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/journalctl *
%sudo ALL=(ALL) NOPASSWD: /bin/rm -rf /tmp/*
%sudo ALL=(ALL) NOPASSWD: /sbin/reboot
%sudo ALL=(ALL) NOPASSWD: /sbin/shutdown *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/snap install *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/snap remove *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/flatpak install *
%sudo ALL=(ALL) NOPASSWD: /usr/bin/flatpak remove *

# Allow same for admin group
%admin ALL=(ALL) NOPASSWD: /opt/rijanos-assistant/rijanos-assistant-root.sh
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt update
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt upgrade
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt install *
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt remove *
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt autoremove *
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt clean
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt show *
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt search *
%admin ALL=(ALL) NOPASSWD: /bin/systemctl *
%admin ALL=(ALL) NOPASSWD: /usr/bin/journalctl *
%admin ALL=(ALL) NOPASSWD: /bin/rm -rf /tmp/*
%admin ALL=(ALL) NOPASSWD: /sbin/reboot
%admin ALL=(ALL) NOPASSWD: /sbin/shutdown *
%admin ALL=(ALL) NOPASSWD: /usr/bin/snap install *
%admin ALL=(ALL) NOPASSWD: /usr/bin/snap remove *
%admin ALL=(ALL) NOPASSWD: /usr/bin/flatpak install *
%admin ALL=(ALL) NOPASSWD: /usr/bin/flatpak remove *
EOF

chmod 440 /etc/sudoers.d/rijanos-assistant

print_header "3. Validate sudoers configuration..."
if visudo -c -f /etc/sudoers.d/rijanos-assistant; then
    print_success "Sudoers configuration is valid!"
else
    print_error "Sudoers configuration is invalid! Restoring backup..."
    if [ -f "/etc/sudoers.d/rijanos-assistant.backup" ]; then
        mv /etc/sudoers.d/rijanos-assistant.backup /etc/sudoers.d/rijanos-assistant
        print_warning "Backup restored. Please check the configuration manually."
    fi
    exit 1
fi

print_header "4. Test sudo access..."
print_status "Testing passwordless sudo access for current user..."
# Test with simpler approach for POSIX compatibility
if [ -n "$SUDO_USER" ]; then
    if su - "$SUDO_USER" -c "sudo -n apt --version" >/dev/null 2>&1; then
        print_success "Passwordless sudo access configured successfully!"
    else
        print_warning "Sudo access test failed. You may need to logout and login again."
    fi
else
    print_warning "Cannot test sudo access - not running via sudo. Please test manually."
fi

print_success "Sudo permissions fixed successfully!"
echo
print_status "RijanOS Assistant should now be able to run system commands without password prompts."
print_status "If you still experience issues, please restart your session (logout/login)."
echo
print_status "To test the fix, try running:"
echo "  sudo apt update"
echo "  (should not prompt for password)"
