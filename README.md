# Ecntica
### The Ecnetica project is an advanced mathematical resource aiming to tear down barriers to resources providing freely accessible content. Through cutting-edge animations and expert instruction, we're democratizing Higher Level mathematics education and empowering every Irish student with the quantitative reasoning skills needed for tomorrow's challenges.

<img src="logo.png" alt="Problem Solving Logo" width="100px" height="auto" style="display: block; margin: 0 auto;">

## Table of Contents

<div style="font-size: 1.3em;">

1. **Required Configuration for Windows Users** 
2. **Building and Running the Code** 
<!--3. **Jupyter Book Explanation**-->

</div>



# Required Configuration for Windows Users
Before contributing please ensure you are using UNIX line break standards.

## Line Endings: Unix vs Windows

Most operating systems use LF (Line Feed only: `\n`) to represent a line ending, but Windows uses its own syntax CRLF (Carriage Return + Line Feed: `\r\n`). This causes inconsistencies in the project and files such as our build script won't run in CRLF.

### Our Solution

This repository enforces **LF line endings** for all text files using `.gitattributes`:

```
* text=auto eol=lf
```

This configuration:
- Forces all text files to use Unix-style (LF) line endings in the repository
- Automatically detects and preserves binary files
- Applies to all contributors regardless of their operating system

#### Repository Normalization
We've used `git add --renormalize .` to convert all existing files to LF line endings and ensure consistency across the entire codebase.

### Windows Users: VS Code Configuration

Windows users should configure VS Code to work seamlessly with LF line endings. Add these settings to your VS Code `settings.json`:

```json
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

##### Verification

You can verify your line endings are correct by checking the bottom-right corner of VS Code - it should show "LF" rather than "CRLF".



# Building and Running the Code

This project uses Jupyter Book to build the site.

## Python Virtual Environment

To build this project you need to set up a python virtual environment using the standard `venv` module.

First we need to set this up with this command, run this from `~/${path-to}/Ecnetica/`:
```bash
python3 -m venv venv
```

This creates our virtual environment and names it `venv`. 

To activate this virtual environment:
```bash
source venv/bin/activate 
```

Now you should see:
```bash
(venv) user@computer 
```

Now we need to install the required packages. Using pip (if you don't have pip install it, eg `sudo apt install python3-pip`) we can install the `requirements.txt` with:
```bash
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


<!--# Jupyter Book Explanation-->

<!--
## Adding Chapters

To add a new chapter:

1. Add the chapter itself
2. Add it to the index page
3. Add it to `_toc.yml`
4. Remove the build folder
5. Rebuild using the jupyter-book command
-->