# EduContentTools - Standalone Application

A powerful tool for creating educational content for Minecraft Education Edition games.

## Quick Start

### macOS
1. Download `EduContentTools` (executable file)
2. Open Terminal and navigate to the download folder
3. Make it executable: `chmod +x EduContentTools`
4. Run: `./EduContentTools`

**First time on macOS**: If macOS blocks the app:
```bash
xattr -dr com.apple.quarantine EduContentTools
```

Or: `System Preferences → Security & Privacy → General` → Click "Open Anyway"

### Windows
1. Download `EduContentTools.exe`
2. Double-click to run
3. If Windows Defender SmartScreen appears, click "More info" → "Run anyway"

## First Time Setup

1. Launch EduContentTools
2. Press `s` for Settings
3. Configure your Azure OpenAI API credentials:
   - API Endpoint
   - API Key
   - Deployment Name
   - API Version (default: 2024-02-15-preview)

## Features

✓ **Game Management**
- Create and organize game folders
- Upload .mcworld files (auto-extracts language files)
- Load and switch between multiple games

✓ **Content Creation**
- AI-powered content generation
- Student guides, workbooks, and quizzes
- Parent and teacher guides
- School leadership information sheets
- Curriculum standards mapping (9+ countries)
- Text complexity analysis

✓ **Document Analysis**
- Upload and analyze PDF, Word, and PowerPoint files
- Automatic AI analysis integration
- Document management (add/remove)

✓ **Multi-Format Export**
- Export in Markdown, Word, or PDF format
- Professional formatting and styling
- Organized by resource type
- Exports to Downloads folder

## Usage

### Creating a Game
1. Press `1` to create a new game
2. Enter a unique game name
3. Upload world file (option `3`)
4. Add documents for analysis (option `d`)

### Creating Educational Content
- `a` - Student Guide
- `b` - Student Workbook
- `c` - Student Quiz
- `p` - Parent Guide
- `t` - Teacher Guide
- `sl` - School Leadership Info Sheet
- `cs` - Curriculum Standards Mapping
- `tc` - Text Complexity Analysis

### Exporting Content
1. Press `e` for Export
2. Choose format:
   - `1` - Markdown (.md)
   - `2` - Word Document (.docx)
   - `3` - PDF (.pdf)
3. Files exported to Downloads folder

### Managing Games
- `l` - List all games
- `2` - Load different game
- `x` - Delete game folder

## Data Storage

All data is stored locally in the `games/` folder next to the executable:

```
EduContentTools/
├── EduContentTools (executable)
└── games/
    ├── Game1/
    │   ├── worlds/
    │   ├── documents/
    │   ├── lang/
    │   ├── creations/
    │   └── metadata.json
    └── Game2/
        └── ...
```

## System Requirements

- **macOS**: 10.13 or later (Intel or Apple Silicon)
- **Windows**: Windows 10 or later
- **Disk Space**: ~50MB for app + space for game data
- **Internet**: Required for Azure OpenAI API calls

## Azure OpenAI Setup

You need an Azure OpenAI account with:
1. An active subscription
2. A deployed GPT model (GPT-4 recommended)
3. API key and endpoint URL

To get started:
1. Visit [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource
3. Deploy a GPT model
4. Copy your API key and endpoint

## Troubleshooting

### Application Won't Start

**macOS**: Remove quarantine attribute
```bash
xattr -dr com.apple.quarantine EduContentTools
```

**Windows**: Run as Administrator (right-click → Run as Administrator)

### API Connection Issues
- Verify your Azure OpenAI credentials in Settings (option `s`)
- Test connection (option `5` in Settings menu)
- Check internet connection

### Missing Features/Errors
- Ensure all dependencies are bundled correctly
- Check application directory for `games/` folder
- Application creates folders automatically on first run

### Export Issues

**Word/PDF export fails**:
- All required libraries are bundled
- Check disk space in Downloads folder
- Ensure Downloads folder is accessible

### Game Data Not Found
- Keep `games/` folder in same directory as executable
- Don't move games manually - use in-app management

## Updates

To update the application:
1. Download the new version
2. Replace the old executable
3. Your `games/` folder data is preserved

**Backup**: Before updating, copy your `games/` folder to a safe location.

## Support & Documentation

For detailed documentation, see:
- `BUILD_INSTRUCTIONS.md` - Building from source
- `EXPORT_FORMATS.md` - Export format details
- `README.md` - Development documentation

## Privacy & Data

- All game data stored locally
- No data sent except to your Azure OpenAI endpoint
- API calls use your Azure OpenAI credentials
- No telemetry or usage tracking

## License

MIT License - See LICENSE file for details

## Credits

Built with:
- Python
- Azure OpenAI API
- ReportLab (PDF generation)
- python-docx (Word documents)
- PyInstaller (standalone packaging)

---

**Version**: 1.0.0  
**Build Date**: November 2025  
**Platform**: macOS & Windows
