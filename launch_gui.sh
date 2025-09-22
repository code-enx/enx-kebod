 #!/bin/bash
 # ENX-Kebord Fast GUI Launcher
 # Optimized for quick startup with error handling

 SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
 cd "$SCRIPT_DIR" || {
     echo "Error: Cannot access ENX-Kebord directory!"
     exit 1
 }

 if [ ! -d "venv" ]; then
     echo "Error: Virtual environment not found!"
     echo "Please run setup first: ./setup_enhanced.sh"
     exit 1
 fi

 if [ ! -f "enx_kebord_gui.py" ]; then
     echo "Error: GUI application not found!"
     echo "Please reinstall ENX-Kebord."
     exit 1
 fi

 # Suppress pygame welcome message for faster startup
 export PYGAME_HIDE_SUPPORT_PROMPT="hide"

 source "$SCRIPT_DIR/venv/bin/activate" || {
     echo "Error: Cannot activate virtual environment!"
     echo "Please run setup: ./setup_enhanced.sh"
     exit 1
 }

 exec "$SCRIPT_DIR/venv/bin/python3" "$SCRIPT_DIR/enx_kebord_gui.py" "$@"
