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
# jupyter-book creates _build/maths/_build/html/ structure
cp -r _build/maths/_build/html/* _build/html/maths/

# Build MAths test (if content exists)
if [ -f "subjects/maths_copy/content/index.md" ]; then
    echo ""
    echo "⚗️ Building Test..."
    cd subjects/maths_copy
    jupyter-book build . --path-output ../../_build/maths_copy
    cd ../..
    mkdir -p _build/html/maths_copy
    cp -r _build/chemistry/_build/html/* _build/html/maths_copy/
else
    echo ""
    echo "⚗️ Skipping TEST (no content yet)"
fi

# Build Chemistry (if content exists)
if [ -f "subjects/chemistry/content/index.md" ]; then
    echo ""
    echo "⚗️ Building Chemistry..."
    cd subjects/chemistry
    jupyter-book build . --path-output ../../_build/chemistry
    cd ../..
    mkdir -p _build/html/chemistry
    cp -r _build/chemistry/_build/html/* _build/html/chemistry/
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
    cp -r _build/physics/_build/html/* _build/html/physics/
else
    echo ""
    echo "⚛️ Skipping Physics (no content yet)"
fi

# Build Landing page
echo ""
echo "🏠 Building landing page..."
cd shared/landing
jupyter-book build . --path-output ../../_build/landing
cd ../..
# Copy just the index.html and its assets from landing build
cp _build/landing/_build/html/index.html _build/html/index.html
# Copy landing CSS if it exists
if [ -d "_build/landing/_build/html/_static" ]; then
    mkdir -p _build/html/_static
    cp -r _build/landing/_build/html/_static/* _build/html/_static/
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
echo "   cd _build/html && python3 -m http.server 8000"
echo "   Then open: http://localhost:8000"
echo ""


