#!/usr/bin/env python3
"""
Secure Environment Setup Script for GenAI Stack
This script helps you set up your environment variables securely
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key(length=32):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Create .env file from template"""
    env_file = Path('.env')
    template_file = Path('env.example')
    
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("❌ Setup cancelled.")
            return False
    
    if not template_file.exists():
        print("❌ env.example file not found!")
        return False
    
    # Read template
    with open(template_file, 'r') as f:
        content = f.read()
    
    # Generate secure secret key
    secret_key = generate_secret_key()
    content = content.replace('your_very_strong_secret_key_here_change_this_in_production', secret_key)
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ .env file created successfully!")
    print(f"🔑 Generated secret key: {secret_key[:8]}...")
    print("\n📝 Next steps:")
    print("1. Edit .env file and add your actual API keys")
    print("2. Never commit .env file to version control")
    print("3. Use env.example as a template for team members")
    
    return True

def check_gitignore():
    """Check if .gitignore properly excludes .env files"""
    gitignore_file = Path('.gitignore')
    
    if not gitignore_file.exists():
        print("⚠️  .gitignore file not found!")
        return False
    
    with open(gitignore_file, 'r') as f:
        content = f.read()
    
    if '.env' in content:
        print("✅ .gitignore properly excludes .env files")
        return True
    else:
        print("❌ .gitignore does not exclude .env files!")
        print("Please add '.env' to your .gitignore file")
        return False

def main():
    print("🔐 GenAI Stack - Secure Environment Setup")
    print("=" * 50)
    
    # Check gitignore
    if not check_gitignore():
        print("\n⚠️  Please fix .gitignore before proceeding")
        return
    
    # Create .env file
    if create_env_file():
        print("\n🎉 Environment setup completed!")
        print("\n🔒 Security reminders:")
        print("- Never share your .env file")
        print("- Use strong, unique API keys")
        print("- Rotate keys regularly")
        print("- Use different keys for development and production")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()







