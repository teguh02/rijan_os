# RijanOS Assistant - Developer Guide

## 🏗️ Arsitektur Aplikasi

### Struktur Proyek
```
RijanOS_Assistant/
├── main.py                 # Entry point aplikasi
├── config.json            # Konfigurasi aplikasi
├── requirements.txt       # Python dependencies
├── gui/                   # Module GUI
│   ├── __init__.py
│   ├── main_window.py     # Window utama dengan tab navigation
│   ├── settings_window.py # Window settings
│   ├── ai_chat_window.py # Window AI chat
│   └── system_tray.py    # System tray icon dan menu
├── core/                  # Module core
│   ├── __init__.py
│   ├── command_executor.py # Eksekusi command dengan validasi
│   ├── package_manager.py # Manajemen paket sistem
│   ├── backup_restore.py # Backup & restore
│   └── system_tools.py   # Tools sistem
└── assets/               # File statis
    ├── __init__.py
    ├── icons/           # Icon aplikasi
    └── logo.png         # Logo RijanOS
```

### Design Patterns

#### 1. MVC Pattern
- **Model**: `core/` modules (business logic)
- **View**: `gui/` modules (UI components)
- **Controller**: `main_window.py` (coordination)

#### 2. Command Pattern
- `command_executor.py`: Encapsulates command execution
- `package_manager.py`: Encapsulates package operations
- `system_tools.py`: Encapsulates system operations

#### 3. Observer Pattern
- PyQt6 signals/slots for UI updates
- Thread-based command execution
- Real-time output display

## 🔧 Core Modules

### CommandExecutor
```python
class CommandExecutor:
    def execute_command(self, command: str) -> Tuple[bool, str, str]
    def execute_safe_command(self, command: str) -> Tuple[bool, str, str]
    def is_command_blocked(self, command: str) -> bool
    def get_system_info(self) -> dict
```

**Fitur:**
- Validasi command berbahaya
- Timeout protection
- Error handling
- System info gathering

### PackageManager
```python
class PackageManager:
    def install_stack(self, stack_name: str) -> Tuple[bool, str, str]
    def update_packages(self) -> Tuple[bool, str, str]
    def upgrade_packages(self) -> Tuple[bool, str, str]
    def clean_cache(self) -> Tuple[bool, str, str]
```

**Fitur:**
- Stack installation
- System updates
- Cache management
- Package search

### BackupRestore
```python
class BackupRestore:
    def create_backup(self, source: str, output: str, format: str) -> Tuple[bool, str, str]
    def restore_backup(self, backup_path: str, target: str) -> Tuple[bool, str, str]
    def list_backup_files(self, directory: str) -> List[str]
```

**Fitur:**
- Multiple format support (tar.gz, zip, 7z)
- Backup validation
- Restore verification
- File listing

### SystemTools
```python
class SystemTools:
    def shutdown_system(self) -> Tuple[bool, str, str]
    def restart_system(self) -> Tuple[bool, str, str]
    def schedule_shutdown(self, time_str: str) -> Tuple[bool, str, str]
    def cancel_scheduled_shutdown(self) -> Tuple[bool, str, str]
```

**Fitur:**
- Power management
- System maintenance
- Health monitoring
- Bug reporting

## 🎨 GUI Modules

### MainWindow
```python
class MainWindow(QMainWindow):
    def create_dashboard_tab(self)
    def create_applications_tab(self)
    def create_multimedia_tab(self)
    def create_maintenance_tab(self)
    def create_backup_tab(self)
    def create_power_tab(self)
    def create_ai_chat_tab(self)
    def create_settings_tab(self)
```

**Fitur:**
- Tab-based navigation
- Real-time output display
- Progress indicators
- Error handling

### SystemTray
```python
class SystemTray(QSystemTrayIcon):
    def setup_menu(self)
    def update_system(self)
    def clean_system(self)
    def shutdown_system(self)
    def restart_system(self)
    def schedule_shutdown(self)
    def cancel_shutdown(self)
```

**Fitur:**
- Tray icon management
- Context menu
- Quick actions
- Minimize to tray

### SettingsWindow
```python
class SettingsWindow(QWidget):
    def create_ai_settings_tab(self)
    def create_security_settings_tab(self)
    def create_package_commands_tab(self)
    def save_config(self)
    def load_config(self)
```

**Fitur:**
- Configuration management
- AI settings
- Security settings
- Package commands editor

### AIChatWindow
```python
class AIChatWindow(QWidget):
    def send_message(self)
    def add_message(self, sender: str, message: str)
    def on_ai_response(self, response: str)
    def on_ai_error(self, error: str)
```

**Fitur:**
- Chat interface
- AI integration
- Message formatting
- Error handling

## 🔒 Keamanan

### Command Validation
```python
def is_command_blocked(self, command: str) -> bool:
    blocked_commands = self.config.get("blocked_commands", [])
    for blocked in blocked_commands:
        if blocked.lower() in command.lower():
            return True
    return False
```

### Safe Execution
```python
def execute_safe_command(self, command: str) -> Tuple[bool, str, str]:
    if self.is_command_blocked(command):
        return False, "", f"Command diblokir untuk keamanan: {command}"
    
    # Additional validation for sudo commands
    if command.startswith("sudo "):
        dangerous_patterns = ["rm -rf", "mkfs", "dd", "format"]
        for pattern in dangerous_patterns:
            if pattern in command:
                return False, "", f"Command berbahaya diblokir: {pattern}"
    
    return self.execute_command(command)
```

### Blocked Commands
```json
{
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
}
```

## 🧪 Testing

