#!/bin/bash
# Build script for Ecnetica multi-subject Jupyter Book platform
# Builds all subjects and organizes them for deployment

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Building Ecnetica Multi-Subject Platform"
echo "============================================"

# Create output directory
mkdir -p _build/html

# Build Maths (primary subject)
echo ""
echo "📐 Building Mathematics..."
cd subjects/maths
jupyter-book build . --path-output ../../_build/maths
cd ../..
mkdir -p _build/html/maths
cp -r _build/maths/html/* _build/html/maths/

# Build Chemistry (if content exists)
if [ -f "subjects/chemistry/content/index.md" ]; then
    echo ""
    echo "⚗️ Building Chemistry..."
    cd subjects/chemistry
    jupyter-book build . --path-output ../../_build/chemistry
    cd ../..
    mkdir -p _build/html/chemistry
    cp -r _build/chemistry/html/* _build/html/chemistry/
else
    echo ""
    echo "⚗️ Skipping Chemistry (no content yet)"
fi

# Build Physics (if content exists)
if [ -f "subjects/physics/content/index.md" ]; then
    echo ""
    echo "⚛️ Building Physics..."
    cd subjects/physics
    jupyter-book build . --path-output ../../_build/physics
    cd ../..
    mkdir -p _build/html/physics
    cp -r _build/physics/html/* _build/html/physics/
else
    echo ""
    echo "⚛️ Skipping Physics (no content yet)"
fi

# Copy landing page
echo ""
echo "🏠 Setting up landing page..."
if [ -f "landing.html" ]; then
    cp landing.html _build/html/index.html
else
    echo "   (No landing.html found, maths will be the default)"
    # Create a simple redirect to maths if no landing page
    echo '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=maths/"></head></html>' > _build/html/index.html
fi

echo ""
echo "✅ Build complete!"
echo ""
echo "📁 Output structure:"
echo "   _build/html/"
echo "   ├── index.html (landing page)"
echo "   ├── maths/"
echo "   ├── chemistry/"
echo "   └── physics/"
echo ""
echo "To view locally:"
echo "   cd _build/html && python -m http.server 8000"
echo "   Then open: http://localhost:8000"
echo ""


