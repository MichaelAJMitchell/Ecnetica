#!/bin/bash

# =============================================================================
# FIX-12.SH - ROLLBACK to working state before recent fixes
# =============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[ROLLBACK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_status "Rolling back to working state..."

# Remove problematic files from recent fixes
print_status "Cleaning up recent changes..."

rm -f "debug-css-test.html" 2>/dev/null || true
rm -f "test-css-structures.sh" 2>/dev/null || true
rm -f "theme/templates/layout-alt.html" 2>/dev/null || true
rm -f "theme/templates/layout-minimal.html" 2>/dev/null || true
rm -f "theme/templates/layout-active.html" 2>/dev/null || true
rm -f "theme/templates/layout-backup.html" 2>/dev/null || true
rm -f "theme/static/css-bridge.css" 2>/dev/null || true

print_status "Restoring working layout from fix-4/fix-5 era..."

# Restore the layout that was working (from fix-4 era)
cat > "theme/templates/layout.html" << 'EOF'
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% if title %}{{ title }} - {% endif %}{{ project }}</title>
    
    <!-- CSS Loading Order -->
    <link rel="stylesheet" type="text/css" href="{{ pathto('_static/theme.css', 1) }}" />
    <link rel="stylesheet" type="text/css" href="{{ pathto('_static/style.css', 1) }}" />
    <link rel="stylesheet" type="text/css" href="{{ pathto('_static/jsxgraph.css', 1) }}" />
    
    <!-- MathJax -->
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    {% block extrahead %}{% endblock %}
</head>

<body class="theme-body">
    <div class="theme-wrapper">
        
        <!-- Skip link -->
        <a class="skip-link" href="#main-content">Skip to main content</a>
        
        <!-- Header -->
        <header class="theme-header">
            {% include "sections/navbar.html" %}
        </header>
        
        <!-- Main container -->
        <div class="theme-container">
            
            <!-- Sidebar -->
            <aside class="theme-sidebar">
                {% include "sections/sidebar.html" %}
            </aside>
            
            <!-- Main content -->
            <main class="theme-main" id="main-content">
                
                <!-- Breadcrumbs -->
                <nav class="theme-breadcrumbs">
                    {% include "components/breadcrumbs.html" %}
                </nav>
                
                <!-- Article -->
                <article class="theme-article">
                    
                    {% if title %}
                    <header class="article-header">
                        <h1 class="article-title">{{ title }}</h1>
                    </header>
                    {% endif %}
                    
                    <div class="article-content user-content">
                        {% block body %}{% endblock %}
                    </div>
                    
                </article>
                
            </main>
            
        </div>
        
        <!-- Footer -->
        <footer class="theme-footer">
            {% include "sections/footer.html" %}
        </footer>
        
    </div>
    
    <!-- JavaScript -->
    <script src="{{ pathto('_static/js/theme.js', 1) }}"></script>
    
    {% block scripts %}{% endblock %}
    
</body>
</html>
EOF

print_status "Restoring working page template..."

cat > "theme/templates/page.html" << 'EOF'
{% extends "layout.html" %}

{%- block body %}
<div class="page-content">
    <div class="page-body">
        {{ body }}
    </div>
</div>
{%- endblock %}
EOF

print_status "Restoring working theme.css..."

# Restore the basic working theme.css (from fix-4/fix-5)
cat > "theme/static/theme.css" << 'EOF'
/*====================================================================*\
CUSTOM JUPYTER BOOK THEME - WORKING VERSION (ROLLBACK)
\*====================================================================*/

/* Basic structure that works */
.theme-body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background: #ffffff;
    color: #2c3e50;
}

