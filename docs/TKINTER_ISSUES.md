# Tkinter Compatibility Issues - Solutions

## 🔴 Problem

The system Python's tkinter (Tk 8.5.9) on macOS 15+ (Sequoia/Sonoma) has compatibility issues causing crashes with the error:

```
macOS 26 (2601) or later required, have instead 16 (1601)!
```

This is a known issue with Apple's Command Line Tools Python and the older Tk framework.

## ✅ Solutions

### Option 1: Use CLI Version (Immediate Solution)

The CLI version works perfectly and has all the same features:

```bash
python main.py
```

**Advantages:**
- ✅ Works immediately
- ✅ All features available
- ✅ No installation needed
- ✅ Same backend, same data

### Option 2: Install Python.org Python (Recommended for GUI)

Install the official Python from python.org which includes a working tkinter:

1. **Download Python:**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.11 or 3.12 (latest stable)
   - Choose the "macOS 64-bit universal2 installer"

2. **Install:**
   - Run the downloaded .pkg file
   - Follow the installation wizard
   - Python will be installed to `/Library/Frameworks/Python.framework/`

3. **Update your environment:**
   ```bash
   # Find the new Python
   which python3.11  # or python3.12
   
   # Create new virtual environment with this Python
   python3.11 -m venv .venv-gui
   source .venv-gui/bin/activate
   pip install -r requirements.txt
   
   # Run GUI
   python gui_app.py
   ```

### Option 3: Use Homebrew Python

Install Python via Homebrew, which includes tkinter:

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python with tkinter
brew install python@3.11
brew install python-tk@3.11

# Create virtual environment
python3.11 -m venv .venv-homebrew
source .venv-homebrew/bin/activate
pip install -r requirements.txt

# Run GUI
python gui_app.py
```

### Option 4: Use PyQt5 Instead (Alternative GUI Framework)

If tkinter continues to have issues, we can rewrite the GUI using PyQt5:

```bash
pip install PyQt5

# Future: Create gui_qt.py using PyQt5
# (More complex but more powerful and stable)
```

### Option 5: Build on Different Machine

Build the standalone executable on a machine with working tkinter:

- **macOS 12-14** (Monterey, Ventura, Sonoma earlier versions)
- **macOS 11** (Big Sur)
- **Another Mac** without Command Line Tools Python

Then distribute the executable.

## 🔍 Checking Your Setup

### Check Python Version:
```bash
python --version
which python
```

### Check Tkinter:
```bash
python -c "import tkinter; print('Tkinter works!')"
```

### Check Tk Version:
```bash
python -c "import tkinter; root = tkinter.Tk(); print(root.tk.eval('info patchlevel')); root.destroy()"
```

**Desired Output:**
- Tk version 8.6.x or higher (not 8.5.9)

## 🎯 Current Workarounds Applied

The launcher now includes:

1. **Graceful Fallback:**
   ```bash
   python launcher.py
   # Automatically uses CLI if GUI fails
   ```

2. **Explicit Mode Selection:**
   ```bash
   python launcher.py --cli   # Force CLI
   python launcher.py --gui   # Force GUI (with error if can't)
   ```

3. **Better Error Messages:**
   - Clear explanation of the problem
   - Actionable solutions
   - Automatic fallback to CLI

## 📊 Python Distribution Comparison

| Distribution | Tk Version | Works on macOS 15+ | Recommended |
|--------------|------------|-------------------|-------------|
| Command Line Tools | 8.5.9 | ❌ Crashes | ❌ |
| Python.org | 8.6.13+ | ✅ Works | ✅ Yes |
| Homebrew | 8.6.x | ✅ Works | ✅ Yes |
| Anaconda | 8.6.x | ✅ Works | ✅ Yes |
| pyenv | 8.6.x | ✅ Works | ⚠️ Requires setup |

## 🚀 Quick Fix Commands

### For Development (use CLI):
```bash
# Use CLI version - works everywhere
python main.py
```

### For GUI (Python.org):
```bash
# Download from python.org first, then:
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m venv .venv-gui
source .venv-gui/bin/activate
pip install -r requirements.txt
python gui_app.py
```

### For GUI (Homebrew):
```bash
# Install Homebrew Python first, then:
brew install python@3.11 python-tk@3.11
python3.11 -m venv .venv-homebrew
source .venv-homebrew/bin/activate
pip install -r requirements.txt
python gui_app.py
```

## 📝 Building Standalone Apps

**On macOS with Working Tkinter:**
```bash
# Use Python.org or Homebrew Python
python build_gui.py gui

# Test
./dist/EduContentTools
```

**On Windows:**
```bash
# Windows doesn't have this issue
python build_gui.py gui
.\dist\EduContentTools.exe
```

## 🔧 Why This Happens

**Technical Background:**

1. **Apple's Command Line Tools Python:**
   - Uses system Tk framework (version 8.5.9)
   - System Tk is very old and not maintained
   - Has hardcoded macOS version checks
   - Breaks on newer macOS versions

2. **Python.org/Homebrew Python:**
   - Bundles its own Tk 8.6.x
   - Doesn't depend on system Tk
   - Works across macOS versions
   - Actively maintained

3. **The Version Check:**
   - Tk 8.5.9 checks for macOS version
   - Expects version format 10.x (older macOS)
   - macOS 15+ uses version 26.x (new format)
   - Check fails → crashes with "abort()"

## ✅ Recommended Approach

**For Personal Use:**
1. Install Python from python.org
2. Use GUI with that Python
3. Keep CLI as backup

**For Distribution:**
1. Build GUI on macOS 12-14 or Windows
2. Include CLI version as well
3. Document tkinter requirements

**For Development:**
1. Use CLI version for now
2. Build GUI on compatible system
3. Test standalone executables

## 📞 Next Steps

1. **Immediate:** Use CLI version
   ```bash
   python main.py
   ```

2. **Short-term:** Install Python.org Python for GUI

3. **Long-term:** Build standalone executables on compatible systems

---

**Updated:** November 26, 2025  
**Status:** Workarounds implemented, CLI fallback working  
**Recommendation:** Use CLI on Command Line Tools Python, or install Python.org Python for GUI
