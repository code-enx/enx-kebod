#!/bin/bash
# ENX-Kebord Installation Script
# Beautiful Keyboard Sound Manager for Linux

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Installation paths
INSTALL_DIR="$HOME/.local/share/enx-kebord"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"
ICON_DIR="$HOME/.local/share/icons"

print_header() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                        🎵 enx-kebord Installation 🎵                        ║"
    echo "║                   Enhanced Keyboard Sound Experience                         ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    print_step "Checking system dependencies..."
    
    local missing_deps=()
    
    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        missing_deps+=("python3-pip")
    fi
    
    # Check git  
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    # Check curl or wget for downloading
    if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
        missing_deps+=("curl or wget")
    fi
    
    # Check audio systems
    if ! command -v pactl &> /dev/null && ! command -v aplay &> /dev/null; then
        missing_deps+=("alsa-utils or pulseaudio-utils")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install them using your package manager:"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip git alsa-utils pulseaudio-utils"
        echo "  Fedora: sudo dnf install python3 python3-pip git alsa-utils pulseaudio-utils"
        echo "  Arch: sudo pacman -S python python-pip git alsa-utils pulseaudio"
        exit 1
    fi
    
    print_success "All dependencies found!"
}

create_directories() {
    print_step "Creating installation directories..."
    
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR" 
    mkdir -p "$DESKTOP_DIR"
    mkdir -p "$AUTOSTART_DIR"
    mkdir -p "$ICON_DIR"
    
    print_success "Directories created!"
}

install_application() {
    print_step "Installing enx-kebord application..."
    
    # Copy all application files
    cp -r * "$INSTALL_DIR/"
    
    # Create virtual environment
    cd "$INSTALL_DIR"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt > /dev/null 2>&1
    
    # Generate all sounds
    print_step "Generating keyboard sounds..."
    "$PWD/venv/bin/python3" sound_generator.py --type all > /dev/null 2>&1
    
    # Set default sound
    if [ ! -f "key_press.wav" ]; then
        cp generated_sounds/keyboard_blue.wav key_press.wav
    fi
    
    # Make scripts executable
    chmod +x *.sh *.py
    
    print_success "Application installed!"
}

create_launchers() {
    print_step "Creating desktop launchers..."

    # Create app desktop entry (absolute Exec using venv-aware launcher)
    cat > "$DESKTOP_DIR/enx-kebord.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=enx-kebord
GenericName=Keyboard Sound Manager
Comment=Mechanical keyboard sound experience with beautiful GUI
Exec=$INSTALL_DIR/launch_gui.sh
Icon=$ICON_DIR/enx-kebord-icon.png
Terminal=false
Categories=AudioVideo;Audio;Utility;
Keywords=keyboard;sound;mechanical;typing;audio;
StartupNotify=true
StartupWMClass=enx-kebord
EOF

    # Create autostart daemon entry (absolute Exec using venv-aware launcher)
    cat > "$AUTOSTART_DIR/enx-kebord-daemon.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=enx-kebord Daemon
GenericName=Keyboard Sound Daemon
Comment=Background daemon for keyboard sounds (auto-start)
Exec=$INSTALL_DIR/launch_daemon.sh
Icon=$ICON_DIR/enx-kebord-icon.png
Terminal=false
Categories=System;
NoDisplay=true
X-GNOME-Autostart-enabled=true
StartupNotify=false
EOF

    # Make desktop files executable
    chmod +x "$DESKTOP_DIR/enx-kebord.desktop"
    chmod +x "$AUTOSTART_DIR/enx-kebord-daemon.desktop"

    # Create command-line launcher that always uses venv
    cat > "$BIN_DIR/enx-kebord" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
exec "\$PWD/venv/bin/python3" enx_kebord_gui.py
EOF
    chmod +x "$BIN_DIR/enx-kebord"

    print_success "Desktop launchers created!"
}

create_icon() {
    print_step "Creating application icon..."
    
    # Create a placeholder icon (replace with a real icon when available)
    cat > "$ICON_DIR/enx-kebord-icon.png" << 'EOF'
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==
EOF
    
    print_success "Icon created!"
}

update_desktop_database() {
    print_step "Updating desktop database..."
    
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    fi
    
    print_success "Desktop database updated!"
}

final_setup() {
    print_step "Performing final setup..."
    
    # Add ~/.local/bin to PATH if not already there
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> ~/.bashrc
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> ~/.zshrc 2>/dev/null || true
        print_warning "Added $BIN_DIR to PATH. Please restart your terminal or run:"
        echo "  export PATH=\"$BIN_DIR:\$PATH\""
    fi
    
    print_success "Final setup completed!"
}

print_completion() {
    echo ""
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                     🎉 Installation Completed! 🎉                          ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${BLUE}🚀 How to use enx-kebord:${NC}"
    echo ""
    echo "1. 🎵 Launch GUI application:"
    echo "   • From command line: enx-kebord"
    echo "   • From applications menu: Search 'enx-kebord'"
    echo ""
    echo "2. 🎮 The daemon will auto-start on next login"
    echo "   • Start manually now: $INSTALL_DIR/keyboard_sound_control.sh start"
    echo ""
    echo "3. ⌨️ Global hotkeys (work anywhere):"
    echo "   • Ctrl+Shift+S - Cycle through sounds"
    echo "   • Shift+↑      - Start daemon"
    echo "   • Shift+↓      - Stop daemon"
    echo ""
    echo "4. 🎛️ Use the GUI to:"
    echo "   • Control keyboard sound volume"
    echo "   • Switch between 16 different sounds"
    echo "   • Monitor audio device changes"
    echo "   • Manage daemon status"
    echo ""
    echo -e "${PURPLE}📁 Installed to: $INSTALL_DIR${NC}"
    echo -e "${PURPLE}🔗 Command: enx-kebord${NC}"
    echo ""
    echo -e "${YELLOW}Tip: The daemon runs in background and GUI opens only when you launch it manually!${NC}"
}

main() {
    print_header
    
    # If running from curl, download the repository first
    if [ "$1" = "--from-github" ] || [ ! -f "enx_kebord_gui.py" ]; then
        print_step "Downloading ENX-Kebord from GitHub..."
        
        # Create temporary directory
        TEMP_DIR=$(mktemp -d)
        cd "$TEMP_DIR"
        
        # Download and extract
        if command -v curl &> /dev/null; then
            curl -fsSL "https://github.com/code-enx/Mech_keyboard_enx-/archive/refs/heads/main.tar.gz" | tar -xz
        elif command -v wget &> /dev/null; then
            wget -qO- "https://github.com/code-enx/Mech_keyboard_enx-/archive/refs/heads/main.tar.gz" | tar -xz
        else
            print_error "Neither curl nor wget found. Please install one of them."
            exit 1
        fi
        
        cd "Mech_keyboard_enx--main"
        print_success "Downloaded successfully!"
    fi
    
    # Check if we have the required files
    if [ ! -f "enx_kebord_gui.py" ]; then
        print_error "ENX-Kebord files not found. Please check the installation."
        exit 1
    fi
    
    check_dependencies
    create_directories
    install_application
    create_launchers
    create_icon
    update_desktop_database
    final_setup
    print_completion
}

# Run main installation
main "$@"