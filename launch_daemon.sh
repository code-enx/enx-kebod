#!/bin/bash
# ENX-Kebord Fast Daemon Launcher

cd "$(dirname "$0")"

# Suppress pygame welcome message
export PYGAME_HIDE_SUPPORT_PROMPT="hide"

# Use virtual environment
source venv/bin/activate

# Launch daemon with venv python
exec "$(pwd)/venv/bin/python3" keyboard_sound_daemon_enhanced.py "$@"
