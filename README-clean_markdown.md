  🧹 Standalone Markdown Cleaner Script

  Features:

  - Recursive directory scanning - finds all .md files in subdirectories
  - Single file processing - can clean individual files
  - Dry run mode - preview changes without modifying files
  - Verbose output - detailed cleaning process information
  - Statistics - summary of files processed and cleaned
  - Same cleaning logic - uses identical patterns from the sync script

  Usage Examples:

  # Clean all .md files in current directory
  python3 .claude/scripts/clean_markdown.py .

  # Clean all .md files in specific directory
  python3 .claude/scripts/clean_markdown.py docs/

  # Clean a single file
  python3 .claude/scripts/clean_markdown.py project_system_instructions.md

  # Preview changes without modifying files
  python3 .claude/scripts/clean_markdown.py docs/ --dry-run

  # Verbose output showing detailed process
  python3 .claude/scripts/clean_markdown.py docs/ --verbose

  What It Cleans:

  - \# Header → # Header
  - \- List item → - List item
  - \*emphasis\* → *emphasis*
  - \1. Numbered → 1. Numbered
  - project\_name → project_name
  - \[link\](url) → [link](url)
  - And many more escaped markdown patterns

  Output Example:

  🧹 Markdown Escape Character Cleaner
  ==================================================
  📁 Target: docs/
  🔍 Found 5 markdown file(s)

  📄 Processing: docs/file1.md
     🔍 Detected 3 types of escaped markdown patterns
     ✅ Cleaned 3 pattern types

  📄 Processing: docs/file2.md
     ✨ File already clean

  📊 SUMMARY
  ==================================================
  Files processed: 5
  Files cleaned: 3
  Total pattern types cleaned: 12
  Success rate: 5/5 files

  The script is now ready to use and will help clean any markdown files that have
  been exported from Google Docs or otherwise have escaped markdown characters!