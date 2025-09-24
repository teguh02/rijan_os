"""
Package Manager untuk RijanOS Assistant
Menangani instalasi dan manajemen paket sistem
"""

import json
import os
from typing import Dict, List, Tuple
from .command_executor import CommandExecutor

class PackageManager:
    """Kelas untuk manajemen paket sistem"""
    
    def __init__(self, config_path: str = "config.json"):
        """Inisialisasi PackageManager"""
        self.config_path = config_path
        self.command_executor = CommandExecutor(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Memuat konfigurasi dari file JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"apt_commands": {}}
        except json.JSONDecodeError:
            return {"apt_commands": {}}
    
    def get_available_stacks(self) -> Dict[str, str]:
        """Mendapatkan daftar stack yang tersedia"""
        return self.config.get("apt_commands", {})
    
    def install_stack(self, stack_name: str) -> Tuple[bool, str, str]:
        """
        Menginstal stack aplikasi
        
        Args:
            stack_name: Nama stack yang akan diinstal
            
        Returns:
            Tuple berisi (success, stdout, stderr)
        """
        stacks = self.get_available_stacks()
        
        if stack_name not in stacks:
            return False, "", f"Stack '{stack_name}' tidak ditemukan"
        
        command = stacks[stack_name]
        return self.command_executor.execute_safe_command(command)
    
    def update_packages(self) -> Tuple[bool, str, str]:
        """Update daftar paket"""
        return self.command_executor.execute_safe_command("sudo apt update")
    
    def upgrade_packages(self) -> Tuple[bool, str, str]:
        """Upgrade semua paket"""
        return self.command_executor.execute_safe_command("sudo apt update && sudo apt upgrade -y")
    
    def upgrade_release(self) -> Tuple[bool, str, str]:
        """Upgrade release sistem"""
        return self.command_executor.execute_safe_command("sudo do-release-upgrade")
    
    def clean_cache(self) -> Tuple[bool, str, str]:
        """Membersihkan cache APT"""
        return self.command_executor.execute_safe_command("sudo apt clean")
    
    def autoremove_packages(self) -> Tuple[bool, str, str]:
        """Menghapus paket yang tidak terpakai"""
        return self.command_executor.execute_safe_command("sudo apt autoremove -y")
    
    def search_package(self, package_name: str) -> Tuple[bool, str, str]:
        """Mencari paket"""
        return self.command_executor.execute_command(f"apt search {package_name}")
    
    def install_package(self, package_name: str) -> Tuple[bool, str, str]:
        """Menginstal paket tunggal"""
        command = f"sudo apt install -y {package_name}"
        return self.command_executor.execute_safe_command(command)
    
    def remove_package(self, package_name: str) -> Tuple[bool, str, str]:
        """Menghapus paket"""
        command = f"sudo apt remove -y {package_name}"
        return self.command_executor.execute_safe_command(command)
    
    def get_installed_packages(self) -> Tuple[bool, str, str]:
        """Mendapatkan daftar paket yang terinstal"""
        return self.command_executor.execute_command("dpkg -l")
    
    def get_package_info(self, package_name: str) -> Tuple[bool, str, str]:
        """Mendapatkan informasi paket"""
        return self.command_executor.execute_command(f"apt show {package_name}")
