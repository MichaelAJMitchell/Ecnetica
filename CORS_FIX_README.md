# CORS Issue Fix for Advanced Graph Demo

## 🚫 The Problem

When opening HTML files directly in the browser (using `file://` protocol), browsers block cross-origin requests for security reasons. This causes the error:

```
Access to fetch at 'file:///.../advanced-graph-data.json' from origin 'null' has been blocked by CORS policy
```

## ✅ Solutions

### **Option 1: Use the Launcher Script (Recommended)**
```bash
./launch_demo.sh
```
This automatically starts a local server and opens the demo in your browser.

### **Option 2: Manual Server Setup**
```bash
# Start a simple HTTP server
python3 -m http.server 8000

# Then visit in browser:
# http://localhost:8000/_static/advanced-graph-demo.html
```

### **Option 3: Use the Python Server**
```bash
python3 serve_demo.py
```
This starts a server with CORS headers and opens the browser automatically.

### **Option 4: Jupyter Book Integration**
The demo works perfectly when integrated into Jupyter Book:
```bash
# Build and serve Jupyter Book
jupyter-book build .
jupyter-book serve _build/html
```

## 🔧 Files Created

- **`serve_demo.py`** - Python server with CORS headers
- **`launch_demo.sh`** - Automated launcher script
- **Updated `advanced-graph-demo.html`** - Better error handling and CORS detection

## 🎯 Why This Happens

Modern browsers implement the **Same-Origin Policy** for security:
- Prevents malicious websites from accessing local files
- Blocks `file://` protocol from making HTTP requests
- Requires a proper HTTP server for local development

## 🚀 Quick Start

1. **Generate the data** (if not already done):
   ```bash
   python3 advanced_graph_processor.py
   ```

2. **Launch the demo**:
   ```bash
   ./launch_demo.sh
   ```

3. **Enjoy the visualization!** 🎉

The demo will automatically open in your browser at `http://localhost:8001/advanced-graph-demo.html`
