# RijanOS Assistant - Dokumentasi Lengkap

## Pendahuluan

**RijanOS Assistant** adalah sistem asisten GUI yang dirancang khusus untuk Rijan OS. Aplikasi ini menyediakan interface yang mudah digunakan untuk manajemen sistem, instalasi paket, backup/restore, dan AI assistant yang terintegrasi.

### Fitur Utama

- **🤖 AI Assistant** (Opsional): Chat dengan AI menggunakan Gemini API untuk bantuan teknis
- **📦 Quick App Installation**: Instalasi stack aplikasi dengan satu klik
- **🔄 System Updates**: Update dan upgrade sistem dengan mudah
- **🎬 Multimedia & Education Apps**: Instalasi aplikasi multimedia dan pendidikan
- **💾 Backup & Restore**: Backup dan restore sistem dengan multiple format
- **⚡ Power Management**: Kontrol power sistem (shutdown, restart, schedule)
- **🔔 System Tray**: Quick actions melalui system tray icon
- **⚙️ Settings**: Konfigurasi lengkap aplikasi

## Persyaratan Sistem

### Sistem Operasi
- **Rijan OS** (berbasis Ubuntu Server atau Ubuntu Desktop)
- Ubuntu 20.04 LTS atau lebih baru
- Desktop Environment (untuk GUI): GNOME, KDE, XFCE, atau LXDE

### Software Requirements
- **Python**: 3.10 atau lebih baru
- **Pip**: Package manager untuk Python
- **Git**: Untuk cloning repository
- **Dependencies**: PyQt6, requests, httpx, jsonlib

### Hardware Requirements
- **RAM**: Minimal 2GB (4GB direkomendasikan)
- **Disk**: Minimal 500MB untuk aplikasi
- **CPU**: x86_64 architecture
- **Display**: 1024x768 atau lebih tinggi

## Instalasi

### Langkah 1: Update Sistem

Pastikan sistem Rijan OS Anda ter-update:

```bash
sudo apt update && sudo apt upgrade -y
```

### Langkah 2: Install Dependencies

Install Python dan dependencies yang diperlukan:

```bash
# Install Python dan tools
sudo apt install -y python3 python3-pip python3-venv git

# Install PyQt6 dan dependencies
sudo apt install -y python3-pyqt6 python3-pyqt6.qtwidgets

# Install additional packages
pip3 install requests httpx
```

### Langkah 3: Clone Repository

Clone atau copy source code RijanOS Assistant:

```bash
# Buat direktori untuk aplikasi
sudo mkdir -p /opt/rijanos-assistant
cd /opt/rijanos-assistant

# Clone repository
sudo git clone https://github.com/teguh02/rijan_os_assistant.git .

# Set permissions
sudo chown -R $USER:$USER /opt/rijanos-assistant
chmod +x /opt/rijanos-assistant/main.py
```

### Langkah 4: Verifikasi Instalasi

Pastikan file `config.json` dibuat otomatis:

```bash
# Cek apakah config.json ada
ls -la /opt/rijanos-assistant/config.json

# Jika belum ada, jalankan aplikasi sekali untuk membuatnya
cd /opt/rijanos-assistant
python3 main.py
```

### Langkah 5: Test Run

Jalankan aplikasi untuk pertama kali:

```bash
cd /opt/rijanos-assistant
python3 main.py
```

## Instalasi untuk Developer

### Langkah 1: Clone Repository

Clone repository dari GitHub:

```bash
# Clone repository
git clone https://github.com/teguh02/rijan_os.git
cd rijan_os

# Checkout ke branch assistant_os
git checkout assistant_os
```

### Langkah 2: Setup Virtual Environment

Buat dan aktifkan virtual environment:

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
# Untuk Linux/macOS:
source venv/bin/activate

# Untuk Windows:
venv\Scripts\activate
```

### Langkah 3: Install Dependencies

Install dependencies yang diperlukan:

```bash
# Install dependencies dari requirements.txt
pip install -r requirements.txt

# Untuk development, install dependencies tambahan
pip install pytest flake8 black isort
```

### Langkah 4: Setup Development Environment

```bash
# Copy dan edit config untuk development
cp config.json config.dev.json

# Edit config untuk development (opsional)
nano config.dev.json
```

### Langkah 5: Run Development Server

```bash
# Jalankan aplikasi dalam mode development
python main.py

