#!/usr/bin/env python3
"""
Standalone Markdown Cleaner Script
Cleans escaped markdown characters from .md files in a directory

This script removes backslash-escaped markdown characters that are commonly
added by Google Docs "Download as Markdown" feature.

Usage:
  python3 clean_markdown.py /path/to/directory
  python3 clean_markdown.py /path/to/directory --dry-run
  python3 clean_markdown.py /path/to/file.md
"""

import os
import sys
import argparse
from markdown_cleaner import MarkdownCleaner


def main():
    parser = argparse.ArgumentParser(
        description='Clean escaped markdown characters from .md files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clean all .md files in current directory
  python3 clean_markdown.py .
  
  # Clean all .md files in specific directory
  python3 clean_markdown.py /path/to/docs
  
  # Clean a single file
  python3 clean_markdown.py /path/to/file.md
  
  # Preview changes without modifying files
  python3 clean_markdown.py /path/to/docs --dry-run
  
  # Verbose output showing detailed cleaning process
  python3 clean_markdown.py /path/to/docs --verbose

Common escaped patterns that will be cleaned:
  \\# Header          → # Header
  \\- List item       → - List item
  \\*emphasis\\*      → *emphasis*
  \\1. Numbered       → 1. Numbered
  project\\_name      → project_name
        """
    )
    
    parser.add_argument('path', help='Path to directory or .md file to clean')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview changes without modifying files')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed cleaning process')
    
    args = parser.parse_args()
    
    # Validate path
    if not os.path.exists(args.path):
        print(f"❌ Path does not exist: {args.path}")
        sys.exit(1)
    
    # Create cleaner and process files
    cleaner = MarkdownCleaner(dry_run=args.dry_run, verbose=args.verbose)
    
    print("🧹 Markdown Escape Character Cleaner")
    print("=" * 50)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - Files will not be modified")
    
    print(f"📁 Target: {args.path}")
    print("")
    
    try:
        success = cleaner.clean_directory(args.path)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()