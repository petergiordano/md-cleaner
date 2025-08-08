# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a markdown cleaning utility repository that provides tools to clean escaped markdown characters from files, particularly those exported from Google Docs via "Download as Markdown" feature. The repository follows a centralized architecture with a single source of truth for all cleaning logic.

## Core Architecture

### Centralized Design Pattern

**IMPORTANT**: This repository uses a centralized architecture where all core cleaning logic resides in a single library file. This eliminates code duplication and ensures consistency across all interfaces.

### Four Interface Implementations

The repository provides four different ways to access the same core cleaning functionality:

1. **`markdown_cleaner.py`** - Core library containing the complete `MarkdownCleaner` class
2. **`clean_markdown.py`** - CLI tool that imports from the core library  
3. **`markdown_cleaner_app.py`** - GUI application that imports from the core library
4. **`index.html`** - Web interface with JavaScript implementation of cleaning patterns

### Key Components

- **MarkdownCleaner class** (`markdown_cleaner.py:16-251`): Complete processing engine with all methods
- **clean_escaped_markdown method** (`markdown_cleaner.py:26-140`): Core pattern matching and replacement logic  
- **Pattern detection system** (`markdown_cleaner.py:51-78`): Heuristic-based detection of escaped markdown patterns
- **File I/O methods** (`markdown_cleaner.py:142-163`): read_file, write_file for CLI operations
- **Directory processing** (`markdown_cleaner.py:198-251`): find_markdown_files, clean_directory for batch operations

### Cleaning Logic Architecture

The cleaning process follows a specific order to avoid pattern conflicts:

1. **Headers** (`\#` → `#`)
2. **Lists** (`\-`, `\*`, `\+`, `\1.` → `-`, `*`, `+`, `1.`)
3. **Emphasis** (`\*text\*` → `*text*`)
4. **Links/Images** (`\[text\]\(url\)` → `[text](url)`)
5. **Special characters** (underscores, plus signs, punctuation)

## Common Commands

### Running the Markdown Cleaner

```bash
# Clean all .md files in current directory
python3 clean_markdown.py .

# Clean specific directory
python3 clean_markdown.py docs/

# Clean single file
python3 clean_markdown.py README.md

# Preview changes without modifying files
python3 clean_markdown.py . --dry-run

# Verbose output showing detailed process
python3 clean_markdown.py . --verbose
```

### Testing All Components

```bash
# Test core library
python3 -c "from markdown_cleaner import MarkdownCleaner; print('✅ Library works')"

# Test CLI
python3 clean_markdown.py --help

# Test web interface
open index.html
```

### Git Operations

```bash
# Standard development workflow
git add .
git commit -m "Description of changes"
git push
```

## GUI Application and Build Process

In addition to the command-line tool, this repository contains a graphical user interface (GUI) application for macOS, built using Python's Tkinter library.

### Key Files for the GUI App

- **`markdown_cleaner.py`**: This is the **core logic library**. It contains the complete `MarkdownCleaner` class and is imported by both the CLI and GUI app. **This is the ONLY place to make cleaning logic changes.**
- **`markdown_cleaner_app.py`**: This is the main script for the GUI application. It handles creating the windows, buttons, and text areas, and imports the `MarkdownCleaner` class from the core library.
- **`setup.py`**: This is the configuration file for the `py2app` utility. It defines how to bundle the `markdown_cleaner_app.py` script and its dependencies into a standalone macOS application (`.app`).
- **`app_icon.icns`**: This is the icon file used for the macOS application bundle.

### Building the Application

The macOS application is built using the `py2app` library. To build or rebuild the app after making changes, run the following command in the terminal from the project's root directory:

```bash
python3 setup.py py2app
```

This command will generate two directories:
- **`build/`**: Contains intermediate files used during the build process.
- **`dist/`**: Contains the final, distributable `Markdown Cleaner.app` file.

These generated directories should not be committed to the Git repository (they're in `.gitignore`).

## File Structure

- `markdown_cleaner.py` - **CORE LIBRARY** - Contains complete MarkdownCleaner class (SINGLE SOURCE OF TRUTH)
- `clean_markdown.py` - CLI tool that imports from core library
- `markdown_cleaner_app.py` - GUI application that imports from core library
- `setup.py` - py2app configuration for building macOS application
- `app_icon.icns` - Icon file for macOS application bundle
- `index.html` - Web-based frontend interface with Overdrive GTM branding
- `README.md` - User documentation and examples
- `CLAUDE.md` - This file (AI development guidance)
- `.gitignore` - Git ignore rules (excludes build/, dist/, __pycache__, etc.)

## Development Notes

### CRITICAL: Centralized Architecture Rules

**⚠️ IMPORTANT**: This repository uses a centralized architecture. Follow these rules:

1. **ALL cleaning logic changes** must be made ONLY in `markdown_cleaner.py`
2. **CLI and GUI tools** import from the core library - never modify cleaning logic in these files
3. **Pattern updates, bug fixes, improvements** go in the core library only
4. **Interface-specific code** (CLI args, GUI widgets) stays in respective files

### Making Changes to Cleaning Logic

1. **Edit** `markdown_cleaner.py` (specifically the `clean_escaped_markdown` method)
2. **Test** all three interfaces: Library, CLI, GUI
3. **Verify** identical cleaning results across all tools

### Pattern Ordering Importance

When modifying cleaning patterns in `markdown_cleaner.py:82-119`, maintain the specific order to prevent conflicts. Headers and lists must be processed before emphasis patterns to avoid false matches.

### Heuristic Detection

The script uses pattern counting (`markdown_cleaner.py:64-68`) to determine if content contains escaped markdown before processing. This prevents unnecessary processing of clean files.

### Error Handling

The centralized implementation gracefully handles:
- Empty content and files without escaped patterns
- File I/O errors with clear error messages  
- Directory traversal issues
- Encoding problems

### Testing Strategy

Always test all four interfaces when making changes:
1. **Library**: Import and call methods directly
2. **CLI**: Run with `--dry-run --verbose` on test files
3. **GUI**: Launch app and test with sample content
4. **Web**: Open index.html and test drag-and-drop functionality