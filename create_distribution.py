#!/usr/bin/env python3
"""
Create a distribution package for EduContentTools
"""

import os
import sys
import shutil
import platform
from datetime import datetime

def create_distribution():
    """Create a distribution package."""
    
    system = platform.system()
    timestamp = datetime.now().strftime("%Y%m%d")
    
    print("=" * 70)
    print("    CREATING DISTRIBUTION PACKAGE")
    print("=" * 70)
    
    # Check if executable exists
    if system == "Darwin":
        exe_name = "EduContentTools"
        package_name = f"EduContentTools-macOS-{timestamp}"
    elif system == "Windows":
        exe_name = "EduContentTools.exe"
        package_name = f"EduContentTools-Windows-{timestamp}"
    else:
        exe_name = "EduContentTools"
        package_name = f"EduContentTools-Linux-{timestamp}"
    
    exe_path = os.path.join("dist", exe_name)
    
    if not os.path.exists(exe_path):
        print(f"\n✗ Executable not found: {exe_path}")
        print("Please build the application first with: python build_app.py")
        sys.exit(1)
    
    # Create package directory
    package_dir = os.path.join("dist", package_name)
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    print(f"\n📦 Creating package: {package_name}")
    print("-" * 70)
    
    # Copy executable
    print(f"✓ Copying executable: {exe_name}")
    shutil.copy2(exe_path, os.path.join(package_dir, exe_name))
    
    # Copy documentation
    docs = [
        ("STANDALONE_README.md", "README.md"),
        ("BUILD_INSTRUCTIONS.md", "BUILD_INSTRUCTIONS.md"),
        ("EXPORT_FORMATS.md", "EXPORT_FORMATS.md"),
        ("requirements.txt", "requirements.txt"),
    ]
    
    for src, dst in docs:
        if os.path.exists(src):
            print(f"✓ Copying: {src} → {dst}")
            shutil.copy2(src, os.path.join(package_dir, dst))
    
    # Create games folder
    games_dir = os.path.join(package_dir, "games")
    os.makedirs(games_dir)
    print(f"✓ Created: games/ folder")
    
    # Create a README in games folder
    with open(os.path.join(games_dir, "README.txt"), 'w') as f:
        f.write("Game Data Folder\n")
        f.write("=" * 50 + "\n\n")
        f.write("This folder stores all your game data:\n")
        f.write("- World files (.mcworld)\n")
        f.write("- Uploaded documents (PDF, Word, PowerPoint)\n")
        f.write("- Language analysis\n")
        f.write("- Created resources (guides, workbooks, etc.)\n\n")
        f.write("Keep this folder with the application.\n")
        f.write("Backup this folder to preserve your data.\n")
    
    # Create zip archive
    print(f"\n📦 Creating archive...")
    archive_path = shutil.make_archive(
        os.path.join("dist", package_name),
        'zip',
        'dist',
        package_name
    )
    
    # Get file sizes
    exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
    zip_size = os.path.getsize(archive_path) / (1024 * 1024)  # MB
    
    print("\n" + "=" * 70)
    print("    DISTRIBUTION PACKAGE CREATED!")
    print("=" * 70)
    print(f"\n📦 Package: {package_name}")
    print(f"📁 Location: dist/{package_name}/")
    print(f"📚 Archive: {os.path.basename(archive_path)}")
    print(f"\n📊 Sizes:")
    print(f"   Executable: {exe_size:.1f} MB")
    print(f"   Archive: {zip_size:.1f} MB")
    
    print(f"\n📋 Package Contents:")
    print(f"   - {exe_name}")
    print(f"   - README.md (user guide)")
    print(f"   - BUILD_INSTRUCTIONS.md")
    print(f"   - EXPORT_FORMATS.md")
    print(f"   - requirements.txt")
    print(f"   - games/ (data folder)")
    
    print(f"\n✓ Ready for distribution!")
    print(f"\n📤 Share: {archive_path}")
    print("=" * 70)

if __name__ == "__main__":
    try:
        create_distribution()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
