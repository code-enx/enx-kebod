#!/bin/bash
# ENX-Kebord Fast GUI Launcher
# Optimized for quick startup with error handling

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || {
    echo "Error: Cannot access ENX-Kebord directory!"
    exit 1
}

# Launch the GUI
python3 gui.py
