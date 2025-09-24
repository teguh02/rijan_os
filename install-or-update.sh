#!/bin/bash
# RijanOS Assistant - Installation & Update Script
# Script instalasi dan update otomatis untuk RijanOS Assistant
# Compatible with both sh and bash

set -e  # Exit on any error

echo "🚀 RijanOS Assistant - Installation & Update Script"
echo "===================================================="

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


# Check if running on Rijan OS or Ubuntu
if ! command -v apt >/dev/null 2>&1; then
    print_error "Script ini hanya untuk sistem berbasis Debian/Ubuntu!"
    exit 1
fi

print_header "1. Update sistem..."
sudo apt update && sudo apt upgrade -y

print_header "2. Install system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git

print_header "3. Try to install PyQt6 from system packages..."
if sudo apt install -y python3-pyqt6 python3-pyqt6.qtwidgets 2>/dev/null; then
    print_success "PyQt6 berhasil diinstal dari system packages"
else
    print_warning "PyQt6 system packages tidak tersedia, akan install via pip"
fi

print_header "4. Create virtual environment..."
cd /tmp
python3 -m venv rijanos-venv
. rijanos-venv/bin/activate

print_header "5. Install Python packages in virtual environment..."
# Install core packages
pip install requests

# Try to install PyQt6 via pip if system packages failed
if ! python3 -c "import PyQt6" 2>/dev/null; then
    print_status "Installing PyQt6 via pip..."
    pip install PyQt6
fi

# Install google-genai for AI features
print_status "Installing google-genai via pip..."
pip install google-genai

print_status "Virtual environment created at: /tmp/rijanos-venv"

print_header "6. Install or update RijanOS Assistant..."
# Check if installation exists
if [ -d "/opt/rijanos-assistant" ]; then
    print_status "Instalasi ditemukan, melakukan update source code..."
    cd /opt/rijanos-assistant
    
    # Backup config.json if exists
    if [ -f "config.json" ]; then
        print_status "Backup konfigurasi pengguna..."
        cp config.json /tmp/rijanos-config-backup.json
    fi
    
    # Update source code from GitHub
    print_status "Mengambil update terbaru dari GitHub..."
    sudo git fetch origin assistant_os
    sudo git reset --hard origin/assistant_os
    sudo git clean -fd
    
    # Restore config.json
    if [ -f "/tmp/rijanos-config-backup.json" ]; then
        print_status "Mengembalikan konfigurasi pengguna..."
        cp /tmp/rijanos-config-backup.json config.json
        rm /tmp/rijanos-config-backup.json
    fi
    
    print_success "Source code berhasil diupdate!"
else
    print_status "Instalasi baru, cloning repository dari GitHub..."
    # Clone repository directly from assistant_os branch
    sudo git clone -b assistant_os https://github.com/teguh02/rijan_os.git /opt/rijanos-assistant
    cd /opt/rijanos-assistant
    print_success "Repository berhasil di-clone!"
fi

# Set ownership to current user
sudo chown -R $USER:$USER /opt/rijanos-assistant

print_header "7. Copy virtual environment to application directory..."
# Copy virtual environment to application directory
cp -r /tmp/rijanos-venv /opt/rijanos-assistant/venv

print_header "8. Set permissions..."
chmod +x /opt/rijanos-assistant/main.py
chmod +x /opt/rijanos-assistant/demo.py
chmod +x /opt/rijanos-assistant/install-or-update.sh
chmod +x /opt/rijanos-assistant/uninstall.sh
chmod +x /opt/rijanos-assistant/rijanos-assistant-root.sh

print_header "8a. Configure sudo for autostart..."
print_status "Adding sudoers rule for RijanOS Assistant autostart..."
# Create sudoers rule for passwordless sudo commands
sudo sh -c 'cat > /etc/sudoers.d/rijanos-assistant' << 'EOF'
# Allow users to run RijanOS Assistant as root without password for autostart
%sudo ALL=(ALL) NOPASSWD: /opt/rijanos-assistant/rijanos-assistant-root.sh

# Allow passwordless sudo for common system commands used by RijanOS Assistant
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt update
%sudo ALL=(ALL) NOPASSWD: /usr/bin/apt upgrade *
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
%sudo ALL=(ALL) NOPASSWD: /usr/sbin/do-release-upgrade
%sudo ALL=(ALL) NOPASSWD: /bin/sh
%sudo ALL=(ALL) NOPASSWD: /bin/bash
%sudo ALL=(ALL) NOPASSWD: /usr/bin/snap install
%sudo ALL=(ALL) NOPASSWD: /usr/bin/snap remove
%sudo ALL=(ALL) NOPASSWD: /usr/bin/flatpak install
%sudo ALL=(ALL) NOPASSWD: /usr/bin/flatpak remove

