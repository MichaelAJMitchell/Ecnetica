# Ecntica
### The Ecnetica project is an advanced mathematical resource aiming to tear down barriers to resources providing freely accessible content. Through cutting-edge animations and expert instruction, we're democratizing Higher Level mathematics education and empowering every Irish student with the quantitative reasoning skills needed for tomorrow's challenges.

<img src="logo.png" alt="Problem Solving Logo" width="100px" height="auto" style="display: block; margin: 0 auto;">

### Table of Contents

<div style="font-size: 1.3em;">

1. **Required Configuration for Windows Users** 
2. **Building and Running the Code** 
3. **Frontend**

</div>

## 1. Required Configuration for Windows Users

Before contributing please ensure you are using UNIX line break standards.

### Line Endings: Unix vs Windows

Most operating systems use LF (Line Feed only: `\n`) to represent a line ending, but Windows uses its own syntax CRLF (Carriage Return + Line Feed: `\r\n`). This causes inconsistencies in the project and files such as our build script won't run in CRLF.

### Our Solution

This repository enforces **LF line endings** for all text files using `.gitattributes`:

``` bash
* text=auto eol=lf
```

This configuration:

- Forces all text files to use Unix-style (LF) line endings in the repository
- Automatically detects and preserves binary files
- Applies to all contributors regardless of their operating system

#### Repository Normalization

We've used `git add --renormalize .` to convert all existing files to LF line endings and ensure consistency across the entire codebase.

#### Windows Users: VS Code Configuration

Windows users should configure VS Code to work seamlessly with LF line endings. Add these settings to your VS Code `settings.json`:

``` json
{
  "files.eol": "\n",
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true
}
```

**To configure these settings:**

**Alternative method:**

1. Go to File → Preferences → Settings
2. Search for "eol"
3. Set "Files: Eol" to "\n"

With this configuration, VS Code will:

- Create new files with LF line endings
- Display line endings consistently
- Avoid unnecessary file modifications

#### Verification

You can verify your line endings are correct by checking the bottom-right corner of VS Code - it should show "LF" rather than "CRLF".



## 2. Building and Running the Code

This project uses Jupyter Book to build the site.

### Python Virtual Environment

To build this project you need to set up a python virtual environment using the standard `venv` module.

Run the script `venv-setup.sh` from `~/${path-to}/Ecnetica/`

``` bash
bash venv-setup.sh
```

This will set up our virtual enviornmnet with our required packages.

#### _Manual Method for building venv_

First we need to set this up with this command, run this from `~/${path-to}/Ecnetica/`:

``` bash
python3 -m venv venv
```

This creates our virtual environment and names it `venv`. 

To activate this virtual environment:

``` bash
source venv/bin/activate 
```

Now you should see:

``` bash
(venv) user@computer 
```

