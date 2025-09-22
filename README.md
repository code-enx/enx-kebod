# ⌨️ enx-kebord

**Linux keyboard sound manager with GUI interface**

Transform any keyboard into a satisfying mechanical keyboard experience with our enhanced daemon system and elegant graphical interface.

## 🌟 Features

| Feature | Description |
|---------|-------------|
| **🎵 16 Realistic Sounds** | Blue, Brown, Red, Hard, Mechanical, Thock, Creamy, and more |
| **🎛️ Beautiful GUI** | Modern Linux-friendly interface with volume control |
| **🎧 Smart Volume Control** | Automatic headphone detection and volume adjustment |
| **⌨️ Global Hotkeys** | Control from anywhere: Ctrl+Shift+S, Shift+↑/↓ |
| **🚀 Auto-Startup** | Daemon starts on login, GUI opens only when needed |
| **🔊 Audio Device Support** | Works with speakers, headphones, USB, Bluetooth |
| **💻 Linux Optimized** | Designed specifically for Linux desktop environments |

## 🚀 Quick Installation

### One-Line Install (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/code-enx/enx kebod/main/install.sh | bash
```

### Manual Install
```bash
# Clone the repository
git clone https://github.com/code-enx/enx kebod.git
cd "enx kebod"

# Run the installer
chmod +x install.sh
./install.sh
```

### Development setup (any path, venv-only)
```bash
# Clone the repository to any directory
git clone https://github.com/code-enx/enx kebod.git
cd "enx kebod"

# Setup venv, install deps, generate sounds (uses local venv, not system Python)
./setup_enhanced.sh

# Start the daemon (runs via venv)
./keyboard_sound_control.sh start

# Launch the GUI from source (runs via venv)
./launch_gui.sh

# Optional: run verification
./verify_enx_kebord.sh
```

That's it! The installer will:
- ✅ Check all dependencies
- ✅ Install the application to `~/.local/share/enx-kebord`
- ✅ Create desktop entries and menu integration
- ✅ Set up auto-startup for the daemon
- ✅ Generate all 16 keyboard sounds
- ✅ Use a private virtual environment for performance (no system Python)

## 🎮 Usage

### Launch the GUI
```bash
# From terminal (after install)
enx-kebord

# From source (development)
./launch_gui.sh

# Or search "enx-kebord" in your applications menu
```

### Global Hotkeys (Work Anywhere!)
- **Ctrl + Shift + S** - Cycle through sounds
- **Shift + ↑** - Start daemon
- **Shift + ↓** - Stop daemon

## 🎵 Available Sound Profiles

### 🔵 Classic Mechanical
- **Blue** - Cherry MX Blue style (sharp click)
- **Brown** - Cherry MX Brown style (tactile bump)
- **Red** - Cherry MX Red style (linear, quiet)

### 🔧 Advanced Mechanical  
- **Hard** 🆕 - Extremely aggressive (metal-on-metal)
- **Mechanical** - Heavy IBM Model M style
- **Thock** - Deep Topre-style sound
- **Creamy** - Lubed switches (smooth)
- **Dry** - Unlubricated (scratchy)
- **Clicky** - Extra clicky Box Jade/Navy
- **Silent** - Dampened switches
- **Tactile** - Pronounced tactile bump

### 📝 Vintage & Special
- **Typewriter** - Classic mechanical typewriter
- **Lofi** - Warm, nostalgic chill sound
- **GX Feryn** - Opera GX gaming optimized
- **Lee Sin** - Sharp, precise martial arts
- **Hacker** - Matrix-style retro terminal

## 🎛️ GUI Features

- **Volume Control** - Slider for keyboard sound volume (independent of system)
- **Sound Management** - Dropdown selection and one-click switching
- **Audio Device Detection** - Automatic headphone/speaker detection
- **Daemon Control** - Start/stop/restart/kill from GUI with real-time status
- **Kill Process** - Forceful termination of stuck daemon processes

## ✅ Verification

```bash
# Run sanity checks (path, venv, sounds, launchers)
./verify_enx_kebord.sh
```

## 🎧 Smart Audio Features

### Automatic Volume Adjustment
- **Headphones detected**: Volume reduced to 10% (very quiet)
- **Speakers detected**: Volume set to 80% (comfortable)
- **Real-time switching** when plugging/unplugging devices

## 🗝️ Uninstallation

### Quick Uninstall
```bash
# Download and run uninstaller
curl -fsSL https://raw.githubusercontent.com/code-enx/enx kebod/main/uninstall.sh | bash
```

### Manual Uninstall
```bash
# If you have the source directory
cd /path/to/enx-kebord
./uninstall.sh

# Or remove manually
rm -rf ~/.local/share/enx-kebord
rm -f ~/.local/share/applications/enx-kebord.desktop
rm -f ~/.config/autostart/enx-kebord-daemon.desktop
rm -f ~/.local/bin/enx-kebord
rm -f ~/.enx_kebord_config.json ~/.keyboard_sound_config.json
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

*Made with ❤️ for the Linux community*
