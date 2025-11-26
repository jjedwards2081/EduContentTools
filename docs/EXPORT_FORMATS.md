# Export Format Guide

The EduContentTools application now supports exporting all your created resources in three different formats to suit various needs.

## Available Export Formats

### 1. Markdown (.md)
**Best for:** Editing, version control, and universal compatibility

**Advantages:**
- Editable in any text editor
- No additional dependencies required
- Perfect for version control systems (Git)
- Can be converted to other formats later
- Small file size

**Opens with:**
- Any text editor (Notepad, TextEdit, VS Code, etc.)
- Markdown viewers (Typora, Marked, etc.)
- Most modern word processors

### 2. Word Document (.docx)
**Best for:** Professional presentations and collaborative editing

**Advantages:**
- Professional formatting with headers and bullet points
- Native Microsoft Word format
- Easy to edit and share with educators
- Compatible with most word processors
- Supports bold text and formatting

**Opens with:**
- Microsoft Word
- Google Docs
- LibreOffice Writer
- Apple Pages

**Requires:** `python-docx` package (already included in requirements.txt)

### 3. PDF (.pdf)
**Best for:** Print-ready documents and final distribution

**Advantages:**
- Professional appearance with styled formatting
- Cannot be accidentally edited
- Universal compatibility
- Perfect for printing and official distribution
- Maintains consistent appearance on all devices

**Opens with:**
- Adobe Acrobat Reader
- Web browsers (Chrome, Safari, Firefox)
- Preview (macOS)
- Most PDF viewers

**Requires:** `reportlab` package
```bash
pip install reportlab
```

## How to Export

1. From the main menu, press `e` for Export
2. Select your desired format:
   - `1` for Markdown (.md)
   - `2` for Word Document (.docx)
   - `3` for PDF (.pdf)
3. The application will convert and export all your creations
4. Files are saved to your Downloads folder with a timestamp
5. Option to open the folder automatically after export

## What Gets Exported

All created resources are exported and organized by category:

- **Student Resources**: Guides, workbooks, quizzes
- **Parent Resources**: Parent guides
- **Teacher Resources**: Teacher implementation guides
- **Leadership Resources**: School leadership information sheets
- **Curriculum Mapping**: Standards alignment documents
- **Text Complexity Analysis**: Language accessibility reports

A README file is included in each export folder with a complete file listing and instructions.

## Export Folder Structure

```
Game_Name_Creations_Export_FORMAT_TIMESTAMP/
├── README.txt
├── Student_Guide_TIMESTAMP.{md|docx|pdf}
├── Student_Workbook_TIMESTAMP.{md|docx|pdf}
├── Parent_Guide_TIMESTAMP.{md|docx|pdf}
├── Teacher_Guide_TIMESTAMP.{md|docx|pdf}
├── Leadership_Info_TIMESTAMP.{md|docx|pdf}
├── Curriculum_Mapping_Country_TIMESTAMP.{md|docx|pdf}
└── Text_Complexity_Analysis_TIMESTAMP.{md|docx|pdf}
```

## Troubleshooting

### Word Export Issues
If Word export fails, ensure `python-docx` is installed:
```bash
pip install python-docx
```

### PDF Export Issues
If PDF export fails, ensure reportlab is installed:
```bash
pip install reportlab
```

Reportlab is a pure-Python library with no system dependencies, making it compatible with all platforms (macOS, Windows, Linux).

### Fallback to Markdown
If conversion fails for any reason:
1. The application will inform you of missing dependencies
2. You can still export as Markdown (no dependencies required)
3. Convert Markdown files later using other tools like Pandoc

## Tips

- **For internal use**: Markdown is perfect for editing and iteration
- **For sharing with educators**: Word format allows easy collaboration
- **For official distribution**: PDF ensures professional appearance
- **Mixed approach**: Export as Markdown for working drafts, then PDF for final versions