# Allow same for admin group
%admin ALL=(ALL) NOPASSWD: /opt/rijanos-assistant/rijanos-assistant-root.sh
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt update
%admin ALL=(ALL) NOPASSWD: /usr/bin/apt upgrade *
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
%admin ALL=(ALL) NOPASSWD: /usr/sbin/do-release-upgrade
%admin ALL=(ALL) NOPASSWD: /bin/sh
%admin ALL=(ALL) NOPASSWD: /bin/bash
%admin ALL=(ALL) NOPASSWD: /usr/bin/snap install *
%admin ALL=(ALL) NOPASSWD: /usr/bin/snap remove *
%admin ALL=(ALL) NOPASSWD: /usr/bin/flatpak install *
%admin ALL=(ALL) NOPASSWD: /usr/bin/flatpak remove *
EOF
sudo chmod 440 /etc/sudoers.d/rijanos-assistant
print_success "Sudoers rule configured for passwordless autostart!"

print_header "9. Create config.json if not exists..."
if [ ! -f "/opt/rijanos-assistant/config.json" ]; then
    print_status "Membuat config.json default..."
    cat > /opt/rijanos-assistant/config.json << 'EOF'
{
  "ai_enabled": false,
  "gemini_api_key": "",
  "gemini_model": "gemini-2.5-flash-lite",
  "console_visible": true,
  "blocked_commands": [
    "rm -rf /",
    "mkfs",
    "dd if=",
    ":(){ :|: & };:",
    "sudo rm -rf /",
    "format",
    "fdisk",
    "parted"
  ],
  "apt_commands": {
    "python_stack": "sudo apt install -y python3 python3-pip python3-venv jupyter-notebook python3-numpy python3-pandas python3-matplotlib",
    "php_stack": "sudo apt install -y php composer",
    "node_stack": "sudo apt install -y nodejs npm yarnpkg",
    "golang_stack": "sudo apt install -y golang",
    "media_tools": "sudo apt install -y vlc gimp audacity obs-studio",
    "education_apps": "sudo apt install -y stellarium texstudio texlive-full",
    "developer_apps": "sudo apt install -y git code docker.io postman",
    "system_apps": "sudo apt install -y htop gparted curl wget",
    "multimedia_apps": "sudo apt install -y audacity vlc gimp obs-studio kdenlive blender",
    "security_apps": "sudo apt install -y clamav clamav-daemon ufw fail2ban rkhunter chkrootkit lynis"
  }
}
EOF
    print_success "config.json berhasil dibuat!"
else
    print_status "config.json sudah ada, tidak perlu dibuat."
fi

print_header "10. Setup system-wide autostart..."
printf "Apakah Anda ingin RijanOS Assistant berjalan otomatis saat login untuk semua pengguna? (y/n): "
read -r REPLY
if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    # Install to system-wide autostart directory
    print_status "Menginstall autostart untuk semua pengguna sistem..."
    sudo mkdir -p /etc/xdg/autostart
    sudo cp rijanos-assistant.desktop /etc/xdg/autostart/
    sudo chmod 644 /etc/xdg/autostart/rijanos-assistant.desktop
    print_success "System-wide autostart berhasil dikonfigurasi!"
    print_status "RijanOS Assistant akan berjalan otomatis saat login untuk semua pengguna"
else
    print_warning "Autostart tidak dikonfigurasi. Anda dapat mengaturnya nanti dengan:"
    print_warning "sudo cp /opt/rijanos-assistant/rijanos-assistant.desktop /etc/xdg/autostart/"
fi

print_header "11. Test installation..."
cd /opt/rijanos-assistant
/opt/rijanos-assistant/venv/bin/python demo.py

print_header "12. Installation/Update completed!"
echo "================================================"
if [ -f "/tmp/rijanos-config-backup.json" ]; then
    print_success "RijanOS Assistant berhasil diupdate!"
    print_status "Konfigurasi pengguna telah dipulihkan"
else
    print_success "RijanOS Assistant berhasil diinstal!"
fi
print_status "Lokasi: /opt/rijanos-assistant"
print_status "Jalankan dengan: /opt/rijanos-assistant/venv/bin/python /opt/rijanos-assistant/main.py"
print_status "Jalankan sebagai root: sudo /opt/rijanos-assistant/rijanos-assistant-root.sh"
print_status "Update script: sudo bash /opt/rijanos-assistant/install-or-update.sh"
print_status "Autostart config: /etc/xdg/autostart/rijanos-assistant.desktop"

echo
print_status "Fitur yang tersedia:"
echo "  🤖 AI Assistant (konfigurasi di Settings)"
echo "  📦 Package Manager"
echo "  🎬 Multimedia Apps"
echo "  💾 Backup & Restore"
echo "  ⚡ Power Management"
echo "  🔔 System Tray"

echo
print_status "Dokumentasi lengkap: /opt/rijanos-assistant/DOCUMENTATION.md"
print_status "Bug report: https://github.com/teguh02/rijan_os/issues"

echo
printf "Apakah Anda ingin menjalankan RijanOS Assistant sekarang? (y/n): "
read -r REPLY
if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    print_status "Menjalankan RijanOS Assistant..."
    /opt/rijanos-assistant/venv/bin/python /opt/rijanos-assistant/main.py
fi

echo
print_status "Terima kasih telah menggunakan RijanOS Assistant!"
