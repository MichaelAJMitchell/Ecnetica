"""
Custom Jupyter Book Theme Package
=================================

A custom theme for Jupyter Book projects with advanced mathematical content,
interactive visualizations, and comprehensive styling support.

Features:
- Custom HTML templates with full layout control
- Integrated CSS theming system
- Light/dark mode support
- Mathematical content optimization
- Interactive component styling
"""

from pathlib import Path

__version__ = "1.0.0"
__author__ = "The Problem Solving Association C.L.G."

def get_html_theme_path():
    """Return the path to the theme's HTML templates."""
    return str(Path(__file__).parent.resolve())

def setup(app):
    """Set up the Sphinx theme."""
    theme_path = get_html_theme_path()
    app.add_html_theme("theme", theme_path)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
