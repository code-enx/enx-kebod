#!/usr/bin/env python3
# Suppress pygame welcome message
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
"""
Enhanced Keyboard Sound Daemon
Features:
- Automatic volume reduction for headphones
- Global hotkeys for control (Shift+Up/Down, Ctrl+Shift+S)
- Sound cycling capability
- Headphone detection (wired/Bluetooth)
"""

import os
import sys
from pathlib import Path
BASE = Path(__file__).resolve().parent
VENV_PY = BASE / 'venv' / 'bin' / 'python3'
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), __file__] + sys.argv[1:])

import json
import subprocess
from pathlib import Path
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Listener
import pygame
import signal
import threading
import time
import psutil
import glob

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
SOUND_DIR = BASE_DIR / "generated_sounds"
CURRENT_SOUND_FILE = BASE_DIR / "key_press.wav"
PID_FILE = Path.home() / ".keyboard_sound_daemon.pid"
CONFIG_FILE = Path.home() / ".keyboard_sound_config.json"

# Available sound types (in order for cycling)
SOUND_TYPES = ['blue', 'brown', 'red', 'mechanical', 'typewriter', 'creamy', 'dry', 
               'thock', 'clicky', 'silent', 'tactile', 'lofi', 'gx_feryn', 'lee_sin', 'hacker', 'hard']