# Atau dengan config khusus
python main.py --config config.dev.json
```

### Langkah 6: Setup Git Hooks (Opsional)

```bash
# Setup pre-commit hooks untuk code quality
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running pre-commit checks..."

# Format code with black
black --check .

# Sort imports
isort --check-only .

# Lint with flake8
flake8 .

echo "Pre-commit checks passed!"
EOF

chmod +x .git/hooks/pre-commit
```

### Struktur Project untuk Developer

```
rijan_os/
├── core/                    # Core modules
│   ├── __init__.py
│   ├── command_executor.py  # Command execution with safety
│   ├── package_manager.py   # Package management
│   └── system_tools.py      # System tools and utilities
├── gui/                     # GUI modules
│   ├── __init__.py
│   ├── main_window.py       # Main application window
│   ├── ai_chat_window.py    # AI chat interface
│   ├── settings_window.py   # Settings window
│   └── system_tray.py       # System tray functionality
├── assets/                  # Static assets
│   ├── __init__.py
│   └── logo.png            # Application logo
├── main.py                  # Application entry point
├── config.json             # Default configuration
├── requirements.txt        # Python dependencies
├── README.md              # Project README
├── DOCUMENTATION.md       # This file
├── DEVELOPER_GUIDE.md     # Developer guide
├── CHANGELOG.md           # Change log
└── install.sh            # Installation script
```

### Development Workflow

#### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Test changes
python main.py

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push to GitHub
git push origin feature/new-feature
```

#### 2. Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Run tests (if available)
pytest
```

#### 3. Configuration for Development

Edit `config.json` untuk development:

```json
{
  "ai_enabled": true,
  "gemini_api_key": "YOUR_DEVELOPMENT_API_KEY",
  "gemini_model": "gemini-2.5-flash-lite",
  "console_visible": true,
  "debug_mode": true,
  "log_level": "DEBUG"
}
```

#### 4. Testing AI Features

```bash
# Test dengan API key development
export GEMINI_API_KEY="your_dev_api_key"
python main.py

# Test tanpa AI (offline mode)
python main.py --no-ai
```

### Developer Tools & Commands

#### Useful Development Commands

```bash
# Check Python syntax
python -m py_compile main.py

# Check imports
python -c "import main; print('All imports OK')"

# Generate requirements.txt
pip freeze > requirements.txt

# Create distribution
python setup.py sdist bdist_wheel

# Install in development mode
pip install -e .
```

#### Debugging

```bash
# Run with debug mode
python main.py --debug

# Run with verbose logging
python main.py --verbose

# Run specific module
python -m gui.ai_chat_window

# Profile performance
python -m cProfile main.py
```

### Contributing Guidelines

1. **Fork** repository di GitHub
2. **Clone** fork Anda ke local machine
3. **Create** feature branch dari `assistant_os`
4. **Make** changes dan test thoroughly
5. **Commit** dengan conventional commit messages
6. **Push** ke fork Anda
7. **Create** Pull Request ke branch `assistant_os`

### API Key untuk Development

Untuk development dengan AI features:

1. Dapatkan API key dari: https://aistudio.google.com/apikey
2. Set di environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
3. Atau edit `config.json`:
   ```json
   {
     "gemini_api_key": "your_api_key_here"
   }
   ```

**⚠️ Penting**: Jangan commit API key ke repository!

### Deployment untuk Developer

```bash
# Build untuk production
python -m build

# Test installation
pip install dist/rijanos-assistant-*.whl

# Create installer
./create_installer.sh

# Deploy to test server
./deploy.sh --env staging
```

## Konfigurasi

### File config.json

RijanOS Assistant menggunakan file `config.json` untuk menyimpan konfigurasi:

```json
{
  "ai_enabled": false,
  "gemini_api_key": "",
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
    "multimedia_apps": "sudo apt install -y audacity vlc gimp obs-studio kdenlive blender"
  }
}
```

### Field Konfigurasi

- **`ai_enabled`**: `true/false` - Aktifkan/nonaktifkan AI assistant
- **`gemini_api_key`**: API key Gemini untuk AI assistant (kosong default)
- **`blocked_commands`**: Daftar command berbahaya yang diblokir
- **`apt_commands`**: Dictionary command apt install untuk berbagai stack

### Mengedit Konfigurasi

#### Via GUI (Direkomendasikan)
1. Buka RijanOS Assistant
2. Klik tab **Settings**
3. Edit konfigurasi sesuai kebutuhan
4. Klik **Simpan Pengaturan**

#### Via File Manual
```bash
# Edit config.json dengan editor favorit
nano /opt/rijanos-assistant/config.json