.theme-wrapper {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.theme-container {
    display: grid;
    grid-template-columns: 280px 1fr;
    grid-template-areas: "sidebar main";
    flex: 1;
    max-width: 1400px;
    margin: 0 auto;
    gap: 20px;
    padding: 0 15px;
}

.theme-sidebar {
    grid-area: sidebar;
    background: #f8f9fa;
    border-right: 1px solid #dee2e6;
    height: calc(100vh - 60px);
    position: sticky;
    top: 60px;
    overflow-y: auto;
    padding: 20px;
}

.theme-main {
    grid-area: main;
    min-width: 0;
    padding: 20px 0;
}

.theme-article {
    background: #ffffff;
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    max-width: none;
    margin: 0;
}

.article-title {
    color: #2c3e50;
    font-size: 2.5em;
    font-weight: 700;
    margin: 0 0 30px 0;
    text-align: center;
}

/* Let user CSS take complete control */
.user-content {
    color: initial;
    font-family: initial;
    line-height: initial;
}

.user-content * {
    color: inherit;
    font-family: inherit;
    line-height: inherit;
}

/* Header */
.theme-header {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

.navbar {
    height: 60px;
    padding: 0 20px;
}

.navbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100%;
    max-width: 1400px;
    margin: 0 auto;
}

.navbar-brand .brand-link {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: #2c3e50;
    font-weight: 600;
}

.brand-logo {
    height: 32px;
    width: auto;
}

.sidebar-title {
    font-size: 1.2em;
    margin: 0 0 10px 0;
    font-weight: 600;
    text-align: center;
}

.sidebar-author {
    font-size: 0.9em;
    margin: 0;
    font-style: italic;
    text-align: center;
    color: #6c757d;
}

/* Footer */
.theme-footer {
    background: #f8f9fa;
    border-top: 1px solid #dee2e6;
    margin-top: auto;
    padding: 20px;
    text-align: center;
    font-size: 0.9em;
    color: #6c757d;
}

/* Breadcrumbs */
.breadcrumbs {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 10px 15px;
    margin-bottom: 20px;
}

.breadcrumb-list {
    display: flex;
    align-items: center;
    list-style: none;
    margin: 0;
    padding: 0;
    flex-wrap: wrap;
}

.breadcrumb-item {
    display: flex;
    align-items: center;
}

.breadcrumb-separator {
    margin: 0 10px;
    color: #adb5bd;
}

.breadcrumb-link {
    color: #6c757d;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 5px;
    border-radius: 4px;
}

.breadcrumb-link:hover {
    background: #ffffff;
    color: #007bff;
}

.breadcrumb-current {
    color: #adb5bd;
    font-weight: 500;
}

/* Theme toggle */
.theme-toggle {
    background: none;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 8px;
    cursor: pointer;
    width: 40px;
    height: 40px;
    position: relative;
}

.theme-icon {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.navbar-utilities {
    display: flex;
    align-items: center;
    gap: 15px;
}

/* Responsive */
@media (max-width: 768px) {
    .theme-container {
        grid-template-columns: 1fr;
        grid-template-areas: "main";
    }
    
    .theme-sidebar {
        display: none;
    }
}

/* Utilities */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: #007bff;
    color: white;
    padding: 8px;
    text-decoration: none;
    z-index: 1200;
}

.skip-link:focus {
    top: 6px;
}

.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
EOF

print_status "Restoring working config..."

# Restore a working config (from fix-5 era)
cat > "_config-rollback.yml" << 'EOF'
# Book settings - ROLLBACK to working version
title: Premium Leaving Certificate Higher Level Maths Notes from TPSA
author: The Problem Solving Association C.L.G.
logo: logo.png

# Execution settings
execute:
  execute_notebooks: force
  hide_input: true

# LaTeX settings
latex:
  latex_documents:
    targetname: book.tex

# Bibliography
bibtex_bibfiles:
  - references.bib

# Repository information
repository:
  url: https://github.com/MichaelAJMitchell/Ecnetica
  path_to_book: ./
  branch: jb

# HTML settings
html:
  use_issues_button: true
  use_repository_button: true
  use_edit_page_button: true
  baseurl: ""
  extra_footer: "Copyright-info"
  sidebar:
    maxdepth: 1

# Sphinx configuration
sphinx:
  config:
    html_theme: theme
    html_theme_path: ["."]
    
    html_theme_options:
      navigation_depth: 4
      collapse_navigation: true
    
    html_static_path: ["_static", "theme/static"]
    html_title: "Premium Leaving Certificate Higher Level Maths Notes from TPSA"
    html_short_title: "TPSA Maths Notes"
    templates_path: ["theme/templates"]

# MyST parser settings
parse:
  myst_enable_extensions:
    - amsmath
    - colon_fence
    - deflist
    - dollarmath
    - html_admonition
    - html_image
    - linkify
    - replacements
    - smartquotes
    - substitution
    - tasklist
  myst_url_schemes: [mailto, http, https]
EOF

print_status "✅ Rollback completed!"
echo
echo "🔄 Restored to working state:"
echo "   • Simple, functional layout template"
echo "   • Basic theme.css that doesn't interfere"
echo "   • Working config without complex options"
echo "   • Removed all recent debug/test files"
echo
echo "📋 Next steps:"
echo "   1. Use rolled-back config: cp _config-rollback.yml _config.yml"
echo "   2. Test basic functionality: ./quick-build.sh"
echo "   3. Verify theme works without CSS conflicts"
echo
echo "💡 Now we can take a simpler approach to fix the CSS integration"
echo "without breaking the basic functionality."