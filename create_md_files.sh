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
echo "This script will create Markdown files based on your _toc.yml structure."
echo "Parent directory: $(pwd)"
read -p "Do you want to continue? (y/n): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Create required directories
echo "Creating directories as needed..."

# Function to create a Markdown file with a specific title
create_markdown() {
    local file="$1"
    local title="$2"
   
    # Safety check: Don't overwrite existing files without confirmation
    if [ -f "${file}.md" ]; then
        read -p "File ${file}.md already exists. Overwrite? (y/n): " overwrite
        if [[ "$overwrite" != "y" && "$overwrite" != "Y" ]]; then
            echo "Skipping ${file}.md"
            return
        fi
    fi
   
    # Safety check: Ensure the path doesn't try to escape the designated directory
    if [[ "$file" == /* || "$file" == ../* ]]; then
        echo "Warning: Skipping unsafe path: $file (absolute or parent directory paths not allowed)"
        return
    fi
   
    # Create directory if it doesn't exist
    mkdir -p "$(dirname "$file")"
   
    # Generate markdown template with the specific title
    markdown_content="# $title

Content goes here.

## Section 1

This is the first section of the $title page.

## Section 2

This is the second section of the $title page.
"
   
    # Write the markdown file
    echo "$markdown_content" > "${file}.md"
    echo "Created ${file}.md with title: ${title}"
}

# Create root index file
echo "Creating root index file..."
create_markdown "content/index" "Interactive Mathematics Resource"

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
       
        # Create markdown file with appropriate title
        create_markdown "$file" "$title"
        count=$((count+1))
    fi
done < _toc.yml

echo "Done! Created $count markdown files."
echo "All files were created successfully!"