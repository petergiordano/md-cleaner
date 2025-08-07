# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a markdown cleaning utility repository that provides tools to clean escaped markdown characters from files, particularly those exported from Google Docs via "Download as Markdown" feature.

## Core Architecture

### Three Implementation Approaches

The repository contains three different implementations of markdown cleaning functionality:

1. **`clean_markdown.py`** - Complete standalone script with CLI interface, file discovery, and processing pipeline
2. **`markdown_cleaner.py`** - Core cleaning function library for integration into other projects
3. **`markdown_cleaner_app.py`** - Graphical user interface (GUI) application using Tkinter for desktop use

### Key Components

- **MarkdownCleaner class** (`clean_markdown.py:23`): Main processing engine with dry-run mode, verbose output, and statistics tracking
- **clean_escaped_markdown function** (`clean_markdown.py:33` and `markdown_cleaner.py:4`): Core pattern matching and replacement logic
- **Pattern detection system** (`clean_markdown.py:52-78`): Heuristic-based detection of escaped markdown patterns before processing

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

- **`markdown_cleaner.py`**: This is the **core logic library**. It contains the `clean_escaped_markdown` function and is imported by both the CLI and the GUI app. Any changes to the cleaning logic should be made in this file.
- **`markdown_cleaner_app.py`**: This is the main script for the GUI application. It handles creating the windows, buttons, and text areas, and it imports its logic from `markdown_cleaner.py`.
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

These generated directories should not be committed to the Git repository.

## File Structure

- `clean_markdown.py` - Main executable script with CLI interface
- `markdown_cleaner.py` - Core cleaning function for library use
- `markdown_cleaner_app.py` - GUI application using Tkinter
- `setup.py` - py2app configuration for building macOS application
- `app_icon.icns` - Icon file for macOS application bundle
- `index.html` - Web-based frontend interface with Overdrive GTM branding
- `README.md` - Usage documentation and examples
- `md-cleaner.code-workspace` - VS Code workspace configuration

## Development Notes

### Pattern Ordering Importance

When modifying cleaning patterns, maintain the specific order in `clean_escaped_markdown()` to prevent conflicts. Headers and lists must be processed before emphasis patterns to avoid false matches.

### Heuristic Detection

The script uses pattern counting (`clean_markdown.py:64-74`) to determine if a file contains escaped markdown before processing. This prevents unnecessary processing of clean files.

### Error Handling

Both implementations gracefully handle empty content and files without escaped patterns, returning the original content unchanged.