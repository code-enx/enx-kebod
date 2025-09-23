# Contributing to Keyboard Sound Daemon

Thank you for your interest in contributing! 🎉

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork:** `git clone https://github.com/code-enx/Mech_keyboard_enx-.git`
3. **Create virtual environment:** `python3 -m venv venv && source venv/bin/activate`
4. **Install dependencies:** `pip install -r requirements.txt`
5. **Make your changes**
6. **Test thoroughly**
7. **Submit a Pull Request**

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Use the [issue tracker](https://github.com/code-enx/Mech_keyboard_enx-/issues)
- Include steps to reproduce
- Mention your OS and Python version

### 💡 Feature Requests
- Check existing issues first
- Describe the use case clearly
- Consider implementation complexity

### 🎵 Sound Packs
- High-quality WAV files (16-bit/44.1kHz)
- 0.1-0.5 seconds duration
- Under 1MB file size
- Submit via Pull Request to `Key_sounds/` folder

### 📚 Documentation
- Fix typos, improve clarity
- Add examples and use cases
- Update installation instructions

## ⚡ Development Tips

- **Test on different platforms** (Linux/macOS/Windows)
- **Follow existing code style**
- **Keep commits atomic and descriptive**
- **Update CHANGELOG.md** for notable changes

## 🔧 Testing

\`\`\`bash
# Test daemon functionality
./keyboard_sound_control.sh start
# Type some keys to verify sounds
./keyboard_sound_control.sh stop

# Test audio system
python3 test_audio.py
\`\`\`

## 📝 Code Style

- Use descriptive variable names
- Add docstrings for functions
- Keep functions focused and small
- Handle errors gracefully

---

**Questions?** Open an issue or start a discussion!

**Happy Contributing!** 🎊
