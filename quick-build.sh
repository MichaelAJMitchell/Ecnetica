#!/bin/bash
DIR=$(pwd)

jupyter-book build . && cd _build/html/ && python -m http.server && cd "$DIR"