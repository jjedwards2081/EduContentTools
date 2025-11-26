# Repository Structure

## 📁 Root Directory

```
EduContentTools/
├── .gitignore              # Git ignore rules
├── .venv/                  # Virtual environment (ignored by git)
├── README.md               # Main documentation
├── requirements.txt        # Python dependencies
│
├── main.py                 # Application entry point
├── game_manager.py         # Core game management logic
├── settings.py             # Configuration management
│
├── build_app.py           # Build standalone executable
├── create_distribution.py # Create distribution packages
├── EduContentTools.spec   # PyInstaller configuration
│
├── docs/                  # Documentation
│   ├── BUILD_INSTRUCTIONS.md
│   ├── EXPORT_FORMATS.md
│   ├── STANDALONE_README.md
│   └── STANDALONE_COMPLETE.md
│
├── dist/                  # Distribution packages
│   └── EduContentTools-macOS-20251126.zip
│
└── games/                 # User data (game projects)
    └── [game-name]/
        ├── game_info.json
        ├── worlds/
        ├── documents/
        ├── lang/
        ├── creations/
        └── exports/
```

## 🧹 Cleaned Up

### Removed:
- ❌ `build/` - Temporary PyInstaller build files
- ❌ `dist/EduContentTools` - Loose executable (kept in ZIP)
- ❌ `dist/EduContentTools-macOS-20251126/` - Unzipped folder
- ❌ `*.pyc` files
- ❌ `__pycache__/` directories

### Organized:
- ✅ Moved all documentation to `docs/`
- ✅ Kept only distribution ZIP in `dist/`
- ✅ Added `.gitignore` for future builds

## 📦 Distribution Files

**Ready to share:**
- `dist/EduContentTools-macOS-20251126.zip` (21 MB)

**To build for Windows:**
```bash
# On a Windows machine:
python build_app.py
python create_distribution.py
```

## 🔧 Development Commands

**Run from source:**
```bash
python main.py
```

**Build executable:**
```bash
python build_app.py
```

**Create distribution:**
```bash
python create_distribution.py
```

**Clean build artifacts:**
```bash
rm -rf build/ dist/EduContentTools dist/EduContentTools-*/
```

## 📝 File Descriptions

### Core Application Files
- **main.py** (97 KB) - Main CLI interface and menu system
- **game_manager.py** (117 KB) - Game logic, file processing, AI integration, exports
- **settings.py** (2.4 KB) - Azure OpenAI configuration management

### Build Files
- **build_app.py** (2.7 KB) - Automated PyInstaller build script
- **create_distribution.py** (3.9 KB) - Distribution package creation
- **EduContentTools.spec** (667 B) - PyInstaller configuration

### Documentation
- **README.md** - Main project documentation
- **docs/STANDALONE_README.md** - User guide for standalone app
- **docs/BUILD_INSTRUCTIONS.md** - Developer build guide
- **docs/EXPORT_FORMATS.md** - Export format specifications
- **docs/STANDALONE_COMPLETE.md** - Complete overview

## 🎯 Repository is Clean!

The repository is now organized and production-ready:
- ✅ No temporary build files
- ✅ Documentation organized in `docs/`
- ✅ Clean distribution in `dist/`
- ✅ Proper `.gitignore` in place
- ✅ Updated README with clear structure
