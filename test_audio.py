#!/usr/bin/env python3
"""
Simple audio test using pygame to match project dependencies.
"""

import os, sys
from pathlib import Path

# Ensure we run under the project venv, not system Python
BASE = Path(__file__).resolve().parent
VENV_PY = BASE / 'venv' / 'bin' / 'python3'
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), __file__] + sys.argv[1:])

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

def test_audio():
    # Use current repo directory
    sound_file = Path(__file__).resolve().parent / "key_press.wav"
    
    print(f"Testing audio file: {sound_file}")
    
    if not sound_file.exists():
        print(f"Error: Sound file not found at {sound_file}")
        print("Hint: run './sound_control.sh switch blue' to set a current sound.")
        return False
    
    try:
        print("Initializing pygame mixer...")
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        print("Loading audio file...")
        sound = pygame.mixer.Sound(str(sound_file))
        
        print("Playing sound...")
        ch = sound.play()
        # Wait briefly for playback
        start = time.time()
        while pygame.mixer.get_busy() and time.time() - start < 2.0:
            time.sleep(0.05)
        
        print("Audio test completed.")
        return True
        
    except Exception as e:
        print(f"Audio test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_audio()
    sys.exit(0 if success else 1)
