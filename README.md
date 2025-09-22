# 🎵 ENX-Kebord - Enhanced Keyboard Sound Manager

**Transform any keyboard into a satisfying mechanical keyboard experience with advanced features**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey)](https://github.com/code-enx/Mech_keyboard_enx-)

*A professional Linux keyboard sound daemon with beautiful GUI, global hotkeys, and intelligent audio management*

## 🚀 Quick Start

\`\`\`bash
# 1. Run the enhanced setup (creates venv, installs deps, generates sounds)
./setup_enhanced.sh

# 2. Start the daemon
./keyboard_sound_control.sh start

# 3. Launch the GUI (optional)
./launch_gui.sh

# 4. Try the global hotkeys!
# Ctrl+Shift+S to cycle sounds
# Shift+↓ to stop, Shift+↑ to start
\`\`\`

**That's it!** Your keyboard now has enhanced mechanical sounds with global controls! 🎉

## ✨ Key Features

### 🎛️ **Beautiful GUI Application**
- Modern Linux-friendly interface with professional styling
- Real-time daemon status monitoring
- Independent volume control for keyboard sounds only
- Audio device detection and management
- Easy sound switching with preview functionality

### 🎵 **16 Realistic Keyboard Sounds**
- **Classic Switches**: Blue (Cherry MX), Brown (Tactile), Red (Linear)
- **Mechanical Variants**: Hard (Aggressive), Thock (Deep), Creamy (Smooth)
- **Vintage & Special**: Typewriter, Lofi, Hacker, and more
- **Physics-based sound synthesis** for realistic audio

### 🎧 **Smart Audio Management**
- **Automatic headphone detection** (wired/Bluetooth)
- **Volume auto-adjustment**: 10% for headphones, 80% for speakers
- **Real-time device switching** support
- **Independent volume control** (doesn't affect system volume)

### ⌨️ **Global Hotkeys (Work Anywhere!)**
- **Ctrl + Shift + S** - Cycle through all 16 sounds
- **Shift + ↑** - Start daemon
- **Shift + ↓** - Stop daemon
- **Visual feedback** via desktop notifications

### 🔄 **Intelligent Sound Application**
- **Real-time file monitoring** - Changes apply instantly without daemon restart
- **Automatic sound reloading** when files are updated
- **Thread-safe audio operations** for stability
- **Backup and recovery** system for sound files

## 📦 Installation

### Prerequisites
- **Python 3.6+** with pip
- **Linux** (Ubuntu/Mint/Debian/Fedora/Arch)
- **Audio system** (ALSA/PulseAudio/PipeWire)
- **Notification system** (libnotify - usually pre-installed)

### One-Command Setup
\`\`\`bash
./setup_enhanced.sh
\`\`\`

### Manual Installation
\`\`\`bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x *.sh *.py

# Generate all sounds
./venv/bin/python3 sound_generator.py --type all

# Start daemon
./keyboard_sound_control.sh start
\`\`\`

## 🎮 Usage

### GUI Application
\`\`\`bash
# Launch the beautiful GUI
./launch_gui.sh

# Or if installed system-wide
enx-kebord
\`\`\`

### Command Line Controls
\`\`\`bash
# Daemon management
./keyboard_sound_control.sh start    # Start daemon
./keyboard_sound_control.sh stop     # Stop daemon
./keyboard_sound_control.sh status   # Check status
./keyboard_sound_control.sh restart  # Restart daemon

# Advanced sound management
./sound_control.sh list              # Show all sounds
./sound_control.sh switch hard       # Switch to specific sound
./sound_control.sh current           # Show current sound + audio device
\`\`\`

## 🔧 How It Works

### Background Daemon
- ✅ **Runs silently** in the background
- ✅ **Monitors keyboard input** system-wide
- ✅ **Plays sounds** with intelligent volume control
- ✅ **File monitoring** - automatically reloads sounds when changed
- ✅ **Audio device detection** - adjusts volume for headphones/speakers

### GUI Application
- ✅ **Opens only when launched** manually
- ✅ **Real-time status** monitoring
- ✅ **Volume control** specifically for keyboard sounds
- ✅ **Sound preview** and switching
- ✅ **Audio device** information and management

### Sound Application Process
1. **Select sound** in GUI dropdown
2. **Click "Apply Sound"** button
3. **File is copied** to active sound location (`key_press.wav`)
4. **Daemon automatically detects** file change within 0.5-1 seconds
5. **Sound is reloaded** and applied immediately
6. **Success notification** confirms the change

## 🛠️ Troubleshooting

### ❌ **"Applied successfully but sound didn't change"** - FIXED! ✅

This was the main issue that has been **COMPLETELY RESOLVED**. The problem was that the daemon wasn't properly monitoring for file changes.

**What was fixed:**
- ✅ **Enhanced file monitoring** - Now checks every 0.5 seconds (was 1 second)
- ✅ **Better file synchronization** - Added `os.sync()` and verification checks
- ✅ **Retry mechanism** - Handles temporary file locks during copy operations
- ✅ **Size verification** - Ensures files are completely copied before reloading
- ✅ **Thread-safe operations** - Prevents race conditions during sound reloading

**Files updated:**
1. `keyboard_sound_daemon_enhanced.py` - Enhanced monitoring and retry logic
2. `enx_kebord_gui.py` - Improved apply function with verification
3. `README.md` - Updated documentation and troubleshooting

### 🔍 **Verification Steps:**
\`\`\`bash
# 1. Check if daemon is running
./keyboard_sound_control.sh status

# 2. Check current sound file
ls -la key_press.wav

# 3. Test sound application
# - Open GUI: ./launch_gui.sh
# - Select a different sound
# - Click "Apply Sound"
# - Type some keys within 1-2 seconds - sound should change!

# 4. Check for notifications
# You should see desktop notifications when sounds are applied and reloaded
\`\`\`

### 🎧 **Audio Issues**
\`\`\`bash
# Test audio detection
./sound_control.sh current

# Check audio systems
pactl list sinks short     # PulseAudio
aplay -l                   # ALSA
bluetoothctl devices       # Bluetooth

# Test sound playback manually
aplay key_press.wav
\`\`\`

### ⌨️ **Global Hotkeys Not Working**
\`\`\`bash
# Check daemon status
./keyboard_sound_control.sh status

# Restart if needed
./keyboard_sound_control.sh restart

# Check permissions
ls -la keyboard_sound_daemon_enhanced.py

# Kill and restart if stuck
./keyboard_sound_control.sh stop
pkill -f keyboard_sound_daemon
./keyboard_sound_control.sh start
\`\`\`

### 🔔 **Notifications Not Showing**
\`\`\`bash
# Test notification system
notify-send "Test" "This is a test notification"

# Install if missing (Ubuntu/Debian)
sudo apt install libnotify-bin

# For other distros
# Fedora: sudo dnf install libnotify
# Arch: sudo pacman -S libnotify
\`\`\`

### **Still Having Issues?**

If sounds still don't apply after the fixes:

1. **Restart the daemon completely:**
   \`\`\`bash
   ./keyboard_sound_control.sh stop
   pkill -f keyboard_sound_daemon  # Force kill any remaining processes
   ./keyboard_sound_control.sh start
   \`\`\`

2. **Check file permissions:**
   \`\`\`bash
   ls -la key_press.wav generated_sounds/
   # All files should be readable/writable by your user
   \`\`\`

3. **Verify sound files exist:**
   \`\`\`bash
   ls -la generated_sounds/keyboard_*.wav
   # Should show 16 sound files
   \`\`\`

4. **Test manual sound switching:**
   \`\`\`bash
   cp generated_sounds/keyboard_hard.wav key_press.wav
   # Then type some keys - should hear the hard sound
   \`\`\`

## 📁 File Structure

\`\`\`
enx-kebord/
├── 🎛️ enx_kebord_gui.py                    # Beautiful GUI application (UPDATED)
├── 🔧 keyboard_sound_daemon_enhanced.py    # Enhanced daemon with file monitoring (UPDATED)
├── 🎵 sound_generator.py                   # Sound generation system
├── 📜 keyboard_sound_control.sh            # Daemon control script
├── 🔊 key_press.wav                        # Current active sound
├── 📁 generated_sounds/                    # All 16 sound files
│   ├── keyboard_blue.wav
│   ├── keyboard_hard.wav
│   └── ... (14 more sounds)
├── 🛠️ setup_enhanced.sh                    # One-click setup
├── 📋 requirements.txt                     # Python dependencies
└── 📚 README.md                           # This documentation (UPDATED)
\`\`\`

## 🎯 What's New in This Version

### 🔄 **MAJOR FIX: Sound Application Issue Resolved**
- **Problem**: Sounds would show "applied successfully" but wouldn't actually change
- **Root Cause**: Daemon file monitoring had timing and synchronization issues
- **Solution**: Complete rewrite of file monitoring system with:
  - **Faster detection** (0.5s instead of 1s)
  - **File synchronization** with `os.sync()`
  - **Size verification** to ensure complete file copies
  - **Retry mechanism** for handling temporary locks
  - **Thread-safe operations** to prevent race conditions

### ✨ **Enhanced Features**
- **Real-time file monitoring** - Detects changes within 0.5-1 seconds
- **Robust error handling** - More informative error messages and recovery
- **Better user feedback** - Clear success/failure notifications
- **Backup system** - Automatic backup of sound files before changes
- **Verification checks** - Ensures files are properly copied before applying

### 🎵 **Sound Profiles Available**
| Sound | Description | Character |
|-------|-------------|-----------|
| `blue` | Cherry MX Blue style | Sharp, clicky |
| `brown` | Cherry MX Brown style | Tactile bump |
| `red` | Cherry MX Red style | Linear, quiet |
| `hard` | Extremely aggressive | Metal-on-metal violence |
| `mechanical` | Heavy mechanical | Loud, satisfying |
| `thock` | Topre-style | Deep, muffled |
| `creamy` | Lubed switches | Smooth, premium |
| `typewriter` | Vintage typewriter | Metallic, classic |
| `lofi` | Chill, warm | Nostalgic, soft |
| `hacker` | Matrix-style | Digital, retro |
| ... | ... | ... |

## 🎉 Ready to Use!

Your **ENX-Kebord** application is now fully functional with the sound application issue **COMPLETELY RESOLVED**. The daemon intelligently monitors for changes and applies them automatically within 1-2 seconds, giving you the seamless mechanical keyboard experience you deserve!

\`\`\`bash
# Get started now
./setup_enhanced.sh
./keyboard_sound_control.sh start

# Launch GUI and try changing sounds - they'll apply instantly!
./launch_gui.sh
\`\`\`

**The "Applied Successfully but No Sound Change" issue is now FIXED!** 🎯

**Transform your typing experience with enhanced mechanical keyboard sounds!** ⌨️✨

---

*Enjoy your enhanced mechanical keyboard experience! 🎵*
