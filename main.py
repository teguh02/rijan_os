#!/usr/bin/env python3
"""
RijanOS Assistant - System Assistant untuk Rijan OS
Entry point aplikasi GUI
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Tambahkan path proyek ke sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    app = QApplication(sys.argv)
    app.setApplicationName("RijanOS Assistant")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Rijan OS")
    
    # Set style untuk tampilan modern
    app.setStyle('Fusion')
    
    # Buat dan tampilkan window utama
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
