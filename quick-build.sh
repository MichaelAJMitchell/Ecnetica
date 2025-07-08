#!/bin/bash
DIR=$(pwd)

jupyter-book build --verbose . && cd _build/html/ && python -m http.server && cd "$DIR"