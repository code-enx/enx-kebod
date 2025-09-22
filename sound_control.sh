#!/bin/bash
# Enhanced sound control utility

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

GENERATED_DIR="generated_sounds"
CONFIG_FILE="$HOME/.keyboard_sound_config.json"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"

show_help() {
    echo "🎵 enx-kebord Sound Controller"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "COMMANDS:"
    echo "  list          - Show all available sounds"
    echo "  switch <type> - Switch to a specific sound type"
    echo "  current       - Show current sound"
    echo "  hotkeys       - Show global hotkeys"
    echo "  generate      - Generate all sound files"
    echo ""
    echo "🔵 CLASSIC SWITCHES:"
    echo "    blue        - Cherry MX Blue (sharp click)"
    echo "    brown       - Cherry MX Brown (tactile bump)" 
    echo "    red         - Cherry MX Red (linear, quiet)"
    echo "🔧 MECHANICAL VARIANTS:"
    echo "    mechanical  - Heavy mechanical (loud click)"
    echo "    creamy      - Creamy smooth click (lubed switches)"
    echo "    dry         - Dry mechanical (unlubed, scratchy)"
    echo "    thock       - Deep thocky sound (Topre-style)"
    echo "    clicky      - Extra clicky (Box Jade/Navy)"
    echo "    silent      - Silent switches (dampened)"
    echo "    tactile     - Pronounced tactile bump"
    echo "    hard        - Extremely hard mechanical (NEW!)"
    echo "📝 VINTAGE:"
    echo "    typewriter  - Vintage typewriter (metallic)"
    echo "🎵 SPECIAL EDITIONS:"
    echo "    lofi        - Lofi chill keyboard (warm, nostalgic)"
    echo "    gx_feryn    - Opera GX Feryn style (smooth gaming)"
    echo "    lee_sin     - Lee Sin inspired (sharp, precise)"
    echo "    hacker      - Hacker terminal (Matrix-like retro)"
    echo ""
    echo "EXAMPLES:"
    echo "  $0 switch blue     # Switch to Cherry MX Blue sound"
    echo "  $0 switch hard     # Switch to hard mechanical sound"
    echo "  $0 current         # Show current sound"
    echo "  $0 hotkeys         # Show available hotkeys"
    echo ""
}

show_hotkeys() {
    echo "⌨️  GLOBAL HOTKEYS (work anywhere):"
    echo ""
    echo "🎮 DAEMON CONTROL:"
    echo "  Shift + ↑     - Start daemon (if stopped)"
    echo "  Shift + ↓     - Stop daemon"
    echo ""
    echo "🎵 SOUND CONTROL:"
    echo "  Ctrl+Shift+S  - Cycle through sounds"
    echo ""
    echo "💡 TIPS:"
    echo "  • Hotkeys work globally (in any application)"
    echo "  • Sound cycling shows desktop notifications"
    echo "  • Volume automatically reduces for headphones"
    echo "  • Current sound is saved and restored on restart"
    echo ""
}

show_current() {
    if [ -f "$CONFIG_FILE" ]; then
        current_type=$(grep -o '"current_sound_type": "[^"]*' "$CONFIG_FILE" | cut -d'"' -f4)
        if [ -n "$current_type" ]; then
            echo "🎵 Current sound: $current_type"
        else
            echo "🎵 Current sound: unknown"
        fi
    else
        echo "🎵 Current sound: not configured (using default)"
    fi
    
    # Check if headphones are detected
    if command -v pactl >/dev/null 2>&1; then
        if pactl list sinks short | grep -i -E "headphone|headset|usb|bluetooth" > /dev/null; then
            echo "🎧 Headphones detected - using reduced volume"
        else
            echo "🔊 Speakers detected - using full volume"
        fi
    fi
}

list_sounds() {
    echo "🎵 Available sounds:"
    echo ""
    ls -1 "$GENERATED_DIR"/keyboard_*.wav 2>/dev/null | while read -r file; do
        basename "$file" .wav | sed 's/keyboard_/  • /'
    done
    echo ""
    echo "💡 Use 'switch <name>' to change sounds"
    echo "💡 Use 'Ctrl+Shift+S' to cycle through sounds globally"
}

switch_sound() {
    local sound_type="$1"
    local sound_file="${GENERATED_DIR}/keyboard_${sound_type}.wav"
    
    if [ ! -f "$sound_file" ]; then
        echo "❌ Sound file not found: $sound_file"
        echo "💡 Generate sounds first: ./setup_enhanced.sh"
        echo "💡 Or use: $0 generate"
        exit 1
    fi
    
    echo "🎵 Switching to ${sound_type} keyboard sound..."
    cp "$sound_file" key_press.wav
    
    echo "🔄 Restarting daemon..."
    ./keyboard_sound_control.sh restart
    
    echo "✅ Now using ${sound_type} keyboard sound!"
    echo "⌨️  Type some keys to hear the new sound!"
    echo "💡 Use Ctrl+Shift+S to cycle sounds globally"
}

generate_sounds() {
    echo "🔄 Generating all keyboard sounds..."
    "$VENV_PYTHON" sound_generator.py --type all
    echo "✅ All sounds generated!"
    echo "💡 Use '$0 switch <type>' to change sounds"
}

# Main logic
case "$1" in
    list)
        list_sounds
        ;;
    switch)
        if [ -z "$2" ]; then
            echo "❌ Please specify a sound type"
            echo "💡 Use: $0 list to see available sounds"
            exit 1
        fi
        switch_sound "$2"
        ;;
    current)
        show_current
        ;;
    hotkeys)
        show_hotkeys
        ;;
    generate)
        generate_sounds
        ;;
    -h|--help|help|"")
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac