"""
Main Window untuk RijanOS Assistant
Window utama aplikasi dengan tab navigation
"""

import sys
import os
import json
import glob
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QGridLayout, QGroupBox,
    QMessageBox, QFileDialog, QProgressBar, QSplitter, QSystemTrayIcon,
    QLineEdit
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap

# Import core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.command_executor import CommandExecutor
from core.package_manager import PackageManager
from core.backup_restore import BackupRestore
from core.system_tools import SystemTools
from gui.settings_window import SettingsWindow
from gui.ai_chat_window import AIChatWindow
from gui.system_tray import SystemTray

class CommandThread(QThread):
    """Thread untuk menjalankan command tanpa memblokir GUI"""
    output_ready = pyqtSignal(str)
    error_ready = pyqtSignal(str)
    finished = pyqtSignal(bool, str, str)
    
    def __init__(self, command_executor, command):
        super().__init__()
        self.command_executor = command_executor
        self.command = command
    
    def run(self):
        """Menjalankan command"""
        success, stdout, stderr = self.command_executor.execute_safe_command(self.command)
        
        if stdout:
            self.output_ready.emit(stdout)
        if stderr:
            self.error_ready.emit(stderr)
        
        self.finished.emit(success, stdout, stderr)

class MainWindow(QMainWindow):
    """Window utama RijanOS Assistant"""
    
    def __init__(self):
        super().__init__()
        self.config_path = "config.json"
        self.config = self._load_config()
        
        # Inisialisasi core modules
        self.command_executor = CommandExecutor(self.config_path)
        self.package_manager = PackageManager(self.config_path)
        self.backup_restore = BackupRestore(self.config_path)
        self.system_tools = SystemTools(self.config_path)
        
        # Thread untuk command execution
        self.command_thread = None
        
        # System tray
        self.system_tray = None
        
        self.init_ui()
        self.setup_connections()
        self.setup_system_tray()
    
    def _load_config(self):
        """Memuat konfigurasi"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"ai_enabled": False}
        except json.JSONDecodeError:
            return {"ai_enabled": False}
    
    def init_ui(self):
        """Inisialisasi UI"""
        self.setWindowTitle("RijanOS Assistant v1.0")
        self.setGeometry(100, 100, 1000, 700)
        
        # Set application icon
        self.set_application_icon()
        
        # Set style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_applications_tab()
        self.create_maintenance_tab()
        self.create_backup_tab()
        self.create_power_tab()
        self.create_repository_tab()
        
        # Add AI Chat tab (always visible)
        self.create_ai_chat_tab()
        
        self.create_settings_tab()
        
        # Output area
        self.create_output_area(main_layout)
    
    def create_dashboard_tab(self):
        """Membuat tab Dashboard"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        
        # Welcome message
        welcome_label = QLabel("Selamat Datang di RijanOS Assistant")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; margin: 10px;")
        layout.addWidget(welcome_label)
        
        # Quick actions
        quick_actions_group = QGroupBox("Aksi Cepat")
        quick_actions_layout = QGridLayout(quick_actions_group)
        
        # Update button
        self.update_btn = QPushButton("🔄 Update Sistem")
        self.update_btn.clicked.connect(self.update_system)
        quick_actions_layout.addWidget(self.update_btn, 0, 0)
        
        # Clean button
        self.clean_btn = QPushButton("🧹 Bersihkan Cache")
        self.clean_btn.clicked.connect(self.clean_system)
        quick_actions_layout.addWidget(self.clean_btn, 0, 1)
        
        # Backup button
        self.backup_btn = QPushButton("💾 Backup Cepat")
        self.backup_btn.clicked.connect(self.quick_backup)
        quick_actions_layout.addWidget(self.backup_btn, 1, 0)
        
        # Bug report button
        self.bug_report_btn = QPushButton("🐛 Laporkan Bug")
        self.bug_report_btn.clicked.connect(self.open_bug_report)
        quick_actions_layout.addWidget(self.bug_report_btn, 1, 1)
        
        layout.addWidget(quick_actions_group)
        
        # System info
        self.create_system_info_section(layout)
        
        self.tab_widget.addTab(dashboard_widget, "🏠 Dashboard")
    
    def create_applications_tab(self):
        """Membuat tab Applications"""
        apps_widget = QWidget()
        layout = QVBoxLayout(apps_widget)
        
        # Development stacks
        dev_group = QGroupBox("Development Stacks")
        dev_layout = QVBoxLayout(dev_group)
        
        # Create horizontal layout for buttons
        dev_buttons_layout = QHBoxLayout()
        
        stacks = [
            ("Python Stack", "python_stack", "🐍"),
            ("PHP Stack", "php_stack", "🐘"),
            ("Node.js Stack", "node_stack", "🟢"),
            ("Go Stack", "golang_stack", "🐹")
        ]
        
        for name, key, icon in stacks:
            btn = QPushButton(f"{icon} {name}")
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Arial', 'DejaVu Sans', sans-serif;
                    color: #000000;
                    padding: 10px;
                    margin: 5px;
                    border: 2px solid #007acc;
                    border-radius: 8px;
                    background-color: #f0f8ff;
                }
                QPushButton:hover {
                    background-color: #e6f3ff;
                    border-color: #0056b3;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #cce7ff;
                    color: #000000;
                }
            """)
            btn.clicked.connect(lambda checked, k=key: self.install_stack(k))
            dev_buttons_layout.addWidget(btn)
        
        dev_layout.addLayout(dev_buttons_layout)
        
        layout.addWidget(dev_group)
        
        # Application categories
        app_group = QGroupBox("Aplikasi")
        app_layout = QVBoxLayout(app_group)
        
        # Create horizontal layout for buttons
        app_buttons_layout = QHBoxLayout()
        
        apps = [
            ("Media Tools", "media_tools", "🎬"),
            ("Education Apps", "education_apps", "📚"),
            ("Developer Apps", "developer_apps", "💻"),
            ("System Apps", "system_apps", "⚙️")
        ]
        
        for name, key, icon in apps:
            btn = QPushButton(f"{icon} {name}")
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Arial', 'DejaVu Sans', sans-serif;
                    color: #000000;
                    padding: 10px;
                    margin: 5px;
                    border: 2px solid #28a745;
                    border-radius: 8px;
                    background-color: #f0fff4;
                }
                QPushButton:hover {
                    background-color: #e6ffe6;
                    border-color: #1e7e34;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #ccffcc;
                    color: #000000;
                }
            """)
            btn.clicked.connect(lambda checked, k=key: self.install_stack(k))
            app_buttons_layout.addWidget(btn)
        
        app_layout.addLayout(app_buttons_layout)
        
        layout.addWidget(app_group)
        
        # Multimedia apps
        multimedia_group = QGroupBox("Multimedia Applications")
        multimedia_layout = QVBoxLayout(multimedia_group)
        
        # Create horizontal layout for buttons
        multimedia_buttons_layout = QHBoxLayout()
        
        # Multimedia apps buttons
        multimedia_apps = [
            ("🎵 Audio Tools", "audacity"),
            ("🎬 Video Players", "vlc"),
            ("🎨 Graphics", "gimp"),
            ("📹 Streaming", "obs-studio"),
            ("✂️ Video Editor", "kdenlive"),
            ("🎭 3D Modeling", "blender")
        ]
        
        for name, app in multimedia_apps:
            btn = QPushButton(name)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Arial', 'DejaVu Sans', sans-serif;
                    color: #000000;
                    padding: 10px;
                    margin: 5px;
                    border: 2px solid #ff6b35;
                    border-radius: 8px;
                    background-color: #fff5f0;
                }
                QPushButton:hover {
                    background-color: #ffe6d9;
                    border-color: #e55a2b;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #ffd9cc;
                    color: #000000;
                }
            """)
            btn.clicked.connect(lambda checked, a=app: self.install_single_package(a))
            multimedia_buttons_layout.addWidget(btn)
        
        multimedia_layout.addLayout(multimedia_buttons_layout)
        
        layout.addWidget(multimedia_group)
        
        # Security apps
        security_group = QGroupBox("Security Applications")
        security_layout = QVBoxLayout(security_group)
        
        # Create horizontal layout for buttons
        security_buttons_layout = QHBoxLayout()
        
        # Security apps buttons
        security_apps = [
            ("🛡️ Antivirus", "clamav"),
            ("🔥 Firewall", "ufw"),
            ("🚫 Intrusion Detection", "fail2ban"),
            ("🔍 Rootkit Scanner", "rkhunter"),
            ("🔐 Rootkit Checker", "chkrootkit"),
            ("📊 Security Audit", "lynis")
        ]
        
        for name, app in security_apps:
            btn = QPushButton(name)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Arial', 'DejaVu Sans', sans-serif;
                    color: #000000;
                    padding: 10px;
                    margin: 5px;
                    border: 2px solid #dc3545;
                    border-radius: 8px;
                    background-color: #fff5f5;
                }
                QPushButton:hover {
                    background-color: #ffe6e6;
                    border-color: #c82333;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #ffcccc;
                    color: #000000;
                }
            """)
            btn.clicked.connect(lambda checked, a=app: self.install_single_package(a))
            security_buttons_layout.addWidget(btn)
        
        security_layout.addLayout(security_buttons_layout)
        
        layout.addWidget(security_group)
        
        # Security configuration
        security_config_group = QGroupBox("Security Configuration")
        security_config_layout = QVBoxLayout(security_config_group)
        
        # Create horizontal layout for buttons
        security_config_buttons_layout = QHBoxLayout()
        
        security_config_buttons = [
            ("🛡️ Configure ClamAV", self.configure_clamav),
            ("🔥 Configure UFW", self.configure_ufw),
            ("🚫 Configure Fail2ban", self.configure_fail2ban),
            ("🔍 Update ClamAV Database", self.update_clamav_db)
        ]
        
        for name, func in security_config_buttons:
            btn = QPushButton(name)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Arial', 'DejaVu Sans', sans-serif;
                    color: #000000;
                    padding: 10px;
                    margin: 5px;
                    border: 2px solid #6f42c1;
                    border-radius: 8px;
                    background-color: #f8f5ff;
                }
                QPushButton:hover {
                    background-color: #f0e6ff;
                    border-color: #5a32a3;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #e6d9ff;
                    color: #000000;
                }
            """)
            btn.clicked.connect(func)
            security_config_buttons_layout.addWidget(btn)
        
        security_config_layout.addLayout(security_config_buttons_layout)
        
        layout.addWidget(security_config_group)
        
        # System maintenance
        maint_group = QGroupBox("Maintenance Sistem")
        maint_layout = QVBoxLayout(maint_group)
        
        # Create horizontal layout for buttons
        maint_buttons_layout = QHBoxLayout()
        
        maint_buttons = [
            ("Update", self.update_packages),
            ("Full Update", self.upgrade_packages),
            ("Release Upgrade", self.upgrade_release)
        ]
        
        for name, func in maint_buttons:
            btn = QPushButton(name)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Arial', 'DejaVu Sans', sans-serif;
                    color: #000000;
                    padding: 10px;
                    margin: 5px;
                    border: 2px solid #17a2b8;
                    border-radius: 8px;
                    background-color: #f0f9ff;
                }
                QPushButton:hover {
                    background-color: #e6f7ff;
                    border-color: #138496;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #ccf2ff;
                    color: #000000;
                }
            """)
            btn.clicked.connect(func)
            maint_buttons_layout.addWidget(btn)
        
        maint_layout.addLayout(maint_buttons_layout)
        
        layout.addWidget(maint_group)
        
        self.tab_widget.addTab(apps_widget, "📦 Applications")
    
    def create_maintenance_tab(self):
        """Membuat tab Maintenance"""
        maint_widget = QWidget()
        layout = QVBoxLayout(maint_widget)
        
        # Cache cleaning
        cache_group = QGroupBox("Pembersihan Cache")
        cache_layout = QGridLayout(cache_group)
        
        cache_buttons = [
            ("Clear APT Cache", self.clear_apt_cache),
            ("Clear Journal Logs", self.clear_journal_logs),
            ("Clear Temp Files", self.clear_temp_files),
            ("Autoremove Packages", self.autoremove_packages)
        ]
        
        for i, (name, func) in enumerate(cache_buttons):
            btn = QPushButton(name)
            btn.clicked.connect(func)
            cache_layout.addWidget(btn, i // 2, i % 2)
        
        layout.addWidget(cache_group)
        
        # System info
        info_group = QGroupBox("Informasi Sistem")
        info_layout = QVBoxLayout(info_group)
        
        info_buttons = [
            ("Disk Usage", self.show_disk_usage),
            ("Memory Usage", self.show_memory_usage),
            ("System Info", self.show_system_info),
            ("Running Processes", self.show_processes)
        ]
        
        for name, func in info_buttons:
            btn = QPushButton(name)
            btn.clicked.connect(func)
            info_layout.addWidget(btn)
        
        layout.addWidget(info_group)
        
        self.tab_widget.addTab(maint_widget, "🔧 Maintenance")
    
    def create_backup_tab(self):
        """Membuat tab Backup & Restore"""
        backup_widget = QWidget()
        layout = QVBoxLayout(backup_widget)
        
        # Backup section
        backup_group = QGroupBox("Backup")
        backup_layout = QVBoxLayout(backup_group)
        
        # Source selection
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Source:"))
        self.source_path_edit = QTextEdit()
        self.source_path_edit.setMaximumHeight(60)
        self.source_path_edit.setPlaceholderText("Pilih folder atau file yang akan di-backup...")
        source_layout.addWidget(self.source_path_edit)
        
        self.browse_source_btn = QPushButton("Browse")
        self.browse_source_btn.clicked.connect(self.browse_source)
        source_layout.addWidget(self.browse_source_btn)
        
        backup_layout.addLayout(source_layout)
        
        # Output selection
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output:"))
        self.output_path_edit = QTextEdit()
        self.output_path_edit.setMaximumHeight(60)
        self.output_path_edit.setPlaceholderText("Pilih lokasi dan nama file backup...")
        output_layout.addWidget(self.output_path_edit)
        
        self.browse_output_btn = QPushButton("Browse")
        self.browse_output_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.browse_output_btn)
        
        backup_layout.addLayout(output_layout)
        
        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        
        self.format_combo = QPushButton("tar.gz")
        self.format_combo.clicked.connect(self.cycle_format)
        format_layout.addWidget(self.format_combo)
        
        format_layout.addStretch()
        
        backup_layout.addLayout(format_layout)
        
        # Backup button
        self.create_backup_btn = QPushButton("💾 Buat Backup")
        self.create_backup_btn.clicked.connect(self.create_backup)
        backup_layout.addWidget(self.create_backup_btn)
        
        layout.addWidget(backup_group)
        
        # Restore section
        restore_group = QGroupBox("Restore")
        restore_layout = QVBoxLayout(restore_group)
        
        # Restore file selection
        restore_file_layout = QHBoxLayout()
        restore_file_layout.addWidget(QLabel("Backup File:"))
        self.restore_file_edit = QTextEdit()
        self.restore_file_edit.setMaximumHeight(60)
        self.restore_file_edit.setPlaceholderText("Pilih file backup yang akan di-restore...")
        restore_file_layout.addWidget(self.restore_file_edit)
        
        self.browse_restore_btn = QPushButton("Browse")
        self.browse_restore_btn.clicked.connect(self.browse_restore_file)
        restore_file_layout.addWidget(self.browse_restore_btn)
        
        restore_layout.addLayout(restore_file_layout)
        
        # Restore target
        restore_target_layout = QHBoxLayout()
        restore_target_layout.addWidget(QLabel("Target:"))
        self.restore_target_edit = QTextEdit()
        self.restore_target_edit.setMaximumHeight(60)
        self.restore_target_edit.setPlaceholderText("Pilih lokasi restore...")
        restore_target_layout.addWidget(self.restore_target_edit)
        
        self.browse_restore_target_btn = QPushButton("Browse")
        self.browse_restore_target_btn.clicked.connect(self.browse_restore_target)
        restore_target_layout.addWidget(self.browse_restore_target_btn)
        
        restore_layout.addLayout(restore_target_layout)
        
        # Restore button
        self.restore_btn = QPushButton("📥 Restore")
        self.restore_btn.clicked.connect(self.restore_backup)
        restore_layout.addWidget(self.restore_btn)
        
        layout.addWidget(restore_group)
        
        self.tab_widget.addTab(backup_widget, "💾 Backup & Restore")
    
    def create_power_tab(self):
        """Membuat tab Power Management"""
        power_widget = QWidget()
        layout = QVBoxLayout(power_widget)
        
        # Immediate Power Actions
        immediate_group = QGroupBox("Immediate Power Actions")
        immediate_layout = QGridLayout(immediate_group)
        
        # Shutdown button
        self.shutdown_btn = QPushButton("🔴 Shutdown Now")
        self.shutdown_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.shutdown_btn.clicked.connect(self.shutdown_system)
        immediate_layout.addWidget(self.shutdown_btn, 0, 0)
        
        # Restart button
        self.restart_btn = QPushButton("🔄 Restart Now")
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e55a00;
            }
        """)
        self.restart_btn.clicked.connect(self.restart_system)
        immediate_layout.addWidget(self.restart_btn, 0, 1)
        
        layout.addWidget(immediate_group)
        
        # Scheduled Shutdown
        schedule_group = QGroupBox("Schedule Shutdown")
        schedule_layout = QVBoxLayout(schedule_group)
        
        # Time input
        time_input_layout = QHBoxLayout()
        time_input_layout.addWidget(QLabel("Waktu Shutdown:"))
        
        self.shutdown_time_edit = QLineEdit()
        self.shutdown_time_edit.setPlaceholderText("Contoh: +30, 23:00, +2h")
        time_input_layout.addWidget(self.shutdown_time_edit)
        
        self.schedule_shutdown_btn = QPushButton("⏰ Schedule")
        self.schedule_shutdown_btn.clicked.connect(self.schedule_shutdown)
        time_input_layout.addWidget(self.schedule_shutdown_btn)
        
        schedule_layout.addLayout(time_input_layout)
        
        # Cancel shutdown button
        self.cancel_shutdown_btn = QPushButton("❌ Cancel Scheduled Shutdown")
        self.cancel_shutdown_btn.clicked.connect(self.cancel_shutdown)
        schedule_layout.addWidget(self.cancel_shutdown_btn)
        
        layout.addWidget(schedule_group)
        
        # Power info
        power_info = QLabel("""
        <b>⚠️ PERINGATAN KEAMANAN ⚠️</b><br>
        • Shutdown dan Restart akan mematikan sistem<br>
        • Pastikan semua pekerjaan sudah disimpan<br>
        • Gunakan dengan hati-hati!<br><br>
        <b>Format Waktu:</b><br>
        • +30 (30 menit dari sekarang)<br>
        • 23:00 (jam 23:00)<br>
        • +2h (2 jam dari sekarang)
        """)
        power_info.setStyleSheet("""
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 10px;
            border-radius: 5px;
            color: #856404;
        """)
        layout.addWidget(power_info)
        
        layout.addStretch()
        
        self.tab_widget.addTab(power_widget, "⚡ Power")
    
    def create_repository_tab(self):
        """Membuat tab Repository Management"""
        repo_widget = QWidget()
        layout = QVBoxLayout(repo_widget)
        
        # Repository Selection
        repo_group = QGroupBox("Pilih Repository Server")
        repo_layout = QVBoxLayout(repo_group)
        
        # Repository info
        repo_info = QLabel("""
        <b>Repository Management</b><br>
        Pilih server repository yang akan digunakan untuk menginstall paket dan update sistem.<br>
        Server repository Indonesia biasanya lebih cepat dan stabil untuk pengguna di Indonesia.
        """)
        repo_info.setWordWrap(True)
        repo_info.setStyleSheet("color: #666; margin-bottom: 10px;")
        repo_layout.addWidget(repo_info)
        
        # Repository buttons
        repo_buttons_layout = QGridLayout()
        
        # Default Ubuntu Repository
        self.default_repo_btn = QPushButton("🌍 Default Ubuntu\n(id.archive.ubuntu.com)")
        self.default_repo_btn.setMinimumHeight(60)
        self.default_repo_btn.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                font-family: 'Arial', 'DejaVu Sans', sans-serif;
                color: #000000;
                padding: 10px;
                margin: 5px;
                border: 2px solid #007acc;
                border-radius: 8px;
                background-color: #f0f8ff;
            }
            QPushButton:hover {
                background-color: #e6f3ff;
                border-color: #0056b3;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #cce7ff;
                color: #000000;
            }
        """)
        self.default_repo_btn.clicked.connect(lambda: self.change_repository("default"))
        repo_buttons_layout.addWidget(self.default_repo_btn, 0, 0)
        
        # Cloudeka Repository
        self.cloudeka_repo_btn = QPushButton("🇮🇩 Cloudeka CDN\n(Jakarta, Indonesia)")
        self.cloudeka_repo_btn.setMinimumHeight(60)
        self.cloudeka_repo_btn.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                font-family: 'Arial', 'DejaVu Sans', sans-serif;
                color: #000000;
                padding: 10px;
                margin: 5px;
                border: 2px solid #28a745;
                border-radius: 8px;
                background-color: #f8fff9;
            }
            QPushButton:hover {
                background-color: #e8f5e8;
                border-color: #1e7e34;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #d4edda;
                color: #000000;
            }
        """)
        self.cloudeka_repo_btn.clicked.connect(lambda: self.change_repository("cloudeka"))
        repo_buttons_layout.addWidget(self.cloudeka_repo_btn, 0, 1)
        
        # Domainesia Repository
        self.domainesia_repo_btn = QPushButton("🇮🇩 Domainesia\n(Jakarta, Indonesia)")
        self.domainesia_repo_btn.setMinimumHeight(60)
        self.domainesia_repo_btn.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                font-family: 'Arial', 'DejaVu Sans', sans-serif;
                color: #000000;
                padding: 10px;
                margin: 5px;
                border: 2px solid #17a2b8;
                border-radius: 8px;
                background-color: #f0fdff;
            }
            QPushButton:hover {
                background-color: #e6f9fc;
                border-color: #138496;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #cceff5;
                color: #000000;
            }
        """)
        self.domainesia_repo_btn.clicked.connect(lambda: self.change_repository("domainesia"))
        repo_buttons_layout.addWidget(self.domainesia_repo_btn, 0, 2)
        
        # AMS Cloud Repository
        self.amscloud_repo_btn = QPushButton("🇮🇩 AMS Cloud\n(Jakarta, Indonesia)")
        self.amscloud_repo_btn.setMinimumHeight(60)
        self.amscloud_repo_btn.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                font-family: 'Arial', 'DejaVu Sans', sans-serif;
                color: #000000;
                padding: 10px;
                margin: 5px;
                border: 2px solid #6f42c1;
                border-radius: 8px;
                background-color: #f8f5ff;
            }
            QPushButton:hover {
                background-color: #f0e6ff;
                border-color: #5a32a3;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #e6d9ff;
                color: #000000;
            }
        """)
        self.amscloud_repo_btn.clicked.connect(lambda: self.change_repository("amscloud"))
        repo_buttons_layout.addWidget(self.amscloud_repo_btn, 1, 0)
        
        # Neva Cloud Repository
        self.nevacloud_repo_btn = QPushButton("🇮🇩 Neva Cloud\n(Jakarta, Indonesia)")
        self.nevacloud_repo_btn.setMinimumHeight(60)
        self.nevacloud_repo_btn.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                font-family: 'Arial', 'DejaVu Sans', sans-serif;
                color: #000000;
                padding: 10px;
                margin: 5px;
                border: 2px solid #fd7e14;
                border-radius: 8px;
                background-color: #fff8f0;
            }
            QPushButton:hover {
                background-color: #fff0e6;
                border-color: #e55a00;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #ffe6cc;
                color: #000000;
            }
        """)
        self.nevacloud_repo_btn.clicked.connect(lambda: self.change_repository("nevacloud"))
        repo_buttons_layout.addWidget(self.nevacloud_repo_btn, 1, 1)
        
        # Datautama Repository
        self.datautama_repo_btn = QPushButton("🇮🇩 Datautama\n(Surabaya, Indonesia)")
        self.datautama_repo_btn.setMinimumHeight(60)
        self.datautama_repo_btn.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                font-family: 'Arial', 'DejaVu Sans', sans-serif;
                color: #000000;
                padding: 10px;
                margin: 5px;
                border: 2px solid #dc3545;
                border-radius: 8px;
                background-color: #fff5f5;
            }
            QPushButton:hover {
                background-color: #ffe6e6;
                border-color: #c82333;
                color: #000000;
            }
            QPushButton:pressed {
                background-color: #ffcccc;
                color: #000000;
            }
        """)
        self.datautama_repo_btn.clicked.connect(lambda: self.change_repository("datautama"))
        repo_buttons_layout.addWidget(self.datautama_repo_btn, 1, 2)
        
        repo_layout.addLayout(repo_buttons_layout)
        layout.addWidget(repo_group)
        
        # Repository Management Actions
        management_group = QGroupBox("Repository Management")
        management_layout = QHBoxLayout(management_group)
        
        # Backup current sources
        self.backup_sources_btn = QPushButton("💾 Backup Current Sources")
        self.backup_sources_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                font-weight: bold;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        self.backup_sources_btn.clicked.connect(self.backup_sources)
        management_layout.addWidget(self.backup_sources_btn)
        
        # Restore sources
        self.restore_sources_btn = QPushButton("🔄 Restore Sources")
        self.restore_sources_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        self.restore_sources_btn.clicked.connect(self.restore_sources)
        management_layout.addWidget(self.restore_sources_btn)
        
        # Test connection
        self.test_repo_btn = QPushButton("🧪 Test Repository")
        self.test_repo_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                font-weight: bold;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        self.test_repo_btn.clicked.connect(self.test_repository)
        management_layout.addWidget(self.test_repo_btn)
        
        layout.addWidget(management_group)
        
        # Current Repository Status
        status_group = QGroupBox("Current Repository Status")
        status_layout = QVBoxLayout(status_group)
        
        self.repo_status_label = QLabel("Status repository akan ditampilkan di sini...")
        self.repo_status_label.setWordWrap(True)
        self.repo_status_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        status_layout.addWidget(self.repo_status_label)
        
        layout.addWidget(status_group)
        
        # Load current status
        self.refresh_repo_status()
        
        # Check and display sudo status
        self.check_and_display_sudo_status()
        
        layout.addStretch()
        
        self.tab_widget.addTab(repo_widget, "📦 Repository")
    
    def create_ai_chat_tab(self):
        """Membuat tab Information"""
        info_widget = QWidget()
        layout = QVBoxLayout(info_widget)
        
        # System Information
        system_group = QGroupBox("System Information")
        system_layout = QVBoxLayout(system_group)
        
        self.system_info_text = QTextEdit()
        self.system_info_text.setReadOnly(True)
        self.system_info_text.setMaximumHeight(200)
        self.system_info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        system_layout.addWidget(self.system_info_text)
        
        # Refresh system info button
        refresh_system_btn = QPushButton("🔄 Refresh System Info")
        refresh_system_btn.clicked.connect(self.refresh_system_info)
        system_layout.addWidget(refresh_system_btn)
        
        layout.addWidget(system_group)
        
        # Hardware Information
        hardware_group = QGroupBox("Hardware Information")
        hardware_layout = QVBoxLayout(hardware_group)
        
        self.hardware_info_text = QTextEdit()
        self.hardware_info_text.setReadOnly(True)
        self.hardware_info_text.setMaximumHeight(200)
        self.hardware_info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        hardware_layout.addWidget(self.hardware_info_text)
        
        # Refresh hardware info button
        refresh_hardware_btn = QPushButton("🔄 Refresh Hardware Info")
        refresh_hardware_btn.clicked.connect(self.refresh_hardware_info)
        hardware_layout.addWidget(refresh_hardware_btn)
        
        layout.addWidget(hardware_group)
        
        # Battery Information
        battery_group = QGroupBox("Battery Information")
        battery_layout = QVBoxLayout(battery_group)
        
        self.battery_info_text = QTextEdit()
        self.battery_info_text.setReadOnly(True)
        self.battery_info_text.setMaximumHeight(150)
        self.battery_info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        battery_layout.addWidget(self.battery_info_text)
        
        # Refresh battery info button
        refresh_battery_btn = QPushButton("🔄 Refresh Battery Info")
        refresh_battery_btn.clicked.connect(self.refresh_battery_info)
        battery_layout.addWidget(refresh_battery_btn)
        
        layout.addWidget(battery_group)
        
        # Network Information
        network_group = QGroupBox("Network Information")
        network_layout = QVBoxLayout(network_group)
        
        self.network_info_text = QTextEdit()
        self.network_info_text.setReadOnly(True)
        self.network_info_text.setMaximumHeight(150)
        self.network_info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        network_layout.addWidget(self.network_info_text)
        
        # Refresh network info button
        refresh_network_btn = QPushButton("🔄 Refresh Network Info")
        refresh_network_btn.clicked.connect(self.refresh_network_info)
        network_layout.addWidget(refresh_network_btn)
        
        layout.addWidget(network_group)
        
        # Load initial information
        self.refresh_system_info()
        self.refresh_hardware_info()
        self.refresh_battery_info()
        self.refresh_network_info()
        
        self.tab_widget.addTab(info_widget, "📊 Information")
    
    def configure_clamav(self):
        """Konfigurasi ClamAV antivirus"""
        try:
            # Start ClamAV daemon
            success1, stdout1, stderr1 = self.system_tools.command_executor.execute_safe_command("sudo systemctl start clamav-daemon")
            success2, stdout2, stderr2 = self.system_tools.command_executor.execute_safe_command("sudo systemctl enable clamav-daemon")
            
            if success1 and success2:
                QMessageBox.information(self, "ClamAV Configuration", "ClamAV daemon berhasil dikonfigurasi dan diaktifkan.")
            else:
                QMessageBox.warning(self, "ClamAV Configuration", f"Error konfigurasi ClamAV:\n{stderr1}\n{stderr2}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error konfigurasi ClamAV: {str(e)}")
    
    def configure_ufw(self):
        """Konfigurasi UFW firewall"""
        try:
            # Enable UFW with default deny
            success1, stdout1, stderr1 = self.system_tools.command_executor.execute_safe_command("sudo ufw --force reset")
            success2, stdout2, stderr2 = self.system_tools.command_executor.execute_safe_command("sudo ufw default deny incoming")
            success3, stdout3, stderr3 = self.system_tools.command_executor.execute_safe_command("sudo ufw default allow outgoing")
            success4, stdout4, stderr4 = self.system_tools.command_executor.execute_safe_command("sudo ufw allow ssh")
            success5, stdout5, stderr5 = self.system_tools.command_executor.execute_safe_command("sudo ufw --force enable")
            
            if all([success1, success2, success3, success4, success5]):
                QMessageBox.information(self, "UFW Configuration", "UFW firewall berhasil dikonfigurasi dengan:\n- Default deny incoming\n- Default allow outgoing\n- SSH allowed\n- Firewall enabled")
            else:
                QMessageBox.warning(self, "UFW Configuration", "Error konfigurasi UFW. Periksa output untuk detail.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error konfigurasi UFW: {str(e)}")
    
    def configure_fail2ban(self):
        """Konfigurasi Fail2ban intrusion detection"""
        try:
            # Start and enable fail2ban
            success1, stdout1, stderr1 = self.system_tools.command_executor.execute_safe_command("sudo systemctl start fail2ban")
            success2, stdout2, stderr2 = self.system_tools.command_executor.execute_safe_command("sudo systemctl enable fail2ban")
            
            if success1 and success2:
                QMessageBox.information(self, "Fail2ban Configuration", "Fail2ban berhasil dikonfigurasi dan diaktifkan.")
            else:
                QMessageBox.warning(self, "Fail2ban Configuration", f"Error konfigurasi Fail2ban:\n{stderr1}\n{stderr2}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error konfigurasi Fail2ban: {str(e)}")
    
    def update_clamav_db(self):
        """Update ClamAV database"""
        try:
            success, stdout, stderr = self.system_tools.command_executor.execute_safe_command("sudo freshclam")
            
            if success:
                QMessageBox.information(self, "ClamAV Database Update", "ClamAV database berhasil diupdate.")
            else:
                QMessageBox.warning(self, "ClamAV Database Update", f"Error update database:\n{stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error update ClamAV database: {str(e)}")
    
    def refresh_system_info(self):
        """Refresh system information"""
        try:
            # Get system information
            success, stdout, stderr = self.system_tools.get_system_info()
            
            if success:
                info_text = stdout
            else:
                info_text = f"Error getting system info: {stderr}"
            
            self.system_info_text.setPlainText(info_text)
        except Exception as e:
            self.system_info_text.setPlainText(f"Error: {str(e)}")
    
    def refresh_hardware_info(self):
        """Refresh hardware information"""
        try:
            # Get hardware information
            success, stdout, stderr = self.system_tools.get_hardware_info()
            
            if success:
                info_text = stdout
            else:
                info_text = f"Error getting hardware info: {stderr}"
            
            self.hardware_info_text.setPlainText(info_text)
        except Exception as e:
            self.hardware_info_text.setPlainText(f"Error: {str(e)}")
    
    def refresh_battery_info(self):
        """Refresh battery information"""
        try:
            # Get battery information
            success, stdout, stderr = self.system_tools.get_battery_info()
            
            if success:
                info_text = stdout
            else:
                info_text = f"Error getting battery info: {stderr}"
            
            self.battery_info_text.setPlainText(info_text)
        except Exception as e:
            self.battery_info_text.setPlainText(f"Error: {str(e)}")
    
    def refresh_network_info(self):
        """Refresh network information"""
        try:
            # Get network information
            success, stdout, stderr = self.system_tools.get_network_info()
            
            if success:
                info_text = stdout
            else:
                info_text = f"Error getting network info: {stderr}"
            
            self.network_info_text.setPlainText(info_text)
        except Exception as e:
            self.network_info_text.setPlainText(f"Error: {str(e)}")
    
    def create_ai_chat_tab(self):
        """Membuat tab AI Chat"""
        self.ai_chat_window = AIChatWindow(self.config_path)
        
        # Check if AI is enabled and API key is set
        ai_enabled = self.config.get("ai_enabled", False)
        api_key = self.config.get("gemini_api_key", "")
        
        if not ai_enabled or not api_key:
            # Create warning widget
            warning_widget = QWidget()
            warning_layout = QVBoxLayout(warning_widget)
            
            # Warning message
            warning_label = QLabel("""
            <div style="text-align: center; padding: 50px;">
                <h2>🤖 AI Assistant</h2>
                <div style="background-color: #fff3cd; border: 2px solid #ffeaa7; padding: 20px; border-radius: 10px; margin: 20px;">
                    <h3 style="color: #856404;">⚠️ AI Assistant Belum Dikonfigurasi</h3>
                    <p style="color: #856404; font-size: 14px;">
                        Untuk menggunakan AI Assistant, Anda perlu:
                    </p>
                    <ul style="text-align: left; color: #856404; font-size: 14px;">
                        <li>✅ Aktifkan AI Assistant di Settings</li>
                        <li>✅ Masukkan Gemini API Key</li>
                        <li>✅ Simpan pengaturan</li>
                    </ul>
                </div>
                <div style="background-color: #d1ecf1; border: 2px solid #bee5eb; padding: 20px; border-radius: 10px; margin: 20px;">
                    <h3 style="color: #0c5460;">📋 Cara Mengaktifkan AI Assistant:</h3>
                    <ol style="text-align: left; color: #0c5460; font-size: 14px;">
                        <li>Buka tab <strong>Settings</strong></li>
                        <li>Aktifkan checkbox <strong>"Aktifkan AI Assistant"</strong></li>
                        <li>Masukkan API key dari: <a href="https://aistudio.google.com/apikey" style="color: #0078d4;">https://aistudio.google.com/apikey</a></li>
                        <li>Klik <strong>"Simpan Pengaturan"</strong></li>
                        <li>Restart aplikasi atau reload tab ini</li>
                    </ol>
                </div>
                <div style="background-color: #f8d7da; border: 2px solid #f5c6cb; padding: 20px; border-radius: 10px; margin: 20px;">
                    <h3 style="color: #721c24;">🔒 Keamanan</h3>
                    <p style="color: #721c24; font-size: 14px;">
                        API key Anda akan disimpan secara lokal dan aman. 
                        Tidak ada data yang dikirim ke server selain Google Gemini.
                    </p>
                </div>
            </div>
            """)
            warning_label.setWordWrap(True)
            warning_layout.addWidget(warning_label)
            
            # Refresh button
            refresh_layout = QHBoxLayout()
            refresh_layout.addStretch()
            
            refresh_btn = QPushButton("🔄 Refresh Status")
            refresh_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
            """)
            refresh_btn.clicked.connect(self.refresh_ai_status)
            refresh_layout.addWidget(refresh_btn)
            
            refresh_layout.addStretch()
            warning_layout.addLayout(refresh_layout)
            
            self.tab_widget.addTab(warning_widget, "🤖 AI Assistant")
        else:
            # AI is enabled and configured
            self.tab_widget.addTab(self.ai_chat_window, "🤖 AI Assistant")
    
    def create_settings_tab(self):
        """Membuat tab Settings"""
        self.settings_window = SettingsWindow(self.config_path)
        self.settings_window.config_updated.connect(self.reload_config)
        self.settings_window.console_visibility_changed.connect(self.toggle_console_from_settings)
        self.tab_widget.addTab(self.settings_window, "⚙️ Settings")
    
    def create_system_info_section(self, layout):
        """Membuat section informasi sistem"""
        info_group = QGroupBox("Informasi Sistem")
        info_layout = QVBoxLayout(info_group)
        
        self.system_info_text = QTextEdit()
        self.system_info_text.setMaximumHeight(150)
        self.system_info_text.setReadOnly(True)
        info_layout.addWidget(self.system_info_text)
        
        refresh_btn = QPushButton("🔄 Refresh Info")
        refresh_btn.clicked.connect(self.refresh_system_info)
        info_layout.addWidget(refresh_btn)
        
        layout.addWidget(info_group)
        
        # Load initial system info
        self.refresh_system_info()
    
    def create_output_area(self, layout):
        """Membuat area output"""
        # Container untuk output area
        self.output_container = QWidget()
        self.output_container.setVisible(True)  # Default visible
        output_layout = QVBoxLayout(self.output_container)
        
        # Splitter untuk output area
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(200)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        splitter.addWidget(self.output_text)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        splitter.addWidget(self.progress_bar)
        
        output_layout.addWidget(splitter)
        layout.addWidget(self.output_container)
    
    def setup_connections(self):
        """Setup signal connections"""
        pass
    
    def toggle_console(self):
        """Toggle console output area visibility"""
        if self.output_container.isVisible():
            # Hide console
            self.output_container.setVisible(False)
            self.toggle_console_btn.setText("📺 Show Console")
            self.toggle_console_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
        else:
            # Show console
            self.output_container.setVisible(True)
            self.toggle_console_btn.setText("📺 Hide Console")
            self.toggle_console_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
            """)
    
    def toggle_console_from_settings(self, visible):
        """Toggle console dari Settings"""
        self.output_container.setVisible(visible)
    
    def setup_system_tray(self):
        """Setup system tray icon"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.system_tray = SystemTray(self.config_path)
            self.system_tray.show_main_window.connect(self.show)
            self.system_tray.quit_application.connect(self.close)
        else:
            print("System tray tidak tersedia di sistem ini")
    
    def closeEvent(self, event):
        """Handler ketika window ditutup"""
        # Cleanup running threads
        if self.command_thread and self.command_thread.isRunning():
            self.command_thread.terminate()
            self.command_thread.wait(3000)  # Wait up to 3 seconds
        
        if self.system_tray and self.system_tray.isVisible():
            # Minimize to tray instead of closing
            self.hide()
            self.system_tray.showMessage(
                "RijanOS Assistant",
                "Aplikasi berjalan di system tray",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
            event.ignore()
        else:
            event.accept()
    
    def reload_config(self):
        """Reload konfigurasi dan update UI"""
        self.config = self._load_config()
        
        # Update AI tab
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "🤖 AI Assistant":
                self.tab_widget.removeTab(i)
                break
        
        # Recreate AI tab with current config
        self.create_ai_chat_tab()
    
    def refresh_ai_status(self):
        """Refresh status AI Assistant"""
        self.reload_config()
        
        # Show message
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self, "Status Diperbarui", 
            "Status AI Assistant telah diperbarui. "
            "Jika Anda sudah mengkonfigurasi AI Assistant di Settings, "
            "tab ini akan menampilkan interface chat."
        )
    
    # Command execution methods
    def execute_command(self, command, show_output=True):
        """Menjalankan command dan menampilkan output"""
        if show_output:
            self.output_text.append(f"$ {command}")
            self.output_text.append("-" * 50)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Cleanup previous thread if exists
        if self.command_thread and self.command_thread.isRunning():
            self.command_thread.terminate()
            self.command_thread.wait()
        
        # Start command thread
        self.command_thread = CommandThread(self.command_executor, command)
        self.command_thread.output_ready.connect(self.append_output)
        self.command_thread.error_ready.connect(self.append_error)
        self.command_thread.finished.connect(self.command_finished)
        self.command_thread.start()
    
    def append_output(self, text):
        """Menambahkan output ke text area"""
        self.output_text.append(text)
        self.output_text.ensureCursorVisible()
    
    def append_error(self, text):
        """Menambahkan error ke text area"""
        self.output_text.append(f"ERROR: {text}")
        self.output_text.ensureCursorVisible()
    
    def command_finished(self, success, stdout, stderr):
        """Handler ketika command selesai"""
        self.progress_bar.setVisible(False)
        
        if not success:
            self.append_error(f"Command gagal dengan exit code: {stderr}")
        else:
            self.append_output("Command berhasil dijalankan.")
    
    # Dashboard methods
    def update_system(self):
        """Update sistem"""
        self.execute_command("sudo apt update")
    
    def clean_system(self):
        """Bersihkan sistem"""
        self.execute_command("sudo apt clean && sudo apt autoremove -y")
    
    def quick_backup(self):
        """Backup cepat home directory"""
        import os
        home_dir = os.path.expanduser("~")
        backup_path = f"{home_dir}/backup_home_{self.get_timestamp()}.tar.gz"
        self.execute_command(f"tar -czf {backup_path} -C {os.path.dirname(home_dir)} {os.path.basename(home_dir)}")
    
    def open_bug_report(self):
        """Buka halaman bug report"""
        self.system_tools.open_bug_report()
        self.append_output("Membuka halaman bug report di browser...")
    
    
    # Application methods
    def install_stack(self, stack_name):
        """Install stack aplikasi"""
        success, stdout, stderr = self.package_manager.install_stack(stack_name)
        
        if success:
            self.append_output(f"Installing {stack_name}...")
            self.append_output(stdout)
        else:
            self.append_error(f"Error installing {stack_name}: {stderr}")
    
    def update_packages(self):
        """Update packages"""
        self.execute_command("sudo apt update")
    
    def upgrade_packages(self):
        """Upgrade packages"""
        self.execute_command("sudo apt update && sudo apt upgrade -y")
    
    def upgrade_release(self):
        """Upgrade release"""
        self.execute_command("sudo do-release-upgrade")
    
    # Maintenance methods
    def clear_apt_cache(self):
        """Clear APT cache"""
        self.execute_command("sudo apt clean")
    
    def clear_journal_logs(self):
        """Clear journal logs"""
        self.execute_command("sudo journalctl --vacuum-time=7d")
    
    def clear_temp_files(self):
        """Clear temp files"""
        self.execute_command("sudo rm -rf /tmp/* && rm -rf ~/.cache/*")
    
    def autoremove_packages(self):
        """Autoremove packages"""
        self.execute_command("sudo apt autoremove -y")
    
    def show_disk_usage(self):
        """Show disk usage"""
        self.execute_command("df -h")
    
    def show_memory_usage(self):
        """Show memory usage"""
        self.execute_command("free -h")
    
    def show_system_info(self):
        """Show system info"""
        self.execute_command("uname -a")
    
    def show_processes(self):
        """Show running processes"""
        self.execute_command("ps aux")
    
    # Backup methods
    def browse_source(self):
        """Browse source path"""
        path = QFileDialog.getExistingDirectory(self, "Pilih Source Directory")
        if path:
            self.source_path_edit.setPlainText(path)
    
    def browse_output(self):
        """Browse output path"""
        path, _ = QFileDialog.getSaveFileName(
            self, "Pilih Output File", "", 
            "All Files (*);;Tar GZ (*.tar.gz);;ZIP (*.zip);;7Z (*.7z)"
        )
        if path:
            self.output_path_edit.setPlainText(path)
    
    def browse_restore_file(self):
        """Browse restore file"""
        path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Backup File", "",
            "All Files (*);;Tar GZ (*.tar.gz);;ZIP (*.zip);;7Z (*.7z)"
        )
        if path:
            self.restore_file_edit.setPlainText(path)
    
    def browse_restore_target(self):
        """Browse restore target"""
        path = QFileDialog.getExistingDirectory(self, "Pilih Target Directory")
        if path:
            self.restore_target_edit.setPlainText(path)
    
    def cycle_format(self):
        """Cycle through backup formats"""
        current = self.format_combo.text()
        formats = ["tar.gz", "zip", "7z"]
        current_index = formats.index(current) if current in formats else 0
        next_index = (current_index + 1) % len(formats)
        self.format_combo.setText(formats[next_index])
    
    def create_backup(self):
        """Create backup"""
        source = self.source_path_edit.toPlainText().strip()
        output = self.output_path_edit.toPlainText().strip()
        format_type = self.format_combo.text()
        
        if not source or not output:
            QMessageBox.warning(self, "Error", "Source dan Output path harus diisi!")
            return
        
        if not os.path.exists(source):
            QMessageBox.warning(self, "Error", f"Source path tidak ditemukan: {source}")
            return
        
        # Add extension if not present
        if not any(output.endswith(ext) for ext in ['.tar.gz', '.zip', '.7z']):
            output += f".{format_type}"
        
        success, stdout, stderr = self.backup_restore.create_backup(source, output, format_type)
        
        if success:
            self.append_output(f"Backup berhasil dibuat: {output}")
            self.append_output(stdout)
        else:
            self.append_error(f"Error membuat backup: {stderr}")
    
    def restore_backup(self):
        """Restore backup"""
        backup_file = self.restore_file_edit.toPlainText().strip()
        target = self.restore_target_edit.toPlainText().strip()
        
        if not backup_file or not target:
            QMessageBox.warning(self, "Error", "Backup file dan Target path harus diisi!")
            return
        
        if not os.path.exists(backup_file):
            QMessageBox.warning(self, "Error", f"Backup file tidak ditemukan: {backup_file}")
            return
        
        success, stdout, stderr = self.backup_restore.restore_backup(backup_file, target)
        
        if success:
            self.append_output(f"Restore berhasil ke: {target}")
            self.append_output(stdout)
        else:
            self.append_error(f"Error restore backup: {stderr}")
    
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Power Management methods
    def shutdown_system(self):
        """Shutdown sistem"""
        reply = QMessageBox.question(
            self, "Shutdown Sistem",
            "⚠️ PERINGATAN! ⚠️\n\nApakah Anda yakin ingin shutdown sistem sekarang?\n\nSemua aplikasi yang berjalan akan ditutup dan sistem akan mati.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, stdout, stderr = self.system_tools.shutdown_system()
            
            if not success:
                self.append_error(f"Error shutdown: {stderr}")
            else:
                self.append_output("Sistem akan shutdown...")
    
    def restart_system(self):
        """Restart sistem"""
        reply = QMessageBox.question(
            self, "Restart Sistem",
            "⚠️ PERINGATAN! ⚠️\n\nApakah Anda yakin ingin restart sistem sekarang?\n\nSemua aplikasi yang berjalan akan ditutup dan sistem akan restart.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, stdout, stderr = self.system_tools.restart_system()
            
            if not success:
                self.append_error(f"Error restart: {stderr}")
            else:
                self.append_output("Sistem akan restart...")
    
    def schedule_shutdown(self):
        """Jadwalkan shutdown"""
        time_str = self.shutdown_time_edit.text().strip()
        
        if not time_str:
            QMessageBox.warning(self, "Error", "Masukkan waktu shutdown!")
            return
        
        # Validasi format waktu
        if not self.validate_time_format(time_str):
            QMessageBox.warning(
                self, "Format Waktu Salah",
                "Format waktu tidak valid!\n\n"
                "Gunakan format:\n"
                "• +30 (30 menit)\n"
                "• 23:00 (jam:menit)\n"
                "• +2h (2 jam)"
            )
            return
        
        # Konfirmasi
        reply = QMessageBox.question(
            self, "Konfirmasi Schedule Shutdown",
            f"Apakah Anda yakin ingin menjadwalkan shutdown pada {time_str}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, stdout, stderr = self.system_tools.schedule_shutdown(time_str)
            
            if success:
                self.append_output(f"Shutdown dijadwalkan pada {time_str}")
                self.append_output(stdout)
            else:
                self.append_error(f"Error menjadwalkan shutdown: {stderr}")
    
    def cancel_shutdown(self):
        """Batalkan shutdown yang dijadwalkan"""
        reply = QMessageBox.question(
            self, "Cancel Shutdown",
            "Apakah Anda yakin ingin membatalkan shutdown yang dijadwalkan?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, stdout, stderr = self.system_tools.cancel_scheduled_shutdown()
            
            if success:
                self.append_output("Shutdown yang dijadwalkan dibatalkan")
                self.append_output(stdout)
            else:
                self.append_error(f"Error membatalkan shutdown: {stderr}")
    
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
    
    # Multimedia methods
    def install_single_package(self, package_name):
        """Install paket tunggal"""
        success, stdout, stderr = self.package_manager.install_package(package_name)                                                                            
        
        if success:
            self.append_output(f"Installing {package_name}...")
            self.append_output(stdout)
        else:
            self.append_error(f"Error installing {package_name}: {stderr}")
    
    # Repository Management Methods
    def change_repository(self, repo_type):
        """Mengganti repository server"""
        try:
            # Check sudo permissions first
            if not self.check_sudo_permissions():
                self.append_error("❌ Sudo permissions tidak tersedia!")
                self.append_error("Jalankan aplikasi dengan: sudo /opt/rijanos-assistant/rijanos-assistant-root.sh")
                return
            
            # Backup current sources first
            self.backup_sources()
            
            # Define repository configurations
            repos = {
                "default": {
                    "name": "Default Ubuntu",
                    "sources_list": """# Ubuntu sources have moved to /etc/apt/sources.list.d/ubuntu.sources
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] https://id.archive.ubuntu.com/ubuntu/ noble main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] https://id.archive.ubuntu.com/ubuntu/ noble-updates main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] https://id.archive.ubuntu.com/ubuntu/ noble-backports main universe restricted multiverse

# Security updates
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] https://security.ubuntu.com/ubuntu/ noble-security main universe restricted multiverse""",
                    "sources_d": """Types: deb
URIs: https://id.archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: https://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg"""
                },
                "cloudeka": {
                    "name": "Cloudeka CDN",
                    "sources_list": """# Ubuntu sources have moved to /etc/apt/sources.list.d/ubuntu.sources
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://cdn.repo.cloudeka.id/ubuntu/ noble main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://cdn.repo.cloudeka.id/ubuntu/ noble-updates main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://cdn.repo.cloudeka.id/ubuntu/ noble-backports main universe restricted multiverse

# Security updates
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://cdn.repo.cloudeka.id/ubuntu/ noble-security main universe restricted multiverse""",
                    "sources_d": """Types: deb
URIs: http://cdn.repo.cloudeka.id/ubuntu/
Suites: noble noble-updates noble-backports noble-security noble-proposed
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg"""
                },
                "domainesia": {
                    "name": "Domainesia",
                    "sources_list": """# Ubuntu sources have moved to /etc/apt/sources.list.d/ubuntu.sources
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://linux.domainesia.com/ubuntu/ubuntu-archive/ noble main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://linux.domainesia.com/ubuntu/ubuntu-archive/ noble-updates main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://linux.domainesia.com/ubuntu/ubuntu-archive/ noble-backports main universe restricted multiverse

# Security updates
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://linux.domainesia.com/ubuntu/ubuntu-archive/ noble-security main universe restricted multiverse""",
                    "sources_d": """Types: deb
URIs: http://linux.domainesia.com/ubuntu/ubuntu-archive/
Suites: noble noble-updates noble-backports noble-security noble-proposed
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg"""
                },
                "amscloud": {
                    "name": "AMS Cloud",
                    "sources_list": """# Ubuntu sources have moved to /etc/apt/sources.list.d/ubuntu.sources
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://mirror.amscloud.co.id/ubuntu/ noble main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://mirror.amscloud.co.id/ubuntu/ noble-updates main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://mirror.amscloud.co.id/ubuntu/ noble-backports main universe restricted multiverse

# Security updates
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://mirror.amscloud.co.id/ubuntu/ noble-security main universe restricted multiverse""",
                    "sources_d": """Types: deb
URIs: http://mirror.amscloud.co.id/ubuntu/
Suites: noble noble-updates noble-backports noble-security noble-proposed
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg"""
                },
                "nevacloud": {
                    "name": "Neva Cloud",
                    "sources_list": """# Ubuntu sources have moved to /etc/apt/sources.list.d/ubuntu.sources
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://mirror.nevacloud.com/ubuntu/ubuntu-archive noble main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://mirror.nevacloud.com/ubuntu/ubuntu-archive noble-updates main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://mirror.nevacloud.com/ubuntu/ubuntu-archive noble-backports main universe restricted multiverse

# Security updates
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://mirror.nevacloud.com/ubuntu/ubuntu-archive noble-security main universe restricted multiverse""",
                    "sources_d": """Types: deb
URIs: http://mirror.nevacloud.com/ubuntu/ubuntu-archive
Suites: noble noble-updates noble-backports noble-security noble-proposed
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg"""
                },
                "datautama": {
                    "name": "Datautama",
                    "sources_list": """# Ubuntu sources have moved to /etc/apt/sources.list.d/ubuntu.sources
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://kartolo.sby.datautama.net.id/ubuntu/ noble main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://kartolo.sby.datautama.net.id/ubuntu/ noble-updates main universe restricted multiverse
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://kartolo.sby.datautama.net.id/ubuntu/ noble-backports main universe restricted multiverse

# Security updates
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] http://kartolo.sby.datautama.net.id/ubuntu/ noble-security main universe restricted multiverse""",
                    "sources_d": """Types: deb
URIs: http://kartolo.sby.datautama.net.id/ubuntu/
Suites: noble noble-updates noble-backports noble-security noble-proposed
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg"""
                }
            }
            
            if repo_type not in repos:
                self.append_error(f"Repository type '{repo_type}' tidak dikenal!")
                return
            
            repo_config = repos[repo_type]
            
            # Show confirmation dialog
            reply = QMessageBox.question(
                self, 
                "Konfirmasi Ganti Repository", 
                f"Apakah Anda yakin ingin mengganti repository ke {repo_config['name']}?\n\n"
                "Perubahan ini akan memodifikasi file /etc/apt/sources.list dan /etc/apt/sources.list.d/ubuntu.sources",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
            
            self.append_output(f"Mengganti repository ke {repo_config['name']}...")
            
            # Combine all commands into one to avoid thread conflicts
            combined_command = f"""
# Update sources.list
echo '{repo_config['sources_list']}' | sudo tee /etc/apt/sources.list > /dev/null

# Update sources.list.d/ubuntu.sources  
echo '{repo_config['sources_d']}' | sudo tee /etc/apt/sources.list.d/ubuntu.sources > /dev/null

# Update package lists
sudo apt update

echo "✅ Repository berhasil diganti ke {repo_config['name']}!"
"""
            
            self.execute_command(combined_command)
            
            # Use QTimer to refresh status after command completes
            QTimer.singleShot(2000, self.refresh_repo_status)
            
        except Exception as e:
            self.append_error(f"Error mengganti repository: {str(e)}")
    
    def backup_sources(self):
        """Backup current sources files"""
        try:
            timestamp = self.get_timestamp()
            backup_dir = f"/tmp/apt-sources-backup-{timestamp}"
            
            # Combine backup commands into one
            backup_command = f"""
# Create backup directory
sudo mkdir -p {backup_dir}

# Backup sources files
sudo cp /etc/apt/sources.list {backup_dir}/sources.list.backup
sudo cp /etc/apt/sources.list.d/ubuntu.sources {backup_dir}/ubuntu.sources.backup

# Change ownership
sudo chown -R $USER:$USER {backup_dir}

echo "✅ Backup sources berhasil dibuat di: {backup_dir}"
"""
            
            self.execute_command(backup_command)
            
        except Exception as e:
            self.append_error(f"Error membuat backup sources: {str(e)}")
    
    def restore_sources(self):
        """Restore sources from backup"""
        try:
            # Find latest backup
            backup_dirs = glob.glob("/tmp/apt-sources-backup-*")
            if not backup_dirs:
                self.append_error("Tidak ada backup sources yang ditemukan!")
                return
            
            latest_backup = max(backup_dirs, key=os.path.getctime)
            
            # Show confirmation dialog
            reply = QMessageBox.question(
                self, 
                "Konfirmasi Restore", 
                f"Apakah Anda yakin ingin mengembalikan sources dari backup?\n\n"
                f"Backup: {latest_backup}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply != QMessageBox.StandardButton.Yes:
                return
            
            # Combine restore commands into one
            restore_command = f"""
# Restore files
sudo cp {latest_backup}/sources.list.backup /etc/apt/sources.list
sudo cp {latest_backup}/ubuntu.sources.backup /etc/apt/sources.list.d/ubuntu.sources

# Update package lists
sudo apt update

echo "✅ Sources berhasil dikembalikan dari backup!"
"""
            
            self.execute_command(restore_command)
            
            # Use QTimer to refresh status after command completes
            QTimer.singleShot(2000, self.refresh_repo_status)
            
        except Exception as e:
            self.append_error(f"Error restore sources: {str(e)}")
    
    def test_repository(self):
        """Test koneksi ke repository"""
        try:
            self.append_output("🧪 Testing repository connection...")
            self.execute_command("sudo apt update --dry-run")
            self.append_output("✅ Repository connection test completed!")
            
        except Exception as e:
            self.append_error(f"Error testing repository: {str(e)}")
    
    def refresh_repo_status(self):
        """Refresh repository status display"""
        try:
            # Read current sources.list
            result = self.command_executor.execute_safe_command("cat /etc/apt/sources.list")
            if result[0]:
                sources_list = result[1]
            else:
                sources_list = "Error reading sources.list"
            
            # Read current ubuntu.sources
            result = self.command_executor.execute_safe_command("cat /etc/apt/sources.list.d/ubuntu.sources")
            if result[0]:
                ubuntu_sources = result[1]
            else:
                ubuntu_sources = "Error reading ubuntu.sources"
            
            # Display status
            status_text = f"""
<b>Current Repository Configuration:</b>

<b>sources.list:</b>
<pre>{sources_list}</pre>

<b>ubuntu.sources:</b>
<pre>{ubuntu_sources}</pre>
            """
            
            self.repo_status_label.setText(status_text)
            
        except Exception as e:
            self.repo_status_label.setText(f"Error loading repository status: {str(e)}")
    
    def get_timestamp(self):
        """Get current timestamp for backup naming"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def check_sudo_permissions(self):
        """Check if sudo permissions are available"""
        try:
            result = self.command_executor.execute_safe_command("sudo -n true")
            return result[0]  # Return True if sudo works without password
        except Exception:
            return False
    
    def check_and_display_sudo_status(self):
        """Check and display sudo status in repository tab"""
        try:
            if self.check_sudo_permissions():
                self.append_output("✅ Sudo permissions tersedia - Repository management siap digunakan")
            else:
                self.append_error("❌ Sudo permissions tidak tersedia!")
                self.append_error("Untuk menggunakan fitur Repository Management:")
                self.append_error("1. Jalankan aplikasi dengan: sudo /opt/rijanos-assistant/rijanos-assistant-root.sh")
                self.append_error("2. Atau konfigurasi sudoers dengan: sudo sh /opt/rijanos-assistant/fix-sudo-permissions.sh")
        except Exception as e:
            self.append_error(f"Error checking sudo status: {str(e)}")
    
    def set_application_icon(self):
        """Set application icon from logo.png"""
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
                # Set window icon
                self.setWindowIcon(QIcon(icon_path))
                print(f"✅ Application icon set from: {icon_path}")
            else:
                print("⚠️ Warning: logo.png not found, using default icon")
                # Use default icon as fallback
                self.setWindowIcon(QIcon())
                
        except Exception as e:
            print(f"⚠️ Warning: Could not set application icon: {e}")
            # Use default icon as fallback
            self.setWindowIcon(QIcon())
