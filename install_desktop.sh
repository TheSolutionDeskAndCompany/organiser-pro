#!/bin/bash
# OrganiserPro Linux Desktop Integration Installer

set -e

echo "🗂️ OrganiserPro Linux Edition - Desktop Integration Setup"
echo "========================================================="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: This script is for Linux systems only."
    echo "   Detected OS: $OSTYPE"
    echo "   Windows and Mac support are planned for future releases."
    exit 1
fi

# Check if organiserpro-gui is available
if ! command -v organiserpro-gui &> /dev/null; then
    echo "❌ Error: organiserpro-gui command not found."
    echo "   Please install OrganiserPro first:"
    echo "   pip install -e ."
    exit 1
fi

# Create directories
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/icons

# Install desktop entry
echo "📋 Installing desktop entry..."
cp organiserpro.desktop ~/.local/share/applications/
chmod +x ~/.local/share/applications/organiserpro.desktop

# Create a simple icon (text-based for now)
echo "🎨 Creating application icon..."
cat > ~/.local/share/icons/organiserpro.svg << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" fill="#2196F3" rx="8"/>
  <text x="32" y="40" font-family="Arial, sans-serif" font-size="32" 
        text-anchor="middle" fill="white">🗂️</text>
</svg>
EOF

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    echo "🔄 Updating desktop database..."
    update-desktop-database ~/.local/share/applications
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    echo "🔄 Updating icon cache..."
    gtk-update-icon-cache ~/.local/share/icons 2>/dev/null || true
fi

echo ""
echo "✅ Desktop integration installed successfully!"
echo ""
echo "You can now:"
echo "  • Find OrganiserPro in your application menu"
echo "  • Launch it from the command line: organiserpro-gui"
echo "  • Right-click on folders to organize them (if supported by your file manager)"
echo ""
echo "🐧 Tested on: GNOME, KDE, XFCE, and other Linux desktop environments"
echo ""
