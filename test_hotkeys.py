#!/usr/bin/env python3
"""
Simple test to verify global hotkeys are working
Press Ctrl+Shift+Q to quit
"""
import os, sys
from pathlib import Path

# Ensure venv is used
BASE = Path(__file__).resolve().parent
VENV_PY = BASE / 'venv' / 'bin' / 'python3'
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), __file__] + sys.argv[1:])

from pynput import keyboard
from pynput.keyboard import Key, KeyCode
import subprocess

print("🎯 Hotkey Test Started!")
print("Press Ctrl+Shift+Q to quit this test")
print("Try these hotkeys:")
print("  Ctrl+Shift+S - Test sound cycling")
print("  Shift+↑      - Test start daemon")  
print("  Shift+↓      - Test stop daemon")
print("")

pressed_keys = set()

def on_press(key):
    pressed_keys.add(key)
    
    # Test hotkey combinations
    if {Key.ctrl, Key.shift, KeyCode.from_char('q')} <= pressed_keys:
        print("✅ Ctrl+Shift+Q detected - exiting test!")
        return False
    elif {Key.ctrl, Key.shift, KeyCode.from_char('s')} <= pressed_keys:
        print("✅ Ctrl+Shift+S detected - this would cycle sounds!")
        subprocess.run(['notify-send', 'Hotkey Test', 'Ctrl+Shift+S working!'], check=False)
    elif {Key.shift, Key.up} <= pressed_keys:
        print("✅ Shift+↑ detected - this would start daemon!")
        subprocess.run(['notify-send', 'Hotkey Test', 'Shift+Up working!'], check=False)
    elif {Key.shift, Key.down} <= pressed_keys:
        print("✅ Shift+↓ detected - this would stop daemon!")
        subprocess.run(['notify-send', 'Hotkey Test', 'Shift+Down working!'], check=False)

def on_release(key):
    pressed_keys.discard(key)

print("Listening for hotkeys...")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("Hotkey test completed!")