#!/usr/bin/env python3
"""
Setup script for Mathematical Concept Scraper
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✓ .env file already exists")
        return True
    
    print("Creating .env file...")
    try:
        with open(env_file, 'w') as f:
            f.write("# OpenAI API Configuration\n")
            f.write("# Get your API key from: https://platform.openai.com/api-keys\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# Optional: Override default model (default: gpt-5-mini)\n")
            f.write("# DEFAULT_MODEL=gpt-5-mini\n\n")
            f.write("# Optional: Override fallback models (comma-separated)\n")
            f.write("# FALLBACK_MODELS=gpt-4o-mini,gpt-4.1-mini,gpt-3.5-turbo,gpt-4-turbo-preview\n")
        
        print("✓ .env file created!")
        print("⚠️  Please edit .env file and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"✗ Error creating .env file: {e}")
        return False

def create_output_directory():
    """Create output directory."""
    output_dir = "output"
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print("✓ Output directory created")
        except Exception as e:
            print(f"✗ Error creating output directory: {e}")
            return False
    else:
        print("✓ Output directory already exists")
    return True

def main():
    """Main setup function."""
    print("=" * 60)
    print("MATHEMATICAL CONCEPT SCRAPER - SETUP")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Create output directory
    if not create_output_directory():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Run the test example: python test_example.py")
    print("3. Process your documents: python main.py --file your_document.pdf")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 