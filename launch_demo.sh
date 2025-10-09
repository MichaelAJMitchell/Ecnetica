#!/bin/bash

# Launch script for the Advanced Graph Demo
# This script handles CORS issues by starting a local server

echo "🚀 Launching Advanced Graph Demo..."
echo "📁 Current directory: $(pwd)"

# Check if the required files exist
if [ ! -f "_static/advanced-graph-demo.html" ]; then
    echo "❌ Error: advanced-graph-demo.html not found in _static directory"
    exit 1
fi

if [ ! -f "_static/advanced-graph-data.json" ]; then
    echo "❌ Error: advanced-graph-data.json not found in _static directory"
    echo "💡 Run 'python3 advanced_graph_processor.py' first to generate the data"
    exit 1
fi

if [ ! -f "_static/advanced-graph-renderer.js" ]; then
    echo "❌ Error: advanced-graph-renderer.js not found in _static directory"
    exit 1
fi

# Start the server
echo "🌐 Starting local server to avoid CORS issues..."
python3 serve_demo.py
