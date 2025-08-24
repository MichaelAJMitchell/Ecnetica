#!/bin/bash
DIR=$(pwd)

if [ "$1" == "testing" ]; then
    echo "Creating minimal content structure for fast testing..."
    
    # Remove old test structure if it exists
    rm -rf content-testing/
    
    # Create minimal content directory structure
    mkdir -p content-testing/content/functions
    mkdir -p content-testing/content/interactive
    
    # Copy config and TOC
    cp _config.yml content-testing/
    cp _toc-testing.yml content-testing/_toc.yml
    
    # Copy other required files
    cp logo.png content-testing/ ||
        echo "logo.png not found, skipping"
    
    cp references.bib content-testing/ ||
        echo "references.bib not found, skipping"
    
    # Copy files maintaining the content/ directory structure
    cp content/index.md content-testing/content/
    cp content/functions/quadratic_functions_gen.md content-testing/content/functions/ 2>/dev/null ||
        echo "quadratic_functions_gen.md not found, skipping"
    cp content/functions/types_and_graphs.md content-testing/content/functions/ 2>/dev/null ||
        echo "types_and_graphs.md not found, skipping"
    
    # Copy ALL interactive files instead of just specific ones
    echo "Copying all interactive files..."
    if [ -d "content/interactive" ]; then
        # Copy all .md files from the interactive directory
        find content/interactive -name "*.md" -type f | while read -r file; do
            # Get the relative path from content/interactive
            rel_file=${file#content/interactive/}
            target_dir="content-testing/content/interactive/$(dirname "$rel_file")"
            
            # Create directory if it doesn't exist
            mkdir -p "$target_dir"
            
            echo "Copying interactive file: $rel_file"
            cp "$file" "content-testing/content/interactive/$rel_file" || echo "Failed to copy $rel_file"
        done
        
        echo "All interactive files copied successfully!"
    else
        echo "Warning: content/interactive directory not found"
    fi
    
    # Copy static assets if they exist
    if [ -d "_static" ]; then
        echo "Copying static assets..."
        cp -r _static content-testing/
    fi
    
    # Build with minimal content
    echo "Building testing content..."
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