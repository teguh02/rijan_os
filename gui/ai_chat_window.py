"""
AI Chat Window untuk RijanOS Assistant
Window untuk chat dengan AI Assistant menggunakan Gemini API
"""

import json
import os
import subprocess
import re
from google import genai
from google.genai import types
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QFont, QTextCursor

class AIRequestThread(QThread):
    """Thread untuk request ke Gemini API menggunakan google-genai library"""
    response_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_key, message, role_instruction, model="gemini-2.5-flash-lite"):
        super().__init__()
        self.api_key = api_key
        self.message = message
        self.role_instruction = role_instruction
        self.model = model
    
    def run(self):
        """Menjalankan request ke Gemini API menggunakan genai library"""
        try:
            # Create client dengan API key eksplisit
            client = genai.Client(api_key=self.api_key)
            
            # Generate content dengan system instruction menggunakan model yang dipilih
            response = client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=self.role_instruction
                ),
                contents=self.message
            )
            
            # Emit the response
            self.response_received.emit(response.text)
                
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}")

class AIChatWindow(QWidget):
    """Window untuk chat dengan AI Assistant"""
    
    def __init__(self, config_path="config.json"):
        super().__init__()
        self.config_path = config_path
        self.config = self._load_config()
        self.api_key = self.config.get("gemini_api_key", "")
        # Build role instruction with blocked commands from config
        blocked_commands = self.config.get("blocked_commands", [])
        blocked_commands_text = "\n".join([f"- {cmd}" for cmd in blocked_commands])
        
        self.role_instruction = f"""You are RijanOS AI Assistant. Please give answers in formal Bahasa Indonesia with clear and structured explanations.

You can execute system commands safely. If user requests to run a system command, use this format:
[EXECUTE_COMMAND]command_here[/EXECUTE_COMMAND]

IMPORTANT: The following commands are STRICTLY PROHIBITED and must NEVER be executed:
{blocked_commands_text}

Only execute safe commands that are not in the prohibited list above. Always prioritize system safety and user data protection."""
        
        self.init_ui()
        self.setup_connections()
    
    def _load_config(self):
        """Memuat konfigurasi"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"gemini_api_key": ""}
        except json.JSONDecodeError:
            return {"gemini_api_key": ""}
    
    def update_role_instruction(self):
        """Update role instruction dengan blocked commands terbaru"""
        blocked_commands = self.config.get("blocked_commands", [])
        blocked_commands_text = "\n".join([f"- {cmd}" for cmd in blocked_commands])
        
        self.role_instruction = f"""You are RijanOS AI Assistant. Please give answers in formal Bahasa Indonesia with clear and structured explanations.

You can execute system commands safely. If user requests to run a system command, use this format:
[EXECUTE_COMMAND]command_here[/EXECUTE_COMMAND]

IMPORTANT: The following commands are STRICTLY PROHIBITED and must NEVER be executed:
{blocked_commands_text}

