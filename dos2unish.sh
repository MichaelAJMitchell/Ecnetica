#!/bin/bash

# pass in everyfile in the current directory to dos2unix
find . -type f | xargs dos2unix 
