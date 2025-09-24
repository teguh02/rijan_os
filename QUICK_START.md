# RijanOS Assistant - Quick Start Guide

## 🚀 Instalasi Cepat

### Linux/Rijan OS
```bash
# Clone repository
git clone https://github.com/teguh02/rijan_os_assistant.git
cd rijan_os_assistant

# Jalankan script instalasi
chmod +x install.sh
./install.sh
```

### Windows
```cmd
# Download dan extract
# Jalankan script instalasi
install.bat
```

## 🎯 Penggunaan Dasar

### 1. Jalankan Aplikasi
```bash
# Linux/Rijan OS
python3 /opt/rijanos-assistant/main.py

# Windows
python "C:\Program Files\RijanOS Assistant\main.py"
```

### 2. Konfigurasi AI Assistant (Opsional)
1. Buka tab **Settings**
2. Aktifkan "Aktifkan AI Assistant"
3. Masukkan Gemini API key
4. Klik **Simpan Pengaturan**

### 3. Instalasi Aplikasi
- **Dashboard**: Aksi cepat (Update, Clean, Backup)
- **Applications**: Stack development (Python, PHP, Node.js, Go)
- **Multimedia**: Audio, video, graphics, streaming, 3D
- **Maintenance**: Pembersihan sistem
- **Power**: Shutdown, restart, schedule shutdown

### 4. System Tray
- Klik close (X) untuk minimize ke tray
- Double-click tray icon untuk buka window
- Right-click untuk menu quick actions

## ⚙️ Konfigurasi Cepat

### AI Assistant
```json
{
  "ai_enabled": true,
  "gemini_api_key": "YOUR_API_KEY_HERE"
}
```

### Blocked Commands
```json
{
  "blocked_commands": [
    "rm -rf /",
    "mkfs",
    "dd if=",
    ":(){ :|: & };:"
  ]
}
```

## 🔧 Troubleshooting

### Error: "PyQt6 tidak tersedia"
```bash
sudo apt install python3-pyqt6
# atau
pip3 install PyQt6
```

### Error: "Permission denied"
```bash
chmod +x /opt/rijanos-assistant/main.py
```

### System Tray Tidak Muncul
```bash
# Install desktop environment
sudo apt install ubuntu-desktop-minimal
```

## 📞 Support

- **GitHub**: https://github.com/teguh02/rijan_os/issues
- **Dokumentasi**: DOCUMENTATION.md
- **Demo**: `python3 demo.py`

---

**RijanOS Assistant v1.1.0** - Quick Start Guide
