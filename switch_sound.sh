#!/bin/bash
# Switch between generated keyboard sounds

GENERATED_DIR="generated_sounds"
SOUNDS=("blue" "brown" "red" "mechanical" "typewriter")

show_help() {
    echo "🎵 Keyboard Sound Switcher"
    echo ""
    echo "Usage: $0 [sound_type]"
    echo ""
    echo "Available sounds:"
    echo "  🔵 CLASSIC SWITCHES:"
    echo "    blue        - Cherry MX Blue (sharp click)"
    echo "    brown       - Cherry MX Brown (tactile bump)" 
    echo "    red         - Cherry MX Red (linear, quiet)"
    echo "  🔧 MECHANICAL VARIANTS:"
    echo "    mechanical  - Heavy mechanical (loud click)"
    echo "    creamy      - Creamy smooth click (lubed switches)"
    echo "    dry         - Dry mechanical (unlubed, scratchy)"
    echo "    thock       - Deep thocky sound (Topre-style)"
    echo "    clicky      - Extra clicky (Box Jade/Navy)"
    echo "    silent      - Silent switches (dampened)"
    echo "    tactile     - Pronounced tactile bump"
    echo "  📝 VINTAGE:"
    echo "    typewriter  - Vintage typewriter (metallic)"
    echo "  🎵 SPECIAL EDITIONS:"
    echo "    lofi        - Lofi chill keyboard (warm, nostalgic)"
    echo "    gx_feryn    - Opera GX Feryn style (smooth gaming)"
    echo "    lee_sin     - Lee Sin inspired (sharp, precise)"
    echo "    hacker      - Hacker terminal (Matrix-like retro)"
    echo "    hard        - Extremely hard mechanical (aggressive)"
    echo ""
    echo "Examples:"
    echo "  $0 blue       # Switch to Cherry MX Blue sound"
    echo "  $0 typewriter # Switch to typewriter sound"
    echo ""
    echo "💡 The daemon will automatically restart with the new sound!"
}

switch_sound() {
    local sound_type="$1"
    local sound_file="${GENERATED_DIR}/keyboard_${sound_type}.wav"
    
    if [ ! -f "$sound_file" ]; then
        echo "❌ Sound file not found: $sound_file"
        echo "💡 Generate sounds first: ./setup_enhanced.sh"
        exit 1
    fi
    
    echo "🎵 Switching to ${sound_type} keyboard sound..."
    cp "$sound_file" key_press.wav
    
    echo "🔄 Restarting daemon..."
    ./keyboard_sound_control.sh restart
    
    echo "✅ Now using ${sound_type} keyboard sound!"
    echo "⌨️  Type some keys to hear the new sound!"
}

# Main logic
case "$1" in
    blue|brown|red|mechanical|typewriter|creamy|dry|thock|clicky|silent|tactile|lofi|gx_feryn|lee_sin|hacker|hard)
        switch_sound "$1"
        ;;
    -h|--help|help|"")
        show_help
        ;;
    *)
        echo "❌ Unknown sound type: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
