#!/bin/bash

# Local installation script for ENX-Kebord (no root required)
set -e  # Exit on any error

# Function to print installation steps
print_step() {
    echo "🔧 $1"
}

# Function to print success messages
print_success() {
    echo "✅ $1"
}

# Function to print error messages
print_error() {
    echo "❌ $1" >&2
}

# Get current directory (where the project is located)
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"

print_step "Starting ENX-Kebord local installation..."
print_step "Installing from: $CURRENT_DIR"

# Create directories
print_step "Creating user directories..."
mkdir -p "$DESKTOP_DIR"
mkdir -p "$AUTOSTART_DIR"

# Make scripts executable
print_step "Setting up permissions..."
chmod +x "$CURRENT_DIR"/*.sh 2>/dev/null || true

# Create virtual environment if it doesn't exist
if [ ! -d "$CURRENT_DIR/venv" ]; then
    print_step "Creating virtual environment..."
    python3 -m venv "$CURRENT_DIR/venv" || {
        print_error "Failed to create virtual environment. Please install python3-venv:"
        print_error "sudo apt install python3-venv python3-pip"
        exit 1
    }
fi

# Activate virtual environment and install dependencies
print_step "Installing Python dependencies..."
source "$CURRENT_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$CURRENT_DIR/requirements.txt" || {
    print_error "Failed to install dependencies"
    exit 1
}

# Create application icon
create_icon() {
    print_step "Creating application icon..."

    # Create a simple keyboard icon using Python PIL
    cat > "$CURRENT_DIR/create_icon.py" << 'EOF'
from PIL import Image, ImageDraw, ImageFont
import os

# Create a 64x64 icon
img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw keyboard background
draw.rounded_rectangle([8, 20, 56, 44], radius=4, fill='#2563eb')

# Draw keys
for i in range(3):
    for j in range(6):
        x = 12 + j * 6
        y = 24 + i * 5
        draw.rectangle([x, y, x+4, y+3], fill='white')

# Save icon
img.save('enx-kebord-icon.png')
print("Icon created successfully!")
EOF

    python3 "$CURRENT_DIR/create_icon.py" 2>/dev/null || {
        # Fallback: create a simple text-based icon
        echo "Creating fallback icon..."
        convert -size 64x64 xc:'#2563eb' \
            -fill white -pointsize 12 -gravity center \
            -annotate +0+0 'ENX' \
            "$CURRENT_DIR/enx-kebord-icon.png" 2>/dev/null || {
            # Ultimate fallback: copy a generic icon
            cp /usr/share/pixmaps/applications-multimedia.png "$CURRENT_DIR/enx-kebord-icon.png" 2>/dev/null || true
        }
    }

    rm -f "$CURRENT_DIR/create_icon.py" 2>/dev/null || true
    print_success "Application icon created!"
}

create_icon

# Create desktop entry with correct paths
print_step "Creating desktop entry..."
cat > "$DESKTOP_DIR/enx-kebord.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ENX-Kebord
GenericName=Keyboard Sound Manager
Comment=Mechanical keyboard sound experience with beautiful GUI
Exec=$CURRENT_DIR/launch_gui.sh
Icon=$CURRENT_DIR/enx-kebord-icon.png
Path=$CURRENT_DIR
Terminal=false
Categories=AudioVideo;Audio;Utility;
Keywords=keyboard;sound;mechanical;typing;audio;
StartupNotify=true
StartupWMClass=enx-kebord
EOF

# Make desktop entry executable
chmod +x "$DESKTOP_DIR/enx-kebord.desktop"

# Create autostart entry for daemon
print_step "Creating autostart entry for daemon..."
cat > "$AUTOSTART_DIR/enx-kebord-daemon.desktop" << EOF
[Desktop Entry]
Type=Application
Name=ENX-Kebord Daemon
Comment=ENX-Kebord background service
Exec=$CURRENT_DIR/keyboard_sound_control.sh start
Icon=$CURRENT_DIR/enx-kebord-icon.png
Path=$CURRENT_DIR
Terminal=false
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
StartupNotify=false
EOF

chmod +x "$AUTOSTART_DIR/enx-kebord-daemon.desktop"

# Update desktop database
print_step "Updating desktop database..."
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

print_success "ENX-Kebord installed successfully!"
print_success "Installation directory: $CURRENT_DIR"
print_success ""
print_success "To launch the application:"
print_success "1. Search for 'ENX-Kebord' in your application menu"
print_success "2. Or run: $CURRENT_DIR/launch_gui.sh"
print_success ""
print_success "The daemon will start automatically on next login."
print_success "To start it now, run: $CURRENT_DIR/keyboard_sound_control.sh start"
