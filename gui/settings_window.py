"""
Settings Window untuk RijanOS Assistant
Window untuk konfigurasi aplikasi
"""

import json
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox,
    QGroupBox, QMessageBox, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QComboBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

class SettingsWindow(QWidget):
    """Window untuk pengaturan aplikasi"""
    
    config_updated = pyqtSignal()
    console_visibility_changed = pyqtSignal(bool)
    
    def __init__(self, config_path="config.json"):
        super().__init__()
        self.config_path = config_path
        self.config = self._load_config()
        self.init_ui()
        self.load_config()
    
    def _load_config(self):
        """Memuat konfigurasi dari file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_config()
        except json.JSONDecodeError:
            return self._create_default_config()
    
    def _create_default_config(self):
        """Membuat konfigurasi default"""
        return {
            "ai_enabled": False,
            "gemini_api_key": "",
            "blocked_commands": [
                "rm -rf /", "mkfs", "dd if=", ":(){ :|: & };:",
                "sudo rm -rf /", "format", "fdisk", "parted"
            ],
            "apt_commands": {
                "python_stack": "sudo apt install -y python3 python3-pip python3-venv jupyter-notebook python3-numpy python3-pandas python3-matplotlib",
                "php_stack": "sudo apt install -y php composer",
                "node_stack": "sudo apt install -y nodejs npm yarnpkg",
                "golang_stack": "sudo apt install -y golang",
                "media_tools": "sudo apt install -y vlc gimp audacity obs-studio",
                "education_apps": "sudo apt install -y libreoffice anki kalzium",
                "developer_apps": "sudo apt install -y git code docker.io postman",
                "system_apps": "sudo apt install -y htop neofetch gparted curl wget"
            }
        }
    
    def init_ui(self):
        """Inisialisasi UI"""
        layout = QVBoxLayout(self)
        
        # Tab widget untuk berbagai pengaturan
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # AI Settings tab
        self.create_ai_settings_tab()
        
        # Security Settings tab
        self.create_security_settings_tab()
        
        # Package Commands tab
        self.create_package_commands_tab()
        
        # UI Settings tab
        self.create_ui_settings_tab()
        
        # Save button
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        
        self.save_btn = QPushButton("💾 Simpan Pengaturan")
        self.save_btn.clicked.connect(self.save_config)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        save_layout.addWidget(self.save_btn)
        
        layout.addLayout(save_layout)
    
    def create_ai_settings_tab(self):
        """Membuat tab AI Settings"""
        ai_widget = QWidget()
        layout = QVBoxLayout(ai_widget)
        
        # AI Enable/Disable
        ai_group = QGroupBox("AI Assistant Settings")
        ai_layout = QVBoxLayout(ai_group)
        
        self.ai_enabled_cb = QCheckBox("Aktifkan AI Assistant")
        self.ai_enabled_cb.stateChanged.connect(self.on_ai_enabled_changed)
        ai_layout.addWidget(self.ai_enabled_cb)
        
        # API Key
        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(QLabel("Gemini API Key:"))
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("Masukkan API key Gemini...")
        api_key_layout.addWidget(self.api_key_edit)
        
        self.show_api_key_btn = QPushButton("👁️")
        self.show_api_key_btn.clicked.connect(self.toggle_api_key_visibility)
        api_key_layout.addWidget(self.show_api_key_btn)
        
        ai_layout.addLayout(api_key_layout)
        
        # API Key info
        api_info = QLabel("Dapatkan API key dari: https://aistudio.google.com/apikey")
        api_info.setStyleSheet("color: #666; font-size: 11px;")
        ai_layout.addWidget(api_info)
        
        # Model Selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model Gemini:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash", 
            "gemini-2.5-pro"
        ])
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_layout.addWidget(self.model_combo)
        ai_layout.addLayout(model_layout)
        
        # Model info
        model_info = QLabel("• Flash-Lite: Efisiensi biaya & latensi rendah\n• Flash: Performa harga terbaik\n• Pro: Akurasi & performa maksimum")
        model_info.setStyleSheet("color: #666; font-size: 11px; margin-left: 10px;")
        ai_layout.addWidget(model_info)
        
        layout.addWidget(ai_group)
        
        # Test connection
        test_layout = QHBoxLayout()
        self.test_connection_btn = QPushButton("🧪 Test Koneksi")
        self.test_connection_btn.clicked.connect(self.test_ai_connection)
        test_layout.addWidget(self.test_connection_btn)
        test_layout.addStretch()
        
        layout.addLayout(test_layout)
        layout.addStretch()
        
        self.tab_widget.addTab(ai_widget, "🤖 AI Settings")
    
    def create_security_settings_tab(self):
        """Membuat tab Security Settings"""
        security_widget = QWidget()
        layout = QVBoxLayout(security_widget)
        
        # Blocked Commands
        blocked_group = QGroupBox("Blocked Commands")
        blocked_layout = QVBoxLayout(blocked_group)
        
        blocked_info = QLabel("Daftar command yang diblokir untuk keamanan:")
        blocked_layout.addWidget(blocked_info)
        
        self.blocked_commands_edit = QTextEdit()
        self.blocked_commands_edit.setMaximumHeight(200)
        self.blocked_commands_edit.setPlaceholderText("Satu command per baris...")
        blocked_layout.addWidget(self.blocked_commands_edit)
        
        # Add/Remove buttons
        blocked_btn_layout = QHBoxLayout()
        
        self.add_blocked_btn = QPushButton("➕ Tambah Command")
        self.add_blocked_btn.clicked.connect(self.add_blocked_command)
        blocked_btn_layout.addWidget(self.add_blocked_btn)
        
        self.remove_blocked_btn = QPushButton("➖ Hapus Command")
        self.remove_blocked_btn.clicked.connect(self.remove_blocked_command)
        blocked_btn_layout.addWidget(self.remove_blocked_btn)
        
        blocked_btn_layout.addStretch()
        blocked_layout.addLayout(blocked_btn_layout)
        
        layout.addWidget(blocked_group)
        
        # Security info
        security_info = QLabel("""
        <b>Peringatan Keamanan:</b><br>
        • Command yang diblokir akan dicegah eksekusinya<br>
        • Pastikan untuk tidak menghapus command yang berbahaya<br>
        • Selalu backup konfigurasi sebelum mengubah pengaturan
        """)
        security_info.setStyleSheet("""
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 10px;
            border-radius: 5px;
            color: #856404;
        """)
        layout.addWidget(security_info)
        
        layout.addStretch()
        
        self.tab_widget.addTab(security_widget, "🔒 Security")
    
    def create_package_commands_tab(self):
        """Membuat tab Package Commands"""
        package_widget = QWidget()
        layout = QVBoxLayout(package_widget)
        
        # Package Commands Table
        package_group = QGroupBox("APT Commands")
        package_layout = QVBoxLayout(package_group)
        
        # Table untuk menampilkan dan mengedit commands
        self.commands_table = QTableWidget()
        self.commands_table.setColumnCount(2)
        self.commands_table.setHorizontalHeaderLabels(["Stack Name", "Command"])
        
        # Set table properties
        header = self.commands_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        self.commands_table.setAlternatingRowColors(True)
        self.commands_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        package_layout.addWidget(self.commands_table)
        
        # Table buttons
        table_btn_layout = QHBoxLayout()
        
        self.add_command_btn = QPushButton("➕ Tambah Command")
        self.add_command_btn.clicked.connect(self.add_command)
        table_btn_layout.addWidget(self.add_command_btn)
        
        self.remove_command_btn = QPushButton("➖ Hapus Command")
        self.remove_command_btn.clicked.connect(self.remove_command)
        table_btn_layout.addWidget(self.remove_command_btn)
        
        self.reset_commands_btn = QPushButton("🔄 Reset Default")
        self.reset_commands_btn.clicked.connect(self.reset_commands)
        table_btn_layout.addWidget(self.reset_commands_btn)
        
        table_btn_layout.addStretch()
        package_layout.addLayout(table_btn_layout)
        
        layout.addWidget(package_group)
        
        # Info
        info_label = QLabel("""
        <b>Cara Menggunakan:</b><br>
        • Klik pada cell untuk mengedit<br>
        • Gunakan tombol + untuk menambah command baru<br>
        • Gunakan tombol - untuk menghapus command yang dipilih<br>
        • Gunakan tombol Reset untuk mengembalikan ke default
        """)
        info_label.setStyleSheet("""
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            padding: 10px;
            border-radius: 5px;
            color: #0c5460;
        """)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        self.tab_widget.addTab(package_widget, "📦 Package Commands")
    
    def create_ui_settings_tab(self):
        """Membuat tab UI Settings"""
        ui_widget = QWidget()
        layout = QVBoxLayout(ui_widget)
        
        # Console Settings
        console_group = QGroupBox("Console Output Settings")
        console_layout = QVBoxLayout(console_group)
        
        # Console visibility toggle
        self.console_visible_cb = QCheckBox("Tampilkan Console Output Area")
        self.console_visible_cb.stateChanged.connect(self.on_console_visibility_changed)
        console_layout.addWidget(self.console_visible_cb)
        
        # Console info
        console_info = QLabel("""
        <b>Console Output Area:</b><br>
        • Menampilkan output command yang dijalankan<br>
        • Menampilkan error messages dan log<br>
        • Berguna untuk debugging dan monitoring<br>
        • Dapat disembunyikan untuk tampilan yang lebih bersih
        """)
        console_info.setStyleSheet("""
            background-color: #e3f2fd;
            border: 1px solid #bbdefb;
            padding: 10px;
            border-radius: 5px;
            color: #1565c0;
        """)
        console_layout.addWidget(console_info)
        
        layout.addWidget(console_group)
        
        # Theme Settings (placeholder for future)
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QVBoxLayout(theme_group)
        
        theme_info = QLabel("""
        <b>Theme Options:</b><br>
        • Light Theme (Default)<br>
        • Dark Theme (Coming Soon)<br>
        • Custom Theme (Coming Soon)
        """)
        theme_info.setStyleSheet("""
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 10px;
            border-radius: 5px;
            color: #495057;
        """)
        theme_layout.addWidget(theme_info)
        
        layout.addWidget(theme_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(ui_widget, "🎨 UI Settings")
    
    def on_console_visibility_changed(self, state):
        """Handler ketika console visibility diubah"""
        # Emit signal untuk memberitahu main window
        self.console_visibility_changed.emit(state == Qt.CheckState.Checked.value)
    
    def load_config(self):
        """Memuat konfigurasi ke UI"""
        # AI Settings
        self.ai_enabled_cb.setChecked(self.config.get("ai_enabled", False))
        self.api_key_edit.setText(self.config.get("gemini_api_key", ""))
        
        # Set selected model
        selected_model = self.config.get("gemini_model", "gemini-2.5-flash-lite")
        index = self.model_combo.findText(selected_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        # UI Settings
        self.console_visible_cb.setChecked(self.config.get("console_visible", True))
        
        # Blocked Commands
        blocked_commands = self.config.get("blocked_commands", [])
        self.blocked_commands_edit.setPlainText("\n".join(blocked_commands))
        
        # Package Commands
        self.load_commands_table()
    
    def load_commands_table(self):
        """Memuat commands ke table"""
        commands = self.config.get("apt_commands", {})
        
        self.commands_table.setRowCount(len(commands))
        
        for row, (name, command) in enumerate(commands.items()):
            name_item = QTableWidgetItem(name)
            command_item = QTableWidgetItem(command)
            
            self.commands_table.setItem(row, 0, name_item)
            self.commands_table.setItem(row, 1, command_item)
    
    def on_ai_enabled_changed(self, state):
        """Handler ketika AI enabled diubah"""
        enabled = state == Qt.CheckState.Checked.value
        self.api_key_edit.setEnabled(enabled)
        self.model_combo.setEnabled(enabled)
        self.test_connection_btn.setEnabled(enabled)
    
    def on_model_changed(self, model_name):
        """Handler ketika model Gemini diubah"""
        # Save immediately when model is changed
        self.save_config()
    
    def toggle_api_key_visibility(self):
        """Toggle visibility API key"""
        if self.api_key_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_api_key_btn.setText("🙈")
        else:
            self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_api_key_btn.setText("👁️")
    
    def test_ai_connection(self):
        """Test koneksi AI"""
        api_key = self.api_key_edit.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "Error", "API key tidak boleh kosong!")
            return
        
        # Simulate test (in real implementation, you would test with Gemini API)
        QMessageBox.information(self, "Test Koneksi", "Koneksi berhasil! (Simulasi)")
    
    def add_blocked_command(self):
        """Tambah blocked command"""
        command, ok = QLineEdit.getText(self, "Tambah Blocked Command", "Masukkan command yang akan diblokir:")
        if ok and command.strip():
            current_text = self.blocked_commands_edit.toPlainText()
            if current_text:
                self.blocked_commands_edit.setPlainText(current_text + "\n" + command.strip())
            else:
                self.blocked_commands_edit.setPlainText(command.strip())
    
    def remove_blocked_command(self):
        """Hapus blocked command"""
        current_text = self.blocked_commands_edit.toPlainText()
        lines = current_text.split("\n")
        
        if lines:
            lines.pop()  # Remove last line
            self.blocked_commands_edit.setPlainText("\n".join(lines))
    
    def add_command(self):
        """Tambah command baru"""
        row_count = self.commands_table.rowCount()
        self.commands_table.insertRow(row_count)
        
        # Set default values
        self.commands_table.setItem(row_count, 0, QTableWidgetItem("new_stack"))
        self.commands_table.setItem(row_count, 1, QTableWidgetItem("sudo apt install -y "))
    
    def remove_command(self):
        """Hapus command yang dipilih"""
        current_row = self.commands_table.currentRow()
        if current_row >= 0:
            self.commands_table.removeRow(current_row)
    
    def reset_commands(self):
        """Reset commands ke default"""
        reply = QMessageBox.question(
            self, "Reset Commands", 
            "Apakah Anda yakin ingin mengembalikan commands ke default?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            default_commands = {
                "python_stack": "sudo apt install -y python3 python3-pip python3-venv jupyter-notebook python3-numpy python3-pandas python3-matplotlib",
                "php_stack": "sudo apt install -y php composer",
                "node_stack": "sudo apt install -y nodejs npm yarnpkg",
                "golang_stack": "sudo apt install -y golang",
                "media_tools": "sudo apt install -y vlc gimp audacity obs-studio",
                "education_apps": "sudo apt install -y libreoffice anki kalzium",
                "developer_apps": "sudo apt install -y git code docker.io postman",
                "system_apps": "sudo apt install -y htop neofetch gparted curl wget"
            }
            
            self.config["apt_commands"] = default_commands
            self.load_commands_table()
    
    def save_config(self):
        """Simpan konfigurasi"""
        try:
            # Update config from UI
            self.config["ai_enabled"] = self.ai_enabled_cb.isChecked()
            self.config["gemini_api_key"] = self.api_key_edit.text().strip()
            self.config["gemini_model"] = self.model_combo.currentText()
            
            # Update UI settings
            self.config["console_visible"] = self.console_visible_cb.isChecked()
            
            # Update blocked commands
            blocked_text = self.blocked_commands_edit.toPlainText()
            self.config["blocked_commands"] = [cmd.strip() for cmd in blocked_text.split("\n") if cmd.strip()]
            
            # Update apt commands
            apt_commands = {}
            for row in range(self.commands_table.rowCount()):
                name_item = self.commands_table.item(row, 0)
                command_item = self.commands_table.item(row, 1)
                
                if name_item and command_item:
                    name = name_item.text().strip()
                    command = command_item.text().strip()
                    
                    if name and command:
                        apt_commands[name] = command
            
            self.config["apt_commands"] = apt_commands
            
            # Save to file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            QMessageBox.information(self, "Berhasil", "Konfigurasi berhasil disimpan!")
            self.config_updated.emit()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan konfigurasi: {str(e)}")
