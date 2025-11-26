#!/usr/bin/env python3
"""
Build script for creating standalone executables for Mac and Windows
"""

import os
import sys
import platform
import subprocess

def install_pyinstaller():
    """Ensure PyInstaller is installed."""
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"], check=True)

def build_executable():
    """Build the standalone executable using PyInstaller."""
    
    system = platform.system()
    print(f"\nBuilding for {system}...")
    
    # Base PyInstaller command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",  # Create a single executable file
        "--name=EduContentTools",  # Name of the executable
        "--clean",  # Clean cache and remove temporary files
        "--noconfirm",  # Replace output directory without asking
        # Add application icon (optional - you can add later)
        # "--icon=icon.ico",  # For Windows
        # "--icon=icon.icns",  # For Mac
    ]
    
    # Platform-specific settings
    if system == "Darwin":  # macOS
        cmd.extend([
            "--osx-bundle-identifier=com.educontenttools.app",
        ])
    elif system == "Windows":
        cmd.extend([
            "--console",  # Keep console window
        ])
    
    # Add the main script
    cmd.append("main.py")
    
    print(f"\nRunning: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    print("\n" + "=" * 70)
    print("BUILD COMPLETE!")
    print("=" * 70)
    
    if system == "Darwin":
        print(f"\n📦 Executable created: dist/EduContentTools")
        print(f"\nTo run: ./dist/EduContentTools")
    elif system == "Windows":
        print(f"\n📦 Executable created: dist\\EduContentTools.exe")
        print(f"\nTo run: .\\dist\\EduContentTools.exe")
    else:
        print(f"\n📦 Executable created in: dist/")
    
    print("\n" + "=" * 70)

def main():
    """Main build process."""
    print("=" * 70)
    print("    EDU CONTENT TOOLS - BUILD STANDALONE APP")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("\n✗ Error: main.py not found!")
        print("Please run this script from the EduContentTools directory.")
        sys.exit(1)
    
    try:
        # Install PyInstaller
        install_pyinstaller()
        
        # Build the executable
        build_executable()
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
