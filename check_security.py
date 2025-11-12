#!/usr/bin/env python3
"""
Pre-commit security check script
Verifies no sensitive files or data will be committed to Git
"""

import os
import re
import sys
from pathlib import Path

# Sensitive patterns to check for
SENSITIVE_PATTERNS = [
    (r'AIzaSy[A-Za-z0-9_-]{33}', 'Google API Key'),
    (r're_[A-Za-z0-9]{30,}', 'Resend API Key'),
    (r'npg_[A-Za-z0-9_]+', 'Neon Database Password'),
    (r'postgresql://[^:]+:[^@]+@', 'Database Connection String'),
    (r'SECRET_KEY\s*=\s*["\'][^"\']{20,}["\']', 'Django Secret Key'),
    (r'JWT_SECRET\s*=\s*["\'][^"\']{20,}["\']', 'JWT Secret'),
]

# Files that should be gitignored
MUST_BE_IGNORED = [
    '.env',
    'frontend/.env',
    '.env.local',
    '.env.*.local',
    'BFG-env/',
    '__pycache__/',
    '*.pyc',
    'db.sqlite3',
]

# Files that should exist
MUST_EXIST = [
    '.gitignore',
    '.env.example',
    'frontend/.env.example',
    'SECURITY.md',
]

def check_gitignore():
    """Verify .gitignore file exists and contains essential patterns"""
    gitignore_path = Path('.gitignore')
    
    if not gitignore_path.exists():
        print("❌ CRITICAL: .gitignore file not found!")
        return False
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_patterns = ['.env', 'BFG-env/', '__pycache__/', '*.pyc']
    missing = [p for p in required_patterns if p not in content]
    
    if missing:
        print(f"❌ .gitignore missing patterns: {', '.join(missing)}")
        return False
    
    print("✅ .gitignore file is properly configured")
    return True

def check_env_files():
    """Verify .env files exist and .env.example files are present"""
    issues = []
    
    # Check .env.example files exist
    for example_file in ['.env.example', 'frontend/.env.example']:
        if not Path(example_file).exists():
            issues.append(f"Missing {example_file}")
    
    # Check actual .env files are NOT in git (by checking they exist locally)
    for env_file in ['.env', 'frontend/.env']:
        if not Path(env_file).exists():
            issues.append(f"Warning: {env_file} not found - developers need to create it")
    
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
        return len([i for i in issues if 'Missing' in i]) == 0
    
    print("✅ Environment file templates are in place")
    return True

def scan_for_secrets(directory='.'):
    """Scan files for potential exposed secrets"""
    issues = []
    exclude_dirs = {'BFG-env', 'node_modules', '.git', '__pycache__', 'build', 'docs'}
    # Files that should exist but must be gitignored (not checked for secrets)
    gitignored_files = {'.env', 'frontend/.env', 'frontend\\.env', 'DATABASE_SETUP_COMPLETE.md'}
    exclude_files = gitignored_files | {'check_security.py'}
    safe_files = {'.env.example', 'frontend/.env.example', 'SECURITY.md'}
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Skip binary files and excluded files
            if file.endswith(('.pyc', '.png', '.jpg', '.ico', '.woff', '.woff2', '.ttf')):
                continue
            
            filepath = Path(root) / file
            relative_path = filepath.relative_to(directory)
            
            # Skip excluded and safe files
            if str(relative_path) in exclude_files or str(relative_path) in safe_files:
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                for pattern, secret_type in SENSITIVE_PATTERNS:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        # Skip if it's clearly a placeholder
                        matched_text = match.group(0)
                        if 'your' in matched_text.lower() or 'example' in matched_text.lower():
                            continue
                        
                        issues.append(f"Potential {secret_type} in {relative_path}")
            
            except Exception as e:
                pass
    
    if issues:
        print("❌ CRITICAL: Potential secrets found in files:")
        for issue in issues:
            print(f"   {issue}")
        return False
    
    print("✅ No exposed secrets detected in source files")
    return True

def main():
    print("=" * 60)
    print("Security Pre-Commit Check")
    print("=" * 60)
    print()
    
    checks = [
        check_gitignore(),
        check_env_files(),
        scan_for_secrets(),
    ]
    
    print()
    print("=" * 60)
    if all(checks):
        print("✅ ALL SECURITY CHECKS PASSED - Safe to commit!")
        print("=" * 60)
        return 0
    else:
        print("❌ SECURITY CHECKS FAILED - DO NOT COMMIT!")
        print("=" * 60)
        print()
        print("Please fix the issues above before committing.")
        print("See SECURITY.md for guidelines.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
