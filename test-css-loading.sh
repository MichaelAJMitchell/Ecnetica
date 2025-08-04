#!/bin/bash

echo "=== CSS LOADING TEST ==="

echo "Checking if CSS files exist:"
ls -la _static/*.css 2>/dev/null || echo "No CSS files in _static/"

echo
echo "Checking build directory:"
if [ -d "_build/html/_static" ]; then
    echo "CSS files in build:"
    ls -la _build/html/_static/*.css 2>/dev/null || echo "No CSS files copied to build"
    
    echo
    echo "Checking file sizes:"
    if [ -f "_build/html/_static/style.css" ]; then
        SIZE=$(stat -f%z "_build/html/_static/style.css" 2>/dev/null || stat -c%s "_build/html/_static/style.css" 2>/dev/null)
        echo "style.css: $SIZE bytes"
    fi
else
    echo "Build directory not found"
fi

echo
echo "After building, check browser console (F12) for CSS loading debug info."
