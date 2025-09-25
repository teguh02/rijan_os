"""
System Tray untuk RijanOS Assistant
Menangani system tray icon dan menu
"""

import sys
import os
from PyQt6.QtWidgets import (
    QSystemTrayIcon, QMenu, QMessageBox, QInputDialog, QWidget, QApplication
)
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QPixmap, QAction

# Import core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.command_executor import CommandExecutor
from core.system_tools import SystemTools

class SystemTray(QSystemTrayIcon):
    """System Tray Icon untuk RijanOS Assistant"""
    
    # Signals
    show_main_window = pyqtSignal()
    quit_application = pyqtSignal()
    
    def __init__(self, config_path="config.json"):
        super().__init__()
        self.config_path = config_path
        self.command_executor = CommandExecutor(config_path)
        self.system_tools = SystemTools(config_path)
        
        self.init_ui()
        self.setup_menu()
        self.setup_connections()
    
    def init_ui(self):
        """Inisialisasi UI system tray"""
        # Set icon (gunakan icon default jika logo.png tidak ada)
        try:
            # Try different possible paths for logo.png
            possible_paths = [
                "assets/logo.png",
                os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png"),
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png"),
                "/opt/rijanos-assistant/assets/logo.png"
            ]
            
            icon_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    icon_path = path
                    break
            
            if icon_path:
                self.setIcon(QIcon(icon_path))
                print(f"✅ System tray icon set from: {icon_path}")
            else:
                print("⚠️ Warning: logo.png not found for system tray, using default icon")
                # Gunakan icon default PyQt6
                app = QApplication.instance()
                if app:
                    self.setIcon(app.style().standardIcon(app.style().StandardPixmap.SP_ComputerIcon))
                else:
                    # Fallback ke icon kosong jika tidak ada QApplication
                    self.setIcon(QIcon())
        except Exception as e:
            print(f"Warning: Could not set system tray icon: {e}")
            # Fallback ke icon kosong
            self.setIcon(QIcon())
        
        # Set tooltip
        self.setToolTip("RijanOS Assistant")
        
        # Show tray icon
        self.show()
    
    def setup_menu(self):
        """Setup context menu untuk system tray"""
        self.menu = QMenu()
        
        # Open Main Window
        self.show_action = QAction("🏠 Buka Window Utama", self)
        self.show_action.triggered.connect(self.show_main_window.emit)
        self.menu.addAction(self.show_action)
        
        self.menu.addSeparator()
        
        # Quick Actions
        self.update_action = QAction("🔄 Update Sistem", self)
        self.update_action.triggered.connect(self.update_system)
        self.menu.addAction(self.update_action)
        
        self.clean_action = QAction("🧹 Bersihkan Cache", self)
        self.clean_action.triggered.connect(self.clean_system)
        self.menu.addAction(self.clean_action)
        
        self.menu.addSeparator()
        
        # Power Options submenu
        self.power_menu = QMenu("⚡ Power Options")
        
        self.shutdown_action = QAction("🔴 Shutdown Now", self)
        self.shutdown_action.triggered.connect(self.shutdown_system)
        self.power_menu.addAction(self.shutdown_action)
        
        self.restart_action = QAction("🔄 Restart Now", self)
        self.restart_action.triggered.connect(self.restart_system)
        self.power_menu.addAction(self.restart_action)
        
        self.schedule_shutdown_action = QAction("⏰ Schedule Shutdown", self)
        self.schedule_shutdown_action.triggered.connect(self.schedule_shutdown)
        self.power_menu.addAction(self.schedule_shutdown_action)
        
        self.cancel_shutdown_action = QAction("❌ Cancel Shutdown", self)
        self.cancel_shutdown_action.triggered.connect(self.cancel_shutdown)
        self.power_menu.addAction(self.cancel_shutdown_action)
        
        self.menu.addMenu(self.power_menu)
        
        self.menu.addSeparator()
        
        # Quit
        self.quit_action = QAction("🚪 Keluar", self)
        self.quit_action.triggered.connect(self.quit_application.emit)
        self.menu.addAction(self.quit_action)
        
        # Set context menu
        self.setContextMenu(self.menu)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Double click untuk buka main window
        self.activated.connect(self.on_tray_activated)
        
        # Right click untuk context menu (sudah diatur di setup_menu)
        # Left click untuk buka main window
        # Middle click untuk quick actions
    
    def on_tray_activated(self, reason):
        """Handler ketika tray icon diaktifkan"""
        # Handle different click types using numeric values
        if reason == 2:  # DoubleClick
            # Double click - buka main window
            self.show_main_window.emit()
        elif reason == 1:  # Trigger (single left click)
            # Single left click - buka main window
            self.show_main_window.emit()
        elif reason == 3:  # MiddleClick
            # Middle click - show quick actions menu
            self.show_quick_actions_menu()
    
    def show_quick_actions_menu(self):
        """Tampilkan quick actions menu"""
        # Create quick actions menu
        quick_menu = QMenu()
        
        # Quick actions
        quick_update = QAction("🔄 Quick Update", self)
        quick_update.triggered.connect(self.quick_update)
        quick_menu.addAction(quick_update)
        
        quick_clean = QAction("🧹 Quick Clean", self)
        quick_clean.triggered.connect(self.quick_clean)
        quick_menu.addAction(quick_clean)
        
        quick_menu.addSeparator()
        
        # System info
        system_info = QAction("📊 System Info", self)
        system_info.triggered.connect(self.show_system_info)
        quick_menu.addAction(system_info)
        
        # Show menu at cursor position
        quick_menu.exec()
    
    def quick_update(self):
        """Quick update sistem"""
        self.showMessage(
            "RijanOS Assistant",
            "Memulai update sistem...",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
        self.update_system()
    
    def quick_clean(self):
        """Quick clean sistem"""
        self.showMessage(
            "RijanOS Assistant",
            "Memulai pembersihan sistem...",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
        self.clean_system()
    
    def show_system_info(self):
        """Tampilkan informasi sistem"""
        info = self.system_tools.get_system_info()
        
        info_text = "📊 System Information:\n\n"
        for key, value in info.items():
            info_text += f"{key.upper()}: {value}\n"
        
        QMessageBox.information(None, "System Information", info_text)
    
    def update_system(self):
        """Update sistem dari tray"""
        reply = QMessageBox.question(
            None, "Update Sistem",
            "Apakah Anda yakin ingin update sistem?\n\nIni akan menjalankan: sudo apt update && sudo apt upgrade -y",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, stdout, stderr = self.system_tools.upgrade_system()
            
            if success:
                self.showMessage(
                    "RijanOS Assistant",
                    "Update sistem berhasil!",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000
                )
            else:
                self.showMessage(
                    "RijanOS Assistant",
                    f"Error update sistem: {stderr}",
                    QSystemTrayIcon.MessageIcon.Critical,
                    5000
                )
    
    def clean_system(self):
        """Bersihkan sistem dari tray"""
        reply = QMessageBox.question(
            None, "Bersihkan Sistem",
            "Apakah Anda yakin ingin membersihkan cache sistem?\n\nIni akan menjalankan: sudo apt clean && sudo apt autoremove -y",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clean APT cache
            success1, stdout1, stderr1 = self.system_tools.clear_apt_cache()
            
            # Autoremove packages
            success2, stdout2, stderr2 = self.system_tools.autoremove_packages()
            
            if success1 and success2:
                self.showMessage(
                    "RijanOS Assistant",
                    "Pembersihan sistem berhasil!",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000
                )
            else:
                self.showMessage(
                    "RijanOS Assistant",
                    f"Error pembersihan sistem: {stderr1 or stderr2}",
                    QSystemTrayIcon.MessageIcon.Critical,
                    5000
                )
    
    def shutdown_system(self):
        """Shutdown sistem"""
        reply = QMessageBox.question(
            None, "Shutdown Sistem",
            "⚠️ PERINGATAN! ⚠️\n\nApakah Anda yakin ingin shutdown sistem sekarang?\n\nSemua aplikasi yang berjalan akan ditutup dan sistem akan mati.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, stdout, stderr = self.system_tools.shutdown_system()
            
            if not success:
                self.showMessage(
                    "RijanOS Assistant",
                    f"Error shutdown: {stderr}",
                    QSystemTrayIcon.MessageIcon.Critical,
                    5000
                )
    
    def restart_system(self):
        """Restart sistem"""
        reply = QMessageBox.question(
            None, "Restart Sistem",
            "⚠️ PERINGATAN! ⚠️\n\nApakah Anda yakin ingin restart sistem sekarang?\n\nSemua aplikasi yang berjalan akan ditutup dan sistem akan restart.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, stdout, stderr = self.system_tools.restart_system()
            
            if not success:
                self.showMessage(
                    "RijanOS Assistant",
                    f"Error restart: {stderr}",
                    QSystemTrayIcon.MessageIcon.Critical,
                    5000
                )
    
    def schedule_shutdown(self):
        """Jadwalkan shutdown"""
        # Input dialog untuk waktu shutdown
        time_input, ok = QInputDialog.getText(
            None, "Schedule Shutdown",
            "Masukkan waktu shutdown:\n\n"
            "Format:\n"
            "• +30 (30 menit dari sekarang)\n"
            "• 23:00 (jam 23:00)\n"
            "• +2h (2 jam dari sekarang)\n\n"
            "Waktu:"
        )
        
        if ok and time_input.strip():
            time_str = time_input.strip()
            
            # Validasi format waktu
            if not self.validate_time_format(time_str):
                QMessageBox.warning(
                    None, "Format Waktu Salah",
                    "Format waktu tidak valid!\n\n"
                    "Gunakan format:\n"
                    "• +30 (30 menit)\n"
                    "• 23:00 (jam:menit)\n"
                    "• +2h (2 jam)"
                )
                return
            
            # Konfirmasi
            reply = QMessageBox.question(
                None, "Konfirmasi Schedule Shutdown",
                f"Apakah Anda yakin ingin menjadwalkan shutdown pada {time_str}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                command = f"sudo shutdown {time_str}"
                success, stdout, stderr = self.command_executor.execute_safe_command(command)
                
                if success:
                    self.showMessage(
                        "RijanOS Assistant",
                        f"Shutdown dijadwalkan pada {time_str}",
                        QSystemTrayIcon.MessageIcon.Information,
                        3000
                    )
                else:
                    self.showMessage(
                        "RijanOS Assistant",
                        f"Error menjadwalkan shutdown: {stderr}",
                        QSystemTrayIcon.MessageIcon.Critical,
                        5000
                    )
    
    def cancel_shutdown(self):
        """Batalkan shutdown yang dijadwalkan"""
        reply = QMessageBox.question(
            None, "Cancel Shutdown",
            "Apakah Anda yakin ingin membatalkan shutdown yang dijadwalkan?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, stdout, stderr = self.command_executor.execute_safe_command("sudo shutdown -c")
            
            if success:
                self.showMessage(
                    "RijanOS Assistant",
                    "Shutdown yang dijadwalkan dibatalkan",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000
                )
            else:
                self.showMessage(
                    "RijanOS Assistant",
                    f"Error membatalkan shutdown: {stderr}",
                    QSystemTrayIcon.MessageIcon.Critical,
                    5000
                )
    
    def validate_time_format(self, time_str):
        """Validasi format waktu"""
        time_str = time_str.strip()
        
        # Format +minutes (e.g., +30, +60)
        if time_str.startswith('+') and time_str[1:].isdigit():
            return True
        
        # Format +hours (e.g., +1h, +2h)
        if time_str.startswith('+') and time_str.endswith('h') and time_str[1:-1].isdigit():
            return True
        
        # Format HH:MM (e.g., 23:00, 14:30)
        if ':' in time_str:
            try:
                parts = time_str.split(':')
                if len(parts) == 2:
                    hour, minute = int(parts[0]), int(parts[1])
                    if 0 <= hour <= 23 and 0 <= minute <= 59:
                        return True
            except ValueError:
                pass
        
        return False
