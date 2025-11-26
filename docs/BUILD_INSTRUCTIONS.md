# Building Standalone Application

This guide explains how to build EduContentTools as a standalone application for macOS and Windows.

## Prerequisites

1. Python 3.9 or higher installed
2. All dependencies installed: `pip install -r requirements.txt`

## Quick Build

### Option 1: Use the Build Script (Recommended)

```bash
python build_app.py
```

This will automatically:
- Install PyInstaller if needed
- Build the appropriate executable for your platform
- Create the app in the `dist/` folder

### Option 2: Manual Build

#### On macOS:
```bash
pyinstaller --onefile --name=EduContentTools --clean --noconfirm main.py
```

Or use the spec file for more control:
```bash
pyinstaller EduContentTools.spec
```

#### On Windows:
```bash
pyinstaller --onefile --name=EduContentTools --console --clean --noconfirm main.py
```

Or use the spec file:
```bash
pyinstaller EduContentTools.spec
```

## Output

After building, you'll find:

### macOS:
- **Executable**: `dist/EduContentTools`
- **App Bundle**: `dist/EduContentTools.app` (if using spec file)
- Run with: `./dist/EduContentTools` or double-click the .app

### Windows:
- **Executable**: `dist\EduContentTools.exe`
- Run with: `.\dist\EduContentTools.exe` or double-click

## Distribution

The standalone executable includes:
- ✓ All Python dependencies
- ✓ Python runtime
- ✓ All application code
- ✓ No installation required

### File Sizes (Approximate)
- macOS: ~50-80 MB
- Windows: ~40-70 MB

## Running the Standalone App

### First Time Setup:
1. Launch the application
2. Go to Settings (option `s`)
3. Configure Azure OpenAI credentials

### macOS Security Note:
If macOS blocks the app, go to:
`System Preferences → Security & Privacy → General`
and click "Open Anyway"

Or remove quarantine attribute:
```bash
xattr -dr com.apple.quarantine dist/EduContentTools.app
```

### Windows Security Note:
Windows Defender SmartScreen may show a warning. Click "More info" → "Run anyway"

## Data Storage

The application stores data in:
- **macOS**: Application directory → `games/` folder
- **Windows**: Application directory → `games\` folder

All game data, documents, and creations are stored locally alongside the executable.

## Updating the Application

To update:
1. Download the new version
2. Replace the old executable
3. Your game data in the `games/` folder will be preserved

## Troubleshooting

### Build Issues

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**PyInstaller errors:**
```bash
pip install --upgrade pyinstaller
```

**Clean build:**
```bash
rm -rf build/ dist/ *.spec
python build_app.py
```

### Runtime Issues

**App won't start:**
- Check that all dependencies are included in the spec file
- Try running from terminal to see error messages

**Import errors:**
- Add missing imports to `hiddenimports` in the spec file
- Rebuild the application

## Advanced: Custom Icon

### macOS (.icns):
```bash
pyinstaller --onefile --name=EduContentTools --icon=icon.icns main.py
```

### Windows (.ico):
```bash
pyinstaller --onefile --name=EduContentTools --icon=icon.ico main.py
```

## Building for Distribution

### macOS:
1. Build the app bundle: `pyinstaller EduContentTools.spec`
2. Test on different Mac systems (Intel and Apple Silicon)
3. Consider code signing for distribution
4. Create DMG installer (optional):
   ```bash
   hdiutil create -volname "EduContentTools" -srcfolder dist/EduContentTools.app -ov -format UDZO EduContentTools.dmg
   ```

### Windows:
1. Build the executable: `pyinstaller EduContentTools.spec`
2. Test on Windows 10/11
3. Consider code signing for distribution
4. Create installer with tools like Inno Setup or NSIS (optional)

## Cross-Platform Building

**Note**: You must build on each platform:
- Build macOS app **on** a Mac
- Build Windows exe **on** Windows

Cross-compilation is not supported by PyInstaller.

## File Structure After Build

```
EduContentTools/
├── dist/
│   ├── EduContentTools(.exe)      # Standalone executable
│   └── EduContentTools.app/       # macOS app bundle (if using spec)
├── build/                          # Temporary build files (can delete)
├── games/                          # Game data (preserved)
├── main.py                         # Source code
├── game_manager.py
├── settings.py
├── build_app.py                    # Build script
├── EduContentTools.spec            # PyInstaller spec
└── requirements.txt
```

## Distribution Checklist

- [ ] Build on target platform
- [ ] Test all features
- [ ] Include README with setup instructions
- [ ] Document Azure OpenAI setup requirements
- [ ] Zip/compress for distribution
- [ ] Include sample data (optional)
- [ ] Create user documentation

## Support

For issues with:
- **Building**: Check PyInstaller documentation
- **Application**: Check application logs
- **Azure OpenAI**: Verify API credentials in Settings
