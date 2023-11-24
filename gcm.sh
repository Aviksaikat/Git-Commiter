#!/bin/bash

# Check if directory argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

# Move to the specified directory
cd "$1" || exit 1

# Add modified files
git diff --name-only --cached > modified_files.txt

# Add untracked files
git ls-files --others --exclude-standard >> modified_files.txt

# Separate added and modified files
added_files=""
modified_files=""

while IFS= read -r file; do
  if [ -e "$file" ]; then
    modified_files+="\n- Update ${file}"
  else
    added_files+="\n- Add new file: ${file}"
  fi
done < modified_files.txt

# Stage all changes
git add .

# Create commit messages
commit_message="feat: Update and modify files for the project"
[ -n "$modified_files" ] && commit_message+=" (modified files:${modified_files})"
[ -n "$added_files" ] && commit_message+=" (added files:${added_files})"

# Commit changes
git commit -m "$commit_message"

# Clean up temporary file
rm modified_files.txt
