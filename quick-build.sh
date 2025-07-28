#!/bin/bash
DIR=$(pwd)

# Fix line endings for WSL compatibility
if [[ -n "${WSL_DISTRO_NAME:-}" ]] || [[ "$(uname -r)" == *microsoft* ]]; then
    # We're in WSL - fix line endings if dos2unix is available
    dos2unix "$0" || {
        # Let the user read the error message, don't guess it's that dos2unix isn't installed
        exit 1
    }
    echo "Line endings fixed for WSL compatibility"
fi

if [ "$1" == "testing" ]; then
    echo "Creating minimal content structure for fast testing..."
    
    # Remove old test structure if it exists
    rm -rf content-testing/
    
    # Create minimal content directory
    mkdir -p content-testing/functions
    mkdir -p content-testing/interactive
    
    # Copy config and TOC
    cp _config.yml content-testing/
    cp _toc-testing.yml content-testing/_toc.yml
    
    # Copy other required files
    cp logo.png content-testing/ ||
        echo "logo.png not found, skipping"
    
    cp references.bib content-testing/ ||
        echo "references.bib not found, skipping"
    
    # Copy only what we need
    cp content/index.md content-testing/
    cp content/functions/quadratic_functions_gen.md content-testing/functions/ ||
        echo "quadratic_functions_gen.md not found, skipping"
    cp content/functions/types_and_graphs.md content-testing/functions/ ||
        echo "types_and_graphs.md not found, skipping"
    
    # Copy interactive tools
    cp content/interactive/python_playground.md content-testing/interactive/ ||
        echo "python_playground.md not found, skipping"
    cp content/interactive/BKT_Simple_Demo.md content-testing/interactive/ ||
        echo "BKT_Simple_Demo.md not found, skipping"
    
    # Copy static assets if they exist
    if [ -d "_static" ]; then
        cp -r _static content-testing/
    fi
    
    # Build with minimal content
    cd content-testing
    jupyter-book build --verbose --path-output ../_build-testing .
    cd ..
    
    echo "Fast testing build complete!"
    cd _build-testing/_build/html/ && python -m http.server && cd "$DIR"
    
# Normal build with full content folder
elif [ -n "$1" ]; then
    # Custom TOC file provided
    TOC_FILE="_toc-$1.yml"
    if [ ! -f "$TOC_FILE" ]; then
        echo "Error: $TOC_FILE not found!"
        exit 1
    fi
    echo "Building with: $TOC_FILE"
    jupyter-book build --verbose --toc "$TOC_FILE" .
    cd _build/html/ && python -m http.server && cd "$DIR"
else
    # Normal build
    jupyter-book build --verbose .
    cd _build/html/ && python -m http.server && cd "$DIR"
fi