#!/bin/bash

# Set the script to exit immediately if any command fails
set -e

# Check if _toc.yml exists
if [ ! -f "_toc.yml" ]; then
    echo "Error: _toc.yml file not found in current directory."
    echo "Please create this file before running the script."
    exit 1
fi

# Ask for confirmation before proceeding
echo "This script will create Jupyter notebook files in a 'content' folder based on your _toc.yml structure."
echo "Parent directory: $(pwd)"
read -p "Do you want to continue? (y/n): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Create content directory
mkdir -p content
echo "Created content directory."

# Function to create a Jupyter notebook with a specific title
create_notebook() {
    local file="content/$1"
    local title="$2"
    
    # Safety check: Don't overwrite existing files without confirmation
    if [ -f "${file}.ipynb" ]; then
        read -p "File ${file}.ipynb already exists. Overwrite? (y/n): " overwrite
        if [[ "$overwrite" != "y" && "$overwrite" != "Y" ]]; then
            echo "Skipping ${file}.ipynb"
            return
        fi
    fi
    
    # Safety check: Ensure the path doesn't try to escape the designated directory
    if [[ "$1" == /* || "$1" == ../* ]]; then
        echo "Warning: Skipping unsafe path: $1 (absolute or parent directory paths not allowed)"
        return
    fi
    
    # Generate JSON template with the specific title
    notebook='{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# '"$title"'\n",
    "\n",
    "Content goes here."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}'
    
    # Create directory if it doesn't exist
    mkdir -p "$(dirname "$file")"
    
    # Write the notebook file
    echo "$notebook" > "${file}.ipynb"
    echo "Created ${file}.ipynb with title: ${title}"
}

# Create root index file
echo "Creating root index file..."
create_notebook "index" "Interactive Mathematics Resource"

# Process the _toc.yml file to extract file paths
echo "Extracting file paths from _toc.yml..."
count=0
while IFS= read -r line; do
    if [[ $line =~ file:\ *(.*) ]]; then
        file="${BASH_REMATCH[1]}"
        file=$(echo "$file" | sed 's/^[ \t]*//')
        
        # Safety check: Ensure the path doesn't try to escape the designated directory
        if [[ "$file" == /* || "$file" == ../* ]]; then
            echo "Warning: Skipping unsafe path: $file (absolute or parent directory paths not allowed)"
            continue
        fi
        
        # Extract directory path
        dir=$(dirname "$file")
        
        # Convert file path to title
        # Extract the basename and remove underscores
        base=$(basename "$file" | tr '_' ' ')
        # Capitalize first letter of each word
        title=$(echo "$base" | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')
        
        # Create notebook file with appropriate title
        create_notebook "$file" "$title"
        count=$((count+1))
    fi
done < _toc.yml

echo "Done! Created $count notebook files."
echo "All files were created in the 'content' directory: $(pwd)/content"
echo ""
echo "NOTE: You may need to update your _toc.yml file to reference paths inside the content folder"
echo "      e.g., change 'file: introduction/overview' to 'file: content/introduction/overview'"