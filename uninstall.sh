#!/bin/bash
# RijanOS Assistant - Uninstall Script
# Script uninstall untuk RijanOS Assistant

set -e  # Exit on any error

echo "🗑️ RijanOS Assistant - Uninstall Script"
echo "====================================="

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

# Confirmation
print_warning "Ini akan menghapus RijanOS Assistant dari sistem Anda."
read -p "Apakah Anda yakin ingin melanjutkan? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Uninstall dibatalkan."
    exit 0
fi

print_header "1. Stop RijanOS Assistant if running..."
pkill -f "python.*main.py" 2>/dev/null || true

print_header "2. Remove application directory..."
if [ -d "/opt/rijanos-assistant" ]; then
    sudo rm -rf /opt/rijanos-assistant
    print_status "Direktori aplikasi dihapus."
else
    print_warning "Direktori aplikasi tidak ditemukan."
fi

print_header "3. Remove autostart configuration..."
if [ -f "~/.config/autostart/rijanos-assistant.desktop" ]; then
    rm ~/.config/autostart/rijanos-assistant.desktop
    print_status "Konfigurasi autostart dihapus."
else
    print_warning "Konfigurasi autostart tidak ditemukan."
fi

print_header "4. Remove user configuration..."
if [ -d "~/.config/rijanos-assistant" ]; then
    rm -rf ~/.config/rijanos-assistant
    print_status "Konfigurasi user dihapus."
else
    print_warning "Konfigurasi user tidak ditemukan."
fi

print_header "5. Remove cache files..."
if [ -d "~/.cache/rijanos-assistant" ]; then
    rm -rf ~/.cache/rijanos-assistant
    print_status "Cache files dihapus."
else
    print_warning "Cache files tidak ditemukan."
fi

print_header "6. Remove dependencies (opsional)..."
read -p "Apakah Anda ingin menghapus dependencies Python (PyQt6, requests, httpx)? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip3 uninstall -y PyQt6 requests httpx 2>/dev/null || true
    print_status "Dependencies Python dihapus."
else
    print_warning "Dependencies Python dipertahankan."
fi

print_header "7. Cleanup completed!"
echo "====================================="
print_status "RijanOS Assistant berhasil dihapus dari sistem!"

echo
print_status "Yang telah dihapus:"
echo "  📁 Direktori aplikasi: /opt/rijanos-assistant"
echo "  🔧 Konfigurasi autostart: ~/.config/autostart/rijanos-assistant.desktop"
echo "  ⚙️ Konfigurasi user: ~/.config/rijanos-assistant"
echo "  🗂️ Cache files: ~/.cache/rijanos-assistant"

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  📦 Dependencies Python: PyQt6, requests, httpx"
fi

echo
print_status "Terima kasih telah menggunakan RijanOS Assistant!"
print_status "Jika Anda ingin menginstal ulang, jalankan: ./install.sh"
