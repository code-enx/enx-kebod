#!/usr/bin/env python3
"""
Keyboard sound daemon for auto-startup - runs silently in background
"""

# Enforce venv: re-exec with local venv Python if not already using it
import os, sys
from pathlib import Path
BASE = Path(__file__).resolve().parent
VENV_PY = BASE / 'venv' / 'bin' / 'python3'
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), __file__] + sys.argv[1:])

from pathlib import Path
from pynput import keyboard
import pygame
import signal
import threading
import time

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
SOUND_FILE = BASE_DIR / "key_press.wav"
PID_FILE = Path.home() / ".keyboard_sound_daemon.pid"

class KeyboardSoundDaemon:
    def __init__(self):
        self.stop_flag = False
        self.sound = None
        
        # Write PID file for process management
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))

        # Initialize pygame mixer (suppress pygame welcome message)
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
        except Exception as e:
            sys.exit(1)

        # Load sound file 
        if SOUND_FILE.exists():
            try:
                self.sound = pygame.mixer.Sound(str(SOUND_FILE))
            except Exception:
                self.sound = None

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
        self.stop_flag = True
        
    def cleanup(self):
        """Clean up resources"""
        try:
            pygame.mixer.quit()
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
                    
        except Exception:
            pass  # Silently handle any errors
        finally:
            self.cleanup()

if __name__ == "__main__":
    # Redirect stdout and stderr to suppress all output
    devnull = open(os.devnull, 'w')
    sys.stdout = devnull
    sys.stderr = devnull
    
    daemon = KeyboardSoundDaemon()
    daemon.run()
