#!/bin/bash
# Build a single subject for quick iteration during development
# Usage: ./build-subject.sh maths|chemistry|physics

set -e

SUBJECT="${1:-maths}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "subjects/$SUBJECT" ]; then
    echo "❌ Subject '$SUBJECT' not found!"
    echo "Available subjects:"
    ls -1 subjects/
    exit 1
fi

echo "📚 Building $SUBJECT..."
cd "subjects/$SUBJECT"
jupyter-book build . --path-output "../../_build/$SUBJECT"
cd ../..

mkdir -p "_build/html/$SUBJECT"
cp -r "_build/$SUBJECT/html/"* "_build/html/$SUBJECT/"

echo ""
echo "✅ $SUBJECT build complete!"
echo "   View at: _build/html/$SUBJECT/index.html"
echo ""
echo "To serve locally:"
echo "   cd _build/html && python -m http.server 8000"
echo "   Then open: http://localhost:8000/$SUBJECT/"



