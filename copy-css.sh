#!/bin/bash

# =============================================================================
# FIX-10.SH - SYSTEMATIC CSS DEBUG - FIND THE REAL PROBLEM
# =============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[DEBUG]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "=== SYSTEMATIC CSS DEBUG ==="

# 1. Check source files
print_status "1. Checking source CSS files..."

if [ -f "_static/style.css" ]; then
    SIZE=$(wc -c < "_static/style.css")
    LINES=$(wc -l < "_static/style.css")
    print_info "✓ _static/style.css exists: $SIZE bytes, $LINES lines"
    
    # Check for specific content we expect
    if grep -q "color:" "_static/style.css"; then
        print_info "  ✓ Contains color declarations"
    else
        print_warning "  ✗ No color declarations found"
    fi
    
    if grep -q "background" "_static/style.css"; then
        print_info "  ✓ Contains background declarations"
    else
        print_warning "  ✗ No background declarations found"
    fi
    
    if grep -q "font" "_static/style.css"; then
        print_info "  ✓ Contains font declarations"
    else
        print_warning "  ✗ No font declarations found"
    fi
    
    # Show first few CSS rules to verify content
    print_info "  First 10 lines of style.css:"
    head -10 "_static/style.css" | sed 's/^/    /'
    
else
    print_error "✗ _static/style.css MISSING!"
    exit 1
fi

if [ -f "theme/static/theme.css" ]; then
    SIZE=$(wc -c < "theme/static/theme.css")
    print_info "✓ theme/static/theme.css exists: $SIZE bytes"
else
    print_error "✗ theme/static/theme.css MISSING!"
fi

# 2. Check build directory
print_status "2. Checking build directory..."

if [ -d "_build/html/_static" ]; then
    print_info "✓ Build static directory exists"
    
    if [ -f "_build/html/_static/style.css" ]; then
        BUILD_SIZE=$(wc -c < "_build/html/_static/style.css")
        print_info "✓ style.css copied to build: $BUILD_SIZE bytes"
        
        # Compare sizes
        SOURCE_SIZE=$(wc -c < "_static/style.css")
        if [ "$BUILD_SIZE" -eq "$SOURCE_SIZE" ]; then
            print_info "  ✓ File sizes match - copy is correct"
        else
            print_warning "  ✗ File sizes don't match: source=$SOURCE_SIZE, build=$BUILD_SIZE"
        fi
    else
        print_error "✗ style.css NOT copied to build directory"
    fi
    
    if [ -f "_build/html/_static/theme.css" ]; then
        print_info "✓ theme.css copied to build"
    else
        print_error "✗ theme.css NOT copied to build"
    fi
    
    # List all CSS files in build
    print_info "CSS files in build directory:"
    ls -la "_build/html/_static/"*.css 2>/dev/null | sed 's/^/  /' || print_warning "No CSS files found in build"
    
else
    print_error "✗ Build directory doesn't exist - run ./quick-build.sh first"
    exit 1
fi

# 3. Create a test page with explicit CSS debugging
print_status "3. Creating CSS debug test page..."

