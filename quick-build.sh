#!/bin/bash
DIR=$(pwd)

if [ -n "$1" ]; then
    # Custom TOC file provided
    # TOC must follow the naming convention _toc-<name>.yml
    TOC_FILE="_toc-$1.yml"
    if [ ! -f "$TOC_FILE" ]; then
        echo "Error: $TOC_FILE not found!"
        exit 1
    fi
    echo "Building with: $TOC_FILE"
    jupyter-book build --verbose --toc "$TOC_FILE" .
else
    jupyter-book build --verbose .
fi

cd _build/html/ && python -m http.server && cd "$DIR"