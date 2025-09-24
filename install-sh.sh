#!/bin/sh
# RijanOS Assistant - Installation Script (sh compatible)
# Script instalasi otomatis untuk RijanOS Assistant
# Compatible with sh, bash, and other POSIX shells

set -e  # Exit on any error

echo "🚀 RijanOS Assistant - Installation Script"
echo "=============================================="

# Colors for output (simplified for sh compatibility)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo "${GREEN}[SUCCESS]${NC} $1"
}

# Check if running as root
if [ "$(id -u)" -eq 0 ]; then
    print_error "Jangan jalankan script ini sebagai root!"
    print_warning "Jalankan sebagai user biasa, script akan meminta sudo jika diperlukan."
    exit 1
fi

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

print_header "4. Install Python packages..."
# Install core packages
pip3 install --user requests

# Try to install PyQt6 via pip if system packages failed
if ! python3 -c "import PyQt6" 2>/dev/null; then
    print_status "Installing PyQt6 via pip..."
    pip3 install --user PyQt6
fi

# Install google-genai for AI features
if ! python3 -c "import google.genai" 2>/dev/null; then
    print_status "Installing google-genai via pip..."
    pip3 install --user google-genai
fi

print_header "5. Create application directory..."
sudo mkdir -p /opt/rijanos-assistant
sudo chown -R "$USER:$USER" /opt/rijanos-assistant

print_header "6. Copy application files..."
if [ -d "/opt/rijanos-assistant" ]; then
    # Copy current directory contents to /opt/rijanos-assistant
    cp -r . /opt/rijanos-assistant/
    cd /opt/rijanos-assistant
else
    print_error "Direktori /opt/rijanos-assistant tidak ditemukan!"
    exit 1
fi

print_header "7. Set permissions..."
chmod +x /opt/rijanos-assistant/main.py
chmod +x /opt/rijanos-assistant/demo.py
chmod +x /opt/rijanos-assistant/install.sh
chmod +x /opt/rijanos-assistant/uninstall.sh

print_header "8. Create config.json if not exists..."
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

print_header "9. Setup autostart (opsional)..."
printf "Apakah Anda ingin RijanOS Assistant berjalan otomatis saat login? (y/n): "
read REPLY
if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    mkdir -p ~/.config/autostart
    cp rijanos-assistant.desktop ~/.config/autostart/
    chmod +x ~/.config/autostart/rijanos-assistant.desktop
    print_status "Autostart berhasil dikonfigurasi!"
else
    print_warning "Autostart tidak dikonfigurasi. Anda dapat mengaturnya nanti."
fi

print_header "10. Test installation..."
cd /opt/rijanos-assistant
python3 demo.py

print_header "11. Installation completed!"
echo "=============================================="
print_status "RijanOS Assistant berhasil diinstal!"
print_status "Lokasi: /opt/rijanos-assistant"
print_status "Jalankan dengan: python3 /opt/rijanos-assistant/main.py"

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
read REPLY
if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    print_status "Menjalankan RijanOS Assistant..."
    python3 /opt/rijanos-assistant/main.py
fi

echo
print_status "Terima kasih telah menggunakan RijanOS Assistant!"
