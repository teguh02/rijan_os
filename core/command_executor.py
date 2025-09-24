"""
Command Executor untuk RijanOS Assistant
Menangani eksekusi command shell dengan validasi keamanan
"""

import subprocess
import json
import os
from typing import Tuple, List, Optional

class CommandExecutor:
    """Kelas untuk mengeksekusi command shell dengan validasi keamanan"""
    
    def __init__(self, config_path: str = "config.json"):
        """Inisialisasi CommandExecutor dengan path ke config file"""
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Memuat konfigurasi dari file JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default config jika file tidak ditemukan
            return {
                "blocked_commands": [
                    "rm -rf /", "mkfs", "dd if=", ":(){ :|: & };:",
                    "sudo rm -rf /", "format", "fdisk", "parted"
                ]
            }
        except json.JSONDecodeError:
            return {"blocked_commands": []}
    
    def is_command_blocked(self, command: str) -> bool:
        """Memeriksa apakah command diblokir"""
        blocked_commands = self.config.get("blocked_commands", [])
        
        for blocked in blocked_commands:
            if blocked.lower() in command.lower():
                return True
        return False
    
    def execute_command(self, command: str, timeout: int = 300) -> Tuple[bool, str, str]:
        """
        Mengeksekusi command shell dengan validasi keamanan
        
        Args:
            command: Command yang akan dieksekusi
            timeout: Timeout dalam detik (default: 5 menit)
            
        Returns:
            Tuple berisi (success, stdout, stderr)
        """
        # Validasi command
        if self.is_command_blocked(command):
            return False, "", f"Command diblokir untuk keamanan: {command}"
        
        try:
            # Eksekusi command dengan subprocess
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd()
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, "", f"Command timeout setelah {timeout} detik"
        except Exception as e:
            return False, "", f"Error eksekusi command: {str(e)}"
    
    def execute_safe_command(self, command: str, timeout: int = 300) -> Tuple[bool, str, str]:
        """
        Mengeksekusi command dengan validasi tambahan untuk command yang memerlukan sudo
        
        Args:
            command: Command yang akan dieksekusi
            timeout: Timeout dalam detik
            
        Returns:
            Tuple berisi (success, stdout, stderr)
        """
        # Periksa apakah command memerlukan sudo
        if command.startswith("sudo "):
            # Validasi tambahan untuk sudo commands
            dangerous_patterns = [
                "rm -rf", "mkfs", "dd", "format", "fdisk", "parted",
                "shutdown", "reboot", "halt", "poweroff"
            ]
            
            for pattern in dangerous_patterns:
                if pattern in command:
                    return False, "", f"Command berbahaya diblokir: {pattern}"
        
        return self.execute_command(command, timeout)
    
    def get_system_info(self) -> dict:
        """Mendapatkan informasi sistem"""
        info = {}
        
        # OS Info
        try:
            result = subprocess.run(["uname", "-a"], capture_output=True, text=True)
            if result.returncode == 0:
                info["os"] = result.stdout.strip()
        except:
            info["os"] = "Unknown"
        
        # Memory Info
        try:
            result = subprocess.run(["free", "-h"], capture_output=True, text=True)
            if result.returncode == 0:
                info["memory"] = result.stdout.strip()
        except:
            info["memory"] = "Unknown"
        
        # Disk Info
        try:
            result = subprocess.run(["df", "-h"], capture_output=True, text=True)
            if result.returncode == 0:
                info["disk"] = result.stdout.strip()
        except:
            info["disk"] = "Unknown"
        
        return info
