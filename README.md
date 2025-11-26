# EduContentTools

A powerful CLI application for creating educational content from Minecraft Education worlds, with AI-powered content generation and multi-format export capabilities.

## 🎯 Features

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

### Option 1: Standalone Application (Recommended)
Download the pre-built executable for your platform - no Python required!

**macOS**: Extract and run `EduContentTools`  
**Windows**: Extract and run `EduContentTools.exe`

See [docs/STANDALONE_README.md](docs/STANDALONE_README.md) for detailed instructions.

### Option 2: Run from Source

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python main.py
```

## 📋 Main Menu Options

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

- [Standalone App Guide](docs/STANDALONE_README.md) - User guide for executables
- [Build Instructions](docs/BUILD_INSTRUCTIONS.md) - Build from source
- [Export Formats](docs/EXPORT_FORMATS.md) - Export format details
- [Complete Overview](docs/STANDALONE_COMPLETE.md) - Full documentation

## 🛠️ Building

To build standalone executables:

```bash
python build_app.py
```

To create distribution packages:

```bash
python create_distribution.py
```

See [docs/BUILD_INSTRUCTIONS.md](docs/BUILD_INSTRUCTIONS.md) for details.

## 📦 Distribution

Pre-built executables available in `dist/` folder:
- `EduContentTools-macOS-[date].zip` - macOS version
- `EduContentTools-Windows-[date].zip` - Windows version (build on Windows)

## 📄 License

MIT
