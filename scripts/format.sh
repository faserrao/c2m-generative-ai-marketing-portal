#!/bin/bash

# Check if a directory argument is provided
if [ $# -eq 0 ]; then
    echo "Please provide a directory path as an argument."
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Set the target directory from the first argument
TARGET_DIR="$1"

# Check if the directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

# Run the formatting tools
echo "isort: Formatting directory: $TARGET_DIR"
isort "$TARGET_DIR"
echo "black: Formatting directory: $TARGET_DIR"
black "$TARGET_DIR"
echo "ruff: Formatting directory: $TARGET_DIR"
ruff check "$TARGET_DIR" --fix

echo "Formatting complete!"