# Atau dengan vim
vim /opt/rijanos-assistant/config.json
```

## Autostart pada Login

### Setup Autostart

Untuk menjalankan RijanOS Assistant otomatis saat login:

```bash
# Buat direktori autostart
mkdir -p ~/.config/autostart

# Buat file desktop entry
cat > ~/.config/autostart/rijanos-assistant.desktop << EOF
[Desktop Entry]
Type=Application
Exec=python3 /opt/rijanos-assistant/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=RijanOS Assistant
Comment=Start RijanOS Assistant on login
Icon=/opt/rijanos-assistant/assets/logo.png
EOF

# Set permissions
chmod +x ~/.config/autostart/rijanos-assistant.desktop
```

### Disable Autostart

Untuk menonaktifkan autostart:

```bash
# Hapus file desktop entry
rm ~/.config/autostart/rijanos-assistant.desktop

# Atau disable tanpa menghapus
chmod -x ~/.config/autostart/rijanos-assistant.desktop
```

## Penggunaan

### Tab Dashboard

**Dashboard** menyediakan aksi cepat:

- **🔄 Update Sistem**: `sudo apt update`
- **🧹 Bersihkan Cache**: `sudo apt clean && sudo apt autoremove -y`
- **💾 Backup Cepat**: Backup home directory
- **🐛 Laporkan Bug**: Buka halaman GitHub issues

### Tab Applications

**Applications** untuk instalasi stack aplikasi:

#### Development Stacks
- **🐍 Python Stack**: Python3, pip, venv, jupyter, numpy, pandas, matplotlib
- **🐘 PHP Stack**: PHP, Composer
- **🟢 Node.js Stack**: Node.js, npm, yarn
- **🐹 Go Stack**: Golang

#### Application Categories
- **🎬 Media Tools**: VLC, GIMP, Audacity, OBS Studio
- **📚 Education Apps**: Stellarium, TeXstudio, TeX Live
- **💻 Developer Apps**: Git, VS Code, Docker, Postman
- **⚙️ System Apps**: htop, GParted, curl, wget

### Tab Multimedia Apps

**Multimedia Apps** untuk aplikasi multimedia:

- **🎵 Audio Tools**: Audacity
- **🎬 Video Players**: VLC
- **🎨 Graphics**: GIMP
- **📹 Streaming**: OBS Studio
- **✂️ Video Editor**: Kdenlive
- **🎭 3D Modeling**: Blender

### Tab Maintenance

**Maintenance** untuk pembersihan sistem:

- **Clear APT Cache**: `sudo apt clean`
- **Clear Journal Logs**: `sudo journalctl --vacuum-time=7d`
- **Clear Temp Files**: `sudo rm -rf /tmp/* && rm -rf ~/.cache/*`
- **Autoremove Packages**: `sudo apt autoremove -y`

### Tab Backup & Restore

**Backup & Restore** untuk backup sistem:

#### Backup
1. Pilih source directory/file
2. Pilih output location
3. Pilih format (tar.gz, zip, 7z)
4. Klik **Buat Backup**

#### Restore
1. Pilih file backup
2. Pilih target directory
3. Klik **Restore**

### Tab Power Management

**Power Management** untuk kontrol power sistem:

#### Immediate Actions
- **🔴 Shutdown Now**: `sudo shutdown -h now`
- **🔄 Restart Now**: `sudo reboot`

#### Scheduled Shutdown
- **Format Waktu**:
  - `+30` (30 menit dari sekarang)
  - `23:00` (jam 23:00)
  - `+2h` (2 jam dari sekarang)
- **Cancel Shutdown**: `sudo shutdown -c`

### Tab AI Assistant

**AI Assistant** untuk chat dengan AI (jika diaktifkan):

1. Konfigurasi API key di Settings
2. Chat dengan AI dalam Bahasa Indonesia
3. Dapatkan bantuan teknis untuk Rijan OS

### System Tray

**System Tray** menyediakan quick actions:

#### Menu Tray
- **🏠 Buka Window Utama**
- **🔄 Update Sistem**
- **🧹 Bersihkan Cache**
- **⚡ Power Options**:
  - Shutdown Now
  - Restart Now
  - Schedule Shutdown
  - Cancel Shutdown
- **🚪 Keluar**

#### Minimize to Tray
- Klik tombol close (X) untuk minimize ke tray
- Double-click tray icon untuk buka window
- Aplikasi tetap berjalan di background

## Keamanan

### Blocked Commands

RijanOS Assistant memblokir command berbahaya secara default:

```json
"blocked_commands": [
  "rm -rf /",
  "mkfs",
  "dd if=",
  ":(){ :|: & };:",
  "sudo rm -rf /",
  "format",
  "fdisk",
  "parted"
]
```

### Menambah Blocked Commands

Edit `config.json` atau via Settings tab:

```json
"blocked_commands": [
  "rm -rf /",
  "mkfs",
  "dd if=",
  ":(){ :|: & };:",
  "sudo rm -rf /",
  "format",
  "fdisk",
  "parted",
  "shutdown",
  "reboot",
  "halt"
]
```

### Validasi Command

Semua command dieksekusi melalui `command_executor.py` dengan:
- Validasi format command
- Pengecekan blocked commands
- Timeout protection
- Error handling

## Troubleshooting

### Error: "PyQt6 tidak tersedia"

```bash
# Install PyQt6
sudo apt install python3-pyqt6

# Atau via pip
pip3 install PyQt6
```

### Error: "Permission denied"

```bash
# Set permissions
chmod +x /opt/rijanos-assistant/main.py
chmod +x /opt/rijanos-assistant/run.sh

# Atau jalankan dengan sudo (tidak direkomendasikan)
sudo python3 /opt/rijanos-assistant/main.py
```

### Error: "API key tidak tersedia"

1. Buka tab **Settings**
2. Masukkan Gemini API key
3. Klik **Simpan Pengaturan**
4. Restart aplikasi

### Error: "Command diblokir"

- Command tersebut ada dalam daftar blocked commands
- Edit daftar di Settings > Security jika diperlukan
- Pastikan command aman sebelum menambahkannya

### System Tray Tidak Muncul

```bash
# Cek apakah system tray tersedia
python3 -c "from PyQt6.QtWidgets import QSystemTrayIcon; print(QSystemTrayIcon.isSystemTrayAvailable())"

# Jika False, install desktop environment
sudo apt install ubuntu-desktop-minimal
```

## Bug Reporting

Jika menemukan bug atau masalah:

1. **GitHub Issues**: https://github.com/teguh02/rijan_os/issues
2. **Email**: support@rijanos.com
3. **Forum**: https://forum.rijanos.com

### Informasi yang Diperlukan

- **OS Version**: `lsb_release -a`
- **Python Version**: `python3 --version`
- **Error Message**: Copy paste error yang muncul
- **Steps to Reproduce**: Langkah-langkah untuk reproduce bug
- **Screenshots**: Jika ada

## Uninstall

### Hapus Aplikasi

```bash
# Hapus direktori aplikasi
sudo rm -rf /opt/rijanos-assistant

# Hapus autostart
rm ~/.config/autostart/rijanos-assistant.desktop

# Hapus dependencies (opsional)
pip3 uninstall PyQt6 requests httpx
```

### Hapus Konfigurasi

```bash
# Hapus config user
rm ~/.config/rijanos-assistant/

# Hapus log files
rm -rf ~/.cache/rijanos-assistant/
```

## Support

### Dokumentasi Resmi
- **GitHub**: https://github.com/teguh02/rijan_os
- **Wiki**: https://github.com/teguh02/rijan_os/wiki
- **Issues**: https://github.com/teguh02/rijan_os/issues

### Komunitas
- **Forum**: https://forum.rijanos.com
- **Discord**: https://discord.gg/rijanos
- **Telegram**: https://t.me/rijanos

### Kontak
- **Email**: support@rijanos.com
- **Twitter**: @RijanOS
- **Website**: https://rijanos.com

---

**RijanOS Assistant v1.1.0** - Sistem Asisten GUI untuk Rijan OS

*Dokumentasi ini adalah bagian dari Rijan OS Developer Resources*
