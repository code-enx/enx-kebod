#!/bin/bash
# Enhanced Keyboard Sound Daemon Setup Script

echo "🎵 Setting up Enhanced Keyboard Sound Daemon..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"

# Generate all sounds if they don't exist
if [ ! -f "generated_sounds/keyboard_hard.wav" ]; then
    echo "🎵 Generating all keyboard sounds (this may take a moment)..."
    "$(pwd)/venv/bin/python3" sound_generator.py --type all > /dev/null
    echo "✅ All sounds generated"
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x *.sh *.py
echo "✅ Scripts made executable"

# Set default sound if key_press.wav doesn't exist
if [ ! -f "key_press.wav" ]; then
    echo "🎵 Setting default sound (blue)..."
    cp generated_sounds/keyboard_blue.wav key_press.wav
    echo "✅ Default sound set"
fi

echo ""
echo "🎉 Enhanced Keyboard Sound Daemon is ready!"
echo ""
echo "🚀 QUICK START:"
echo "  ./keyboard_sound_control.sh start    # Start the daemon"
echo "  ./sound_control.sh hotkeys          # View all hotkeys"
echo "  ./sound_control.sh current          # Check current sound"
echo ""
echo "⌨️  NEW HOTKEYS (work anywhere):"
echo "  Shift + ↑       - Start daemon"
echo "  Shift + ↓       - Stop daemon"  
echo "  Ctrl+Shift+S    - Cycle through sounds"
echo ""
echo "🎵 NEW FEATURES:"
echo "  • Automatic volume reduction for headphones"
echo "  • 16 different keyboard sounds (including new 'hard' sound)"
echo "  • Global hotkey support"
echo "  • Sound cycling with notifications"
echo "  • Enhanced control scripts"
echo ""
echo "💡 TIPS:"
echo "  • Use './sound_control.sh' for advanced sound management"
echo "  • Notifications will show when switching sounds"
echo "  • Volume automatically adjusts for headphones vs speakers"
echo ""
echo "Ready to start? Run: ./keyboard_sound_control.sh start"