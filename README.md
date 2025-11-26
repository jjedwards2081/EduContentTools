# EduContentTools

A powerful desktop application for creating educational content from Minecraft Education worlds, with AI-powered content generation and multi-format export capabilities.

## 🎯 Features

- **🎨 Modern GUI or CLI**: Choose between a clean desktop interface or traditional command-line
- **Game Management**: Create, organize, and manage game projects
- **World File Processing**: Upload and extract language files from .mcworld files
- **Document Analysis**: Analyze supporting documents (PDF, Word, PowerPoint)
- **AI-Powered Content Creation**: Generate comprehensive educational resources:
  - Student guides, workbooks, and quizzes
  - Parent guides and teacher implementation guides
  - School leadership information sheets
  - Curriculum standards mapping (9+ countries)
  - Text complexity analysis
- **Multi-Format Export**: Export in Markdown, Word, or PDF with proper table formatting
- **Automated Workflows**: Automatic extraction and analysis when files are uploaded

## 🚀 Quick Start

> **⚠️ macOS 15+ GUI Users:** If you get a crash, see **[QUICKFIX.md](QUICKFIX.md)** for a 5-minute solution!

### Option 1: Standalone Application (Recommended) 🎨
Download the pre-built executable for your platform - no Python required!

**macOS**: Extract and run `EduContentTools` (GUI mode)  
**Windows**: Extract and run `EduContentTools.exe` (GUI mode)

The GUI provides a modern, visual interface with tabbed navigation, drag-and-drop support, and real-time progress updates.

See [docs/STANDALONE_README.md](docs/STANDALONE_README.md) for detailed instructions.

### Option 2: Run from Source

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:

**Universal Launcher (Recommended):**
```bash
python launcher.py           # Starts in CLI mode (safe default)
python launcher.py --cli     # Explicitly use CLI mode
python launcher.py --gui     # Try GUI mode (requires compatible Python)
```

**Direct Launch:**
```bash
python gui_app.py    # GUI mode
python main.py       # CLI mode
```

> **⚠️ macOS 15+ GUI Issue:** Command Line Tools Python uses old Tk 8.5 which crashes. **Solution:** Install Python from python.org or Homebrew. See **[QUICKFIX.md](QUICKFIX.md)** for step-by-step instructions (5 minutes). Detailed info: [docs/TKINTER_ISSUES.md](docs/TKINTER_ISSUES.md)

## 🎨 GUI Interface

The desktop GUI provides:
- **📋 Overview Tab**: View game info, upload files, extract language data
- **✏️ Content Tab**: Edit context, gameplay, and objectives
- **🎨 Create Tab**: Generate all content types with visual progress
- **📤 Export Tab**: Export to Markdown, Word, or PDF with logs

See [docs/GUI_GUIDE.md](docs/GUI_GUIDE.md) for complete GUI documentation.

## 📋 CLI Menu Options

1. **Create New Game** - Start a new educational content project
2. **Load Existing Game** - Continue working on a saved project
3. **Upload World File** - Add .mcworld file (auto-extracts language data)
4. **Upload Documents** - Add supporting materials (PDF, Word, PPT)
5. **Create Content** - Generate educational resources with AI assistance
6. **Export All Creations** - Export everything in MD/Word/PDF format
7. **Settings** - Configure Azure OpenAI credentials
8. **Delete Game** - Remove a game project (with confirmation)
9. **Exit**

### Content Creation Options

- 📚 **Student Resources**: Guides, workbooks, quizzes
- 👨‍👩‍👧 **Parent Resources**: Implementation guides and support materials
- 🍎 **Teacher Resources**: Lesson plans and classroom strategies
- 🏫 **Leadership Materials**: Executive summaries for administrators
- 🌍 **Curriculum Mapping**: Align to standards (9+ countries supported)
- ♿ **Accessibility Analysis**: Text complexity with simplification recommendations

### Export Formats

All exports include properly formatted tables and are organized by category:

- **Markdown (.md)**: Editable text format
- **Word (.docx)**: Professional formatting with tables
- **PDF (.pdf)**: Print-ready with formatted tables

Exports are saved to `games/[game-name]/exports/` with a detailed README.

## ⚙️ Configuration

Configure Azure OpenAI credentials in Settings (option 7):

- **API Endpoint**: `https://your-resource.openai.azure.com/`
- **API Key**: Your Azure OpenAI API key
- **Deployment Name**: Your model deployment name
- **API Version**: Default `2024-02-15-preview`

## 💾 Data Storage

**Standalone App**: Data stored in `games/` folder next to executable  
**Python Version**: Data stored in project `games/` folder

Structure:
```
games/
├── [game-name]/
│   ├── game_info.json
│   ├── worlds/
│   ├── documents/
│   ├── lang/
│   ├── creations/
│   └── exports/
```

## 🔧 Requirements

### Standalone Application
- No requirements! Just download and run
- Available for macOS and Windows

### Running from Source
- Python 3.9+
- Dependencies in `requirements.txt`:
  - openai >= 1.0.0
  - PyPDF2 >= 3.0.0
  - python-docx >= 1.0.0
  - python-pptx >= 0.6.0
  - reportlab >= 4.0.0
  - pyinstaller >= 6.0.0 (for building)

## 📚 Documentation

- **[GUI Guide](docs/GUI_GUIDE.md)** - Desktop application user guide
- **[Tkinter Issues](docs/TKINTER_ISSUES.md)** - ⚠️ macOS 15+ GUI compatibility solutions
- **[Standalone App Guide](docs/STANDALONE_README.md)** - User guide for executables
- **[Build Instructions](docs/BUILD_INSTRUCTIONS.md)** - Build from source
- **[Export Formats](docs/EXPORT_FORMATS.md)** - Export format details
- **[Complete Overview](docs/STANDALONE_COMPLETE.md)** - Full documentation

## 🛠️ Building

**Build GUI Application (Recommended):**
```bash
python build_gui.py gui
```

**Build CLI Application:**
```bash
python build_gui.py cli
```

**Build Both:**
```bash
python build_gui.py both
```

**Create Distribution Packages:**
```bash
python create_distribution.py
```

See [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md) for details.

## 📦 Distribution

Pre-built executables available in `dist/` folder:
- `EduContentTools-macOS-[date].zip` - macOS version (GUI + CLI)
- `EduContentTools-Windows-[date].zip` - Windows version (GUI + CLI) - build on Windows

**What's included:**
- GUI executable (modern desktop interface)
- CLI executable (command-line interface)
- Complete documentation
- Example games folder structure

## 📄 License

MIT
