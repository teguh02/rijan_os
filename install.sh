#!/bin/sh

# Rijan OS Welcome Screen Installer
# Automatic installation script for Linux systems
# Compatible with sh and bash

set -e  # Exit on any error

# Check if we have bash available, if not continue with sh
if command -v bash >/dev/null 2>&1; then
    # Re-execute with bash if available for better compatibility
    if [ "$0" != "/bin/bash" ] && [ "$0" != "/usr/bin/bash" ]; then
        exec bash "$0" "$@"
    fi
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        print_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

# Install system dependencies
install_dependencies() {
    print_info "Installing system dependencies..."
    
    # Update package list
    apt update
    
    # Install Python and required packages
    apt install -y python3 python3-pip python3-venv python3-tk \
                   libjpeg-dev libpng-dev libtiff-dev libfreetype6-dev \
                   python3-pil python3-pil.imagetk
    
    print_success "System dependencies installed"
}

# Setup application
setup_application() {
    print_info "Setting up Rijan OS Welcome Screen..."
    
    # Create application directory
    mkdir -p /opt/rijan-os-welcome
    
    # Copy files
    cp -r . /opt/rijan-os-welcome/
    cd /opt/rijan-os-welcome
    
    # Create virtual environment
    python3 -m venv venv
    . venv/bin/activate
    
    # Install Python dependencies
    pip install -r requirements.txt
    
    # Set permissions
    chmod +x main.py
    chown -R root:root /opt/rijan-os-welcome
    
    print_success "Application setup completed"
}

# Create launcher script
create_launcher() {
    print_info "Creating launcher script..."
    
    cat > /usr/local/bin/rijan-welcome << 'EOF'
#!/bin/bash
cd /opt/rijan-os-welcome
. venv/bin/activate
python3 main.py
EOF
    
    chmod +x /usr/local/bin/rijan-welcome
    
    print_success "Launcher script created"
}

# Create systemd service
create_service() {
    print_info "Creating systemd service..."
    
    cat > /etc/systemd/system/rijan-welcome.service << 'EOF'
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
    
    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable rijan-welcome.service
    
    print_success "Systemd service created and enabled"
}

# Create desktop entry for autostart
create_desktop_entry() {
    print_info "Creating desktop entry for autostart..."
    
    # Create for all users
    mkdir -p /etc/xdg/autostart
    
    cat > /etc/xdg/autostart/rijan-welcome.desktop << 'EOF'
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
    
    print_success "Desktop entry created"
}

# Test installation
test_installation() {
    print_info "Testing installation..."
    
    # Test launcher script
    if [ -x /usr/local/bin/rijan-welcome ]; then
        print_success "Launcher script is executable"
    else
        print_error "Launcher script not found or not executable"
        return 1
    fi
    
    # Test systemd service
    if systemctl is-enabled rijan-welcome.service >/dev/null 2>&1; then
        print_success "Systemd service is enabled"
    else
        print_warning "Systemd service is not enabled"
    fi
    
    # Test Python dependencies
    cd /opt/rijan-os-welcome
    . venv/bin/activate
    if python3 -c "import tkinter, PIL" >/dev/null 2>&1; then
        print_success "Python dependencies are working"
    else
        print_error "Python dependencies test failed"
        return 1
    fi
    
    print_success "Installation test completed"
}

# Main installation function
main() {
    print_info "Starting Rijan OS Welcome Screen installation..."
    echo
    
    # Check prerequisites
    check_root
    
    # Install components
    install_dependencies
    setup_application
    create_launcher
    create_service
    create_desktop_entry
    test_installation
    
    echo
    print_success "Installation completed successfully!"
    echo
    print_info "You can now:"
    print_info "  - Test manually: /usr/local/bin/rijan-welcome"
    print_info "  - Check service: systemctl status rijan-welcome.service"
    print_info "  - View logs: journalctl -u rijan-welcome.service"
    print_info "  - Disable autostart: systemctl disable rijan-welcome.service"
    echo
    print_warning "The welcome screen will run automatically on next login/startup"
    echo
}

# Handle script arguments
case "${1:-install}" in
    "install")
        main
        ;;
    "uninstall")
        print_info "Uninstalling Rijan OS Welcome Screen..."
        systemctl stop rijan-welcome.service >/dev/null 2>&1 || true
        systemctl disable rijan-welcome.service >/dev/null 2>&1 || true
        rm -rf /opt/rijan-os-welcome
        rm -f /usr/local/bin/rijan-welcome
        rm -f /etc/systemd/system/rijan-welcome.service
        rm -f /etc/xdg/autostart/rijan-welcome.desktop
        systemctl daemon-reload
        print_success "Uninstallation completed"
        ;;
    "test")
        print_info "Testing installation..."
        test_installation
        ;;
    *)
        echo "Usage: $0 {install|uninstall|test}"
        echo "  install   - Install the welcome screen (default)"
        echo "  uninstall - Remove the welcome screen"
        echo "  test      - Test the installation"
        exit 1
        ;;
esac
