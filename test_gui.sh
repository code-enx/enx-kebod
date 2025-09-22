#!/bin/bash
# Simple test script to verify GUI can launch

echo "=== ENX-Kebord GUI Test ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python3 --version)"
echo "Available Python files:"
ls -la *.py

if [ -f "enx_kebord_gui.py" ]; then
    echo "Found enx_kebord_gui.py"
    echo "Testing direct launch..."
    python3 enx_kebord_gui.py --help 2>/dev/null || {
        echo "Direct launch failed, checking dependencies..."
        python3 -c "import tkinter; print('tkinter: OK')" 2>/dev/null || echo "tkinter: MISSING"
        python3 -c "import pygame; print('pygame: OK')" 2>/dev/null || echo "pygame: MISSING"
        python3 -c "import pynput; print('pynput: OK')" 2>/dev/null || echo "pynput: MISSING"
    }
else
    echo "enx_kebord_gui.py not found!"
fi
