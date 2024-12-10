#!/bin/bash

# Specify the directory to search in (default is the current directory)
SEARCH_DIR="${1:-.}"

# The Unicode character U+200E (LRM) in hex format
UNICODE_CHARACTER=$'\xE2\x80\x8E'

# Search for the character in all files in the specified directory (recursively)
echo "Searching for files containing the U+200E character in directory: $SEARCH_DIR"

# Find all files and check for occurrences of U+200E
find "$SEARCH_DIR" -type f -exec grep -lU "$UNICODE_CHARACTER" {} \;

echo "Search completed."
