# RijanOS Assistant

Sistem asisten GUI untuk Rijan OS yang menyediakan interface yang mudah digunakan untuk manajemen sistem, instalasi paket, backup/restore, dan AI assistant.

## Fitur

### 🤖 AI Assistant (Opsional)
- Chat dengan AI menggunakan Gemini API
- Jawaban dalam Bahasa Indonesia yang formal dan terstruktur
- Validasi keamanan untuk mencegah eksekusi command berbahaya

### 📦 Package Manager
- Instalasi stack aplikasi dengan satu klik
- Development stacks: Python, PHP, Node.js, Go
- Aplikasi: Media tools, Education apps, Developer tools, System tools
- **Multimedia apps**: Audacity, VLC, GIMP, OBS Studio, Kdenlive, Blender
- Maintenance sistem: Update, upgrade, autoremove

### 💾 Backup & Restore
- Backup folder atau filesystem
- Multiple format: tar.gz, zip, 7z
- Restore dari file backup
- Interface yang user-friendly

### 🔧 System Maintenance
- Pembersihan cache APT
- Pembersihan journal logs
- Pembersihan file temporary
- Autoremove paket yang tidak terpakai

### ⚡ Power Management
- **Shutdown & Restart**: Kontrol power sistem dengan aman
- **Scheduled Shutdown**: Jadwalkan shutdown dengan format waktu fleksibel
- **Cancel Shutdown**: Batalkan shutdown yang dijadwalkan
- Konfirmasi keamanan sebelum eksekusi

### 🎬 Multimedia Apps
- **Audio Tools**: Audacity untuk editing audio
- **Video Players**: VLC untuk pemutaran video
- **Graphics**: GIMP untuk editing gambar
- **Streaming**: OBS Studio untuk streaming
- **Video Editor**: Kdenlive untuk editing video
- **3D Modeling**: Blender untuk modeling 3D

### 🔔 System Tray
- **Tray Icon**: Aplikasi berjalan di system tray
- **Quick Actions**: Update sistem, bersihkan cache
- **Power Options**: Shutdown, restart, schedule shutdown
- **Minimize to Tray**: Aplikasi tidak benar-benar tertutup

### ⚙️ Settings
- Konfigurasi AI Assistant
- Pengaturan keamanan (blocked commands)
- Edit apt commands secara interaktif
- Simpan preferensi pengguna

## Instalasi

1. Clone repository:
```bash
git clone https://github.com/teguh02/rijan_os.git
cd rijan_os/os_assistant
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Jalankan aplikasi:
```bash
python3 main.py
```

## Konfigurasi

### AI Assistant
1. Buka tab Settings
2. Aktifkan "Aktifkan AI Assistant"
3. Masukkan Gemini API key
4. Klik "Simpan Pengaturan"

### Keamanan
- Edit daftar blocked commands di Settings > Security
- Command berbahaya akan diblokir secara otomatis
- Selalu backup konfigurasi sebelum mengubah pengaturan

### Package Commands
- Edit apt commands di Settings > Package Commands
- Tambah/hapus stack aplikasi sesuai kebutuhan
- Reset ke default jika diperlukan

## Struktur Proyek

```
RijanOS_Assistant/
├── main.py                 # Entry point
├── config.json            # Konfigurasi aplikasi
├── requirements.txt       # Dependencies
├── gui/                   # Module GUI
│   ├── __init__.py
│   ├── main_window.py     # Window utama
│   ├── settings_window.py # Window settings
│   └── ai_chat_window.py # Window AI chat
├── core/                  # Module core
│   ├── __init__.py
│   ├── command_executor.py # Eksekusi command
│   ├── package_manager.py # Manajemen paket
│   ├── backup_restore.py # Backup & restore
│   └── system_tools.py   # Tools sistem
└── assets/               # File statis
    ├── __init__.py
    ├── icons/           # Icon aplikasi
    └── logo.png         # Logo RijanOS
```

## Keamanan

- Semua command dieksekusi melalui `command_executor.py`
- Validasi command berbahaya sebelum eksekusi
- Daftar blocked commands yang dapat dikustomisasi
- Tidak ada eksekusi command otomatis tanpa konfirmasi

## Troubleshooting

### Error "API key tidak tersedia"
- Pastikan Gemini API key sudah dikonfigurasi di Settings
- Periksa koneksi internet

### Error "Command diblokir"
- Command tersebut ada dalam daftar blocked commands
- Edit daftar blocked commands di Settings jika diperlukan

### Error "Permission denied"
- Pastikan aplikasi dijalankan dengan permission yang cukup
- Beberapa command memerlukan sudo

## Kontribusi

1. Fork repository
2. Buat feature branch
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## Lisensi

MIT License - lihat file LICENSE untuk detail.

## Support

- GitHub Issues: https://github.com/teguh02/rijan_os/issues
- Email: support@rijanos.com

---

**RijanOS Assistant v1.0** - Dibuat dengan ❤️ untuk Rijan OS
