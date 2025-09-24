# Panduan Instalasi RijanOS Assistant

## Persyaratan Sistem

- **OS**: Linux (Rijan OS, Ubuntu, Debian, dll)
- **Python**: 3.8 atau lebih baru
- **RAM**: Minimal 2GB
- **Disk**: Minimal 100MB untuk aplikasi

## Instalasi Cepat

### 1. Clone Repository
```bash
git clone https://github.com/teguh02/rijan_os.git
cd rijan_os/os_assistant
```

### 2. Install Dependencies
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Atau gunakan virtual environment (direkomendasikan)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
# Langsung
python3 main.py

# Atau gunakan script
./run.sh    # Linux/Mac
run.bat     # Windows
```

## Instalasi Manual

### 1. Install Python Dependencies
```bash
pip3 install PyQt6>=6.4.0
pip3 install requests>=2.28.0
```

### 2. Verifikasi Instalasi
```bash
python3 demo.py
```

### 3. Konfigurasi Awal
1. Jalankan aplikasi: `python3 main.py`
2. Buka tab **Settings**
3. Konfigurasi AI Assistant (opsional):
   - Aktifkan "Aktifkan AI Assistant"
   - Masukkan Gemini API key
   - Klik "Simpan Pengaturan"

## Troubleshooting

### Error: "PyQt6 tidak tersedia"
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pyqt6

# Atau install via pip
pip3 install PyQt6
```

### Error: "Permission denied"
```bash
# Pastikan file executable
chmod +x run.sh
chmod +x main.py
```

### Error: "API key tidak tersedia"
1. Buka tab Settings
2. Masukkan Gemini API key
3. Klik "Simpan Pengaturan"

### Error: "Command diblokir"
- Command tersebut ada dalam daftar blocked commands
- Edit daftar di Settings > Security jika diperlukan

## Konfigurasi Lanjutan

### 1. AI Assistant
- Dapatkan API key dari: https://makersuite.google.com/app/apikey
- Masukkan di Settings > AI Settings
- Test koneksi untuk memastikan berfungsi

### 2. Keamanan
- Edit blocked commands di Settings > Security
- Tambah command berbahaya yang ingin diblokir
- Selalu backup konfigurasi sebelum mengubah

### 3. Package Commands
- Edit apt commands di Settings > Package Commands
- Tambah stack aplikasi sesuai kebutuhan
- Reset ke default jika diperlukan

## Uninstall

```bash
# Hapus virtual environment
rm -rf venv/

# Hapus dependencies (jika tidak digunakan aplikasi lain)
pip3 uninstall PyQt6 requests

# Hapus aplikasi
rm -rf /path/to/rijanos_assistant/
```

## Support

Jika mengalami masalah:
1. Cek log error di terminal
2. Pastikan dependencies terinstall dengan benar
3. Cek konfigurasi di Settings
4. Laporkan bug di: https://github.com/teguh02/rijan_os/issues

---

**RijanOS Assistant v1.0** - Panduan Instalasi