Only execute safe commands that are not in the prohibited list above. Always prioritize system safety and user data protection."""
    
    def reload_config(self):
        """Reload konfigurasi dan update role instruction"""
        self.config = self._load_config()
        self.api_key = self.config.get("gemini_api_key", "")
        self.update_role_instruction()
        self.update_api_status()
    
    def init_ui(self):
        """Inisialisasi UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        self.status_label = QLabel("🤖 AI Assistant")
        self.status_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #0078d4;
            padding: 10px;
        """)
        header_layout.addWidget(self.status_label)
        
        header_layout.addStretch()
        
        # API status
        self.api_status_label = QLabel("❌ API Key tidak tersedia")
        self.api_status_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        header_layout.addWidget(self.api_status_label)
        
        layout.addLayout(header_layout)
        
        # Chat area
        self.create_chat_area(layout)
        
        # Input area
        self.create_input_area(layout)
        
        # Update API status
        self.update_api_status()
    
    def create_chat_area(self, layout):
        """Membuat area chat"""
        # Chat container
        chat_container = QFrame()
        chat_container.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
        """)
        chat_layout = QVBoxLayout(chat_container)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                color: black;
                background-color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.4;
            }
        """)
        
        # Add chat display to layout - THIS WAS MISSING!
        chat_layout.addWidget(self.chat_display)
        
        # Add chat container to main layout
        layout.addWidget(chat_container)
    
    def execute_system_command(self, command):
        """Eksekusi perintah sistem dengan validasi keamanan"""
        try:
            # Load blocked commands from config
            blocked_commands = self.config.get("blocked_commands", [])
            
            # Check if command is blocked
            for blocked in blocked_commands:
                if blocked.lower() in command.lower():
                    self.add_message("system", f"❌ Perintah diblokir untuk keamanan: {command}")
                    return
            
            # Execute command safely
            self.add_message("system", f"🔧 Mengeksekusi perintah: {command}")
            
            # Run command with timeout (5 minutes)
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    self.add_message("system", f"✅ Output:\n{result.stdout.strip()}")
                else:
                    self.add_message("system", "✅ Perintah berhasil dieksekusi")
            else:
                if result.stderr.strip():
                    self.add_message("system", f"❌ Error:\n{result.stderr.strip()}")
                else:
                    self.add_message("system", f"❌ Perintah gagal (exit code: {result.returncode})")
                    
        except subprocess.TimeoutExpired:
            self.add_message("system", "❌ Perintah timeout setelah 5 menit")
        except Exception as e:
            self.add_message("system", f"❌ Error eksekusi perintah: {str(e)}")
        
        chat_layout.addWidget(self.chat_display)
        layout.addWidget(chat_container)
    
    def create_input_area(self, layout):
        """Membuat area input"""
        input_container = QFrame()
        input_container.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: white;
                padding: 10px;
            }
        """)
        input_layout = QVBoxLayout(input_container)
        
        # Input field
        input_row = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Tulis pesan Anda di sini...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        input_row.addWidget(self.message_input)
        
        # Send button
        self.send_btn = QPushButton("📤 Kirim")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)
        input_row.addWidget(self.send_btn)
        
        input_layout.addLayout(input_row)
        layout.addWidget(input_container)
    
    def setup_connections(self):
        """Setup signal connections"""
        pass
    
    def update_api_status(self):
        """Update status API"""
        if self.api_key:
            self.api_status_label.setText("✅ API Key tersedia")
            self.api_status_label.setStyleSheet("color: #28a745; font-weight: bold;")
            self.send_btn.setEnabled(True)
        else:
            self.api_status_label.setText("❌ API Key tidak tersedia")
            self.api_status_label.setStyleSheet("color: #dc3545; font-weight: bold;")
            self.send_btn.setEnabled(False)
            # Status bar removed - no need to show status
    
    def send_message(self):
        """Kirim pesan ke AI"""
        message = self.message_input.text().strip()
        
        if not message:
            return
        
        if not self.api_key:
            self.add_message("system", "Error: API key tidak tersedia. Silakan konfigurasi di Settings.")
            return
        
        # Add user message to chat
        self.add_message("user", message)
        
        # Clear input
        self.message_input.clear()
        
        # Update status
        # Status bar removed
        self.send_btn.setEnabled(False)
        
        # Start AI request thread with selected model
        selected_model = self.config.get("gemini_model", "gemini-2.5-flash-lite")
        self.ai_thread = AIRequestThread(self.api_key, message, self.role_instruction, selected_model)
        self.ai_thread.response_received.connect(self.on_ai_response)
        self.ai_thread.error_occurred.connect(self.on_ai_error)
        self.ai_thread.start()
    
    def add_message(self, sender, message):
        """Tambahkan pesan ke chat display"""
        print(f"DEBUG: Adding message from {sender}: {message[:50]}...")
        
        # Format message with HTML for better display
        if sender == "user":
            formatted_message = f"<p><b>ANDA:</b> {message}</p><hr style='border: 1px solid #ddd; margin: 10px 0;'>"
        elif sender == "ai":
            formatted_message = f"<p><b>🤖 AI ASSISTANT:</b> {message}</p><hr style='border: 1px solid #ddd; margin: 10px 0;'>"
        else:  # system
            formatted_message = f"<p style='color: #666; font-style: italic;'><b>SYSTEM:</b> {message}</p><hr style='border: 1px solid #ccc; margin: 5px 0;'>"
        
        # Use append to add message to history (not overwrite)
        self.chat_display.append(formatted_message)
        self.chat_display.ensureCursorVisible()
        
        # Debug: check current content
        current_content = self.chat_display.toPlainText()
        print(f"DEBUG: Message added to display. Current chat length: {len(current_content)} chars")
        print(f"DEBUG: Current chat display = {current_content[-100:]}")  # Show last 100 chars
    
    def format_message(self, message):
        """Format pesan untuk tampilan yang lebih baik"""
        # Replace newlines with HTML breaks
        formatted = message.replace('\n', '<br>')
        
        # Format code blocks
        import re
        formatted = re.sub(r'```(.*?)```', r'<pre style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; border: 1px solid #e9ecef; font-family: monospace; white-space: pre-wrap;"><code>\1</code></pre>', formatted, flags=re.DOTALL)
        
        # Format inline code
        formatted = re.sub(r'`([^`]+)`', r'<code style="background-color: #f8f9fa; padding: 2px 4px; border-radius: 3px; font-family: monospace;">\1</code>', formatted)
        
        # Format bold text
        formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
        
        # Format italic text
        formatted = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted)
        
        return formatted
    
    def on_ai_response(self, response):
        """Handler ketika mendapat response dari AI"""
        # Check if response contains command to execute
        if "[EXECUTE_COMMAND]" in response and "[/EXECUTE_COMMAND]" in response:
            # Extract command from response
            command_match = re.search(r'\[EXECUTE_COMMAND\](.*?)\[/EXECUTE_COMMAND\]', response, re.DOTALL)
            if command_match:
                command = command_match.group(1).strip()
                # Execute command safely
                self.execute_system_command(command)
                # Remove command tags from response
                response = re.sub(r'\[EXECUTE_COMMAND\].*?\[/EXECUTE_COMMAND\]', '', response, flags=re.DOTALL).strip()
        
        # Use QTimer.singleShot for thread-safe GUI update
        QTimer.singleShot(0, lambda: self.add_message("ai", response))
        QTimer.singleShot(0, lambda: self.send_btn.setEnabled(True))
    
    def on_ai_error(self, error):
        """Handler ketika terjadi error"""
        self.add_message("system", f"Error: {error}")
        # Status bar removed
        self.send_btn.setEnabled(True)
    
    def clear_chat(self):
        """Bersihkan chat"""
        self.chat_display.clear()
        # Add simple clear message
        self.add_message("system", "Chat telah dibersihkan. Silakan mulai percakapan baru!")
    
    def execute_system_command(self, command):
        """Eksekusi perintah sistem dengan validasi keamanan"""
        try:
            # Load blocked commands from config
            blocked_commands = self.config.get("blocked_commands", [])
            
            # Check if command is blocked
            for blocked in blocked_commands:
                if blocked.lower() in command.lower():
                    self.add_message("system", f"❌ Perintah diblokir untuk keamanan: {command}")
                    return
            
            # Execute command safely
            self.add_message("system", f"🔧 Mengeksekusi perintah: {command}")
            
            # Run command with timeout (5 minutes)
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    self.add_message("system", f"✅ Output:\n{result.stdout.strip()}")
                else:
                    self.add_message("system", "✅ Perintah berhasil dieksekusi")
            else:
                if result.stderr.strip():
                    self.add_message("system", f"❌ Error:\n{result.stderr.strip()}")
                else:
                    self.add_message("system", f"❌ Perintah gagal (exit code: {result.returncode})")
                    
        except subprocess.TimeoutExpired:
            self.add_message("system", "❌ Perintah timeout setelah 5 menit")
        except Exception as e:
            self.add_message("system", f"❌ Error eksekusi perintah: {str(e)}")
