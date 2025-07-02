#!/bin/bash

# Quick Jupyter Book Build and Serve Script
# Builds jupyter book and starts server, but returns to project directory

# Save current directory
SCRIPT_DIR=$(pwd)


# Build jupyter book and start server, then return to project directory
jupyter-book build . && cd _build/html/ && python -m http.server && cd "$SCRIPT_DIR"