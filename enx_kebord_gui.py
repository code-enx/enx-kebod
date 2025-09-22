#!/usr/bin/env python3
"""
ENX-Kebord GUI Application
Beautiful Linux-friendly interface for managing keyboard sounds
"""

 # Enforce venv: re-exec with local venv Python if not already using it
 import os
 import sys
 from pathlib import Path

 BASE = Path(__file__).resolve().parent
 VENV_PY = BASE / 'venv' / 'bin' / 'python3'
 if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
     os.execv(str(VENV_PY), [str(VENV_PY), __file__] + sys.argv[1:])

 import tkinter as tk
 from tkinter import ttk, messagebox, filedialog
 import subprocess
 import json
 import threading
 import time
 import pygame

 # Configuration
 CONFIG_FILE = Path.home() / ".enx_kebord_config.json"
 DAEMON_SCRIPT = Path(__file__).parent / "keyboard_sound_control.sh"
 SOUND_DIR = Path(__file__).parent / "generated_sounds"
 CURRENT_SOUND_FILE = Path(__file__).parent / "key_press.wav"

 # Available sound types
 SOUND_TYPES = [
     ('Blue (Cherry MX)', 'blue'),
     ('Brown (Tactile)', 'brown'),
     ('Red (Linear)', 'red'),
     ('Hard (Aggressive)', 'hard'),
     ('Mechanical (Heavy)', 'mechanical'),
     ('Thock (Deep)', 'thock'),
     ('Creamy (Smooth)', 'creamy'),
     ('Dry (Scratchy)', 'dry'),
     ('Clicky (Extra)', 'clicky'),
     ('Silent (Quiet)', 'silent'),
     ('Tactile (Bump)', 'tactile'),
     ('Typewriter (Vintage)', 'typewriter'),
     ('Lofi (Chill)', 'lofi'),
     ('GX Feryn (Gaming)', 'gx_feryn'),
     ('Lee Sin (Sharp)', 'lee_sin'),
     ('Hacker (Matrix)', 'hacker'),
 ]

 class EnxKebordGUI:
     def __init__(self, root):
         self.root = root
         self.setup_window()
         self.load_config()
         self.create_widgets()
         self.update_status()
         self.start_status_monitor()

     def setup_window(self):
         """Setup main window with modern Linux styling"""
         self.root.title("enx-kebord - Keyboard Sound Manager")
         self.root.geometry("480x650")
         self.root.resizable(True, True)

         style = ttk.Style()
         style.theme_use('clam')  # Modern flat theme

         # Configure styles
         style.configure('Title.TLabel', font=('Ubuntu', 16, 'bold'), foreground='#2c3e50')
         style.configure('Subtitle.TLabel', font=('Ubuntu', 10), foreground='#34495e')
         style.configure('Modern.TFrame', relief='flat', borderwidth=1)
         style.configure('Card.TFrame', relief='solid', borderwidth=1, background='#ecf0f1')
         style.configure('Action.TButton', font=('Ubuntu', 10, 'bold'))
         style.configure('Success.TButton', background='#27ae60', foreground='white')
         style.configure('Danger.TButton', background='#e74c3c', foreground='white')
         style.configure('Primary.TButton', background='#3498db', foreground='white')
         self.root.configure(bg='#ecf0f1')

     def load_config(self):
         """Load application configuration"""
         self.config = {
             'volume': 0.7,
             'current_sound': 'blue',
             'auto_start': True,
             'daemon_running': False
         }
         try:
             if CONFIG_FILE.exists():
                 with open(CONFIG_FILE, 'r') as f:
                     saved_config = json.load(f)
                     self.config.update(saved_config)
         except Exception:
             pass

     def save_config(self):
         """Save application configuration"""
         try:
             with open(CONFIG_FILE, 'w') as f:
                 json.dump(self.config, f, indent=2)
         except Exception:
             pass

     def create_widgets(self):
         """Create all GUI widgets"""
         main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="20")
         main_frame.pack(fill=tk.BOTH, expand=True)

         self.create_header(main_frame)
         self.create_status_section(main_frame)
         self.create_volume_section(main_frame)
         self.create_sound_section(main_frame)
         self.create_audio_section(main_frame)
         self.create_control_section(main_frame)
         self.create_footer(main_frame)

     def create_header(self, parent):
         header_frame = ttk.Frame(parent, style='Modern.TFrame')
         header_frame.pack(fill=tk.X, pady=(0, 20))

         title_label = ttk.Label(header_frame, text="⌨️ enx-kebord", style='Title.TLabel')
         title_label.pack(anchor=tk.W)

         subtitle_label = ttk.Label(header_frame, text="Mechanical Keyboard Sound Manager", style='Subtitle.TLabel')
         subtitle_label.pack(anchor=tk.W)

         ttk.Separator(header_frame, orient='horizontal').pack(fill=tk.X, pady=(10, 0))

     # Other GUI section methods remain identical, just ensure 4-space indentation
     # Example for status section:
     def create_status_section(self, parent):
         status_frame = ttk.LabelFrame(parent, text="🔊 Status", padding="15")
         status_frame.pack(fill=tk.X, pady=(0, 15))

         self.status_var = tk.StringVar(value="Checking...")
         self.status_label = ttk.Label(status_frame, textvariable=self.status_var, font=('Ubuntu', 11))
         self.status_label.pack(anchor=tk.W)

         self.current_sound_var = tk.StringVar(value="Loading...")
         current_sound_label = ttk.Label(status_frame, textvariable=self.current_sound_var, style='Subtitle.TLabel')
         current_sound_label.pack(anchor=tk.W, pady=(5, 0))

     # Continue with all other create_XXX methods, using 4-space indentation consistently

     def start_status_monitor(self):
         """Start background status monitoring"""
         def monitor():
             while True:
                 time.sleep(5)
                 self.root.after(0, self.update_status)
         monitor_thread = threading.Thread(target=monitor, daemon=True)
         monitor_thread.start()

 def main():
     """Main application entry point"""
     try:
         pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
         pygame.mixer.init()
     except Exception:
         pass

     root = tk.Tk()
     app = EnxKebordGUI(root)

     # Center window on screen
     root.update_idletasks()
     x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
     y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
     root.geometry(f"+{x}+{y}")

     root.mainloop()

 if __name__ == "__main__":
     main()
