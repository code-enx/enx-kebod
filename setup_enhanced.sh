#!/bin/bash
# Enhanced Keyboard Sound Daemon Setup Script

echo "🎵 Setting up Enhanced Keyboard Sound Daemon..."
echo ""

echo "📋 Checking system dependencies..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.6+ first."
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is required but not installed. Please install python3-pip first."
    exit 1
fi

# Check for audio system
if ! command -v pactl &> /dev/null && ! command -v aplay &> /dev/null; then
    echo "⚠️  Warning: No audio system detected (PulseAudio/ALSA). Audio may not work."
fi

# Check for notification system
if ! command -v notify-send &> /dev/null; then
    echo "⚠️  Warning: notify-send not found. Install libnotify-bin for notifications."
fi

echo "✅ System dependencies checked"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Check requirements.txt"
    exit 1
fi
echo "✅ Dependencies installed"

# Generate all sounds if they don't exist
if [ ! -f "generated_sounds/keyboard_hard.wav" ]; then
    echo "🎵 Generating all keyboard sounds (this may take a moment)..."
    "$(pwd)/venv/bin/python3" sound_generator.py --type all > /dev/null
    if [ $? -ne 0 ]; then
        echo "❌ Failed to generate sounds. Check sound_generator.py"
        exit 1
    fi
    echo "✅ All sounds generated"
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x *.sh *.py
echo "✅ Scripts made executable"

# Set default sound if key_press.wav doesn't exist
if [ ! -f "key_press.wav" ]; then
    echo "🎵 Setting default sound (blue)..."
    if [ -f "generated_sounds/keyboard_blue.wav" ]; then
        cp generated_sounds/keyboard_blue.wav key_press.wav
        echo "✅ Default sound set"
    else
        echo "⚠️  Warning: Default sound file not found"
    fi
fi

echo "🧪 Testing daemon startup..."
timeout 5 "$(pwd)/venv/bin/python3" keyboard_sound_daemon_enhanced.py &
DAEMON_PID=$!
sleep 2
if kill -0 $DAEMON_PID 2>/dev/null; then
    kill $DAEMON_PID 2>/dev/null
    echo "✅ Daemon test successful"
else
    echo "⚠️  Warning: Daemon test failed - check permissions and dependencies"
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
