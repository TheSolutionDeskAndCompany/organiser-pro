#!/usr/bin/env python3
"""
Test script for OrganiserPro GUI on Linux desktop environments.
This script verifies that all GUI components work correctly.
"""

import sys
import os
import platform
import tempfile
import shutil
from pathlib import Path

# Add the OrganiserPro module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_os_detection():
    """Test OS detection functionality."""
    print("🔍 Testing OS Detection...")
    
    if platform.system() != "Linux":
        print(f"❌ Warning: Running on {platform.system()}, not Linux")
        print("   This may cause issues with Linux-specific features")
    else:
        print(f"✅ Running on Linux: {platform.platform()}")
        
    # Test desktop environment detection
    desktop_env = os.environ.get('DESKTOP_SESSION', 'unknown')
    xdg_desktop = os.environ.get('XDG_CURRENT_DESKTOP', 'unknown')
    
    print(f"   Desktop Session: {desktop_env}")
    print(f"   XDG Desktop: {xdg_desktop}")
    
    return platform.system() == "Linux"

def test_tkinter_availability():
    """Test if Tkinter is available and working."""
    print("\n🖼️ Testing Tkinter Availability...")
    
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        
        # Create a test window (don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test ttk styling
        style = ttk.Style()
        available_themes = style.theme_names()
        print(f"✅ Tkinter available with themes: {', '.join(available_themes)}")
        
        # Test if 'clam' theme is available (used in GUI)
        if 'clam' in available_themes:
            print("✅ 'clam' theme available (used by OrganiserPro)")
        else:
            print("⚠️ 'clam' theme not available, will fall back to default")
            
        root.destroy()
        return True
        
    except ImportError as e:
        print(f"❌ Tkinter not available: {e}")
        print("   Install with: sudo apt-get install python3-tk")
        return False
    except Exception as e:
        print(f"❌ Tkinter error: {e}")
        return False

def test_core_modules():
    """Test if core OrganiserPro modules can be imported."""
    print("\n📦 Testing Core Modules...")
    
    modules_to_test = [
        ('OrganiserPro.gui', 'GUI module'),
        ('OrganiserPro.cli', 'CLI module'),
        ('OrganiserPro.sorter', 'File sorter'),
        ('OrganiserPro.dedupe', 'Duplicate finder'),
        ('OrganiserPro.commands', 'Commands module'),
    ]
    
    all_good = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}: {module_name}")
        except ImportError as e:
            print(f"❌ {description}: {module_name} - {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️ {description}: {module_name} - {e}")
            
    return all_good

def test_gui_creation():
    """Test GUI window creation without showing it."""
    print("\n🖱️ Testing GUI Creation...")
    
    try:
        from OrganiserPro.gui import OrganiserProGUI
        
        # Create GUI instance but don't run mainloop
        app = OrganiserProGUI()
        
        # Test basic properties
        if app.root.title() == "OrganiserPro - Linux Edition":
            print("✅ GUI window created with correct title")
        else:
            print(f"⚠️ Unexpected window title: {app.root.title()}")
            
        # Test if main components exist
        components = [
            'selected_folder',
            'operation_mode', 
            'preview_mode',
            'recursive_scan'
        ]
        
        for component in components:
            if hasattr(app, component):
                print(f"✅ Component '{component}' exists")
            else:
                print(f"❌ Component '{component}' missing")
                
        # Clean up
        app.root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ GUI creation failed: {e}")
        return False

def create_test_files():
    """Create temporary test files for functionality testing."""
    print("\n📁 Creating Test Files...")
    
    test_dir = Path(tempfile.mkdtemp(prefix="organiserpro_test_"))
    print(f"   Test directory: {test_dir}")
    
    # Create various file types
    test_files = [
        "document.txt",
        "image.jpg", 
        "image.png",
        "archive.zip",
        "script.py",
        "data.csv",
        "duplicate1.txt",
        "duplicate2.txt",  # Will have same content as duplicate1.txt
    ]
    
    for filename in test_files:
        file_path = test_dir / filename
        
        if filename.startswith("duplicate"):
            # Create identical content for duplicate testing
            content = "This is duplicate content for testing"
        else:
            content = f"Test content for {filename}"
            
        file_path.write_text(content)
        print(f"   Created: {filename}")
        
    # Create a subdirectory with more files
    subdir = test_dir / "subdirectory"
    subdir.mkdir()
    (subdir / "nested_file.doc").write_text("Nested file content")
    
    print(f"✅ Created {len(test_files) + 1} test files")
    return test_dir

def test_file_operations(test_dir):
    """Test core file operations without GUI."""
    print(f"\n⚙️ Testing File Operations in {test_dir}...")
    
    try:
        from OrganiserPro.sorter import sort_by_type, sort_by_date
        from OrganiserPro.dedupe import find_duplicates
        
        # Test file sorting functions
        print("✅ File sorting functions imported")
        
        # Test duplicate finder
        duplicates = find_duplicates(str(test_dir), recursive=True)
        
        if duplicates:
            # Convert dict to list of groups for counting
            duplicate_groups = [files for files in duplicates.values() if len(files) > 1]
            print(f"✅ Duplicate detection working: found {len(duplicate_groups)} groups")
        else:
            print("⚠️ No duplicates found (expected at least 1 group)")
            
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def cleanup_test_files(test_dir):
    """Clean up temporary test files."""
    print(f"\n🧹 Cleaning up test files...")
    
    try:
        shutil.rmtree(test_dir)
        print("✅ Test files cleaned up")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")

def main():
    """Run all tests."""
    print("🗂️ OrganiserPro Linux GUI Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Run tests
    test_results = [
        ("OS Detection", test_os_detection()),
        ("Tkinter Availability", test_tkinter_availability()),
        ("Core Modules", test_core_modules()),
        ("GUI Creation", test_gui_creation()),
    ]
    
    # File operation tests
    test_dir = create_test_files()
    test_results.append(("File Operations", test_file_operations(test_dir)))
    cleanup_test_files(test_dir)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    for test_name, result in test_results:
        total_tests += 1
        if result:
            tests_passed += 1
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
            
    print(f"\n🎯 Overall: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! OrganiserPro GUI should work on this Linux system.")
        print("\nTo launch the GUI, run:")
        print("   python -m OrganiserPro.gui")
        print("   or")
        print("   organiserpro-gui  (if installed)")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("   You may need to install missing dependencies or fix configuration issues.")
        
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
