#!/bin/bash

# Add modified files
git diff --name-only --cached > modified_files.txt

# Add untracked files
git ls-files --others --exclude-standard >> modified_files.txt

# Create commit message
commit_message="feat: Add and modify files for the project

$(awk '{print "- " $1}' modified_files.txt)"

# Add the files
git add .
# Commit changes
git commit -m "$commit_message"

# Clean up temporary file
rm modified_files.txt
