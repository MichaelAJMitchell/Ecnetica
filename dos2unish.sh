#!/bin/bash

# pass in everyfile in the current directory to dos2unix
# important: don't remove the f flag, otherwise it will corrupt binary files
find . -type f | xargs dos2unix 
