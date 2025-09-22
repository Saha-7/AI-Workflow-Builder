#!/usr/bin/env python3
"""
Setup script for GenAI Stack Backend
"""
import os
import subprocess
import sys

def setup_backend():
    """Setup the backend environment"""
    print("Setting up GenAI Stack Backend...")
    
    # Create .env file if it doesn't exist
    env_file = ".env"
    if not os.path.exists(env_file):
        print("Creating .env file...")
        env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# SerpAPI Configuration
SERPAPI_KEY=your_serpapi_key_here

# Database Configuration
DATABASE_URL=postgresql://genai_user:genai_password@localhost:5432/genai_stack

# ChromaDB Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8001

# Application Configuration
SECRET_KEY=your_very_strong_secret_key_here_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")
    
    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    
    # Create uploads directory
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print("✅ Uploads directory created")
    else:
        print("✅ Uploads directory already exists")
    
    print("\n🎉 Backend setup completed!")
    print("\nTo start the backend:")
    print("  python start.py")
    print("\nTo test the backend:")
    print("  python test_backend.py")
    
    return True

if __name__ == "__main__":
    setup_backend()


