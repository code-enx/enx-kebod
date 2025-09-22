#!/bin/bash
# ENX-Kebord GUI Launcher - Fixed for local installation

echo "=== ENX-Kebord GUI Launcher Debug ==="
echo "Current working directory: $(pwd)"
echo "Script location: ${BASH_SOURCE[0]}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Resolved script directory: $SCRIPT_DIR"

cd "$SCRIPT_DIR" || {
    echo "Error: Cannot access ENX-Kebord directory: $SCRIPT_DIR"
    notify-send "ENX-Kebord Error" "Cannot access application directory" 2>/dev/null || true
    exit 1
}

echo "Changed to directory: $(pwd)"
echo "Contents of directory:"
ls -la

if [ ! -f "$SCRIPT_DIR/enx_kebord_gui.py" ]; then
    echo "Error: GUI application not found: $SCRIPT_DIR/enx_kebord_gui.py"
    echo "Looking for alternative names..."
    if [ -f "$SCRIPT_DIR/gui.py" ]; then
        echo "Found gui.py instead"
        GUI_FILE="gui.py"
    else
        echo "No GUI file found. Available Python files:"
        ls -la *.py 2>/dev/null || echo "No Python files found"
        notify-send "ENX-Kebord Error" "GUI application not found" 2>/dev/null || true
        exit 1
    fi
else
    GUI_FILE="enx_kebord_gui.py"
fi

echo "Using GUI file: $GUI_FILE"

if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Warning: Virtual environment not found in $SCRIPT_DIR"
    echo "Attempting to run with system Python..."
    PYTHON_CMD="python3"
else
    echo "Virtual environment found, activating..."
    source "$SCRIPT_DIR/venv/bin/activate" || {
        echo "Error: Cannot activate virtual environment"
        echo "Falling back to system Python..."
        PYTHON_CMD="python3"
    }
    if [ -n "$VIRTUAL_ENV" ]; then
        PYTHON_CMD="$SCRIPT_DIR/venv/bin/python3"
        echo "Using virtual environment Python: $PYTHON_CMD"
    else
        PYTHON_CMD="python3"
        echo "Using system Python: $PYTHON_CMD"
    fi
fi

export PYGAME_HIDE_SUPPORT_PROMPT="hide"
export DISPLAY="${DISPLAY:-:0}"

echo "Starting ENX-Kebord GUI..."
echo "Command: $PYTHON_CMD $SCRIPT_DIR/$GUI_FILE"
exec "$PYTHON_CMD" "$SCRIPT_DIR/$GUI_FILE" "$@"
