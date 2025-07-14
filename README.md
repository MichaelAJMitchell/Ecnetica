# Building and Running the code

This project uses Jupyter Book to build the site
### Python Virtual Environment

To build this project you need to set up a python virtual environment using the standard `venv` module.
First we need to set this up with this command, run this from `~/projects/Ecnetica/`
```
python3 -m venv venv
```
This creates our virtual environment and names it `venv`. 
To activate this virtual environment
```
source venv/bin/activate 
```
Now you should see
```
(venv) user@computer 
```

Now we need to install the required packages. Using pip (if you don't have pip install it, eg `sudo apt install python3-pip`) we can install the `requirements.txt` with
```
pip install -r requirements.txt
```
Now we have our `venv` set up ready for building our site. Make sure for the rest of the process you have the virtual environment running.

### Building
This site uses jupyter notebooks for compiling. From `~/projects/Ecnetica/` run the script `quick-build.sh`
```
bash quick-build.sh
```
This script runs `jupyter-book build .`, then navigates to `Ecnetica/_build/html` and runs a python server. Note: the website must be loaded in a server or else the python quizzes won't be able to load properly. 

Now you should be able to view the site from `http://localhost:8000/`, to escape this process `ctrl +c`

Note: the bash script can also be run with the command
``` 
./quick-build.sh
```
As long as you have made the bash script executable with 

```
chmod u+x quick-build.sh
``` 
both 
```./quick-build.sh``` and ``` bash quick-build.sh``` are identical


## Adding Chapters

You have to

1. Add the chapter itself
2. Add it to the index page
3. Add it to _toc.yml
4. Remove the build folder
5. Rebuild using the jupyter-book command
