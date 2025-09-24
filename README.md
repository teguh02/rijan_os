# Rijan OS Welcome Screen

Aplikasi GUI Python menggunakan Tkinter yang berfungsi sebagai layar selamat datang untuk sistem operasi Rijan OS.

## Struktur Proyek

```
RijanOS_Welcome/
├── main.py              # File utama aplikasi
├── requirements.txt     # Dependencies Python
├── README.md           # Dokumentasi proyek
└── images/             # Folder gambar wallpaper
    ├── wallpaper1.jpg  # Background slide 1
    ├── wallpaper2.jpg  # Background slide 2
    ├── wallpaper3.jpg  # Background slide 3
    ├── wallpaper4.jpg  # Background slide 4
    └── wallpaper5.jpg  # Background slide 5
```

## Fitur

1. **Pengecekan State File**: Aplikasi akan mengecek file `~/.rijan_welcome_done`. Jika file ada, aplikasi akan keluar otomatis.

2. **5 Slide Welcome**: Menampilkan 5 slide dengan konten informatif tentang Rijan OS dalam Bahasa Indonesia.

3. **Desain Modern & Profesional**: 
   - Background gradient yang indah dengan efek blur
   - Typography yang elegan dengan hierarki yang jelas
   - Glass morphism effect pada container utama
   - Skema warna modern dengan palet yang konsisten

4. **Navigasi Interaktif**: 
   - Tombol dengan hover effects dan animasi halus
   - Progress indicators dengan dots yang responsif
   - Keyboard navigation (panah kiri/kanan, spasi, ESC)
   - Visual feedback untuk setiap interaksi

5. **Layout Responsif**: 
   - Auto-resizing untuk berbagai ukuran layar
   - Content positioning yang dinamis
   - Scaling gambar yang optimal

6. **User Experience**: 
   - Animasi transisi yang halus
   - Countdown timer saat selesai
   - Visual hierarchy yang jelas
   - Icon dan emoji untuk setiap slide

7. **State Management**: 
   - Setelah selesai, aplikasi akan membuat file state agar tidak muncul lagi
   - File state berisi timestamp dan informasi sistem saat completion
   - Tracking waktu penyelesaian welcome setup

## Instalasi dan Penggunaan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```bash
python main.py
```

### 3. Ganti Gambar Wallpaper (Opsional)

Ganti file `wallpaper1.jpg` sampai `wallpaper5.jpg` di folder `images/` dengan gambar wallpaper yang diinginkan. Pastikan gambar berformat JPG dan memiliki resolusi yang baik (minimal 1920x1080).

## Konten Slide

1. **Slide 1** 🇮🇩: **Selamat Datang di Rijan OS** - Sistem operasi asli buatan anak bangsa
2. **Slide 2** ✨: **Desain yang Elegan** - Perpaduan sempurna dari berbagai OS
3. **Slide 3** ⚡: **Performa Optimal** - Ringan dan cepat untuk semua perangkat
4. **Slide 4** 💼: **Siap Produktif** - Sudah dilengkapi aplikasi penting
5. **Slide 5** 🔒: **Bebas & Aman** - Open source, transparan, dan aman

## Reset Welcome Screen

Untuk menampilkan welcome screen lagi, hapus file state:

```bash
# Linux/macOS
rm ~/.rijan_welcome_done

# Windows PowerShell
Remove-Item "$env:USERPROFILE\.rijan_welcome_done"
```

### Isi File State

Setelah menyelesaikan welcome screen, file `~/.rijan_welcome_done` akan berisi:
```
Rijan OS Welcome Screen completed on: 2024-09-24 15:30:45
User completed the welcome setup successfully.
System: nt
Timestamp (ISO): 2024-09-24T15:30:45.123456
```

## Kustomisasi

File `main.py` dibuat dengan struktur yang mudah dimodifikasi:

- **Konten slide**: Edit array `self.slide_contents`
- **Warna tema**: Ubah kode warna hex di berbagai widget
- **Font**: Modifikasi parameter font pada label dan button
- **Ukuran window**: Sesuaikan di method `setup_window()`

## Requirements

- Python 3.7+
- Tkinter (biasanya sudah terinstal dengan Python)
- Pillow (PIL) untuk manipulasi gambar

## Deployment di Linux Rijan OS

### Instalasi Otomatis (Rekomendasi)

Gunakan script instalasi otomatis untuk kemudahan:

```bash
# Download dan extract aplikasi
# Kemudian jalankan:
sudo ./install.sh

# Untuk uninstall:
sudo ./install.sh uninstall

# Untuk test instalasi:
sudo ./install.sh test
```

### Instalasi Manual

Jika ingin instalasi manual, ikuti langkah-langkah berikut:

#### 1. Persiapan Sistem

Pastikan sistem Rijan OS sudah memiliki Python dan dependencies yang diperlukan:

```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Install Python dan pip jika belum ada
sudo apt install python3 python3-pip python3-venv python3-tk -y

