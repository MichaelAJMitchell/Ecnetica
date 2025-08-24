#!/bin/bash

# Simple Python environment rebuild script
set -e

echo "Rebuilding Python environment..."

# Remove old environment
if [ -d "venv" ]; then
    echo "Removing old venv..."
    rm -rf venv
fi

# Create new environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate and install requirements
echo "Installing requirements..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Done! Activate with: source venv/bin/activate"