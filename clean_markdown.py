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
import re
import glob
from pathlib import Path


class MarkdownCleaner:
    """Cleans escaped markdown characters from markdown files"""
    
    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.files_processed = 0
        self.files_cleaned = 0
        self.total_changes = 0
    
    def clean_escaped_markdown(self, content):
        """
        Clean escaped markdown characters from content
        
        Google Docs "Download as Markdown" feature escapes markdown syntax,
        resulting in content like:
        - \\# Header → # Header
        - \\- List item → - List item 
        - \\*emphasis\\* → *emphasis*
        - \\1. Numbered → 1. Numbered
        - \\+1-2 → +1-2
        - project\\_system\\_instructions → project_system_instructions
        
        This function gracefully handles both escaped and non-escaped content.
        """
        if not content:
            return content, 0
            
        # First, check if content appears to be escaped (heuristic)
        escaped_indicators = [
            r'\\#',          # Escaped headers
            r'\\-\s',        # Escaped lists  
            r'\\\*.*\\\*',   # Escaped emphasis
            r'\\\d+\.',      # Escaped numbered lists
            r'\\>',          # Escaped blockquotes
            r'\\\[.*\\\]',   # Escaped links
            r'\\\+',         # Escaped plus signs
            r'\\\_',         # Escaped underscores in text
            r'\\\s*$',       # Trailing standalone backslashes
        ]
        
        # Count potential escaped markdown patterns
        escape_count = 0
        for indicator in escaped_indicators:
            if re.search(indicator, content):
                escape_count += 1
        
        # If no escaped patterns detected, return original content
        if escape_count == 0:
            if self.verbose:
                print(f"   ℹ️  No escaped markdown patterns detected")
            return content, 0
            
        if self.verbose:
            print(f"   🔍 Detected {escape_count} types of escaped markdown patterns")
        
        # Pattern to match escaped markdown characters
        # Matches: \# \* \- \+ \. \1 \2 etc.
        # Ordered by specificity to avoid conflicts
        patterns = [
            # Headers: \# \## \### etc. (handle escaped consecutive hashes)
            (r'\\(#{1,6})', r'\1'),
            
            # Lists: \- \* \+ at start of line or after whitespace
            (r'(^|\s)\\([-*+])\s', r'\1\2 '),
            
            # Numbered lists: \1. \2. etc. (both at start of line and mid-text)
            (r'(^|\s)\\(\d+)\.', r'\1\2.'),
            (r'\\(\d+)\.', r'\1.'),  # Catch remaining escaped numbers with dots
            
            # Escaped plus signs: \+1-2 → +1-2
            (r'\\(\+)', r'\1'),
            
            # Escaped underscores in text: project\_system\_instructions → project_system_instructions
            (r'\\(_)', r'\1'),
            
            # Emphasis: \*text\* \_text\_ (but not legitimate double backslashes)
            (r'(?<!\\)\\([*_])', r'\1'),
            
            # Inline code: \`code\`
            (r'(?<!\\)\\(`)', r'\1'),
            
            # Links: \[text\]\(url\) (but preserve legitimate escapes)
            (r'(?<!\\)\\([\[\]])', r'\1'),
            (r'(?<!\\)\\([()])', r'\1'),
            
            # Horizontal rules: \--- \***
            (r'(?<!\\)\\([-*]{3,})', r'\1'),
            
            # Blockquotes: \> 
            (r'(^|\s)\\(>)\s', r'\1\2 '),
            
            # Trailing standalone backslashes (common in Google Docs exports)
            (r'\\\s*$', r''),
            
            # Escaped periods in general text (not just numbered lists)
            (r'(?<!\\)\\(\.)', r'\1'),
        ]
        
        cleaned_content = content
        changes_made = 0
        
        for pattern, replacement in patterns:
            before_length = len(cleaned_content)
            cleaned_content = re.sub(pattern, replacement, cleaned_content, flags=re.MULTILINE)
            after_length = len(cleaned_content)
            
            if before_length != after_length:
                changes_made += 1
        
        # Report cleanup results
        if self.verbose:
            if changes_made > 0:
                print(f"   🧹 Cleaned {changes_made} types of escaped markdown characters")
            else:
                print(f"   ℹ️  No escaped markdown characters found to clean")
        
        return cleaned_content, changes_made
    
    def read_file(self, file_path):
        """Read markdown file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return None
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return None
    
    def write_file(self, file_path, content):
        """Write content to markdown file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            print(f"❌ Error writing file {file_path}: {e}")
            return False
    
    def clean_file(self, file_path):
        """Clean a single markdown file"""
        print(f"📄 Processing: {file_path}")
        
        # Read file content
        content = self.read_file(file_path)
        if content is None:
            return False
        
        # Clean escaped markdown
        cleaned_content, changes_made = self.clean_escaped_markdown(content)
        
        # Track statistics
        self.files_processed += 1
        if changes_made > 0:
            self.files_cleaned += 1
            self.total_changes += changes_made
        
        # Write cleaned content (unless dry run)
        if changes_made > 0:
            if self.dry_run:
                print(f"   🔍 [DRY RUN] Would clean {changes_made} pattern types")
            else:
                if self.write_file(file_path, cleaned_content):
                    print(f"   ✅ Cleaned {changes_made} pattern types")
                else:
                    print(f"   ❌ Failed to write cleaned content")
                    return False
        else:
            print(f"   ✨ File already clean")
        
        return True
    
    def find_markdown_files(self, path):
        """Find all .md files in a directory (recursive)"""
        if os.path.isfile(path):
            if path.endswith('.md'):
                return [path]
            else:
                print(f"❌ File {path} is not a markdown file (.md)")
                return []
        
        if not os.path.isdir(path):
            print(f"❌ Path {path} is not a file or directory")
            return []
        
        # Find all .md files recursively
        md_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        
        return sorted(md_files)
    
    def clean_directory(self, path):
        """Clean all markdown files in a directory"""
        md_files = self.find_markdown_files(path)
        
        if not md_files:
            print(f"❌ No markdown files found in {path}")
            return False
        
        print(f"🔍 Found {len(md_files)} markdown file(s)")
        print("")
        
        # Process each file
        success_count = 0
        for file_path in md_files:
            if self.clean_file(file_path):
                success_count += 1
            print("")  # Blank line between files
        
        # Print summary
        print("📊 SUMMARY")
        print("=" * 50)
        print(f"Files processed: {self.files_processed}")
        print(f"Files cleaned: {self.files_cleaned}")
        print(f"Total pattern types cleaned: {self.total_changes}")
        print(f"Success rate: {success_count}/{len(md_files)} files")
        
        if self.dry_run:
            print("")
            print("🔍 DRY RUN MODE - No files were modified")
            print("Run without --dry-run to apply changes")
        
        return success_count == len(md_files)


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