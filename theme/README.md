# Custom Jupyter Book Theme

This is a custom theme for the Ecnetica Jupyter Book project.

## Structure

- `__init__.py` - Python package configuration
- `theme.conf` - Theme configuration file
- `static/` - CSS and JavaScript files
  - `theme.css` - Main theme stylesheet
  - `js/theme.js` - Theme JavaScript functionality
- `templates/` - Jinja2 HTML templates
  - `layout.html` - Main page layout
  - `page.html` - Content page template
  - `sections/` - Reusable page sections
  - `components/` - Small reusable components

## Installation

1. The theme directory should be in your project root
2. Update your `_config.yml` to use `html_theme: theme`
3. Add `html_theme_path: ["."]` to your sphinx config
4. Build your book as usual

## Customization

- Edit CSS variables in `static/theme.css` to change colors and spacing
- Modify templates in `templates/` to change HTML structure
- Add custom JavaScript to `static/js/theme.js`

## Features

- Responsive design with mobile navigation
- Light/dark theme switching
- Collapsible sidebar navigation
- Reading progress indicator
- Enhanced accessibility
- Integration with existing styles
