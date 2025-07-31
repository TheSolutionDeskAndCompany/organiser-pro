#!/bin/bash
# OrganiserPro Linux Edition - One-Click Install and Run Script
# This script installs OrganiserPro and sets up desktop integration for Linux users

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
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

print_header() {
    echo -e "${BOLD}${BLUE}$1${NC}"
}

# Main installation function
main() {
    print_header "🗂️ OrganiserPro Linux Edition - Installation Script"
    echo "=================================================================="
    echo ""
    
    # Check if running on Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        print_error "This script is for Linux systems only."
        print_error "Detected OS: $OSTYPE"
        echo ""
        echo "Windows and Mac support are planned for future releases."
        echo "Visit our GitHub repository for updates on cross-platform support."
        exit 1
    fi
    
    print_success "Running on Linux: $(uname -s) $(uname -r)"
    
    # Detect desktop environment
    if [ -n "$XDG_CURRENT_DESKTOP" ]; then
        print_status "Desktop Environment: $XDG_CURRENT_DESKTOP"
    elif [ -n "$DESKTOP_SESSION" ]; then
        print_status "Desktop Session: $DESKTOP_SESSION"
    else
        print_warning "Could not detect desktop environment, but continuing..."
    fi
    
    echo ""
    
    # Check Python installation
    print_status "Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed or not in PATH."
        echo ""
        echo "Please install Python 3.8 or higher:"
        echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
        echo "  Fedora/RHEL:   sudo dnf install python3 python3-pip"
        echo "  Arch Linux:    sudo pacman -S python python-pip"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
    
    # Check pip installation
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        print_error "pip is not installed."
        echo ""
        echo "Please install pip:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-pip"
        echo "  Fedora/RHEL:   sudo dnf install python3-pip"
        echo "  Arch Linux:    sudo pacman -S python-pip"
        exit 1
    fi
    
    print_success "pip found"
    
    # Check Tkinter availability
    print_status "Checking Tkinter availability..."
    
    if ! python3 -c "import tkinter" &> /dev/null; then
        print_warning "Tkinter is not available. Attempting to provide installation instructions..."
        echo ""
        echo "Tkinter is required for the GUI. Please install it:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
        echo "  Fedora/RHEL:   sudo dnf install tkinter"
        echo "  Arch Linux:    sudo pacman -S tk"
        echo ""
        read -p "Have you installed Tkinter? Press Enter to continue or Ctrl+C to exit..."
        
        # Test again
        if ! python3 -c "import tkinter" &> /dev/null; then
            print_error "Tkinter is still not available. Please install it and run this script again."
            exit 1
        fi
    fi
    
    print_success "Tkinter is available"
    echo ""
    
    # Install OrganiserPro
    print_header "📦 Installing OrganiserPro..."
    
    print_status "Installing OrganiserPro in development mode..."
    
    # Try to install, with user-friendly error handling
    if pip3 install -e . &> /dev/null || pip install -e . &> /dev/null; then
        print_success "OrganiserPro installed successfully!"
    else
        print_error "Failed to install OrganiserPro."
        echo ""
        echo "This might be due to:"
        echo "1. Missing permissions - try running with sudo (not recommended)"
        echo "2. Missing development tools - install build-essential or equivalent"
        echo "3. Virtual environment issues - try creating a virtual environment first"
        echo ""
        echo "For a virtual environment approach:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -e ."
        echo ""
        exit 1
    fi
    
    echo ""
    
    # Test if the GUI can be imported
    print_status "Testing OrganiserPro installation..."
    
    if python3 -c "from OrganiserPro.gui import OrganiserProGUI; print('Import successful')" &> /dev/null; then
        print_success "OrganiserPro GUI module is working correctly!"
    else
        print_error "OrganiserPro installation test failed."
        echo ""
        echo "The installation completed but the GUI module cannot be imported."
        echo "This might indicate missing dependencies or installation issues."
        echo ""
        echo "Try running: python3 -c 'from OrganiserPro.gui import OrganiserProGUI'"
        echo "to see the specific error message."
        exit 1
    fi
    
    echo ""
    
    # Desktop Integration
    print_header "🖥️ Setting up Desktop Integration..."
    
    if [ -f "install_desktop.sh" ]; then
        print_status "Running desktop integration setup..."
        
        # Make sure the desktop install script is executable
        chmod +x install_desktop.sh
        
        # Run the desktop integration script
        if ./install_desktop.sh; then
            print_success "Desktop integration completed!"
        else
            print_warning "Desktop integration had some issues, but OrganiserPro should still work."
            echo "You can launch it manually with: python3 -m OrganiserPro.gui"
        fi
    else
        print_warning "Desktop integration script not found. Creating basic integration..."
        
        # Create basic desktop integration if script is missing
        mkdir -p ~/.local/share/applications
        
        cat > ~/.local/share/applications/organiserpro.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=OrganiserPro
GenericName=File Organizer
Comment=Organize your files with ease - Linux Edition
Exec=python3 -m OrganiserPro.gui
Terminal=false
StartupNotify=true
Categories=Utility;FileManager;System;
Keywords=file;organizer;sort;duplicate;cleanup;
EOF
        
        chmod +x ~/.local/share/applications/organiserpro.desktop
        
        # Update desktop database if available
        if command -v update-desktop-database &> /dev/null; then
            update-desktop-database ~/.local/share/applications &> /dev/null || true
        fi
        
        print_success "Basic desktop integration created!"
    fi
    
    echo ""
    
    # Final success message
    print_header "🎉 Installation Complete!"
    echo "=================================================================="
    echo ""
    print_success "OrganiserPro Linux Edition has been successfully installed!"
    echo ""
    echo "You can now:"
    echo "  • Find 'OrganiserPro' in your application menu"
    echo "  • Launch it from the command line: python3 -m OrganiserPro.gui"
    echo "  • Or run: organiserpro-gui (if the command is available)"
    echo ""
    
    # Ask if user wants to launch the app
    echo "Would you like to launch OrganiserPro now? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Launching OrganiserPro GUI..."
        echo ""
        
        # Try to launch the GUI
        if command -v organiserpro-gui &> /dev/null; then
            organiserpro-gui &
        else
            python3 -m OrganiserPro.gui &
        fi
        
        print_success "OrganiserPro is starting..."
        echo ""
        echo "If the application doesn't appear:"
        echo "1. Check if there are any error messages above"
        echo "2. Try running: python3 -m OrganiserPro.gui"
        echo "3. Make sure your desktop environment supports GUI applications"
    else
        echo ""
        print_status "You can launch OrganiserPro anytime from your application menu"
        print_status "or by running: python3 -m OrganiserPro.gui"
    fi
    
    echo ""
    echo "If you encounter any issues:"
    echo "• Check the README.md file for troubleshooting tips"
    echo "• Run the test suite: python3 test_gui_linux.py"
    echo "• Visit our GitHub repository for support"
    echo ""
    print_success "Thank you for using OrganiserPro Linux Edition! 🐧"
}

# Run the main function
main "$@"
