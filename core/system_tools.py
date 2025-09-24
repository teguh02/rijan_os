"""
System Tools untuk RijanOS Assistant
Menangani tools dan utilitas sistem
"""

import os
import webbrowser
from typing import Tuple
from .command_executor import CommandExecutor

class SystemTools:
    """Kelas untuk tools dan utilitas sistem"""
    
    def __init__(self, config_path: str = "config.json"):
        """Inisialisasi SystemTools"""
        self.config_path = config_path
        self.command_executor = CommandExecutor(config_path)
    
    def clear_journal_logs(self, days: int = 7) -> Tuple[bool, str, str]:
        """
        Membersihkan journal logs
        
        Args:
            days: Jumlah hari log yang akan dipertahankan
            
        Returns:
            Tuple berisi (success, stdout, stderr)
        """
        command = f"sudo journalctl --vacuum-time={days}d"
        return self.command_executor.execute_safe_command(command)
    
    def clear_temp_files(self) -> Tuple[bool, str, str]:
        """Membersihkan file temporary"""
        commands = [
            "sudo rm -rf /tmp/*",
            "rm -rf ~/.cache/*"
        ]
        
        results = []
        for cmd in commands:
            success, stdout, stderr = self.command_executor.execute_safe_command(cmd)
            results.append((success, stdout, stderr))
        
        # Gabungkan hasil
        all_success = all(result[0] for result in results)
        combined_stdout = "\n".join([result[1] for result in results if result[1]])
        combined_stderr = "\n".join([result[2] for result in results if result[2]])
        
        return all_success, combined_stdout, combined_stderr
    
    def clear_apt_cache(self) -> Tuple[bool, str, str]:
        """Membersihkan cache APT"""
        return self.command_executor.execute_safe_command("sudo apt clean")
    
    def autoremove_packages(self) -> Tuple[bool, str, str]:
        """Menghapus paket yang tidak terpakai"""
        return self.command_executor.execute_safe_command("sudo apt autoremove -y")
    
    def update_system(self) -> Tuple[bool, str, str]:
        """Update sistem"""
        return self.command_executor.execute_safe_command("sudo apt update")
    
    def upgrade_system(self) -> Tuple[bool, str, str]:
        """Upgrade sistem"""
        return self.command_executor.execute_safe_command("sudo apt update && sudo apt upgrade -y")
    
    def get_system_info(self) -> dict:
        """Mendapatkan informasi sistem"""
        return self.command_executor.get_system_info()
    
    def get_disk_usage(self) -> Tuple[bool, str, str]:
        """Mendapatkan penggunaan disk"""
        return self.command_executor.execute_command("df -h")
    
    def get_memory_usage(self) -> Tuple[bool, str, str]:
        """Mendapatkan penggunaan memory"""
        return self.command_executor.execute_command("free -h")
    
    def get_cpu_info(self) -> Tuple[bool, str, str]:
        """Mendapatkan informasi CPU"""
        return self.command_executor.execute_command("lscpu")
    
    def get_network_info(self) -> Tuple[bool, str, str]:
        """Mendapatkan informasi network"""
        return self.command_executor.execute_command("ip addr show")
    
    def get_running_processes(self) -> Tuple[bool, str, str]:
        """Mendapatkan proses yang berjalan"""
        return self.command_executor.execute_command("ps aux")
    
    def get_system_uptime(self) -> Tuple[bool, str, str]:
        """Mendapatkan uptime sistem"""
        return self.command_executor.execute_command("uptime")
    
    def open_bug_report(self) -> bool:
        """Membuka halaman bug report di browser"""
        try:
            url = "https://github.com/teguh02/rijan_os/issues"
            webbrowser.open(url)
            return True
        except Exception:
            return False
    
    def restart_system(self) -> Tuple[bool, str, str]:
        """Restart sistem (HATI-HATI!)"""
        return self.command_executor.execute_safe_command("sudo reboot")
    
    def shutdown_system(self) -> Tuple[bool, str, str]:
        """Shutdown sistem (HATI-HATI!)"""
        return self.command_executor.execute_safe_command("sudo shutdown -h now")
    
    def schedule_shutdown(self, time_str: str) -> Tuple[bool, str, str]:
        """Jadwalkan shutdown"""
        command = f"sudo shutdown {time_str}"
        return self.command_executor.execute_safe_command(command)
    
    def cancel_scheduled_shutdown(self) -> Tuple[bool, str, str]:
        """Batalkan shutdown yang dijadwalkan"""
        return self.command_executor.execute_safe_command("sudo shutdown -c")
    
    def check_system_health(self) -> dict:
        """Memeriksa kesehatan sistem"""
        health = {
            "disk_usage": False,
            "memory_usage": False,
            "system_load": False,
            "errors": []
        }
        
        # Cek disk usage
        success, stdout, stderr = self.get_disk_usage()
        if success:
            health["disk_usage"] = True
        else:
            health["errors"].append(f"Error cek disk: {stderr}")
        
        # Cek memory usage
        success, stdout, stderr = self.get_memory_usage()
        if success:
            health["memory_usage"] = True
        else:
            health["errors"].append(f"Error cek memory: {stderr}")
        
        # Cek system load
        success, stdout, stderr = self.get_system_uptime()
        if success:
            health["system_load"] = True
        else:
            health["errors"].append(f"Error cek uptime: {stderr}")
        
        return health
    
    def get_system_info(self) -> Tuple[bool, str, str]:
        """Mendapatkan informasi sistem"""
        import platform
        
        info_lines = []
        
        # Deteksi platform sederhana
        if platform.system() == "Windows":
            # Windows commands - hanya yang pasti ada
            try:
                # systeminfo - command paling reliable di Windows
                success, stdout, stderr = self.command_executor.execute_safe_command("systeminfo", timeout=30)
                if success:
                    info_lines.append("=== System Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                else:
                    info_lines.append("=== System Information (ERROR) ===")
                    info_lines.append(f"Error: {stderr}")
                    info_lines.append("")
                
                # whoami - simple command
                success, stdout, stderr = self.command_executor.execute_safe_command("whoami", timeout=10)
                if success:
                    info_lines.append("=== Current User ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                
            except Exception as e:
                info_lines.append(f"Error getting system info: {str(e)}")
        else:
            # Linux commands - hanya yang pasti ada
            try:
                # uname -a - command paling reliable di Linux
                success, stdout, stderr = self.command_executor.execute_safe_command("uname -a", timeout=10)
                if success:
                    info_lines.append("=== System Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                else:
                    info_lines.append("=== System Information (ERROR) ===")
                    info_lines.append(f"Error: {stderr}")
                    info_lines.append("")
                
                # whoami - simple command
                success, stdout, stderr = self.command_executor.execute_safe_command("whoami", timeout=10)
                if success:
                    info_lines.append("=== Current User ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                
            except Exception as e:
                info_lines.append(f"Error getting system info: {str(e)}")
        
        return True, "\n".join(info_lines), ""
    
    def get_hardware_info(self) -> Tuple[bool, str, str]:
        """Mendapatkan informasi hardware"""
        import platform
        
        info_lines = []
        
        # Deteksi platform sederhana
        if platform.system() == "Windows":
            # Windows commands - hanya yang pasti ada
            try:
                # wmic cpu - command paling reliable untuk CPU info
                success, stdout, stderr = self.command_executor.execute_safe_command("wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors /format:list", timeout=20)
                if success:
                    info_lines.append("=== CPU Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                else:
                    info_lines.append("=== CPU Information (ERROR) ===")
                    info_lines.append(f"Error: {stderr}")
                    info_lines.append("")
                
                # wmic memorychip - memory info
                success, stdout, stderr = self.command_executor.execute_safe_command("wmic memorychip get Capacity,Speed,Manufacturer /format:list", timeout=20)
                if success:
                    info_lines.append("=== Memory Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                
            except Exception as e:
                info_lines.append(f"Error getting hardware info: {str(e)}")
        else:
            # Linux commands - hanya yang pasti ada
            try:
                # lscpu - command paling reliable untuk CPU info di Linux
                success, stdout, stderr = self.command_executor.execute_safe_command("lscpu", timeout=15)
                if success:
                    info_lines.append("=== CPU Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                else:
                    info_lines.append("=== CPU Information (ERROR) ===")
                    info_lines.append(f"Error: {stderr}")
                    info_lines.append("")
                
                # free -h - memory info
                success, stdout, stderr = self.command_executor.execute_safe_command("free -h", timeout=10)
                if success:
                    info_lines.append("=== Memory Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                
            except Exception as e:
                info_lines.append(f"Error getting hardware info: {str(e)}")
        
        return True, "\n".join(info_lines), ""
    
    def get_battery_info(self) -> Tuple[bool, str, str]:
        """Mendapatkan informasi battery"""
        import platform
        
        info_lines = []
        
        # Deteksi platform sederhana
        if platform.system() == "Windows":
            # Windows commands - hanya yang pasti ada
            try:
                # wmic battery - command paling reliable untuk battery info di Windows
                success, stdout, stderr = self.command_executor.execute_safe_command("wmic path win32_battery get Name,EstimatedChargeRemaining,Status /format:list", timeout=15)
                if success:
                    info_lines.append("=== Battery Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                else:
                    info_lines.append("=== Battery Information (ERROR) ===")
                    info_lines.append(f"Error: {stderr}")
                    info_lines.append("")
                
            except Exception as e:
                info_lines.append(f"Error getting battery info: {str(e)}")
        else:
            # Linux commands - hanya yang pasti ada
            try:
                # cat /sys/class/power_supply/BAT0/capacity - command paling reliable untuk battery di Linux
                success, stdout, stderr = self.command_executor.execute_safe_command("cat /sys/class/power_supply/BAT0/capacity", timeout=10)
                if success:
                    info_lines.append("=== Battery Information ===")
                    info_lines.append(f"Battery Capacity: {stdout.strip()}%")
                    info_lines.append("")
                else:
                    info_lines.append("=== Battery Information (ERROR) ===")
                    info_lines.append(f"Error: {stderr}")
                    info_lines.append("")
                
            except Exception as e:
                info_lines.append(f"Error getting battery info: {str(e)}")
        
        return True, "\n".join(info_lines), ""
    
    def get_network_info(self) -> Tuple[bool, str, str]:
        """Mendapatkan informasi network"""
        import platform
        
        info_lines = []
        
        # Deteksi platform sederhana
        if platform.system() == "Windows":
            # Windows commands - hanya yang pasti ada
            try:
                # ipconfig /all - command paling reliable untuk network info di Windows
                success, stdout, stderr = self.command_executor.execute_safe_command("ipconfig /all", timeout=20)
                if success:
                    info_lines.append("=== Network Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                else:
                    info_lines.append("=== Network Information (ERROR) ===")
                    info_lines.append(f"Error: {stderr}")
                    info_lines.append("")
                
            except Exception as e:
                info_lines.append(f"Error getting network info: {str(e)}")
        else:
            # Linux commands - hanya yang pasti ada
            try:
                # ip addr show - command paling reliable untuk network info di Linux
                success, stdout, stderr = self.command_executor.execute_safe_command("ip addr show", timeout=15)
                if success:
                    info_lines.append("=== Network Information ===")
                    info_lines.append(stdout.strip())
                    info_lines.append("")
                else:
                    info_lines.append("=== Network Information (ERROR) ===")
                    info_lines.append(f"Error: {stderr}")
                    info_lines.append("")
                
            except Exception as e:
                info_lines.append(f"Error getting network info: {str(e)}")
        
        return True, "\n".join(info_lines), ""
