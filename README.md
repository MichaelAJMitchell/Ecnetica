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

<!--
**Alternative execution:**
The bash script can also be run with the command:
```bash
bash quick-build.sh
```
but I prefer `./`
-->

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


<!--
## Adding Chapters

To add a new chapter:

1. Add the chapter itself
2. Add it to the index page
3. Add it to `_toc.yml`
4. Remove the build folder
5. Rebuild using the jupyter-book command
-->