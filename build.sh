#!/bin/bash

# Rijan OS Welcome Screen Build Script
# Creates distributable packages for different platforms

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Clean previous builds
clean_build() {
    print_info "Cleaning previous builds..."
    rm -rf build/ dist/ *.spec
    print_success "Build directory cleaned"
}

# Install build dependencies
install_build_deps() {
    print_info "Installing build dependencies..."
    pip install pyinstaller
    print_success "Build dependencies installed"
}

# Build standalone executable
build_executable() {
    print_info "Building standalone executable..."
    
    pyinstaller \
        --onefile \
        --windowed \
        --add-data "images:images" \
        --add-data "requirements.txt:." \
        --name "rijan-welcome" \
        --icon "images/wallpaper1.jpg" \
        main.py
    
    print_success "Executable built successfully"
}

# Create distribution package
create_package() {
    print_info "Creating distribution package..."
    
    # Create package directory
    mkdir -p dist/rijan-os-welcome-package
    
    # Copy files
    cp -r images/ dist/rijan-os-welcome-package/
    cp main.py dist/rijan-os-welcome-package/
    cp requirements.txt dist/rijan-os-welcome-package/
    cp README.md dist/rijan-os-welcome-package/
    cp install.sh dist/rijan-os-welcome-package/
    cp build.sh dist/rijan-os-welcome-package/
    
    # Create package info
    cat > dist/rijan-os-welcome-package/VERSION << EOF
Rijan OS Welcome Screen
Version: 1.0.0
Build Date: $(date)
Platform: Linux
EOF
    
    # Create tarball
    cd dist/
    tar -czf rijan-os-welcome-$(date +%Y%m%d).tar.gz rijan-os-welcome-package/
    cd ..
    
    print_success "Distribution package created"
}

# Create DEB package
create_deb_package() {
    print_info "Creating DEB package..."
    
    # Create package structure
    mkdir -p dist/deb/rijan-welcome/DEBIAN
    mkdir -p dist/deb/rijan-welcome/opt/rijan-os-welcome
    mkdir -p dist/deb/rijan-welcome/usr/local/bin
    mkdir -p dist/deb/rijan-welcome/etc/systemd/system
    mkdir -p dist/deb/rijan-welcome/etc/xdg/autostart
    
    # Copy application files
    cp -r images/ dist/deb/rijan-welcome/opt/rijan-os-welcome/
    cp main.py dist/deb/rijan-welcome/opt/rijan-os-welcome/
    cp requirements.txt dist/deb/rijan-welcome/opt/rijan-os-welcome/
    
    # Create launcher script
    cat > dist/deb/rijan-welcome/usr/local/bin/rijan-welcome << 'EOF'
#!/bin/bash
cd /opt/rijan-os-welcome
python3 main.py
EOF
    chmod +x dist/deb/rijan-welcome/usr/local/bin/rijan-welcome
    
    # Create systemd service
    cat > dist/deb/rijan-welcome/etc/systemd/system/rijan-welcome.service << 'EOF'
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

[Install]
WantedBy=graphical-session.target
EOF
    
    # Create desktop entry
    cat > dist/deb/rijan-welcome/etc/xdg/autostart/rijan-welcome.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Rijan OS Welcome
Exec=/usr/local/bin/rijan-welcome
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
    
    # Create control file
    cat > dist/deb/rijan-welcome/DEBIAN/control << EOF
Package: rijan-welcome
Version: 1.0.0
Section: misc
Priority: optional
Architecture: all
Depends: python3, python3-tk, python3-pil, python3-pil.imagetk
Maintainer: Rijan OS Team <team@rijanos.org>
Description: Rijan OS Welcome Screen
 A beautiful welcome screen application for Rijan OS
 that introduces users to the operating system features.
EOF
    
    # Create postinst script
    cat > dist/deb/rijan-welcome/DEBIAN/postinst << 'EOF'
#!/bin/bash
set -e

# Install Python dependencies
cd /opt/rijan-os-welcome
python3 -m pip install -r requirements.txt

# Enable systemd service
systemctl daemon-reload
systemctl enable rijan-welcome.service

echo "Rijan OS Welcome Screen installed successfully"
EOF
    chmod +x dist/deb/rijan-welcome/DEBIAN/postinst
    
    # Create prerm script
    cat > dist/deb/rijan-welcome/DEBIAN/prerm << 'EOF'
#!/bin/bash
set -e

# Disable and stop service
systemctl disable rijan-welcome.service || true
systemctl stop rijan-welcome.service || true
EOF
    chmod +x dist/deb/rijan-welcome/DEBIAN/prerm
    
    # Build DEB package
    dpkg-deb --build dist/deb/rijan-welcome dist/rijan-welcome_1.0.0_all.deb
    
    print_success "DEB package created"
}

# Main build function
main() {
    print_info "Starting build process..."
    echo
    
    case "${1:-all}" in
        "clean")
            clean_build
            ;;
        "executable")
            clean_build
            install_build_deps
            build_executable
            ;;
        "package")
            clean_build
            create_package
            ;;
        "deb")
            clean_build
            create_deb_package
            ;;
        "all")
            clean_build
            install_build_deps
            build_executable
            create_package
            if command -v dpkg-deb &> /dev/null; then
                create_deb_package
            else
                print_info "dpkg-deb not found, skipping DEB package creation"
            fi
            ;;
        *)
            echo "Usage: $0 {clean|executable|package|deb|all}"
            echo "  clean      - Clean build directory"
            echo "  executable - Build standalone executable"
            echo "  package    - Create distribution tarball"
            echo "  deb        - Create DEB package"
            echo "  all        - Build everything (default)"
            exit 1
            ;;
    esac
    
    echo
    print_success "Build process completed!"
    echo
    print_info "Build artifacts:"
    ls -la dist/ 2>/dev/null || echo "No build artifacts found"
}

main "$@"
