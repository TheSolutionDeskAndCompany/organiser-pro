# 🗂️ OrganiserPro - Linux Edition

[![Python 3.8–3.13](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-blue)](https://pypi.org/project/organiserpro/)
[![Tests](https://github.com/the-solution-desk/OrganiserPro/actions/workflows/ci.yml/badge.svg)](https://github.com/the-solution-desk/OrganiserPro/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Linux Only](https://img.shields.io/badge/platform-Linux-orange.svg)](https://www.linux.org/)
[![GUI Only](https://img.shields.io/badge/interface-GUI%20Only-green.svg)]()

> **OrganiserPro Linux Edition** is a powerful, Linux desktop application for sorting, deduplicating, and managing your files with an intuitive graphical interface. Keep your files tidy—sort, organize, and eliminate clutter with just a few clicks.

**🐧 Linux Desktop Only (for now)** • **🖱️ Graphical Interface Only—No Command Line Needed**

---

## ✨ Features

- **Smart File Sorting**
  - Sort files by type (extension) with intuitive GUI controls
  - Organize by modification or creation date
  - Customizable date formats through easy dropdown menus
  - *Preview mode* to see changes before applying

- **Duplicate Detection**
  - Find duplicate files by content with visual comparison
  - Remove or move duplicates with simple checkbox selection
  - Recursive directory scanning with progress display

- **User-Friendly GUI**
  - Clean, modern Tkinter interface designed for Linux desktops
  - Visual progress bars for long operations
  - Drag-and-drop folder selection
  - Clear error dialogs and comprehensive help tooltips
  - Works seamlessly with GNOME, KDE, XFCE, and other Linux desktop environments

---

## 🚀 Installation

### 🎯 Quick Install (Recommended for New Users)

**Just want to get started? Follow these simple steps:**

1. **Open a terminal** in the OrganiserPro directory
2. **Copy and paste this command:**
   ```bash
   ./install_and_run.sh
   ```
3. **That's it!** The script will install everything and launch the app

**Or install manually:**

1. Open a terminal in the OrganiserPro directory
2. Run: `pip install -e .`
3. Run: `./install_desktop.sh`
4. Find "OrganiserPro" in your app menu and launch it!

---

### 🔧 Advanced Installation

#### Prerequisites
- **Linux Desktop Environment** (GNOME, KDE, XFCE, etc.)
- Python 3.8 or higher
- Tkinter (usually included with Python on Linux)
- pip (Python package manager)

### Install from Source (Recommended for Linux)

```bash
# Clone the repository
git clone https://github.com/yourusername/OrganiserPro.git
cd OrganiserPro

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the application
pip install -e .
```

### Quick Install via pip

```bash
pip install organiserpro
```

### Verify Tkinter Installation

If you encounter GUI issues, ensure Tkinter is installed:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install tkinter

# Arch Linux
sudo pacman -S tk
```

---

## 🛠️ Usage

### Launching the Application

```bash
# Launch the GUI application
organiserpro-gui

# Or run directly from source
python -m OrganiserPro.gui
```

### Using the GUI Interface

1. **Select Folder**: Click "Browse" or drag-and-drop a folder into the application
2. **Choose Operation**: 
   - **Sort by Type**: Organize files into folders by extension
   - **Sort by Date**: Organize files by creation/modification date
   - **Find Duplicates**: Scan for and manage duplicate files
3. **Preview Changes**: Use "Preview" mode to see what will happen before applying
4. **Apply Changes**: Click "Execute" to perform the selected operation

### Desktop Integration

After installation, you can:
- Launch from your application menu
- Right-click on folders in your file manager and select "Organize with OrganiserPro" (if desktop integration is set up)
- Double-click the OrganiserPro desktop shortcut

---

## 🏁 Quickstart

1. **Launch OrganiserPro**: Run `organiserpro-gui` or find it in your application menu
2. **Select a folder**: Click "Browse" and choose your Downloads folder
3. **Choose "Sort by Type"**: Select this option from the main interface
4. **Preview**: Click "Preview" to see what changes will be made
5. **Execute**: Click "Execute" to organize your files

That's it! Your files are now neatly organized into folders by type.

---

## 📸 GUI Preview

The OrganiserPro interface provides:
- **Clean folder selection** with drag-and-drop support
- **Visual progress bars** showing operation status
- **Preview mode** to see changes before applying
- **Results summary** showing files organized by category
- **Error dialogs** with helpful troubleshooting information

---

## 🚀 Future Releases

**Windows and Mac support are planned for a future release!** 

The current Linux Edition is designed with cross-platform compatibility in mind. Future releases will include:
- Native Windows GUI with Windows-specific file handling
- macOS version with native look and feel
- Enhanced drag-and-drop integration for all platforms
- Platform-specific installer packages

**Want to help?** Open an issue or contribute to the cross-platform development effort!

---

## 🔧 Troubleshooting

### App Menu Icon Doesn't Appear

If OrganiserPro doesn't show up in your application menu after installation:

1. **Refresh the desktop database:**
   ```bash
   update-desktop-database ~/.local/share/applications
   ```

2. **Log out and log back in** - This refreshes the desktop environment

3. **Restart your computer** - Sometimes required for desktop integration

4. **Check if the desktop file exists:**
   ```bash
   ls ~/.local/share/applications/organiserpro.desktop
   ```

5. **Manually launch from terminal:**
   ```bash
   python3 -m OrganiserPro.gui
   ```

### Installation Issues

**"Tkinter not found" error:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install tkinter

# Arch Linux
sudo pacman -S tk
```

**"Permission denied" during installation:**
- Try using a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -e .
  ```

**"Command not found: organiserpro-gui":**
- Use the full Python command: `python3 -m OrganiserPro.gui`
- Or reinstall with: `pip install -e .`

### GUI Issues

**Application window doesn't appear:**
1. Check terminal for error messages
2. Ensure you're running on a Linux desktop environment
3. Try running the test suite: `python3 test_gui_linux.py`

**"No folder selected" error:**
- Click the "Browse..." button to select a folder
- Make sure you're selecting a folder, not a file
- Check folder permissions

**Files not organizing as expected:**
- Use "Preview" mode first to see what will happen
- Check that you have write permissions to the folder
- Ensure the folder contains files (not just subfolders)

### Getting Help

1. **Run the diagnostic test:**
   ```bash
   python3 test_gui_linux.py
   ```

2. **Check the logs** - Error messages appear in the GUI results area

3. **Visit our GitHub repository** for additional support and to report issues

4. **Common solutions:**
   - Restart your desktop environment
   - Check file and folder permissions
   - Ensure Python 3.8+ is installed
   - Verify Tkinter is available

---

## 📚 Documentation

For full documentation, advanced usage, and configuration options, visit [Read the Docs](https://organiserpro.readthedocs.io/).

- [Troubleshooting](TROUBLESHOOTING.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

### Development Setup

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```
4. Make your changes and run tests:
   ```bash
   pytest
   ```
5. Commit your changes: `git commit -m "Add some feature"`
6. Push to the branch: `git push origin feature/your-feature`
7. Create a new Pull Request

Please also see our [Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md).

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For questions or suggestions, please [open an issue](https://github.com/the-solution-desk/organiserpro/issues) or email [opensource@thesolutiondesk.com](mailto:opensource@thesolutiondesk.com).

> **Note for Ubuntu/Debian/Python 3.12+ users:**  
> If you try to install system-wide with pip, you may see an `externally-managed-environment` error due to recent Python packaging changes ([PEP 668](https://peps.python.org/pep-0668/)).  
> Using a virtual environment avoids this problem and keeps your Python setup clean.

For more help, see the [Python packaging user guide](https://packaging.python.org/tutorials/installing-packages/).

---

## 🔗 Quick Links

- [Full Documentation](https://organiserpro.readthedocs.io/en/latest/)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Open an Issue](https://github.com/the-solution-desk/organiserpro/issues)
- [Start a Discussion](https://github.com/the-solution-desk/organiserpro/discussions)

---
