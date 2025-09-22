#!/bin/bash
# ENX-Kebord Uninstall Script

echo "🗑️  ENX-Kebord Uninstaller"
echo "=========================="
echo ""

# Stop daemon if running
echo "⏹️  Stopping daemon..."
if [ -f ~/.local/share/enx-kebord/keyboard_sound_control.sh ]; then
    ~/.local/share/enx-kebord/keyboard_sound_control.sh stop 2>/dev/null || true
fi
if [ -f ./keyboard_sound_control.sh ]; then
    ./keyboard_sound_control.sh stop 2>/dev/null || true
fi

# Remove application files
echo "🗂️  Removing application files..."
rm -rf ~/.local/share/enx-kebord
echo "   ✅ ~/.local/share/enx-kebord removed"

# Remove desktop entries
echo "🖥️  Removing desktop integration..."
rm -f ~/.local/share/applications/enx-kebord.desktop
rm -f ~/.config/autostart/enx-kebord-daemon.desktop
echo "   ✅ Desktop entries removed"

# Remove launcher
echo "🔗 Removing command launcher..."
rm -f ~/.local/bin/enx-kebord
echo "   ✅ Command launcher removed"

# Remove configuration files
echo "⚙️  Removing configuration files..."
rm -f ~/.enx_kebord_config.json
rm -f ~/.keyboard_sound_config.json
rm -f ~/.keyboard_sound_daemon.pid
echo "   ✅ Configuration files removed"

# Remove icons
echo "🎨 Removing icons..."
rm -f ~/.local/share/icons/enx-kebord-icon.png
echo "   ✅ Icons removed"

echo ""
echo "✅ ENX-Kebord has been completely uninstalled!"
echo ""
echo "💡 If you installed from source directory, you can also remove:"
echo "   rm -rf /path/to/your/enx-kebord/source"
echo ""
echo "🔄 You may need to restart your session to fully remove menu entries."