cat > "debug-css-test.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>CSS Debug Test</title>
    <style>
        /* Inline test styles */
        .inline-test { background: red; color: white; padding: 10px; margin: 10px 0; }
        .debug-info { background: #f0f0f0; padding: 15px; margin: 10px 0; border: 1px solid #ccc; }
    </style>
    <!-- Load CSS files in the same order as theme -->
    <link rel="stylesheet" href="_build/html/_static/theme.css">
    <link rel="stylesheet" href="_build/html/_static/style.css">
</head>
<body>
    <div class="inline-test">INLINE CSS TEST - If you see this red box, inline CSS works</div>
    
    <div class="debug-info">
        <h3>CSS Loading Debug</h3>
        <p>This page loads CSS files directly to test if they work outside the theme.</p>
    </div>
    
    <!-- Test elements that should be styled by your CSS -->
    <div class="container">
        <h1>Test Heading</h1>
        <p>Test paragraph with some content.</p>
        
        <!-- Common classes from your CSS -->
        <div class="visualization-container">Visualization Container Test</div>
        <div class="mcq-module">MCQ Module Test</div>
    </div>
    
    <script>
        // Check what CSS rules are loaded
        console.log('=== CSS DEBUG ===');
        const sheets = document.styleSheets;
        console.log('Loaded stylesheets:', sheets.length);
        
        for (let i = 0; i < sheets.length; i++) {
            try {
                console.log(`Sheet ${i}:`, sheets[i].href);
                console.log(`  Rules:`, sheets[i].cssRules.length);
            } catch(e) {
                console.log(`Sheet ${i}: Cannot access rules`, e);
            }
        }
        
        // Test computed styles
        const testElement = document.querySelector('.container');
        if (testElement) {
            const styles = getComputedStyle(testElement);
            console.log('Container computed styles:', {
                color: styles.color,
                backgroundColor: styles.backgroundColor,
                fontSize: styles.fontSize,
                fontFamily: styles.fontFamily
            });
        }
    </script>
</body>
</html>
EOF

print_info "Created debug-css-test.html - open this in browser to test CSS loading"

# 4. Create a minimal layout that ONLY loads your CSS
print_status "4. Creating minimal test layout..."

cat > "theme/templates/layout.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% if title %}{{ title }} - {% endif %}{{ project }}</title>
    
    <!-- CSS DEBUG: Load your style.css ONLY -->
    <link rel="stylesheet" type="text/css" href="{{ pathto('_static/style.css', 1) }}" />
    
    <!-- Debug styles to verify CSS loading -->
    <style>
        .css-debug-marker {
            background: lime !important;
            color: black !important;
            padding: 10px !important;
            margin: 10px 0 !important;
            border: 3px solid red !important;
            font-weight: bold !important;
        }
        body { margin: 0; padding: 20px; font-family: Arial, sans-serif; }
    </style>
    
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>

<body>
    <!-- Debug marker -->
    <div class="css-debug-marker">
        CSS DEBUG: If you see this GREEN box, inline CSS works. 
        Your style.css should style the content below.
    </div>
    
    <!-- Minimal structure that matches what your CSS expects -->
    <div class="container">
        <h1>{% if title %}{{ title }}{% endif %}</h1>
        {% block body %}{% endblock %}
    </div>
    
    <!-- CSS Loading Check Script -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log('=== CSS LOADING DEBUG ===');
            
            // List all stylesheets
            const sheets = document.styleSheets;
            console.log('Total stylesheets loaded:', sheets.length);
            
            for (let i = 0; i < sheets.length; i++) {
                try {
                    const sheet = sheets[i];
                    console.log(`Stylesheet ${i + 1}:`);
                    console.log('  URL:', sheet.href);
                    console.log('  Rules:', sheet.cssRules ? sheet.cssRules.length : 'Cannot access');
                    
                    // Try to find some rules
                    if (sheet.cssRules) {
                        for (let j = 0; j < Math.min(5, sheet.cssRules.length); j++) {
                            console.log(`    Rule ${j + 1}:`, sheet.cssRules[j].cssText.substring(0, 100));
                        }
                    }
                } catch(e) {
                    console.log(`  Error accessing stylesheet ${i + 1}:`, e.message);
                }
            }
            
            // Check computed styles on key elements
            const container = document.querySelector('.container');
            if (container) {
                const styles = getComputedStyle(container);
                console.log('Container computed styles:');
                console.log('  color:', styles.color);
                console.log('  background-color:', styles.backgroundColor);
                console.log('  font-family:', styles.fontFamily);
                console.log('  font-size:', styles.fontSize);
                console.log('  margin:', styles.margin);
                console.log('  padding:', styles.padding);
                console.log('  max-width:', styles.maxWidth);
            }
            
            // Look for elements that should be styled
            const styledElements = document.querySelectorAll('h1, h2, p, .visualization-container, .mcq-module');
            console.log('Found styled elements:', styledElements.length);
            styledElements.forEach((el, index) => {
                const styles = getComputedStyle(el);
                console.log(`Element ${index + 1} (${el.tagName}${el.className ? '.' + el.className : ''}):`, {
                    color: styles.color,
                    fontSize: styles.fontSize,
                    fontWeight: styles.fontWeight
                });
            });
        });
    </script>
</body>
</html>
EOF

print_status "Created minimal debug layout"

# 5. Copy CSS manually to ensure it's there
print_status "5. Manually copying CSS files..."

mkdir -p "_build/html/_static"
cp "_static/style.css" "_build/html/_static/style.css" 2>/dev/null || print_error "Failed to copy style.css"

if [ -f "theme/static/theme.css" ]; then
    cp "theme/static/theme.css" "_build/html/_static/theme.css" 2>/dev/null || print_error "Failed to copy theme.css"
fi

print_status "Manual CSS copy completed"

print_info "✅ Systematic debug setup completed!"
echo
echo "🔍 DEBUG STEPS:"
echo "   1. Build with minimal layout: ./quick-build.sh"
echo "   2. Check browser console (F12) for detailed CSS debug info"
echo "   3. Look for GREEN debug box (shows inline CSS works)"
echo "   4. Open debug-css-test.html in browser to test CSS files directly"
echo
echo "📋 What to check:"
echo "   • GREEN box = Inline CSS works"
echo "   • Browser console = Detailed CSS loading info"
echo "   • Network tab = See if CSS files are actually requested/loaded"
echo "   • Computed styles = See what styles are actually applied"
echo
echo "🎯 This will tell us:"
echo "   • Are CSS files being loaded?"
echo "   • Are there CSS syntax errors?"
echo "   • Are selectors matching elements?"
echo "   • What computed styles are actually applied?"