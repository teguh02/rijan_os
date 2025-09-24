#!/usr/bin/env python3
"""
Rijan OS Welcome Screen Application
===================================

Aplikasi GUI menggunakan Tkinter yang berfungsi sebagai layar selamat datang
untuk Rijan OS. Aplikasi ini menampilkan 5 slide dengan gambar latar belakang
dan teks informatif tentang sistem operasi Rijan OS.

Fitur:
- Pengecekan file state untuk mencegah tampilnya welcome screen berulang
- 5 slide dengan background image dan overlay teks
- Navigasi dengan tombol Kembali/Selanjutnya/Finish
- Auto-resizing dan scaling gambar
- Interface dalam Bahasa Indonesia
- Desain modern dan profesional

Author: Rijan OS Team
"""

import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import sys
import math
from datetime import datetime


class RijanOSWelcome:
    """
    Kelas utama untuk aplikasi Welcome Screen Rijan OS
    """
    
    def __init__(self):
        """Inisialisasi aplikasi"""
        self.root = tk.Tk()
        self.current_slide = 0
        self.total_slides = 5
        self.images = []
        self.photo_images = []
        self.slide_transition_active = False
        
        # Konten slide dalam Bahasa Indonesia dengan judul dan deskripsi terpisah
        self.slide_contents = [
            {
                "title": "Selamat Datang di Rijan OS",
                "subtitle": "Sistem Operasi Asli Buatan Anak Bangsa",
                "description": "Dirancang ringan, modern, dan ramah pengguna untuk semua kalangan",
                "icon": "🇮🇩"
            },
            {
                "title": "Desain yang Elegan",
                "subtitle": "Perpaduan Sempurna dari Berbagai OS",
                "description": "Menggabungkan keindahan macOS, kemudahan Windows,\ndan kekuatan Linux berbasis KDE Plasma",
                "icon": "✨"
            },
            {
                "title": "Performa Optimal",
                "subtitle": "Ringan dan Cepat",
                "description": "Cocok untuk komputer lama maupun perangkat modern\ndengan optimasi kinerja terdepan",
                "icon": "⚡"
            },
            {
                "title": "Siap Produktif",
                "subtitle": "Aplikasi Lengkap Tersedia",
                "description": "Sudah dilengkapi aplikasi penting seperti\nperamban web, perkantoran, dan multimedia",
                "icon": "💼"
            },
            {
                "title": "Bebas & Aman",
                "subtitle": "Open Source & Transparan",
                "description": "Kode terbuka dengan fokus pada stabilitas,\nkeamanan, dan privasi pengguna",
                "icon": "🔒"
            }
        ]
        
        # Path untuk file state
        self.state_file = Path.home() / ".rijan_welcome_done"
        
        # Tema warna modern
        self.colors = {
            'primary': '#6366f1',      # Indigo modern
            'primary_dark': '#4f46e5', # Indigo gelap
            'secondary': '#8b5cf6',    # Purple
            'accent': '#06b6d4',       # Cyan
            'success': '#10b981',      # Green
            'warning': '#f59e0b',      # Amber
            'danger': '#ef4444',       # Red
            'dark': '#1f2937',         # Gray dark
            'light': '#f9fafb',        # Gray light
            'white': '#ffffff',
            'overlay': '#000000',      # Black overlay
            'text_primary': '#111827',
            'text_secondary': '#6b7280',
            'glass': '#2d3748',        # Glass effect (solid color)
            'glass_light': '#4a5568'   # Lighter glass effect
        }
        
        # Setup aplikasi
        self.setup_window()
        self.load_images()
        self.create_widgets()
        self.show_slide()
    
    def check_state_file(self):
        """
        Cek apakah file state sudah ada
        Jika ada, keluar dari aplikasi
        """
        if self.state_file.exists():
            print("Welcome screen sudah pernah ditampilkan. Keluar dari aplikasi...")
            sys.exit(0)
    
    def setup_window(self):
        """Setup konfigurasi window utama"""
        self.root.title("Selamat Datang di Rijan OS")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Set window properties untuk tampilan modern
        self.root.configure(bg=self.colors['dark'])
        
        # Fullscreen atau maximize window
        try:
            self.root.state('zoomed')  # Windows
        except:
            self.root.attributes('-zoomed', True)  # Linux
        
        # Bind event untuk resize dan animasi
        self.root.bind('<Configure>', self.on_window_resize)
        self.root.bind('<KeyPress>', self.on_key_press)
        
        # Set minimum size
        self.root.minsize(800, 600)
        
        # Center window
        self.center_window()
        
        # Set window icon (jika ada)
        try:
            self.root.iconbitmap('images/icon.ico')
        except:
            pass
    
    def on_key_press(self, event):
        """Handle keyboard navigation"""
        if event.keysym == 'Right' or event.keysym == 'space':
            self.next_slide()
        elif event.keysym == 'Left':
            self.previous_slide()
        elif event.keysym == 'Escape':
            self.root.quit()
        elif event.keysym == 'Home':
            self.current_slide = 0
            self.show_slide()
        elif event.keysym == 'End':
            self.current_slide = self.total_slides - 1
            self.show_slide()
    
    def center_window(self):
        """Posisikan window di tengah layar"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_images(self):
        """Load dan resize gambar wallpaper dengan efek blur untuk background"""
        images_dir = Path("images")
        
        # Jika folder images tidak ada, buat folder dan file placeholder
        if not images_dir.exists():
            self.create_placeholder_images()
        
        # Load gambar wallpaper
        for i in range(1, 6):
            image_path = images_dir / f"wallpaper{i}.jpg"
            if image_path.exists():
                try:
                    img = Image.open(image_path)
                    # Enhance gambar untuk tampilan yang lebih baik
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.1)
                    enhancer = ImageEnhance.Color(img)
                    img = enhancer.enhance(1.2)
                    self.images.append(img)
                except Exception as e:
                    print(f"Error loading {image_path}: {e}")
                    # Buat gambar placeholder jika gagal load
                    self.images.append(self.create_gradient_image(1920, 1080, i))
            else:
                # Buat gambar placeholder dengan gradient yang indah
                self.images.append(self.create_gradient_image(1920, 1080, i))
        
        # Resize gambar sesuai ukuran window
        self.resize_images()
    
    def create_gradient_image(self, width, height, slide_num):
        """Buat gambar gradient yang indah sebagai placeholder"""
        img = Image.new('RGB', (width, height))
        
        # Gradient colors untuk setiap slide
        gradient_colors = [
            ('#667eea', '#764ba2'),  # Blue to purple
            ('#f093fb', '#f5576c'),  # Pink to red
            ('#4facfe', '#00f2fe'),  # Blue to cyan
            ('#43e97b', '#38f9d7'),  # Green to cyan
            ('#fa709a', '#fee140')   # Pink to yellow
        ]
        
        start_color, end_color = gradient_colors[slide_num - 1]
        
        # Convert hex to RGB
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        
        # Create gradient
        for y in range(height):
            ratio = y / height
            r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
            g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
            b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
            
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        return img
    
    def create_color_image(self, width, height, color):
        """Buat gambar solid color sebagai placeholder"""
        img = Image.new('RGB', (width, height), color)
        return img
    
    def create_placeholder_images(self):
        """Buat folder images dan file placeholder jika tidak ada"""
        images_dir = Path("images")
        images_dir.mkdir(exist_ok=True)
        
        print("Folder 'images' dibuat. Silakan tambahkan file wallpaper1.jpg sampai wallpaper5.jpg")
        print("Sementara ini akan menggunakan gambar placeholder berwarna.")
    
    def resize_images(self):
        """Resize gambar sesuai ukuran window saat ini dengan efek blur"""
        window_width = self.root.winfo_width() or 1200
        window_height = self.root.winfo_height() or 800
        
        self.photo_images.clear()
        
        for img in self.images:
            # Resize gambar dengan mempertahankan aspect ratio
            img_resized = img.resize((window_width, window_height), Image.Resampling.LANCZOS)
            
            # Tambahkan efek blur halus untuk background
            img_blurred = img_resized.filter(ImageFilter.GaussianBlur(radius=1.5))
            
            # Tambahkan overlay gelap untuk readability
            overlay = Image.new('RGBA', (window_width, window_height), (0, 0, 0, 60))
            img_with_overlay = Image.alpha_composite(img_blurred.convert('RGBA'), overlay)
            
            photo_img = ImageTk.PhotoImage(img_with_overlay)
            self.photo_images.append(photo_img)
    
    def create_widgets(self):
        """Buat widget-widget GUI dengan desain modern"""
        # Canvas untuk background image
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.colors['dark'])
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Main container dengan glass morphism effect
        self.main_container = tk.Frame(self.canvas, bg=self.colors['glass'], relief='flat', bd=1)
        
        # Icon frame
        self.icon_frame = tk.Frame(self.main_container, bg=self.colors['glass'])
        self.icon_label = tk.Label(
            self.icon_frame,
            text="",
            font=("Segoe UI Emoji", 64),
            bg=self.colors['glass'],
            fg=self.colors['white']
        )
        self.icon_label.pack(pady=(0, 20))
        self.icon_frame.pack(pady=(40, 20))
        
        # Title frame
        self.title_frame = tk.Frame(self.main_container, bg=self.colors['glass'])
        self.title_label = tk.Label(
            self.title_frame,
            text="",
            font=("Segoe UI", 32, "bold"),
            bg=self.colors['glass'],
            fg=self.colors['white'],
            justify=tk.CENTER
        )
        self.title_label.pack()
        self.title_frame.pack(pady=(0, 10))
        
        # Subtitle frame
        self.subtitle_frame = tk.Frame(self.main_container, bg=self.colors['glass'])
        self.subtitle_label = tk.Label(
            self.subtitle_frame,
            text="",
            font=("Segoe UI", 18, "normal"),
            bg=self.colors['glass'],
            fg=self.colors['accent'],
            justify=tk.CENTER
        )
        self.subtitle_label.pack()
        self.subtitle_frame.pack(pady=(0, 20))
        
        # Description frame
        self.description_frame = tk.Frame(self.main_container, bg=self.colors['glass'])
        self.description_label = tk.Label(
            self.description_frame,
            text="",
            font=("Segoe UI", 14),
            bg=self.colors['glass'],
            fg='#e5e7eb',
            justify=tk.CENTER,
            wraplength=700
        )
        self.description_label.pack()
        self.description_frame.pack(pady=(0, 40))
        
        # Progress indicators
        self.progress_frame = tk.Frame(self.main_container, bg=self.colors['glass'])
        self.progress_dots = []
        for i in range(self.total_slides):
            dot = tk.Label(
                self.progress_frame,
                text="●",
                font=("Arial", 16),
                bg=self.colors['glass'],
                fg=self.colors['text_secondary']
            )
            dot.pack(side=tk.LEFT, padx=5)
            self.progress_dots.append(dot)
        self.progress_frame.pack(pady=(0, 40))
        
        # Bottom navigation frame dengan background yang lebih gelap untuk kontras
        self.nav_frame = tk.Frame(self.root, bg=self.colors['dark'], height=100, relief='flat', bd=1)
        self.nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.nav_frame.pack_propagate(False)
        
        # Navigation buttons container
        self.nav_container = tk.Frame(self.nav_frame, bg=self.colors['dark'])
        self.nav_container.pack(expand=True, fill=tk.BOTH)
        
        # Back button dengan hover effect
        self.back_button = tk.Button(
            self.nav_container,
            text="← Kembali",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['text_secondary'],
            fg=self.colors['white'],
            activebackground=self.colors['primary'],
            activeforeground=self.colors['white'],
            relief='flat',
            padx=30,
            pady=15,
            command=self.previous_slide,
            cursor='hand2',
            bd=0
        )
        self.back_button.pack(side=tk.LEFT, padx=30, pady=30)
        
        # Next button dengan gradient effect
        self.next_button = tk.Button(
            self.nav_container,
            text="Selanjutnya →",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            activebackground=self.colors['primary_dark'],
            activeforeground=self.colors['white'],
            relief='flat',
            padx=30,
            pady=15,
            command=self.next_slide,
            cursor='hand2',
            bd=0
        )
        self.next_button.pack(side=tk.RIGHT, padx=30, pady=30)
        
        # Slide counter dengan background yang lebih kontras dan border
        self.counter_label = tk.Label(
            self.nav_container,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['glass'],
            fg=self.colors['white'],
            padx=20,
            pady=10,
            relief='solid',
            bd=1,
            highlightbackground=self.colors['text_secondary'],
            highlightthickness=1
        )
        self.counter_label.pack(pady=20)
        
        # Bind hover effects
        self.setup_hover_effects()
    
    def setup_hover_effects(self):
        """Setup efek hover untuk tombol"""
        # Hover effect untuk back button
        def on_back_enter(event):
            self.back_button.config(bg=self.colors['primary'])
        
        def on_back_leave(event):
            if self.current_slide > 0:
                self.back_button.config(bg=self.colors['text_secondary'])
        
        # Hover effect untuk next button
        def on_next_enter(event):
            if self.current_slide < self.total_slides - 1:
                self.next_button.config(bg=self.colors['primary_dark'])
            else:
                self.next_button.config(bg=self.colors['success'])
        
        def on_next_leave(event):
            if self.current_slide < self.total_slides - 1:
                self.next_button.config(bg=self.colors['primary'])
            else:
                self.next_button.config(bg=self.colors['success'])
        
        self.back_button.bind("<Enter>", on_back_enter)
        self.back_button.bind("<Leave>", on_back_leave)
        self.next_button.bind("<Enter>", on_next_enter)
        self.next_button.bind("<Leave>", on_next_leave)
    
    def show_slide(self):
        """Tampilkan slide saat ini dengan animasi"""
        if not self.photo_images:
            return
        
        if self.slide_transition_active:
            return
            
        self.slide_transition_active = True
        
        # Set background image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_images[self.current_slide])
        
        # Update konten slide
        current_slide = self.slide_contents[self.current_slide]
        self.icon_label.config(text=current_slide['icon'])
        self.title_label.config(text=current_slide['title'])
        self.subtitle_label.config(text=current_slide['subtitle'])
        self.description_label.config(text=current_slide['description'])
        
        # Posisikan content frame di tengah
        self.update_content_position()
        
        # Update tombol navigasi
        self.update_navigation_buttons()
        
        # Update progress indicators
        self.update_progress_indicators()
        
        # Update counter
        self.counter_label.config(text=f"{self.current_slide + 1} dari {self.total_slides}")
        
        # Animasi fade in sederhana
        self.root.after(100, lambda: setattr(self, 'slide_transition_active', False))
    
    def update_content_position(self):
        """Update posisi content frame di tengah canvas"""
        self.root.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Ukuran main container yang lebih besar
        content_width = min(900, canvas_width - 100)
        content_height = min(600, canvas_height - 200)
        
        # Posisi tengah
        x = (canvas_width - content_width) // 2
        y = (canvas_height - content_height) // 2 - 50  # Sedikit ke atas
        
        # Tempatkan main container
        try:
            self.canvas.delete(self.canvas_window)
        except:
            pass
            
        self.canvas_window = self.canvas.create_window(
            x, y, 
            anchor=tk.NW, 
            window=self.main_container,
            width=content_width,
            height=content_height
        )
    
    def update_progress_indicators(self):
        """Update indikator progress dots"""
        for i, dot in enumerate(self.progress_dots):
            if i == self.current_slide:
                dot.config(fg=self.colors['accent'], text="●")
            elif i < self.current_slide:
                dot.config(fg=self.colors['success'], text="●")
            else:
                dot.config(fg=self.colors['text_secondary'], text="○")
    
    def update_navigation_buttons(self):
        """Update status tombol navigasi dengan styling modern"""
        # Tombol Kembali
        if self.current_slide == 0:
            self.back_button.config(
                state=tk.DISABLED,
                bg=self.colors['text_secondary'],
                fg='#9ca3af'
            )
        else:
            self.back_button.config(
                state=tk.NORMAL,
                bg=self.colors['text_secondary'],
                fg=self.colors['white']
            )
        
        # Tombol Selanjutnya/Finish
        if self.current_slide == self.total_slides - 1:
            self.next_button.config(
                text="Selesai ✓",
                bg=self.colors['success'],
                activebackground='#059669'
            )
        else:
            self.next_button.config(
                text="Selanjutnya →",
                bg=self.colors['primary'],
                activebackground=self.colors['primary_dark']
            )
    
    def previous_slide(self):
        """Kembali ke slide sebelumnya"""
        if self.current_slide > 0:
            self.current_slide -= 1
            self.show_slide()
    
    def next_slide(self):
        """Lanjut ke slide berikutnya atau finish"""
        if self.current_slide < self.total_slides - 1:
            self.current_slide += 1
            self.show_slide()
        else:
            self.finish_welcome()
    
    def finish_welcome(self):
        """Selesai welcome screen dengan animasi, buat file state dan keluar"""
        # Animasi fade out sederhana
        self.animate_finish()
    
    def animate_finish(self):
        """Animasi saat finish"""
        # Update tampilan untuk slide terakhir
        self.icon_label.config(text="🎉")
        self.title_label.config(text="Terima Kasih!")
        self.subtitle_label.config(text="Setup Rijan OS Selesai")
        self.description_label.config(text="Selamat menikmati pengalaman Rijan OS\nyang luar biasa!")
        
        # Hide navigation buttons
        self.nav_frame.pack_forget()
        
        # Countdown dan keluar
        self.countdown_and_exit(3)
    
    def countdown_and_exit(self, seconds):
        """Countdown sebelum keluar"""
        if seconds > 0:
            self.description_label.config(
                text=f"Selamat menikmati pengalaman Rijan OS\nyang luar biasa!\n\nMenutup dalam {seconds} detik..."
            )
            self.root.after(1000, lambda: self.countdown_and_exit(seconds - 1))
        else:
            self.create_state_file_and_exit()
    
    def create_state_file_and_exit(self):
        """Buat file state dengan timestamp dan keluar dari aplikasi"""
        try:
            # Buat timestamp
            now = datetime.now()
            timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Tulis timestamp ke file state
            with open(self.state_file, 'w', encoding='utf-8') as f:
                f.write(f"Rijan OS Welcome Screen completed on: {timestamp_str}\n")
                f.write(f"User completed the welcome setup successfully.\n")
                f.write(f"System: {os.name}\n")
                f.write(f"Timestamp (ISO): {now.isoformat()}\n")
            
            print(f"File state dibuat dengan timestamp: {self.state_file}")
            print(f"Completed at: {timestamp_str}")
            print("Welcome screen selesai. Terima kasih telah menggunakan Rijan OS!")
        except Exception as e:
            print(f"Error membuat file state: {e}")
            # Fallback: buat file kosong jika gagal menulis
            try:
                self.state_file.touch()
            except:
                pass
        
        # Keluar dari aplikasi
        self.root.quit()
        self.root.destroy()
    
    def on_window_resize(self, event):
        """Handle event resize window"""
        if event.widget == self.root:
            # Resize gambar ketika window diresize
            self.resize_images()
            # Update tampilan slide
            self.show_slide()
    
    def run(self):
        """Jalankan aplikasi"""
        # Cek file state terlebih dahulu
        self.check_state_file()
        
        print("Memulai Rijan OS Welcome Screen...")
        print("Gunakan tombol navigasi untuk menjelajahi slide.")
        
        # Jalankan main loop
        self.root.mainloop()


def main():
    """Fungsi utama"""
    try:
        app = RijanOSWelcome()
        app.run()
    except KeyboardInterrupt:
        print("\nAplikasi dihentikan oleh user.")
    except Exception as e:
        print(f"Error menjalankan aplikasi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
