#!/usr/bin/env python3
"""
Test headphone detection manually
"""
import os, sys
from pathlib import Path

# Ensure venv is used
BASE = Path(__file__).resolve().parent
VENV_PY = BASE / 'venv' / 'bin' / 'python3'
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), __file__] + sys.argv[1:])

import subprocess

def test_detection():
    print("🎧 Testing Headphone Detection Methods:")
    print("=" * 50)
    
    headphone_detected = False
    
    # Method 1: PulseAudio/PipeWire
    print("\n1. PulseAudio/PipeWire Detection:")
    try:
        result = subprocess.run(['pactl', 'list', 'sinks'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            output_lower = result.stdout.lower()
            headphone_indicators = ['headphone', 'headset', 'usb audio', 'usb-audio', 'usb_audio']
            found_indicators = [ind for ind in headphone_indicators if ind in output_lower]
            if found_indicators:
                print(f"   ✅ Found: {found_indicators}")
                headphone_detected = True
            else:
                print("   ❌ No headphone indicators found")
            print(f"   📝 Output sample: {output_lower[:200]}...")
        else:
            print("   ❌ pactl command failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Method 2: ALSA
    print("\n2. ALSA Detection:")
    try:
        result = subprocess.run(['aplay', '-l'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            output_lower = result.stdout.lower()
            usb_indicators = ['usb audio', 'usb-audio', 'headphone', 'headset']
            found_indicators = [ind for ind in usb_indicators if ind in output_lower]
            if found_indicators:
                print(f"   ✅ Found: {found_indicators}")
                headphone_detected = True
            else:
                print("   ❌ No USB/headphone indicators found")
            print(f"   📝 Output: {result.stdout}")
        else:
            print("   ❌ aplay command failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Method 3: /proc/asound/cards
    print("\n3. /proc/asound/cards Detection:")
    try:
        with open('/proc/asound/cards', 'r') as f:
            cards_content = f.read().lower()
            indicators = ['usb-audio', 'headphone', 'headset']
            found_indicators = [ind for ind in indicators if ind in cards_content]
            if found_indicators:
                print(f"   ✅ Found: {found_indicators}")
                headphone_detected = True
            else:
                print("   ❌ No headphone indicators found")
            print(f"   📝 Content: {cards_content}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Method 4: Bluetooth
    print("\n4. Bluetooth Detection:")
    try:
        bt_result = subprocess.run(['bluetoothctl', 'devices'], capture_output=True, text=True, timeout=3)
        if bt_result.returncode == 0 and bt_result.stdout.strip():
            bt_devices = bt_result.stdout.lower()
            print(f"   📝 Bluetooth devices: {bt_result.stdout}")
            
            bt_info = subprocess.run(['bluetoothctl', 'info'], capture_output=True, text=True, timeout=3)
            if 'connected: yes' in bt_info.stdout.lower():
                audio_indicators = ['headphone', 'headset', 'speaker', 'audio']
                found_indicators = [ind for ind in audio_indicators if ind in bt_devices]
                if found_indicators:
                    print(f"   ✅ Found connected: {found_indicators}")
                    headphone_detected = True
                else:
                    print("   ❌ No audio devices connected")
            else:
                print("   ❌ No Bluetooth devices connected")
        else:
            print("   ❌ No Bluetooth devices found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 FINAL RESULT: {'🎧 Headphones DETECTED' if headphone_detected else '🔊 Speakers/No headphones detected'}")
    
    if headphone_detected:
        print("🔉 Volume will be set to 10% (very quiet)")
    else:
        print("🔊 Volume will be set to 80% (normal)")
    
    return headphone_detected

if __name__ == "__main__":
    test_detection()
