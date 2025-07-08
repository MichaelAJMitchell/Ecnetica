# Points to note for running locally

## Running the code

1. jupyter-book build . (In the project home directory)
2. Navigate to the _build/html
3. Run
   ```
   python -m http.server
   ```
### Or
Run this script in the home directory, ctrl +c to escape

```bash quick-build.sh```

## Adding Chapters

You have to

1. Add the chapter itself
2. Add it to the index page
3. Add it to _toc.yml
4. Remove the build folder
5. Rebuild using the jupyter-book command
