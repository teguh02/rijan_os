#!/bin/bash
# RijanOS Assistant Root Wrapper
# Script untuk menjalankan RijanOS Assistant sebagai root saat autostart

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    # Try to run with sudo
    exec sudo -E "$0" "$@"
fi

# Set display environment for GUI
export DISPLAY=:0
export XAUTHORITY="/home/$SUDO_USER/.Xauthority"

# Run RijanOS Assistant
cd /opt/rijanos-assistant
exec ./venv/bin/python main.py "$@"