### Unit Tests
```python
# test_command_executor.py
def test_command_validation():
    executor = CommandExecutor()
    assert executor.is_command_blocked("rm -rf /") == True
    assert executor.is_command_blocked("ls -la") == False

def test_safe_execution():
    executor = CommandExecutor()
    success, stdout, stderr = executor.execute_safe_command("echo test")
    assert success == True
    assert "test" in stdout
```

### Integration Tests
```python
# test_package_manager.py
def test_stack_installation():
    pm = PackageManager()
    success, stdout, stderr = pm.install_stack("python_stack")
    assert success == True

def test_system_update():
    pm = PackageManager()
    success, stdout, stderr = pm.update_packages()
    assert success == True
```

### GUI Tests
```python
# test_gui.py
def test_main_window_creation():
    app = QApplication([])
    window = MainWindow()
    assert window is not None
    assert window.tab_widget.count() > 0

def test_system_tray():
    app = QApplication([])
    tray = SystemTray()
    assert tray.isVisible() == True
```

## 🚀 Deployment

### Build Script
```bash
#!/bin/bash
# build.sh - Build script untuk RijanOS Assistant

# Create distribution directory
mkdir -p dist/rijanos-assistant

# Copy source files
cp -r gui/ core/ assets/ dist/rijanos-assistant/
cp main.py config.json requirements.txt dist/rijanos-assistant/

# Create installer
cat > dist/install.sh << 'EOF'
#!/bin/bash
# Auto-generated installer
# ... installation logic ...
EOF

chmod +x dist/install.sh
```

### Package Creation
```bash
# Create Debian package
dpkg-deb --build rijanos-assistant

# Create RPM package
rpmbuild -ba rijanos-assistant.spec

# Create AppImage
appimagetool rijanos-assistant.AppDir rijanos-assistant.AppImage
```

## 📊 Performance

### Memory Usage
- **Base**: ~50MB
- **With AI**: ~100MB
- **Peak**: ~200MB (during operations)

### CPU Usage
- **Idle**: <1%
- **Operations**: 10-50%
- **AI Processing**: 20-80%

### Disk Usage
- **Application**: ~50MB
- **Dependencies**: ~200MB
- **Cache**: ~10MB

## 🔧 Configuration

### Environment Variables
```bash
export RIJANOS_ASSISTANT_CONFIG="/path/to/config.json"
export RIJANOS_ASSISTANT_LOG_LEVEL="INFO"
export RIJANOS_ASSISTANT_DEBUG="false"
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rijanos-assistant.log'),
        logging.StreamHandler()
    ]
)
```

## 🐛 Debugging

### Debug Mode
```python
# Enable debug mode
DEBUG = os.getenv('RIJANOS_ASSISTANT_DEBUG', 'false').lower() == 'true'

if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
    print("Debug mode enabled")
```

### Common Issues
1. **PyQt6 not found**: Install python3-pyqt6
2. **Permission denied**: Check file permissions
3. **System tray not available**: Install desktop environment
4. **AI not working**: Check API key configuration

### Log Analysis
```bash
# View logs
tail -f rijanos-assistant.log

# Filter errors
grep "ERROR" rijanos-assistant.log

# Filter warnings
grep "WARNING" rijanos-assistant.log
```

## 📈 Monitoring

### Health Checks
```python
def check_system_health(self) -> dict:
    health = {
        "disk_usage": self.check_disk_usage(),
        "memory_usage": self.check_memory_usage(),
        "system_load": self.check_system_load(),
        "errors": []
    }
    return health
```

### Metrics Collection
```python
def collect_metrics(self) -> dict:
    metrics = {
        "uptime": self.get_uptime(),
        "operations_count": self.get_operations_count(),
        "error_count": self.get_error_count(),
        "last_update": self.get_last_update()
    }
    return metrics
```

## 🔄 Updates

### Version Management
```python
VERSION = "1.1.0"
BUILD_DATE = "2024-12-19"
GIT_COMMIT = "abc123"

def check_for_updates(self) -> bool:
    # Check GitHub for new releases
    # Compare versions
    # Download if newer version available
    pass
```

### Auto-Update
```python
def auto_update(self):
    if self.check_for_updates():
        self.download_update()
        self.install_update()
        self.restart_application()
```

## 📚 API Reference

### Core API
```python
# CommandExecutor
execute_command(command: str) -> Tuple[bool, str, str]
execute_safe_command(command: str) -> Tuple[bool, str, str]
is_command_blocked(command: str) -> bool

# PackageManager
install_stack(stack_name: str) -> Tuple[bool, str, str]
update_packages() -> Tuple[bool, str, str]
upgrade_packages() -> Tuple[bool, str, str]

# BackupRestore
create_backup(source: str, output: str, format: str) -> Tuple[bool, str, str]
restore_backup(backup_path: str, target: str) -> Tuple[bool, str, str]

# SystemTools
shutdown_system() -> Tuple[bool, str, str]
restart_system() -> Tuple[bool, str, str]
schedule_shutdown(time_str: str) -> Tuple[bool, str, str]
```

### GUI API
```python
# MainWindow
create_dashboard_tab()
create_applications_tab()
create_multimedia_tab()
create_maintenance_tab()
create_backup_tab()
create_power_tab()

# SystemTray
setup_menu()
update_system()
clean_system()
shutdown_system()
restart_system()

# SettingsWindow
save_config()
load_config()
create_ai_settings_tab()
create_security_settings_tab()

# AIChatWindow
send_message()
add_message(sender: str, message: str)
on_ai_response(response: str)
on_ai_error(error: str)
```

---

**RijanOS Assistant v1.1.0** - Developer Guide

*Dokumentasi ini adalah bagian dari Rijan OS Developer Resources*
