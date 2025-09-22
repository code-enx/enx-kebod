# 🚀 Installing ENX-Kebord from GitHub

## Quick One-Line Installation

```bash
curl -fsSL https://raw.githubusercontent.com/code-enx/enx kebod/main/install.sh | bash -s -- --from-github
```

## Manual Installation

### 1. Clone the Repository
```bash
git clone https://github.com/code-enx/enx kebod.git
cd Mech_keyboard_enx-
```

### 2. Run the Installer
```bash
chmod +x install.sh
./install.sh
```

### 3. Launch the Application
```bash
# From command line
enx-kebord

# Or search "enx-kebord" in your applications menu
```

## System Requirements

- **OS**: Linux (Ubuntu, Debian, Fedora, Arch, Linux Mint, etc.)
- **Python**: 3.6+
- **Audio**: PulseAudio/PipeWire or ALSA
- **Dependencies**: Automatically installed by the installer

## Installation Process

The installer will:
1. ✅ Check system dependencies
2. ✅ Install to `~/.local/share/enx-kebord`
3. ✅ Create virtual environment with all dependencies
4. ✅ Generate all 16 keyboard sounds
5. ✅ Set up desktop integration and menu entries
6. ✅ Configure auto-startup daemon
7. ✅ Add command-line launcher to PATH

## What You Get

- **🎵 16 Keyboard Sounds**: Blue, Brown, Red, Hard, Mechanical, Thock, and more
- **🎛️ Beautiful GUI**: Modern Linux-friendly interface
- **⌨️ Global Hotkeys**: Ctrl+Shift+S (cycle sounds), Shift+↑/↓ (daemon control)
- **🎧 Smart Audio**: Auto-adjusts volume for headphones vs speakers
- **🚀 Auto-Start**: Daemon runs on login, GUI launches on demand

## Uninstallation

```bash
# Remove application files
rm -rf ~/.local/share/enx-kebord

# Remove desktop entries
rm -f ~/.local/share/applications/enx-kebord.desktop
rm -f ~/.config/autostart/enx-kebord-daemon.desktop

# Remove launcher
rm -f ~/.local/bin/enx-kebord

# Remove config
rm -f ~/.enx_kebord_config.json
rm -f ~/.keyboard_sound_config.json
```

## Troubleshooting

### Audio Issues
```bash
# Test audio system
pactl info
aplay -l
```

### Permission Issues
```bash
# Make scripts executable
chmod +x ~/.local/share/enx-kebord/*.sh
chmod +x ~/.local/share/enx-kebord/*.py
```

### Missing Dependencies
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv git alsa-utils pulseaudio-utils

# Fedora
sudo dnf install python3 python3-pip git alsa-utils pulseaudio-utils

# Arch
sudo pacman -S python python-pip git alsa-utils pulseaudio
```

## Support

- !!**Issues**: https://github.com/code-enx/enx kebod/issues
- 📖 **Documentation**: https://github.com/code-enx/enx kebod
- 💬 **Discussions**: https://github.com/code-enx/enx kebod/discussions
