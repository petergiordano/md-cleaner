# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a markdown cleaning utility repository that provides tools to clean escaped markdown characters from files, particularly those exported from Google Docs via "Download as Markdown" feature.

## Core Architecture

### Two Implementation Approaches

The repository contains two different implementations of markdown cleaning functionality:

1. **`clean_markdown.py`** - Complete standalone script with CLI interface, file discovery, and processing pipeline
2. **`markdown_cleaner.py`** - Core cleaning function library for integration into other projects

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

## File Structure

- `clean_markdown.py` - Main executable script with CLI interface
- `markdown_cleaner.py` - Core cleaning function for library use
- `README-clean_markdown.md` - Usage documentation and examples
- `md-cleaner.code-workspace` - VS Code workspace configuration

## Development Notes

### Pattern Ordering Importance

When modifying cleaning patterns, maintain the specific order in `clean_escaped_markdown()` to prevent conflicts. Headers and lists must be processed before emphasis patterns to avoid false matches.

### Heuristic Detection

The script uses pattern counting (`clean_markdown.py:64-74`) to determine if a file contains escaped markdown before processing. This prevents unnecessary processing of clean files.

### Error Handling

Both implementations gracefully handle empty content and files without escaped patterns, returning the original content unchanged.