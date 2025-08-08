# 🧹 Markdown Cleaner

This repository provides a powerful and flexible utility for cleaning escaped markdown characters from text, with multiple interfaces for different use cases. The core logic is centralized, ensuring consistent results whether you use the command-line tool, the desktop app, or the Python library.

## ✨ Key Features

- **Centralized Logic**: The cleaning engine is built into a core library, ensuring identical, reliable results across all tools
- **Command-Line Interface**: A powerful CLI for batch processing, automation, and server-side tasks  
- **Graphical User Interface**: An intuitive desktop app for macOS for easy, interactive cleaning
- **Web Interface**: A professional web-based frontend with modern design
- **Importable Library**: A simple Python library to integrate the cleaning functionality into your own projects

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- For macOS app building: `pip3 install py2app`

### Installation
```bash
git clone https://github.com/petergiordano/md-cleaner.git
cd md-cleaner
```

## 🛠️ The Tools

### 1. `clean_markdown.py` (Command-Line Tool)

A robust CLI for developers and power users.

**Features:**
- Recursively scan and clean all .md files in a directory
- Process a single file
- Perform a "dry run" to preview changes without modifying files
- Get verbose output and statistics on the cleaning process

**Usage:**
```bash
# Clean all markdown files in the current directory
python3 clean_markdown.py .

# Clean a single file
python3 clean_markdown.py /path/to/your/file.md

# Preview changes in a directory
python3 clean_markdown.py /path/to/docs --dry-run

# Verbose output with detailed statistics
python3 clean_markdown.py /path/to/docs --verbose
```

### 2. `markdown_cleaner_app.py` (Desktop App)

A user-friendly desktop application for macOS.

**Features:**
- Simple, modern interface with side-by-side input and output panels
- Open .md or .txt files directly from Finder
- Paste text for quick cleaning
- Copy the cleaned text to your clipboard or save it to a new file

**Building the App:**
```bash
# Install py2app
pip3 install py2app

# Build the application
python3 setup.py py2app
```
The final application will be in the `dist/` folder.

### 3. `markdown_cleaner.py` (Core Library)

The heart of the project. This is a simple, importable library containing the MarkdownCleaner class.

**Basic Usage:**
```python
from markdown_cleaner import MarkdownCleaner

# Create an instance of the cleaner
cleaner = MarkdownCleaner()

# Get your raw markdown content
raw_content = "\\# This is an \\*escaped\\* header."

# Clean the content
cleaned_content, changes_made = cleaner.clean_escaped_markdown(raw_content)

print(cleaned_content)
# Output: # This is an *escaped* header.
```

**Advanced Usage:**
```python
# With verbose output and dry-run mode
cleaner = MarkdownCleaner(dry_run=True, verbose=True)

# Process entire files
content = cleaner.read_file("document.md")
cleaned_content, changes = cleaner.clean_escaped_markdown(content)
cleaner.write_file("cleaned_document.md", cleaned_content)

# Process directories
success = cleaner.clean_directory("/path/to/markdown/files")
```

### 4. Web Interface (`index.html`)

A professional web-based interface with modern design and drag-and-drop functionality.

**Features:**
- Drag-and-drop file upload
- Real-time cleaning preview
- Download cleaned files
- Professional Overdrive GTM branding
- Responsive design for desktop and mobile

Simply open `index.html` in your web browser to use the interface.

## 📝 What Gets Cleaned

The cleaner handles these escaped markdown patterns:

| Before | After |
|--------|-------|
| `\# Header` | `# Header` |
| `\- List item` | `- List item` |
| `\*emphasis\*` | `*emphasis*` |
| `\1. Numbered` | `1. Numbered` |
| `project\_name` | `project_name` |
| `\[link\]\(url\)` | `[link](url)` |

## 🔧 Development & Maintenance

This project follows the **"Don't Repeat Yourself" (DRY)** principle. The core cleaning logic, including all regular expression patterns, resides exclusively in the `MarkdownCleaner` class within the `markdown_cleaner.py` file.

### Making Changes
- **To update cleaning logic**: Edit only `markdown_cleaner.py`
- **Both CLI and GUI tools** automatically inherit changes
- **All three interfaces** (Library/CLI/GUI) use identical logic

### Architecture
```
markdown_cleaner.py (Core Library)
├── clean_markdown.py (CLI imports from core)
├── markdown_cleaner_app.py (GUI imports from core)  
└── index.html (Web interface with JS implementation)
```

## 🧪 Testing

```bash
# Test the CLI tool
python3 clean_markdown.py . --dry-run --verbose

# Test the library
python3 -c "from markdown_cleaner import MarkdownCleaner; print('✅ Import successful')"
```

## 📁 Repository Structure

```
md-cleaner/
├── clean_markdown.py          # CLI tool
├── markdown_cleaner.py        # Core library  
├── markdown_cleaner_app.py    # GUI application
├── setup.py                   # py2app build configuration
├── index.html                 # Web interface
├── app_icon.icns             # macOS app icon
├── README.md                 # This file
├── CLAUDE.md                 # AI development guidance
└── .gitignore                # Git ignore rules
```

## 🐛 Troubleshooting

**CLI Issues:**
- Ensure Python 3.7+ is installed
- Check file permissions for target directories
- Use `--verbose` flag for detailed error information

**GUI App Issues:**  
- Install `py2app`: `pip3 install py2app`
- Build issues: Clean with `rm -rf build dist` before rebuilding

**Import Issues:**
- Ensure `markdown_cleaner.py` is in your Python path
- Check for conflicting module names

## 📄 License

[Add your license information here]