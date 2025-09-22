#!/bin/bash
# Control script for keyboard sound daemon

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DAEMON_PATH="$SCRIPT_DIR/keyboard_sound_daemon_enhanced.py"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"
PID_FILE="$HOME/.keyboard_sound_daemon.pid"

case "$1" in
    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "Keyboard sound daemon is already running (PID: $PID)"
                exit 0
            else
                rm -f "$PID_FILE"
            fi
        fi
        echo "Starting keyboard sound daemon (venv)..."
        "$VENV_PYTHON" "$DAEMON_PATH" &
        echo "Daemon started."
        ;;
    
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "Stopping keyboard sound daemon (PID: $PID)..."
                kill "$PID"
                rm -f "$PID_FILE"
                echo "Daemon stopped."
            else
                echo "Daemon not running."
                rm -f "$PID_FILE"
            fi
        else
            echo "Daemon not running (no PID file)."
        fi
        ;;
    
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "Keyboard sound daemon is running (PID: $PID)"
            else
                echo "Daemon not running (stale PID file)"
                rm -f "$PID_FILE"
            fi
        else
            echo "Daemon not running."
        fi
        ;;
    
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac