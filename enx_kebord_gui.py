 #!/usr/bin/env python3
 """
 ENX-Kebord GUI Application
 Beautiful Linux-friendly interface for managing keyboard sounds
 """

 # Enforce venv: re-exec with local venv Python if not already using it
 import os, sys
 from pathlib import Path
 BASE = Path(__file__).resolve().parent
 VENV_PY = BASE / 'venv' / 'bin' / 'python3'
 if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
     os.execv(str(VENV_PY), [str(VENV_PY), __file__] + sys.argv[1:])

 import tkinter as tk
 from tkinter import ttk, messagebox, filedialog
 import subprocess
 import json
 import os
 import threading
 import time
 from pathlib import Path

 # Suppress pygame messages
 os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
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

         # Modern Linux styling
         style = ttk.Style()
         style.theme_use('clam')  # Modern flat theme

         # Configure colors for Linux-friendly appearance
         style.configure('Title.TLabel', font=('Ubuntu', 16, 'bold'), foreground='#2c3e50')
         style.configure('Subtitle.TLabel', font=('Ubuntu', 10), foreground='#34495e')
         style.configure('Modern.TFrame', relief='flat', borderwidth=1)
         style.configure('Card.TFrame', relief='solid', borderwidth=1, background='#ecf0f1')

         # Configure button styles
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
         # Main container
         main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="20")
         main_frame.pack(fill=tk.BOTH, expand=True)

         # Header
         self.create_header(main_frame)

         # Status section
         self.create_status_section(main_frame)

         # Volume control section
         self.create_volume_section(main_frame)

         # Sound selection section
         self.create_sound_section(main_frame)

         # Audio device section
         self.create_audio_section(main_frame)

         # Control buttons
         self.create_control_section(main_frame)

         # Footer
         self.create_footer(main_frame)

     def create_header(self, parent):
         """Create header section"""
         header_frame = ttk.Frame(parent, style='Modern.TFrame')
         header_frame.pack(fill=tk.X, pady=(0, 20))

         # App title
         title_label = ttk.Label(header_frame, text="⌨️ enx-kebord", style='Title.TLabel')
         title_label.pack(anchor=tk.W)

         subtitle_label = ttk.Label(header_frame, text="Mechanical Keyboard Sound Manager", style='Subtitle.TLabel')
         subtitle_label.pack(anchor=tk.W)

         # Separator
         ttk.Separator(header_frame, orient='horizontal').pack(fill=tk.X, pady=(10, 0))

     def create_status_section(self, parent):
         """Create status section"""
         status_frame = ttk.LabelFrame(parent, text="🔊 Status", padding="15")
         status_frame.pack(fill=tk.X, pady=(0, 15))

         # Status indicator
         self.status_var = tk.StringVar(value="Checking...")
         self.status_label = ttk.Label(status_frame, textvariable=self.status_var, font=('Ubuntu', 11))
         self.status_label.pack(anchor=tk.W)

         # Current sound info
         self.current_sound_var = tk.StringVar(value="Loading...")
         current_sound_label = ttk.Label(status_frame, textvariable=self.current_sound_var, style='Subtitle.TLabel')
         current_sound_label.pack(anchor=tk.W, pady=(5, 0))

     def create_volume_section(self, parent):
         """Create volume control section"""
         volume_frame = ttk.LabelFrame(parent, text="🔉 Keyboard Sound Volume", padding="15")
         volume_frame.pack(fill=tk.X, pady=(0, 15))

         # Volume slider
         self.volume_var = tk.DoubleVar(value=self.config['volume'] * 100)
         volume_slider = ttk.Scale(
             volume_frame,
             from_=0,
             to=100,
             variable=self.volume_var,
             orient=tk.HORIZONTAL,
             command=self.on_volume_change
         )
         volume_slider.pack(fill=tk.X, pady=(0, 10))

         # Volume percentage display
         self.volume_display_var = tk.StringVar(value=f"{int(self.volume_var.get())}%")
         volume_display = ttk.Label(volume_frame, textvariable=self.volume_display_var, font=('Ubuntu', 10, 'bold'))
         volume_display.pack(anchor=tk.CENTER)

         # Volume presets
         preset_frame = ttk.Frame(volume_frame)
         preset_frame.pack(fill=tk.X, pady=(10, 0))

         ttk.Button(preset_frame, text="Quiet (20%)", command=lambda: self.set_volume_preset(20)).pack(side=tk.LEFT, padx=(0, 5))
         ttk.Button(preset_frame, text="Normal (70%)", command=lambda: self.set_volume_preset(70)).pack(side=tk.LEFT, padx=(0, 5))
         ttk.Button(preset_frame, text="Loud (100%)", command=lambda: self.set_volume_preset(100)).pack(side=tk.LEFT)

     def create_sound_section(self, parent):
         """Create sound selection section"""
         sound_frame = ttk.LabelFrame(parent, text="🎵 Keyboard Sound Profile", padding="15")
         sound_frame.pack(fill=tk.X, pady=(0, 15))

         # Sound selection combobox
         # Find the display name for the current sound
         current_display_name = "Blue (Cherry MX)"  # Default
         for name, key in SOUND_TYPES:
             if key == self.config['current_sound']:
                 current_display_name = name
                 break

         self.sound_var = tk.StringVar(value=current_display_name)
         sound_combo = ttk.Combobox(
             sound_frame,
             textvariable=self.sound_var,
             values=[name for name, _ in SOUND_TYPES],
             state='readonly',
             font=('Ubuntu', 10)
         )
         sound_combo.pack(fill=tk.X, pady=(0, 10))
         sound_combo.bind('<<ComboboxSelected>>', self.on_sound_change)

         # Sound control buttons
         sound_control_frame = ttk.Frame(sound_frame)
         sound_control_frame.pack(fill=tk.X)

         ttk.Button(
             sound_control_frame,
             text="🎵 Test Sound",
             command=self.test_sound,
             style='Primary.TButton'
         ).pack(side=tk.LEFT, padx=(0, 10))

         ttk.Button(
             sound_control_frame,
             text="🔄 Apply Sound",
             command=self.apply_sound,
             style='Success.TButton'
         ).pack(side=tk.LEFT)

     def create_audio_section(self, parent):
         """Create audio device section"""
         audio_frame = ttk.LabelFrame(parent, text="🎧 Audio Device", padding="15")
         audio_frame.pack(fill=tk.X, pady=(0, 15))

         # Audio device info
         self.audio_device_var = tk.StringVar(value="Detecting...")
         audio_label = ttk.Label(audio_frame, textvariable=self.audio_device_var, style='Subtitle.TLabel')
         audio_label.pack(anchor=tk.W)

         # Refresh button
         ttk.Button(
             audio_frame,
             text="🔄 Refresh Audio Info",
             command=self.refresh_audio_info
         ).pack(anchor=tk.W, pady=(10, 0))

     def create_control_section(self, parent):
         """Create daemon control section"""
         control_frame = ttk.LabelFrame(parent, text="🎮 Daemon Control", padding="15")
         control_frame.pack(fill=tk.X, pady=(0, 15))

         button_frame = ttk.Frame(control_frame)
         button_frame.pack(fill=tk.X)

         self.start_button = ttk.Button(
             button_frame,
             text="▶️ Start Daemon",
             command=self.start_daemon,
             style='Success.TButton'
         )
         self.start_button.pack(side=tk.LEFT, padx=(0, 10))

         self.stop_button = ttk.Button(
             button_frame,
             text="⏹️ Stop Daemon",
             command=self.stop_daemon,
             style='Danger.TButton'
         )
         self.stop_button.pack(side=tk.LEFT, padx=(0, 10))

         ttk.Button(
             button_frame,
             text="🔄 Restart",
             command=self.restart_daemon
         ).pack(side=tk.LEFT, padx=(0, 10))

         # Kill process button
         ttk.Button(
             button_frame,
             text="🛑 Kill Process",
             command=self.kill_daemon,
             style='Danger.TButton'
         ).pack(side=tk.LEFT)

         # Hotkeys info
         hotkey_info = ttk.Label(
             control_frame,
             text="💡 Global Hotkeys: Ctrl+Shift+S (cycle), Shift+↑ (start), Shift+↓ (stop)",
             style='Subtitle.TLabel'
         )
         hotkey_info.pack(pady=(10, 0))

     def create_footer(self, parent):
         """Create footer section"""
         footer_frame = ttk.Frame(parent)
         footer_frame.pack(fill=tk.X, pady=(10, 0))

         ttk.Separator(footer_frame, orient='horizontal').pack(fill=tk.X, pady=(0, 10))

         footer_label = ttk.Label(
             footer_frame,
             text="enx-kebord v2.0 | Enhanced Keyboard Sound Experience",
             style='Subtitle.TLabel'
         )
         footer_label.pack(anchor=tk.CENTER)

     def on_volume_change(self, value):
         """Handle volume slider change"""
         volume_percent = int(float(value))
         self.volume_display_var.set(f"{volume_percent}%")
         self.config['volume'] = volume_percent / 100.0
         self.apply_volume()

     def set_volume_preset(self, percent):
         """Set volume to a preset value"""
         self.volume_var.set(percent)
         self.on_volume_change(percent)

     def apply_volume(self):
         """Apply volume to the daemon"""
         # This will be implemented to communicate with the daemon
         self.save_config()

     def on_sound_change(self, event=None):
         """Handle sound selection change"""
         selected_name = self.sound_var.get()
         # Find the corresponding sound key
         for name, key in SOUND_TYPES:
             if name == selected_name:
                 self.config['current_sound'] = key
                 break
         self.save_config()

     def test_sound(self):
         """Test the currently selected sound"""
         try:
             selected_name = self.sound_var.get()
             if not selected_name:
                 messagebox.showerror("Error", "No sound selected")
                 return

             sound_key = None
             for name, key in SOUND_TYPES:
                 if name == selected_name:
                     sound_key = key
                     break

             if not sound_key:
                 messagebox.showerror("Error", f"Invalid sound selection: {selected_name}")
                 return

             sound_file = SOUND_DIR / f"keyboard_{sound_key}.wav"
             if not sound_file.exists():
                 messagebox.showerror("Error", f"Sound file not found: {sound_file}\nPlease check installation or regenerate sounds")
                 return

             try:
                 # Initialize pygame mixer if not already done
                 if not pygame.mixer.get_init():
                     pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

                 # Load and play sound
                 sound = pygame.mixer.Sound(str(sound_file))
                 sound.set_volume(self.config.get('volume', 0.7))
                 sound.play()

                 # Show temporary message
                 self.current_sound_var.set(f"🎵 Testing: {selected_name}")
                 self.root.after(2000, self.update_current_sound_display)

             except pygame.error as pg_error:
                 messagebox.showerror("Error", f"Pygame audio error: {pg_error}\nTry restarting the application or check audio system")
             except Exception as audio_error:
                 messagebox.showerror("Error", f"Audio playback failed: {audio_error}")

         except Exception as e:
             import traceback
             error_details = traceback.format_exc()
             messagebox.showerror("Error", f"Failed to test sound: {str(e)}\n\nDetails:\n{error_details}")
             print(f"Test sound error: {error_details}")

     def apply_sound(self):
         """Apply the selected sound"""
         try:
             selected_name = self.sound_var.get()
             if not selected_name:
                 messagebox.showerror("Error", "No sound selected")
                 return

             sound_key = None
             for name, key in SOUND_TYPES:
                 if name == selected_name:
                     sound_key = key
                     break

             if not sound_key:
                 messagebox.showerror("Error", f"Invalid sound selection: {selected_name}")
                 return

             # Check if sound file exists
             sound_file = SOUND_DIR / f"keyboard_{sound_key}.wav"
             if not sound_file.exists():
                 messagebox.showerror("Error", f"Sound file not found: {sound_file}\nPlease regenerate sounds or check installation")
                 return

             # Check if we can write to the target file
             if not CURRENT_SOUND_FILE.parent.exists():
                 messagebox.showerror("Error", f"Target directory doesn't exist: {CURRENT_SOUND_FILE.parent}")
                 return

             import shutil
             try:
                 # Create a backup of the current sound file if it exists
                 if CURRENT_SOUND_FILE.exists():
                     backup_file = CURRENT_SOUND_FILE.with_suffix('.wav.backup')
                     shutil.copy2(str(CURRENT_SOUND_FILE), str(backup_file))

                 # Copy the new sound file
                 shutil.copy2(str(sound_file), str(CURRENT_SOUND_FILE))

                 import os
                 os.sync()  # Force filesystem sync

                 time.sleep(0.2)

             except PermissionError:
                 messagebox.showerror("Error", f"Permission denied when copying to {CURRENT_SOUND_FILE}")
                 return
             except Exception as copy_error:
                 messagebox.showerror("Error", f"Failed to copy sound file: {copy_error}")
                 return

             # Verify the copy was successful
             if not CURRENT_SOUND_FILE.exists():
                 messagebox.showerror("Error", "Sound file was not copied successfully")
                 return

             if CURRENT_SOUND_FILE.stat().st_size == 0:
                 messagebox.showerror("Error", "Sound file was copied but is empty")
                 return

             if CURRENT_SOUND_FILE.stat().st_size != sound_file.stat().st_size:
                 messagebox.showerror("Error", "Sound file copy verification failed - sizes don't match")
                 return

             # Update config
             self.config['current_sound'] = sound_key
             self.save_config()

             # Update the dropdown to show the selected sound
             self.sound_var.set(selected_name)

             daemon_running = self.config.get('daemon_running', False)
             if daemon_running:
                 success_msg = f"Sound '{selected_name}' applied successfully!\n\nThe daemon will automatically detect and load the new sound within 1-2 seconds."
                 messagebox.showinfo("Success", success_msg)
                 self.current_sound_var.set(f"Applied: {selected_name} (Loading...)")
                 self.root.after(3000, lambda: self.current_sound_var.set(f"Current: {selected_name}"))
             else:
                 success_msg = f"Sound '{selected_name}' applied successfully!\n\nStart the daemon to hear the new sound."
                 messagebox.showinfo("Success", success_msg)
                 self.current_sound_var.set(f"Applied: {selected_name} (Start daemon to activate)")

             try:
                 subprocess.run([
                     'notify-send',
                     'enx-kebord',
                     f"Applied: {selected_name}",
                     '-t', '2000'
                 ], check=False)
             except Exception:
                 pass  # Ignore notification errors

             self.update_current_sound_display()

         except ImportError as e:
             messagebox.showerror("Error", f"Missing required module: {str(e)}")
         except Exception as e:
             import traceback
             error_details = traceback.format_exc()
             messagebox.showerror("Error", f"Failed to apply sound: {str(e)}\n\nDetails:\n{error_details}")
             print(f"Apply sound error: {error_details}")  # Also print to console for debugging

     def refresh_audio_info(self):
         """Refresh audio device information"""
         try:
             # Import the AudioDeviceDetector from the daemon
             import sys
             sys.path.append(str(Path(__file__).parent))
             from keyboard_sound_daemon_enhanced import AudioDeviceDetector

             headphones_detected = AudioDeviceDetector.detect_headphones()
             volume_multiplier = AudioDeviceDetector.get_volume_multiplier()

             if headphones_detected:
                 self.audio_device_var.set(f"🎧 Headphones detected - Volume: {int(volume_multiplier*100)}%")
             else:
                 self.audio_device_var.set(f"🔊 Speakers detected - Volume: {int(volume_multiplier*100)}%")

         except Exception as e:
             # Fallback method
             try:
                 result = subprocess.run(["pactl", "info"], capture_output=True, text=True)
                 if "PulseAudio" in result.stdout or "PipeWire" in result.stdout:
                     self.audio_device_var.set("🔊 Audio system detected")
                 else:
                     self.audio_device_var.set("🔊 Audio system available")
             except:
                 self.audio_device_var.set(f"Audio info unavailable")

     def start_daemon(self):
         """Start the keyboard sound daemon"""
         try:
             result = subprocess.run([str(DAEMON_SCRIPT), "start"], capture_output=True, text=True)
             if result.returncode == 0:
                 messagebox.showinfo("Success", "Daemon started successfully!")
                 self.update_status()
             else:
                 messagebox.showerror("Error", f"Failed to start daemon: {result.stderr}")
         except Exception as e:
             messagebox.showerror("Error", f"Failed to start daemon: {str(e)}")

     def stop_daemon(self):
         """Stop the keyboard sound daemon"""
         try:
             result = subprocess.run([str(DAEMON_SCRIPT), "stop"], capture_output=True, text=True)
             if result.returncode == 0:
                 messagebox.showinfo("Success", "Daemon stopped successfully!")
                 self.update_status()
             else:
                 messagebox.showerror("Error", f"Failed to stop daemon: {result.stderr}")
         except Exception as e:
             messagebox.showerror("Error", f"Failed to stop daemon: {str(e)}")

     def restart_daemon(self):
         """Restart the keyboard sound daemon"""
         try:
             result = subprocess.run([str(DAEMON_SCRIPT), "restart"], capture_output=True, text=True)
             if result.returncode == 0:
                 messagebox.showinfo("Success", "Daemon restarted successfully!")
                 self.update_status()
             else:
                 messagebox.showerror("Error", f"Failed to restart daemon: {result.stderr}")
         except Exception as e:
             messagebox.showerror("Error", f"Failed to restart daemon: {str(e)}")

     def kill_daemon(self):
         """Forcefully kill the daemon process"""
         try:
             import psutil
             import os

             # First try the normal stop command
             result = subprocess.run([str(DAEMON_SCRIPT), "stop"], capture_output=True, text=True, timeout=3)

             # Then look for any remaining processes and kill them
             killed_count = 0
             for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                 try:
                     cmdline = ' '.join(proc.info['cmdline'] or [])
                     if 'keyboard_sound_daemon' in cmdline or 'enx_kebord' in cmdline:
                         proc.kill()
                         killed_count += 1
                 except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                     continue

             # Remove PID file if it exists
             pid_file = Path.home() / ".keyboard_sound_daemon.pid"
             if pid_file.exists():
                 pid_file.unlink()

             if killed_count > 0:
                 messagebox.showinfo("Success", f"Killed {killed_count} process(es) successfully!")
             else:
                 messagebox.showinfo("Info", "No daemon processes found to kill")

             self.update_status()

         except ImportError:
             messagebox.showerror("Error", "psutil not available for process killing")
         except Exception as e:
             messagebox.showerror("Error", f"Failed to kill daemon: {str(e)}")

     def restart_daemon_quietly(self):
         """Restart the daemon quietly without showing messages"""
         try:
             # Start daemon restart in background without waiting
             subprocess.Popen([str(DAEMON_SCRIPT), "restart"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
             # Update status after a short delay
             self.root.after(2000, self.update_status)
         except Exception:
             pass  # Ignore errors for quiet restart

     def update_status(self):
         """Update daemon status display"""
         try:
             result = subprocess.run([str(DAEMON_SCRIPT), "status"], capture_output=True, text=True)
             if "running" in result.stdout.lower():
                 self.status_var.set("✅ Daemon is running")
                 self.config['daemon_running'] = True
                 self.start_button.configure(state='disabled')
                 self.stop_button.configure(state='normal')
             else:
                 self.status_var.set("❌ Daemon is not running")
                 self.config['daemon_running'] = False
                 self.start_button.configure(state='normal')
                 self.stop_button.configure(state='disabled')
         except Exception:
             self.status_var.set("❓ Unable to check daemon status")

         self.update_current_sound_display()

     def update_current_sound_display(self):
         """Update current sound display"""
         current_sound = self.config['current_sound']
         for name, key in SOUND_TYPES:
             if key == current_sound:
                 self.current_sound_var.set(f"Current: {name}")
                 break

     def start_status_monitor(self):
         """Start background status monitoring"""
         def monitor():
             while True:
                 time.sleep(5)  # Update every 5 seconds
                 self.root.after(0, self.update_status)

         monitor_thread = threading.Thread(target=monitor, daemon=True)
         monitor_thread.start()

 def main():
     """Main application entry point"""
     # Initialize pygame for sound testing with optimized settings
     try:
         pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
         pygame.mixer.init()
     except Exception:
         pass  # Continue without sound preview if pygame fails

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
