# EduContentTools - GUI Application Guide

## 🎨 Desktop GUI Application

EduContentTools now includes a modern desktop GUI application alongside the CLI version!

### Features

**Clean, Modern Interface:**
- ✅ Tabbed interface for easy navigation
- ✅ Visual game management with list view
- ✅ Real-time status updates
- ✅ Multi-threaded operations (no freezing during AI tasks)
- ✅ Native look and feel on macOS and Windows

**Main Components:**

1. **Overview Tab** 📋
   - View game information at a glance
   - Upload world files and documents
   - Extract language files
   - See status and progress

2. **Content Tab** ✏️
   - Edit game context
   - Edit gameplay description
   - Edit learning objectives
   - Save all content with one click

3. **Create Tab** 🎨
   - Student resources (guides, workbooks, quizzes)
   - Parent and teacher guides
   - School leadership materials
   - Curriculum standards mapping
   - Text complexity analysis
   - Real-time progress display

4. **Export Tab** 📤
   - Export to Markdown, Word, or PDF
   - Visual format selection
   - Export log display

### Running the GUI

**From Source:**
```bash
# GUI mode (default)
python gui_app.py

# Or use the launcher
python launcher.py

# Explicitly request GUI
python launcher.py --gui
```

**Standalone Executable:**
```bash
# Build GUI version
python build_gui.py

# Or build both GUI and CLI
python build_gui.py both

# Run the executable
./dist/EduContentTools          # macOS
.\dist\EduContentTools.exe      # Windows
```

### CLI vs GUI

**CLI Version:**
- Traditional command-line interface
- Menu-driven navigation
- Best for: SSH, automation, scripting
- Run: `python main.py` or `python launcher.py --cli`

**GUI Version:**
- Modern desktop application
- Visual, mouse-driven interface
- Best for: Daily use, non-technical users
- Run: `python gui_app.py` or `python launcher.py --gui`

### System Requirements

**GUI Application:**
- **Python**: 3.7 or higher
- **tkinter**: Usually included with Python
- **Operating System**:
  - macOS 10.15 (Catalina) or later
  - Windows 10 or later
  - Linux with X11 or Wayland

**Note**: If tkinter is not available, the application will fall back to CLI mode.

### Building Standalone Executables

**Build GUI Only:**
```bash
python build_gui.py gui
```

**Build CLI Only:**
```bash
python build_gui.py cli
```

**Build Both:**
```bash
python build_gui.py both
```

**Output:**
- GUI: `dist/EduContentTools` (or `.exe` on Windows)
- CLI: `dist/EduContentTools-CLI` (or `.exe` on Windows)

### Distribution

**For End Users:**

The GUI executable provides the best experience:
- No Python installation needed
- Double-click to run
- Native macOS/Windows look
- No command line knowledge required

**For Power Users:**

The CLI executable provides:
- Full feature parity with GUI
- Automation capabilities
- SSH-friendly
- Lower resource usage

### Troubleshooting

**GUI won't start:**
1. Check Python version: `python --version` (need 3.7+)
2. Test tkinter: `python -c "import tkinter; tkinter.Tk()"`
3. Fall back to CLI: `python launcher.py --cli`

**macOS: "App is damaged" message:**
```bash
xattr -dr com.apple.quarantine EduContentTools
```

**Windows: SmartScreen warning:**
1. Click "More info"
2. Click "Run anyway"

**Performance issues:**
- GUI uses threading to prevent freezing during AI operations
- Close other resource-intensive applications
- Ensure adequate RAM (4GB+ recommended)

### Keyboard Shortcuts

**Global:**
- `Cmd/Ctrl + Q` - Quit application
- `Cmd/Ctrl + W` - Close window
- `Tab` - Navigate between fields
- `Enter` - Activate focused button

**Text Editing:**
- `Cmd/Ctrl + A` - Select all
- `Cmd/Ctrl + C` - Copy
- `Cmd/Ctrl + V` - Paste
- `Cmd/Ctrl + X` - Cut
- `Cmd/Ctrl + Z` - Undo

### Interface Themes

The GUI automatically uses the best available theme for your platform:

- **macOS**: Aqua theme (native macOS look)
- **Windows**: Vista/Windows theme (native Windows look)
- **Linux**: Clam theme (clean cross-platform look)

### API Integration

The GUI uses the same backend as the CLI (`game_manager.py`), ensuring:
- ✅ Feature parity between CLI and GUI
- ✅ Shared data format
- ✅ Consistent behavior
- ✅ Easy maintenance

### Development

**File Structure:**
```
gui_app.py          # Main GUI application
main.py             # CLI application
launcher.py         # Universal launcher (auto-detects)
game_manager.py     # Shared backend/API
settings.py         # Configuration management
build_gui.py        # Build script for GUI/CLI
```

**Adding Features:**

To add a new feature:
1. Implement backend logic in `game_manager.py`
2. Add CLI interface in `main.py`
3. Add GUI interface in `gui_app.py`
4. Test both interfaces

**Backend API Pattern:**
```python
# In game_manager.py
def new_feature(self, game_name, params):
    """Implement feature logic here."""
    # Do work
    return result

# In main.py (CLI)
def new_feature_cli(self):
    """CLI interface for new feature."""
    result = self.game_manager.new_feature(self.current_game, params)
    print(f"Result: {result}")

# In gui_app.py (GUI)
def new_feature_gui(self):
    """GUI interface for new feature."""
    def task():
        result = self.game_manager.new_feature(self.current_game, params)
        self.root.after(0, lambda: self.show_result(result))
    threading.Thread(target=task, daemon=True).start()
```

### Future Enhancements

Potential improvements:
- [ ] Drag-and-drop file upload
- [ ] Progress bars for long operations
- [ ] Recent games menu
- [ ] Keyboard shortcuts panel
- [ ] Dark mode theme
- [ ] Custom icons and branding
- [ ] Preferences panel
- [ ] Inline document preview
- [ ] Export preview
- [ ] Undo/redo for content editing

### Support

**GUI Issues:**
- Check tkinter installation
- Update Python to latest version
- Report issues with screenshots

**Feature Requests:**
- GUI feature parity maintained with CLI
- Suggest UI improvements
- Request new creation types

---

**Version**: 1.0.0 with GUI  
**Updated**: November 26, 2025  
**Status**: ✅ Production Ready