# Install dependencies sistem untuk Pillow
sudo apt install libjpeg-dev libpng-dev libtiff-dev libfreetype6-dev -y
```

### 2. Setup Aplikasi

```bash
# Clone atau copy aplikasi ke direktori sistem
sudo mkdir -p /opt/rijan-os-welcome
sudo cp -r * /opt/rijan-os-welcome/
cd /opt/rijan-os-welcome

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set permissions
sudo chmod +x main.py
sudo chown -R root:root /opt/rijan-os-welcome
sudo chmod 755 /opt/rijan-os-welcome/main.py
```

### 3. Buat Executable Script

Buat script launcher di `/usr/local/bin/rijan-welcome`:

```bash
sudo tee /usr/local/bin/rijan-welcome << 'EOF'
#!/bin/bash
cd /opt/rijan-os-welcome
source venv/bin/activate
python3 main.py
EOF

sudo chmod +x /usr/local/bin/rijan-welcome
```

### 4. Konfigurasi Startup (Systemd Service)

Buat service systemd untuk menjalankan saat startup:

```bash
sudo tee /etc/systemd/system/rijan-welcome.service << 'EOF'
[Unit]
Description=Rijan OS Welcome Screen
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/local/bin/rijan-welcome
Environment=DISPLAY=:0
User=root
Group=root
Restart=no
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=graphical-session.target
EOF

# Enable service untuk startup
sudo systemctl daemon-reload
sudo systemctl enable rijan-welcome.service
```

### 5. Alternatif: Autostart dengan Desktop Entry

Untuk user-level autostart, buat file desktop entry:

```bash
mkdir -p ~/.config/autostart
tee ~/.config/autostart/rijan-welcome.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Rijan OS Welcome
Comment=Rijan OS Welcome Screen
Exec=/usr/local/bin/rijan-welcome
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
StartupNotify=false
EOF
```

### 6. Build untuk Distribusi

Gunakan script build otomatis:

```bash
# Build semua format (executable, tarball, deb)
./build.sh

# Build hanya executable
./build.sh executable

# Build hanya tarball distribusi
./build.sh package

# Build hanya DEB package
./build.sh deb

# Clean build directory
./build.sh clean
```

Atau manual dengan PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --add-data "images:images" main.py

# Hasil build akan ada di folder dist/
```

### 7. Integrasi dengan Display Manager

Untuk integrasi yang lebih dalam dengan sistem, tambahkan ke display manager:

#### Untuk GDM (GNOME Display Manager):
```bash
sudo tee /etc/gdm3/PostLogin/Default << 'EOF'
#!/bin/sh
/usr/local/bin/rijan-welcome &
EOF

sudo chmod +x /etc/gdm3/PostLogin/Default
```

#### Untuk SDDM (KDE Display Manager):
```bash
sudo tee -a /etc/sddm.conf << 'EOF'
[General]
DisplayServer=x11

[X11]
SessionCommand=/usr/local/bin/rijan-welcome; /etc/X11/Xsession
EOF
```

### 8. Testing dan Debugging

```bash
# Test manual
/usr/local/bin/rijan-welcome

# Cek status service
sudo systemctl status rijan-welcome.service

# Lihat logs
sudo journalctl -u rijan-welcome.service -f

# Test autostart
sudo systemctl start rijan-welcome.service

# Disable jika diperlukan
sudo systemctl disable rijan-welcome.service
```

### 9. Konfigurasi Tambahan

#### Untuk mencegah multiple instance:
Tambahkan lock file mechanism di awal main.py:

```python
import fcntl
import sys

# Prevent multiple instances
lock_file = "/tmp/rijan-welcome.lock"
try:
    lock = open(lock_file, 'w')
    fcntl.lockf(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print("Welcome screen already running")
    sys.exit(0)
```

#### Untuk delay startup (opsional):
```bash
# Tambahkan delay 5 detik sebelum menjalankan
sudo sed -i '/ExecStart=/i ExecStartPre=/bin/sleep 5' /etc/systemd/system/rijan-welcome.service
sudo systemctl daemon-reload
```

## Troubleshooting

### Gambar tidak muncul
- Pastikan file wallpaper ada di folder `images/`
- Cek format file (harus JPG)
- Pastikan Pillow terinstal dengan benar

### Window tidak fullscreen di Linux
- Ganti `self.root.state('zoomed')` dengan `self.root.attributes('-zoomed', True)`
- Atau gunakan `self.root.attributes('-fullscreen', True)` untuk fullscreen penuh

### Service tidak jalan saat startup
```bash
# Cek status service
sudo systemctl status rijan-welcome.service

# Cek logs untuk error
sudo journalctl -u rijan-welcome.service

# Pastikan DISPLAY environment tersedia
export DISPLAY=:0
```

### Error permission di Linux
```bash
# Fix permission
sudo chown -R root:root /opt/rijan-os-welcome
sudo chmod +x /opt/rijan-os-welcome/main.py
sudo chmod +x /usr/local/bin/rijan-welcome
```

### Error import PIL di Linux
```bash
sudo apt install python3-pil python3-pil.imagetk
# atau
pip install --upgrade Pillow
```

## Uninstall

Untuk menghapus aplikasi dari sistem:

```bash
# Stop dan disable service
sudo systemctl stop rijan-welcome.service
sudo systemctl disable rijan-welcome.service

# Hapus files
sudo rm -rf /opt/rijan-os-welcome
sudo rm /usr/local/bin/rijan-welcome
sudo rm /etc/systemd/system/rijan-welcome.service
sudo rm ~/.config/autostart/rijan-welcome.desktop

# Reload systemd
sudo systemctl daemon-reload
```

## Lisensi

Proyek ini dibuat untuk Rijan OS dan dapat dimodifikasi sesuai kebutuhan.
