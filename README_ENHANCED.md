<div align="center">

# ⌨️ Enhanced Keyboard Sound Daemon

**Transform any keyboard into a satisfying mechanical keyboard experience with advanced features**

> This project uses its own virtual environment for speed. It is path-agnostic and can live anywhere.
> - Venv: ./venv (created by setup)
> - Sound files: ./generated_sounds (managed by the app)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)](https://github.com/code-enx/Mech_keyboard_enx-)

*An advanced daemon with global hotkeys, headphone detection, and 16 realistic keyboard sounds*

[Quick Start](#-quick-start) • [New Features](#-whats-new) • [Global Hotkeys](#-global-hotkeys) • [Sound Profiles](#-sound-profiles) • [Installation](#-installation)

</div>

---

## 🚀 What's New in Enhanced Version

| 🆕 New Feature | Description |
|----------------|-------------|
| **🎧 Smart Volume** | Automatically reduces volume for headphones (wired/Bluetooth) |
| **⌨️ Global Hotkeys** | Control daemon from anywhere with Shift+Up/Down, Ctrl+Shift+S |
| **🎵 Sound Cycling** | Cycle through 16 sounds with desktop notifications |
| **💾 Sound Memory** | Remembers your preferred sound across restarts |
| **🔊 Hard Sound** | New extremely aggressive mechanical keyboard sound |
| **📱 Notifications** | Desktop notifications when switching sounds |

---

## ⚡ Quick Start

\`\`\`bash
# 1. Run the enhanced setup (creates venv, installs deps, generates sounds)
./setup_enhanced.sh

# 2. Start the daemon (uses venv)
./keyboard_sound_control.sh start

# 3. Launch the GUI (optional, uses venv)
./launch_gui.sh

# 4. Try the new global hotkeys!
# Ctrl+Shift+S to cycle sounds
# Shift+↓ to stop, Shift+↑ to start
\`\`\`

**That's it!** Your keyboard now has enhanced mechanical sounds with global controls! 🎉

---

## ⌨️ Global Hotkeys (Work Anywhere!)

### 🎮 Daemon Control
- **Shift + ↑** - Start daemon (if stopped)
- **Shift + ↓** - Stop daemon instantly

### 🎵 Sound Control  
- **Ctrl + Shift + S** - Cycle through all 16 sounds
  - Shows desktop notification with current sound
  - Automatically saves your preference

### 💡 Hotkey Tips
- Work in **any application** (global system-wide)
- **No need to open terminal** - control everything with keys
- **Visual feedback** via desktop notifications
- **Instant response** - no delays

---

## 🎵 Sound Profiles (16 Total!)

<details>
<summary><strong>🔵 Classic Mechanical Switches</strong></summary>

| Sound | Description | Character |
|-------|-------------|-----------|
| `blue` | Cherry MX Blue style | Sharp, clicky |
| `brown` | Cherry MX Brown style | Tactile bump |
| `red` | Cherry MX Red style | Linear, quiet |

</details>

<details>
<summary><strong>🔧 Mechanical Variants</strong></summary>

| Sound | Description | Character |
|-------|-------------|-----------|
| `mechanical` | Heavy mechanical | Loud, satisfying |
| `creamy` | Lubed switches | Smooth, premium |
| `dry` | Unlubricated | Scratchy, raw |
| `thock` | Topre-style | Deep, muffled |
| `clicky` | Box Jade/Navy | Extra clicky |
| `silent` | Dampened switches | Quiet, subtle |
| `tactile` | Pronounced bump | Sharp tactile |
| `hard` 🆕 | **Extremely aggressive** | **Metal-on-metal violence** |

</details>

<details>
<summary><strong>📝 Vintage & Special</strong></summary>

| Sound | Description | Character |
|-------|-------------|-----------|
| `typewriter` | Vintage typewriter | Metallic, classic |
| `lofi` | Chill, warm | Nostalgic, soft |
| `gx_feryn` | Gaming optimized | Smooth, precise |
| `lee_sin` | Martial arts inspired | Sharp, precise strikes |
| `hacker` | Retro terminal | Matrix-like, digital |

</details>

---

## 🎧 Smart Audio Features

### Automatic Headphone Detection
- **🔍 Detects wired headphones** (USB, 3.5mm)
- **📡 Detects Bluetooth audio devices**
- **🔊 Automatically adjusts volume**
  - 30% volume for headphones (ear protection)
  - 100% volume for speakers
- **⚡ Real-time switching** (plugging/unplugging)

### Supported Audio Systems
- **ALSA** (Advanced Linux Sound Architecture)  
- **PulseAudio** (most modern Linux distros)
- **Bluetooth** via BlueZ stack

---

## 🛠️ Enhanced Controls

### New Sound Control Script
\`\`\`bash
# Advanced sound management
./sound_control.sh list         # Show all available sounds
./sound_control.sh switch hard  # Switch to specific sound
./sound_control.sh current      # Show current sound + audio device
./sound_control.sh hotkeys      # Display all global hotkeys
./sound_control.sh generate     # Generate all sound files
\`\`\`

### Traditional Controls (Still Work)
\`\`\`bash
./keyboard_sound_control.sh start    # Start daemon
./keyboard_sound_control.sh stop     # Stop daemon  
./keyboard_sound_control.sh status   # Check status
./keyboard_sound_control.sh restart  # Restart daemon
\`\`\`

---

## 📚 Installation

### 📍 Prerequisites
- **Python 3.6+** with pip
- **Linux** (Ubuntu/Mint/Debian/Fedora/Arch)
- **Audio system** (ALSA/PulseAudio)
- **Notification system** (libnotify - usually pre-installed)

### 🛠️ Enhanced Setup

\`\`\`bash
# One-command setup (recommended)
./setup_enhanced.sh

# Manual setup (if preferred)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x *.sh *.py
./venv/bin/python3 sound_generator.py --type all
./keyboard_sound_control.sh start
\`\`\`

---

## ⚙️ Configuration

### Config File Location
\`\`\`bash
~/.keyboard_sound_config.json
\`\`\`

### What's Stored
- Current sound preference
- Sound cycling position
- User preferences

### Sound Files Location
\`\`\`bash
./generated_sounds/
├── keyboard_blue.wav
├── keyboard_brown.wav
├── keyboard_hard.wav    # 🆕 New!
└── ... (13 more sounds)
\`\`\`

---

## ✅ Verification

\`\`\`bash
# Run sanity checks (path, venv, sounds, launchers)
./verify_enx_kebord.sh
\`\`\`

## 🔧 Troubleshooting

### Global Hotkeys Not Working
\`\`\`bash
# Check if daemon is running
./keyboard_sound_control.sh status

# Restart if needed  
./keyboard_sound_control.sh restart

# Check for permission issues
ls -la keyboard_sound_daemon_enhanced.py
\`\`\`

### Audio Issues
\`\`\`bash
# Test audio detection
./sound_control.sh current

# Check audio systems
pactl list sinks short     # PulseAudio
aplay -l                   # ALSA
bluetoothctl devices       # Bluetooth
\`\`\`

### Notifications Not Showing
\`\`\`bash
# Test notification system
notify-send "Test" "This is a test notification"

# Install if missing (Ubuntu/Debian)
sudo apt install libnotify-bin
\`\`\`

---

## 🎮 Usage Examples

### Typical Workflow
1. **Start daemon**: `./keyboard_sound_control.sh start`
2. **Use hotkeys to cycle sounds**: Press `Ctrl+Shift+S` until you find your favorite
3. **Stop when needed**: Press `Shift+↓` 
4. **Restart later**: Press `Shift+↑`

### Power User Tips
\`\`\`bash
# Generate a specific sound on demand
python3 sound_generator.py --type hard --duration 0.2

# Switch to hard sound and restart
./sound_control.sh switch hard

# Check what's currently running
./sound_control.sh current
\`\`\`

---

## 📋 File Structure

\`\`\`
enx kebod/
├── 🆕 keyboard_sound_daemon_enhanced.py  # Enhanced daemon
├── 🆕 sound_control.sh                   # Advanced controls
├── 🆕 setup_enhanced.sh                  # One-click setup
├── 📄 sound_generator.py                 # Sound generation (updated)
├── 📜 keyboard_sound_control.sh          # Basic controls (updated)
├── 🔊 key_press.wav                      # Current active sound
├── 📁 generated_sounds/                  # All 16 sound files
│   ├── keyboard_hard.wav    🆕           # New aggressive sound
│   └── ... (15 other sounds)
├── 📋 requirements.txt                   # Dependencies (updated)
└── 📚 README_ENHANCED.md                 # This documentation
\`\`\`

---

## 🚨 What Changed from Original

### New Dependencies
\`\`\`
psutil>=5.8.0    # For system process monitoring
\`\`\`

### New Files
- `keyboard_sound_daemon_enhanced.py` - Main enhanced daemon
- `sound_control.sh` - Advanced sound management
- `setup_enhanced.sh` - One-click setup
- `verify_enx_kebord.sh` - Sanity checks for path, venv, and sounds
- `README_ENHANCED.md` - Enhanced documentation

### Enhanced Files
- `sound_generator.py` - Added "hard" sound profile  
- `switch_sound.sh` - Updated with new sound
- `requirements.txt` - Added psutil dependency
- `keyboard_sound_control.sh` - Points to enhanced daemon

---

## 🎉 Ready to Rock?

\`\`\`bash
# Get started in seconds
./setup_enhanced.sh
./keyboard_sound_control.sh start

# Try the new hotkeys
# Ctrl+Shift+S to cycle sounds!
\`\`\`

**Transform your typing experience with enhanced mechanical keyboard sounds!** ⌨️✨

---

*Enjoy your enhanced mechanical keyboard experience! 🎵*
