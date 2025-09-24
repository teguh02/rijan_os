"""
Backup & Restore untuk RijanOS Assistant
Menangani backup dan restore sistem
"""

import os
import subprocess
import shutil
from datetime import datetime
from typing import Tuple, List, Optional
from .command_executor import CommandExecutor

class BackupRestore:
    """Kelas untuk backup dan restore sistem"""
    
    def __init__(self, config_path: str = "config.json"):
        """Inisialisasi BackupRestore"""
        self.config_path = config_path
        self.command_executor = CommandExecutor(config_path)
    
    def create_backup(self, source_path: str, output_path: str, 
                     format_type: str = "tar.gz") -> Tuple[bool, str, str]:
        """
        Membuat backup dari path tertentu
        
        Args:
            source_path: Path yang akan di-backup
            output_path: Path output backup
            format_type: Format backup (tar.gz, zip, 7z)
            
        Returns:
            Tuple berisi (success, stdout, stderr)
        """
        if not os.path.exists(source_path):
            return False, "", f"Source path tidak ditemukan: {source_path}"
        
        # Tambahkan timestamp ke nama file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(output_path)
        name, ext = os.path.splitext(base_name)
        if not ext:
            ext = f".{format_type}"
        
        final_output = f"{name}_{timestamp}{ext}"
        
        try:
            if format_type == "tar.gz":
                return self._create_tar_backup(source_path, final_output)
            elif format_type == "zip":
                return self._create_zip_backup(source_path, final_output)
            elif format_type == "7z":
                return self._create_7z_backup(source_path, final_output)
            else:
                return False, "", f"Format tidak didukung: {format_type}"
                
        except Exception as e:
            return False, "", f"Error membuat backup: {str(e)}"
    
    def _create_tar_backup(self, source_path: str, output_path: str) -> Tuple[bool, str, str]:
        """Membuat backup dengan tar.gz"""
        command = f"tar -czf {output_path} -C {os.path.dirname(source_path)} {os.path.basename(source_path)}"
        return self.command_executor.execute_command(command)
    
    def _create_zip_backup(self, source_path: str, output_path: str) -> Tuple[bool, str, str]:
        """Membuat backup dengan zip"""
        try:
            if os.path.isfile(source_path):
                shutil.make_archive(output_path.replace('.zip', ''), 'zip', os.path.dirname(source_path), os.path.basename(source_path))
            else:
                shutil.make_archive(output_path.replace('.zip', ''), 'zip', source_path)
            return True, f"Backup berhasil dibuat: {output_path}", ""
        except Exception as e:
            return False, "", f"Error membuat zip backup: {str(e)}"
    
    def _create_7z_backup(self, source_path: str, output_path: str) -> Tuple[bool, str, str]:
        """Membuat backup dengan 7z"""
        command = f"7z a {output_path} {source_path}"
        return self.command_executor.execute_command(command)
    
    def restore_backup(self, backup_path: str, target_path: str) -> Tuple[bool, str, str]:
        """
        Restore backup ke path tertentu
        
        Args:
            backup_path: Path file backup
            target_path: Path tujuan restore
            
        Returns:
            Tuple berisi (success, stdout, stderr)
        """
        if not os.path.exists(backup_path):
            return False, "", f"File backup tidak ditemukan: {backup_path}"
        
        try:
            if backup_path.endswith('.tar.gz'):
                return self._restore_tar_backup(backup_path, target_path)
            elif backup_path.endswith('.zip'):
                return self._restore_zip_backup(backup_path, target_path)
            elif backup_path.endswith('.7z'):
                return self._restore_7z_backup(backup_path, target_path)
            else:
                return False, "", f"Format backup tidak didukung: {backup_path}"
                
        except Exception as e:
            return False, "", f"Error restore backup: {str(e)}"
    
    def _restore_tar_backup(self, backup_path: str, target_path: str) -> Tuple[bool, str, str]:
        """Restore backup tar.gz"""
        os.makedirs(target_path, exist_ok=True)
        command = f"tar -xzf {backup_path} -C {target_path}"
        return self.command_executor.execute_command(command)
    
    def _restore_zip_backup(self, backup_path: str, target_path: str) -> Tuple[bool, str, str]:
        """Restore backup zip"""
        try:
            os.makedirs(target_path, exist_ok=True)
            shutil.unpack_archive(backup_path, target_path)
            return True, f"Restore berhasil ke: {target_path}", ""
        except Exception as e:
            return False, "", f"Error restore zip backup: {str(e)}"
    
    def _restore_7z_backup(self, backup_path: str, target_path: str) -> Tuple[bool, str, str]:
        """Restore backup 7z"""
        os.makedirs(target_path, exist_ok=True)
        command = f"7z x {backup_path} -o{target_path}"
        return self.command_executor.execute_command(command)
    
    def list_backup_files(self, directory: str) -> List[str]:
        """Mendapatkan daftar file backup di direktori"""
        backup_files = []
        
        if not os.path.exists(directory):
            return backup_files
        
        for file in os.listdir(directory):
            if file.endswith(('.tar.gz', '.zip', '.7z')):
                backup_files.append(os.path.join(directory, file))
        
        return sorted(backup_files, key=os.path.getmtime, reverse=True)
    
    def get_backup_info(self, backup_path: str) -> dict:
        """Mendapatkan informasi file backup"""
        info = {
            "path": backup_path,
            "size": 0,
            "modified": "",
            "format": ""
        }
        
        if os.path.exists(backup_path):
            stat = os.stat(backup_path)
            info["size"] = stat.st_size
            info["modified"] = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            
            if backup_path.endswith('.tar.gz'):
                info["format"] = "tar.gz"
            elif backup_path.endswith('.zip'):
                info["format"] = "zip"
            elif backup_path.endswith('.7z'):
                info["format"] = "7z"
        
        return info
