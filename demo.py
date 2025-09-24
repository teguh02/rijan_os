#!/usr/bin/env python3
"""
Demo script untuk RijanOS Assistant
Menunjukkan fitur-fitur utama aplikasi
"""

import json
import os
import sys

def print_banner():
    """Print banner aplikasi"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    RijanOS Assistant v1.0                   ║
    ║                                                              ║
    ║  🤖 AI Assistant    📦 Package Manager    💾 Backup/Restore  ║
    ║  🔧 Maintenance     ⚙️ Settings          🐛 Bug Report       ║
    ║                                                              ║
    ║  Sistem Asisten GUI untuk Rijan OS                           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Cek dependencies yang diperlukan"""
    print("🔍 Checking dependencies...")
    
    try:
        import PyQt6
        print("✅ PyQt6 tersedia")
    except ImportError:
        print("❌ PyQt6 tidak tersedia. Install dengan: pip install PyQt6")
        return False
    
    try:
        import requests
        print("✅ requests tersedia")
    except ImportError:
        print("❌ requests tidak tersedia. Install dengan: pip install requests")
        return False
    
    return True

def show_config():
    """Tampilkan konfigurasi default"""
    print("\n📋 Konfigurasi Default:")
    
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        print(f"  • AI Enabled: {config.get('ai_enabled', False)}")
        print(f"  • API Key: {'✅ Tersedia' if config.get('gemini_api_key') else '❌ Tidak tersedia'}")
        print(f"  • Blocked Commands: {len(config.get('blocked_commands', []))} commands")
        print(f"  • APT Commands: {len(config.get('apt_commands', {}))} stacks")
        
    except FileNotFoundError:
        print("  ❌ File config.json tidak ditemukan")
    except json.JSONDecodeError:
        print("  ❌ Error parsing config.json")

def show_features():
    """Tampilkan fitur-fitur aplikasi"""
    print("\n🎯 Fitur-fitur RijanOS Assistant:")
    
    features = [
        ("🤖 AI Assistant", "Chat dengan AI menggunakan Gemini API"),
        ("📦 Package Manager", "Instalasi stack aplikasi dengan satu klik"),
        ("🎬 Multimedia Apps", "Audio, video, graphics, streaming, 3D modeling"),
        ("💾 Backup & Restore", "Backup/restore sistem dengan multiple format"),
        ("🔧 System Maintenance", "Pembersihan cache dan maintenance sistem"),
        ("⚡ Power Management", "Shutdown, restart, dan scheduled shutdown"),
        ("🔔 System Tray", "Aplikasi berjalan di system tray dengan quick actions"),
        ("⚙️ Settings", "Konfigurasi AI, keamanan, dan apt commands"),
        ("🐛 Bug Report", "Laporkan bug langsung ke GitHub")
    ]
    
    for feature, description in features:
        print(f"  {feature}: {description}")

def show_usage():
    """Tampilkan cara penggunaan"""
    print("\n📖 Cara Penggunaan:")
    
    usage_steps = [
        "1. Jalankan aplikasi: python3 main.py",
        "2. Buka tab Settings untuk konfigurasi AI (opsional)",
        "3. Gunakan tab Dashboard untuk aksi cepat",
        "4. Gunakan tab Applications untuk instalasi software",
        "5. Gunakan tab Multimedia untuk aplikasi multimedia",
        "6. Gunakan tab Maintenance untuk pembersihan sistem",
        "7. Gunakan tab Power untuk kontrol power sistem",
        "8. Gunakan tab Backup & Restore untuk backup/restore",
        "9. Gunakan tab AI Assistant untuk chat dengan AI",
        "10. Aplikasi berjalan di system tray saat ditutup"
    ]
    
    for step in usage_steps:
        print(f"  {step}")

def show_security():
    """Tampilkan informasi keamanan"""
    print("\n🔒 Informasi Keamanan:")
    
    security_info = [
        "• Semua command dieksekusi melalui command_executor.py",
        "• Validasi command berbahaya sebelum eksekusi",
        "• Daftar blocked commands yang dapat dikustomisasi",
        "• Tidak ada eksekusi command otomatis tanpa konfirmasi",
        "• Command berbahaya seperti 'rm -rf /' diblokir secara default"
    ]
    
    for info in security_info:
        print(f"  {info}")

def main():
    """Fungsi utama demo"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies tidak lengkap. Install terlebih dahulu:")
        print("   pip install -r requirements.txt")
        return
    
    # Show configuration
    show_config()
    
    # Show features
    show_features()
    
    # Show usage
    show_usage()
    
    # Show security
    show_security()
    
    print("\n🚀 Siap untuk menjalankan RijanOS Assistant!")
    print("   Jalankan: python3 main.py")
    print("   Atau gunakan: ./run.sh (Linux/Mac) atau run.bat (Windows)")

if __name__ == "__main__":
    main()
