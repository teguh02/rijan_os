# Changelog RijanOS Assistant

## [v1.1.0] - 2024-12-19

### ✨ Fitur Baru
- **🎬 Multimedia Apps Tab**: Tab baru untuk instalasi aplikasi multimedia
  - Audacity (audio editor)
  - VLC (video player)
  - GIMP (image editor)
  - OBS Studio (streaming software)
  - Kdenlive (video editor)
  - Blender (3D modeling)
- **⚡ Power Management Tab**: Kontrol power sistem
  - Shutdown Now
  - Restart Now
  - Schedule Shutdown (format: +30, 23:00, +2h)
  - Cancel Scheduled Shutdown
- **🔔 System Tray Icon**: Aplikasi berjalan di system tray
  - Quick actions: Update sistem, bersihkan cache
  - Power options: Shutdown, restart, schedule shutdown
  - Minimize to tray saat window ditutup
- **📦 Updated Package Commands**:
  - Education apps: stellarium, texstudio, texlive-full
  - Multimedia apps: audacity, vlc, gimp, obs-studio, kdenlive, blender
  - Developer apps: ditambahkan Visual Studio Code
  - System apps: dihapus neofetch

### 🔧 Perbaikan
- Validasi format waktu untuk scheduled shutdown
- Konfirmasi keamanan untuk power operations
- System tray integration yang lebih baik
- UI/UX improvements untuk tab baru

### 🛡️ Keamanan
- Semua power commands melalui command_executor.py
- Validasi format waktu yang ketat
- Konfirmasi dialog untuk operasi berbahaya

## [v1.0.0] - 2024-12-19

### ✨ Fitur Awal
- **🤖 AI Assistant**: Chat dengan Gemini API
- **📦 Package Manager**: Instalasi stack aplikasi
- **💾 Backup & Restore**: Backup/restore dengan multiple format
- **🔧 System Maintenance**: Pembersihan cache dan maintenance
- **⚙️ Settings**: Konfigurasi aplikasi
- **🐛 Bug Report**: Integrasi dengan GitHub issues

### 🏗️ Arsitektur
- Modular design dengan core dan gui modules
- Command executor dengan validasi keamanan
- Config system dengan JSON
- PyQt6 GUI framework
- Thread-based command execution

---

**RijanOS Assistant** - Sistem Asisten GUI untuk Rijan OS
