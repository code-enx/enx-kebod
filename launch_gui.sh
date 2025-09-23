#!/bin/bash
# ENX-Kebord Fast GUI Launcher
# Optimized for quick startup

cd "$(dirname "$0")"

# Suppress pygame welcome message for faster startup
export PYGAME_HIDE_SUPPORT_PROMPT="hide"

# Use virtual environment
source venv/bin/activate

# Launch GUI with venv python
exec "$(pwd)/venv/bin/python3" enx_kebord_gui.py "$@"