Now we need to install the required packages. Using pip (if you don't have pip install it, eg `sudo apt install python3-pip`) we can install the `requirements.txt` with:

``` bash
pip install -r requirements.txt
```

Now we have our `venv` set up ready for building our site. Make sure for the rest of the process you have the virtual environment running.

## Building

### Making the Script Executable

First, make the build script executable:

```bash
chmod u+x quick-build.sh
```

### Standard Build
This site uses jupyter notebooks for compiling. From `~/${path-to}/Ecnetica/` run:

```bash
./quick-build.sh
```

This script runs `jupyter-book build .`, then navigates to `Ecnetica/_build/html` and runs a python server. Note: the website must be loaded in a server or else the python quizzes won't be able to load properly. 

Now you should be able to view the site from `http://localhost:8000/`, to escape this process `Ctrl + C`.

### Fast Testing Build

For rapid theme development and testing, use the testing build which only builds a few specified pages (configurable in quick-build.sh):

```bash
./quick-build.sh testing
```

This creates a minimal `content-testing/` directory with essential files and builds much faster for iterating on:

- Theme customizations
- Navbar layout changes
- CSS modifications
- Interactive component testing

The testing build currently includes:

- Index page
- Quadratic functions (with interactive visualizations)
- Interactive tools (Python playground, BKT demo)

### Custom TOC Build

You can also build with custom table of contents files:

```bash
./quick-build.sh <name>
```

This uses `_toc-<name>.yml` file. For example:

- `./quick-build.sh full` uses `_toc-full.yml`
- `./quick-build.sh minimal` uses `_toc-minimal.yml`


# 3. Frontend Customization

The Ecnetica project uses a frontend system built on Jupyter Book with PyData Sphinx Theme, with custom CSS and JavaScript.

## Frontend Structure Overview

The frontend consists of several key components located in the _static/ directory:

```
_static/
├── style.css            # Main consolidated stylesheet
├── theme.js             # Theme toggle and navigation functionality
├── jsxgraph.css         # JSXGraph mathematical visualization styling
├── jsxgraph-module.js   # JSXGraph component system and theming
├── math_visualiser.css  # Dedicated mathematical visualization styles
├── math_visualiser.js   # Interactive math visualization engine
├── math.min.js         # Mathematical computation library
└── IdentityQuestions.js # Interactive math question module system
```

## Configuration Files

The frontend is configured through the `_config.yml` file in the Sphinx section:

```
html:
  extra_css:
    - "_static/style.css"
    - "_static/jsxgraph.css"
    - "_static/math_visualiser.css"
  extra_js:
    - "_static/theme.js"
    - "_static/math_visualiser.js"
    - "_static/jsxgraph-module.js"
    - "_static/math.min.js"
    - "_static/IdentityQuestions.js"

sphinx:
  config:
    html_theme: pydata_sphinx_theme
    html_theme_options:
      navbar_start: ["navbar-logo"]
      navbar_center: []
      navbar_end: ["search-button"]
      # Additional theme options...
```

## Main Stylesheet (`_static/style.css`)

Your primary stylesheet is a comprehensive, well-organized file that serves as the foundation for your site's visual design. Here's how it's structured:

### **CSS Variables System**
The stylesheet starts with a complete theming system using CSS custom properties:

```css
:root {
 /* Background colors */
 --background-primary: #ffffff;
 --background-secondary: #f8f9fa;
 --text-primary: #2c3e50;
 --primary: #3498db;
 /* ...and many more */
}
```

This CSS variables approach is what enables your light/dark theme toggle functionality. When users click the theme toggle button, JavaScript changes the `data-theme` attribute on the HTML element, and the CSS variables automatically update all colors site-wide.

We also use limited dark theme overrides
```css
html[data-theme="dark"] {
  /* Only overrides variables that need different values in dark mode */
}
```

You use dark theme overrides sparingly - most of the theming work is handled by the CSS variables system itself.

### **Main Component Categories**
The stylesheet is organized into clear sections:

1. CSS VARIABLES (ROOT & THEMES)
2. BASE TYPOGRAPHY & LAYOUT
3. VISUALIZATION CONTAINERS (CORE MATH CONTENT)
4. MATH QUESTION MODULE
5. INTERACTIVE ELEMENTS
6. SUPPORTING CONTENT
7. RESPONSIVE DESIGN
8. THEME STYLES (includes navbar and width adjustments)

## Theme JavaScript `_static/theme.js`

**1. Theme Toggle System**

Automatically detects user's theme preference and provides a smooth toggle between light/dark modes with localStorage persistence.

**2. Course Navigator**

Creates a collapsible, searchable course outline that shows the hierarchical structure of your content with current page highlighting.

**3. Tools Finder**

Creates a floating tools panel that provides quick access to interactive mathematical tools and demos throughout the site.

**4. Sidebar Management**

Dynamically hides sidebars and expands the main content area to use the full width of the screen in any file contained in `content/interactive/`.


## Extra Stylesheets and JavaScript 

**JSXGraph Stylesheet `_static/jsxgraph.css`**

Base styling for the JSXGraph library that handles interactive mathematical graphs, including graph containers, navigation controls, and mathematical object appearance.

**Mathematical Visualization Stylesheet `_static/math_visualiser.css`**

Dedicated styles for your custom mathematical visualization containers, providing responsive layouts, control interfaces, and theme-aware styling for interactive math content.

**JSXGraph Module System `_static/jsxgraph-module.js`**

Enhances JSXGraph with automatic theming, color management, and pre-configured templates for mathematical objects like points, lines, and functions.

**Mathematical Visualization Engine `_static/math_visualiser.js`**

Your custom engine that creates interactive mathematical visualizations with real-time analysis, parameter controls, and multi-instance support for complex mathematical content.

**Mathematical Computation Library `_static/math.min.js`**

Provides advanced mathematical functions for expression parsing, symbolic mathematics, and numerical calculations used by your interactive components.

**Interactive Question System `_static/IdentityQuestions.js`**

Creates category-based mathematical question modules with LaTeX support for educational interactions across scientific, engineering, financial, and creative contexts.

# 4. Adding New Content

#### How to Add a New Page

This guide walks you through the complete process of adding a new page to the Ecnetica course website.

## Steps Overview

1. Create the content file
2. Add to Table of Contents (_toc.yml) 
3. Update Course Navigator (JSON)
4. Test and Build

---

## 1. Create the Content File

Create your new markdown file in the appropriate directory under `content/`:

```
content/
├── algebra/
├── functions/
├── geometry/
├── introduction/
├── interactive/
├── number_systems/
├── probability/
├── statistics/
└── trigonometry/
```

### Example: Adding a new algebra topic

```bash
# Create the file
touch content/algebra/my_new_topic.md
```

## 2. Add to Table of Contents

Edit `_toc.yml` to include your new page in the site navigation.

### For a standalone page:
```yaml
- caption: Algebra
  chapters:
  - file: content/algebra/existing_topic
  - file: content/algebra/my_new_topic  # Add this line
```

### For a page with subsections:
```yaml
- caption: Algebra
  chapters:
  - file: content/algebra/my_new_topic
    sections:
    - file: content/algebra/my_new_topic_part1
    - file: content/algebra/my_new_topic_part2
```

### For adding to existing sections:
```yaml
- caption: Algebra
  chapters:
  - file: content/algebra/expressions_manipulation
    sections:
    - file: content/algebra/algebraic_notation
    - file: content/algebra/substitution_simplification
    - file: content/algebra/my_new_topic  # Add this line
```

---

## 3. Update Course Navigator (JSON)

Edit `_static/course_structure.json` to add your new page to the custom course navigator.

### Example: Adding to existing section
```json
{
  "Algebra": {
    "Expressions Manipulation": {
      "Algebraic Notation": "/content/algebra/algebraic_notation.html",
      "Substitution Simplification": "/content/algebra/substitution_simplification.html",
      "My New Topic": "/content/algebra/my_new_topic.html"
    }
  }
}
```

### Example: Adding new section
```json
{
  "Algebra": {
    "Expressions Manipulation": {
      "Algebraic Notation": "/content/algebra/algebraic_notation.html"
    },
    "My New Section": {
      "My New Topic": "/content/algebra/my_new_topic.html",
      "Another Topic": "/content/algebra/another_topic.html"
    }
  }
}
```

### Example: Adding new chapter
```json
{
  "Introduction": {
    "Course Overview": "/content/introduction/course_overview.html"
  },
  "My New Chapter": {
    "Topic 1": "/content/my_chapter/topic1.html",
    "Topic 2": "/content/my_chapter/topic2.html"
  },
  "Algebra": {
    "Expressions Manipulation": {
      "Algebraic Notation": "/content/algebra/algebraic_notation.html"
    }
  }
}
```

**Important Notes:**
- Use `.html` extension in the JSON (Jupyter Book converts `.md` to `.html`)
- File paths should match the structure in `_toc.yml`
- Maintain consistent indentation in JSON

---

## 4. Test and Build

### Quick Testing Build
For rapid testing during development:
```bash
./quick-build.sh testing
```

### Full Build
Once you're satisfied with your changes:
```bash
./quick-build.sh
```

### Verify Your Changes
1. **Check the sidebar navigation** - your page should appear in the main navigation
2. **Check the course navigator** - your page should appear in the custom navigator (book icon in navbar)
3. **Test the search** - your page should be searchable in the course navigator
4. **Check links** - ensure all internal links work correctly

