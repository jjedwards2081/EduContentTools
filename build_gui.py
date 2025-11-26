#!/usr/bin/env python3
"""
Build script for creating standalone EduContentTools executables.
Supports both GUI and CLI versions.
"""

import subprocess
import sys
import os
import platform


def build_app(mode="gui"):
    """Build the standalone application using PyInstaller.
    
    Args:
        mode: "gui" for GUI app (default), "cli" for CLI app, "both" for both
    """
    print("=" * 70)
    print("Building EduContentTools Standalone Application")
    print("=" * 70)
    print()
    
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    print(f"Mode: {mode.upper()}")
    print()
    
    builds = []
    if mode == "both":
        builds = [("gui", "EduContentTools"), ("cli", "EduContentTools-CLI")]
    elif mode == "gui":
        builds = [("gui", "EduContentTools")]
    elif mode == "cli":
        builds = [("cli", "EduContentTools-CLI")]
    else:
        print(f"Error: Unknown mode '{mode}'")
        return False
    
    all_success = True
    
    for build_mode, app_name in builds:
        print("-" * 70)
        print(f"Building {build_mode.upper()} version: {app_name}")
        print("-" * 70)
        
        # Determine entry point and options
        if build_mode == "gui":
            entry_point = "gui_app.py"
            # On Windows, use --noconsole to hide console window for GUI
            extra_args = ["--noconsole"] if platform.system() == "Windows" else []
        else:
            entry_point = "main.py"
            extra_args = []
        
        # Build command using the current Python interpreter
        build_cmd = [
            sys.executable,
            "-m", "PyInstaller",
            "--onefile",
            "--name", app_name,
            "--clean",
            "--noconfirm",
        ] + extra_args + [
            # Hidden imports
            "--hidden-import", "openai",
            "--hidden-import", "PyPDF2",
            "--hidden-import", "docx",
            "--hidden-import", "pptx",
            "--hidden-import", "reportlab",
            "--hidden-import", "reportlab.platypus",
            "--hidden-import", "reportlab.lib",
            "--hidden-import", "reportlab.lib.styles",
            "--hidden-import", "reportlab.lib.pagesizes",
            "--hidden-import", "reportlab.lib.units",
            "--hidden-import", "reportlab.lib.colors",
            entry_point
        ]
        
        print(f"Entry point: {entry_point}")
        print(f"Building...")
        print()
        
        try:
            # Run PyInstaller
            result = subprocess.run(build_cmd, check=True, capture_output=True, text=True)
            
            print(f"[OK] {app_name} build completed successfully!")
            print()
            
        except subprocess.CalledProcessError as e:
            print()
            print(f"[ERROR] {app_name} build failed with error code {e.returncode}")
            print()
            if e.stderr:
                print("Error output:")
                print(e.stderr[-500:])  # Last 500 chars
            all_success = False
        
        except Exception as e:
            print()
            print(f"[ERROR] Unexpected error building {app_name}: {e}")
            all_success = False
    
    if all_success:
        print()
        print("=" * 70)
        print("[OK] All builds completed successfully!")
        print("=" * 70)
        print()
        print("Executable location(s):")
        
        for _, app_name in builds:
            if platform.system() == "Windows":
                print(f"  dist/{app_name}.exe")
            else:
                print(f"  dist/{app_name}")
        
        print()
        print("To run the GUI version:")
        if platform.system() == "Windows":
            print("  .\\dist\\EduContentTools.exe")
        else:
            print("  ./dist/EduContentTools")
        
        print()
        print("To create a distribution package, run:")
        print("  python create_distribution.py")
        
        return True
    else:
        print()
        print("=" * 70)
        print("[ERROR] Some builds failed")
        print("=" * 70)
        print()
        print("Common fixes:")
        print("  1. Ensure PyInstaller is installed: pip install pyinstaller")
        print("  2. Check that all dependencies are installed: pip install -r requirements.txt")
        print("  3. Try cleaning build artifacts: rm -rf build/ dist/ *.spec")
        return False


if __name__ == "__main__":
    # Check command line arguments
    mode = "gui"  # Default to GUI
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--gui", "gui"]:
            mode = "gui"
        elif sys.argv[1] in ["--cli", "cli"]:
            mode = "cli"
        elif sys.argv[1] in ["--both", "both"]:
            mode = "both"
        else:
            print(f"Usage: {sys.argv[0]} [gui|cli|both]")
            print("  gui  - Build GUI version only (default)")
            print("  cli  - Build CLI version only")
            print("  both - Build both GUI and CLI versions")
            sys.exit(1)
    
    success = build_app(mode)
    sys.exit(0 if success else 1)