class AudioDeviceDetector:
    """Detects audio output devices and determines if headphones are connected"""
    
    @staticmethod
    def detect_headphones():
        """Detect if headphones (wired or Bluetooth) are connected"""
        try:
            # Method 1: Check PulseAudio/PipeWire sinks for headphone indicators
            try:
                pa_result = subprocess.run(['pactl', 'list', 'sinks'], capture_output=True, text=True, timeout=5)
                if pa_result.returncode == 0:
                    output_lower = pa_result.stdout.lower()
                    # Look for headphone/headset indicators
                    headphone_indicators = ['headphone', 'headset', 'usb audio', 'usb-audio', 'usb_audio']
                    if any(indicator in output_lower for indicator in headphone_indicators):
                        return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            # Method 2: Check ALSA for headphone/USB devices
            try:
                result = subprocess.run(['aplay', '-l'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    output_lower = result.stdout.lower()
                    # Look for USB audio or headphone indicators
                    usb_indicators = ['usb audio', 'usb-audio', 'headphone', 'headset']
                    if any(indicator in output_lower for indicator in usb_indicators):
                        return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            # Method 3: Check for Bluetooth audio devices
            try:
                bt_result = subprocess.run(['bluetoothctl', 'devices'], capture_output=True, text=True, timeout=3)
                if bt_result.returncode == 0:
                    bt_devices = bt_result.stdout.lower()
                    if bt_devices.strip():  # If there are any Bluetooth devices
                        # Check if any are connected
                        bt_info = subprocess.run(['bluetoothctl', 'info'], capture_output=True, text=True, timeout=3)
                        if 'connected: yes' in bt_info.stdout.lower():
                            audio_indicators = ['headphone', 'headset', 'speaker', 'audio']
                            if any(indicator in bt_devices for indicator in audio_indicators):
                                return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            
            # Method 4: Check /proc/asound/cards for USB/headphone devices
            try:
                with open('/proc/asound/cards', 'r') as f:
                    cards_content = f.read().lower()
                    if any(indicator in cards_content for indicator in ['usb-audio', 'headphone', 'headset']):
                        return True
            except (IOError, FileNotFoundError):
                pass
                    
        except Exception:
            pass
        
        return False
    
    @staticmethod
    def get_volume_multiplier():
        """Get volume multiplier based on audio device"""
        if AudioDeviceDetector.detect_headphones():
            return 0.1  # Reduce volume to 10% for headphones (very quiet)
        return 0.8  # 80% volume for speakers (also reduced from 100%)

class KeyboardSoundDaemonEnhanced:
    def __init__(self):
        self.stop_flag = False
        self.sound = None
        self.volume_multiplier = 1.0
        self.current_sound_index = 0
        self.hotkey_listener = None
        self.pressed_keys = set()
        
        # Load configuration
        self.load_config()
        
        # Write PID file for process management
        try:
            with open(PID_FILE, 'w') as f:
                f.write(str(os.getpid()))
        except IOError:
            pass  # Continue even if we can't write PID file

        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            print("Audio system initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize audio system: {e}")
            print("Daemon will continue but sounds may not work")

        # Load current sound and detect headphones
        self.load_sound()
        self.update_volume()
        
        # Start volume monitoring thread
        self.volume_monitor_thread = threading.Thread(target=self.monitor_audio_devices, daemon=True)
        self.volume_monitor_thread.start()
        
        # Start global hotkey listener
        self.start_hotkey_listener()

    def load_config(self):
        """Load configuration from file"""
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.current_sound_index = config.get('current_sound_index', 0)
                    # Ensure index is within bounds
                    if self.current_sound_index >= len(SOUND_TYPES):
                        self.current_sound_index = 0
            else:
                self.current_sound_index = 0
        except (json.JSONDecodeError, IOError):
            self.current_sound_index = 0

    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'current_sound_index': self.current_sound_index,
                'current_sound_type': SOUND_TYPES[self.current_sound_index]
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError:
            pass

    def load_sound(self):
        """Load the current sound file"""
        if CURRENT_SOUND_FILE.exists():
            try:
                self.sound = pygame.mixer.Sound(str(CURRENT_SOUND_FILE))
                print(f"Loaded sound: {CURRENT_SOUND_FILE}")
            except Exception as e:
                print(f"Error loading sound: {e}")
                self.sound = None
        else:
            print(f"Sound file not found: {CURRENT_SOUND_FILE}")

    def update_volume(self):
        """Update volume based on current audio device"""
        self.volume_multiplier = AudioDeviceDetector.get_volume_multiplier()
        if self.sound:
            try:
                self.sound.set_volume(self.volume_multiplier)
                device_type = "headphones" if self.volume_multiplier == 0.1 else "speakers"
                print(f"Volume adjusted for {device_type}: {int(self.volume_multiplier * 100)}%")
            except Exception:
                pass

    def monitor_audio_devices(self):
        """Monitor for audio device changes"""
        last_headphone_state = AudioDeviceDetector.detect_headphones()
        
        while not self.stop_flag:
            try:
                current_headphone_state = AudioDeviceDetector.detect_headphones()
                if current_headphone_state != last_headphone_state:
                    self.update_volume()
                    last_headphone_state = current_headphone_state
                time.sleep(5)  # Check every 5 seconds
            except Exception:
                pass

    def cycle_sound(self):
        """Cycle to the next sound in the list"""
        self.current_sound_index = (self.current_sound_index + 1) % len(SOUND_TYPES)
        current_sound_type = SOUND_TYPES[self.current_sound_index]
        
        # Update the current sound file
        sound_file = SOUND_DIR / f"keyboard_{current_sound_type}.wav"
        if sound_file.exists():
            try:
                # Copy the new sound to the current sound file
                subprocess.run(['cp', str(sound_file), str(CURRENT_SOUND_FILE)], check=True)
                self.load_sound()
                self.update_volume()
                self.save_config()
                
                print(f"Switched to sound: {current_sound_type}")
                
                # Show notification (if available)
                try:
                    subprocess.run([
                        'notify-send', 
                        'enx-kebord', 
                        f'Switched to: {current_sound_type}',
                        '-t', '2000'
                    ], check=False, timeout=5)
                except:
                    pass
                    
            except subprocess.SubprocessError as e:
                print(f"Error switching sound: {e}")

    def start_hotkey_listener(self):
        """Start the global hotkey listener"""
        def on_press(key):
            try:
                self.pressed_keys.add(key)
                
                # Check for hotkey combinations
                if self.is_hotkey_pressed([Key.shift, Key.up]):
                    self.start_daemon()
                elif self.is_hotkey_pressed([Key.shift, Key.down]):
                    self.stop_daemon()
                elif self.is_hotkey_pressed([Key.ctrl, Key.shift, KeyCode.from_char('s')]):
                    self.cycle_sound()
            except Exception:
                pass

        def on_release(key):
            try:
                self.pressed_keys.discard(key)
            except Exception:
                pass
            return not self.stop_flag

        try:
            self.hotkey_listener = Listener(on_press=on_press, on_release=on_release)
            self.hotkey_listener.daemon = True
            self.hotkey_listener.start()
            print("Global hotkeys enabled")
        except Exception as e:
            print(f"Warning: Could not start hotkey listener: {e}")

    def is_hotkey_pressed(self, key_combination):
        """Check if a specific hotkey combination is pressed"""
        return all(key in self.pressed_keys for key in key_combination)

    def start_daemon(self):
        """Handle daemon start hotkey (placeholder - daemon is already running)"""
        try:
            subprocess.run([
                'notify-send', 
                'enx-kebord daemon', 
                'Already running',
                '-t', '1000'
            ], check=False, timeout=5)
        except:
            pass

    def stop_daemon(self):
        """Handle daemon stop hotkey"""
        print("Stopping daemon via hotkey...")
        self.stop_flag = True
        try:
            subprocess.run([
                'notify-send', 
                'enx-kebord daemon', 
                'Stopping daemon...',
                '-t', '1000'
            ], check=False, timeout=5)
        except:
            pass

    def play_sound(self):
        """Play the sound"""
        if self.stop_flag or not self.sound:
            return

        try:
            self.sound.play()
        except Exception:
            pass  # Silently ignore audio errors

    def on_press(self, key):
        """Handle key press - play sound"""
        if not self.stop_flag:
            self.play_sound()
        return not self.stop_flag  # Continue listening unless stopped

    def on_release(self, key):
        """Handle key release - no special actions needed"""
        return not self.stop_flag  # Continue listening unless stopped

    def signal_handler(self, signum, frame):
        """Handle termination signals"""
        print(f"Received signal {signum}, stopping daemon...")
        self.stop_flag = True
        
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up daemon resources...")
        try:
            pygame.mixer.quit()
        except:
            pass
        
        # Stop hotkey listener
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
            except:
                pass
        
        # Remove PID file
        try:
            if PID_FILE.exists():
                PID_FILE.unlink()
        except:
            pass

    def run(self):
        """Main daemon loop"""
        print("Starting enx-kebord daemon...")
        print(f"Current sound: {SOUND_TYPES[self.current_sound_index]}")
        print("Global hotkeys: Ctrl+Shift+S (cycle), Shift+↑ (start), Shift+↓ (stop)")
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

        try:
            with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
                
                # Keep the daemon running
                while not self.stop_flag:
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"Daemon error: {e}")
        finally:
            self.cleanup()
            print("Daemon stopped")

if __name__ == "__main__":
    try:
        daemon = KeyboardSoundDaemonEnhanced()
        daemon.run()
    except KeyboardInterrupt:
        print("Daemon stopped by user")
    except Exception as e:
        print(f"Daemon error: {e}")
        sys.exit(1)
