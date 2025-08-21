#!/usr/bin/env python3
"""
Wrapper script to run the ontology creation scripts with virtual environment support.
This script automatically adds the virtual environment's site-packages to the Python path.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Check if virtual environment exists
    venv_path = script_dir / "venv"
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run setup.py first.")
        sys.exit(1)
    
    # Add virtual environment site-packages to Python path
    if sys.platform == "win32":
        site_packages = venv_path / "Lib" / "site-packages"
    else:
        site_packages = venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    
    if site_packages.exists():
        sys.path.insert(0, str(site_packages))
        print(f"✅ Added virtual environment site-packages to Python path: {site_packages}")
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Import and run the main module
    try:
        from main import main as main_function
        print("🚀 Running main.py...")
        main_function()
    except ImportError as e:
        print(f"❌ Failed to import main module: {e}")
        print("Trying to run main.py directly...")
        
        # Fallback: run main.py as a subprocess
        try:
            result = subprocess.run([sys.executable, "main.py"] + sys.argv[1:], 
                                  cwd=script_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to run main.py: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error running main module: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 