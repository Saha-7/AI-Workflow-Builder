#!/usr/bin/env python3
"""
Security Check Script for GenAI Stack
This script checks for accidentally committed secrets and API keys
"""

import os
import re
import sys
from pathlib import Path

# Patterns to check for (case-insensitive)
SECRET_PATTERNS = [
    r'sk-proj-[a-zA-Z0-9]{20,}',
    r'AIzaSy[a-zA-Z0-9_-]{35}',
    r'password\s*=\s*["\'][^"\']+["\']',
    r'secret\s*=\s*["\'][^"\']+["\']',
    r'api_key\s*=\s*["\'][^"\']+["\']',
    r'token\s*=\s*["\'][^"\']+["\']',
    r'key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
]

# File extensions to check
CHECK_EXTENSIONS = {'.py', '.js', '.ts', '.tsx', '.jsx', '.json', '.yml', '.yaml', '.md'}

# Directories to skip
SKIP_DIRS = {'node_modules', '.git', '__pycache__', 'build', 'dist', '.next', 'venv', 'env'}

# Files to skip
SKIP_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'}

# Files to skip (by pattern)
SKIP_FILE_PATTERNS = {'.md', 'README', 'SECURITY', 'CHANGELOG'}

def check_file(file_path):
    """Check a single file for secrets"""
    issues = []
    
    # Skip certain files
    if file_path.name in SKIP_FILES:
        return issues
    
    # Skip documentation files
    if any(pattern in file_path.name for pattern in SKIP_FILE_PATTERNS):
        return issues
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                for pattern in SECRET_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Skip if it's a template or example
                        if any(x in line.lower() for x in ['example', 'template', 'your_', 'placeholder', 'integrity', 'sha512', 'sha256']):
                            continue
                        
                        issues.append({
                            'file': str(file_path),
                            'line': i,
                            'content': line.strip(),
                            'pattern': pattern
                        })
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return issues

def check_directory(directory):
    """Check all files in a directory"""
    all_issues = []
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            
            # Check file extension
            if file_path.suffix.lower() in CHECK_EXTENSIONS:
                issues = check_file(file_path)
                all_issues.extend(issues)
    
    return all_issues

def main():
    print("🔍 GenAI Stack - Security Check")
    print("=" * 40)
    
    # Check current directory
    issues = check_directory('.')
    
    if not issues:
        print("✅ No secrets found in code!")
        print("🔒 Your code appears to be secure.")
        return 0
    
    print(f"❌ Found {len(issues)} potential security issues:")
    print()
    
    for issue in issues:
        print(f"📁 File: {issue['file']}")
        print(f"📍 Line {issue['line']}: {issue['content']}")
        print(f"🔍 Pattern: {issue['pattern']}")
        print("-" * 40)
    
    print("\n🚨 Security Recommendations:")
    print("1. Remove hardcoded secrets from code")
    print("2. Use environment variables instead")
    print("3. Add .env files to .gitignore")
    print("4. Use the setup-env.py script for secure setup")
    print("5. Review the SECURITY.md file for best practices")
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
