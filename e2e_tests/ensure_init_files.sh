#!/bin/bash
# ensure_init_files.sh
# Ensures all __init__.py files exist and are committed to git
# Run this once to commit all __init__.py files to the repository

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Ensuring all __init__.py files exist and are committed to git..."
echo ""

# List of all required __init__.py files
INIT_FILES=(
    "__init__.py"
    "config/__init__.py"
    "fixtures/__init__.py"
    "pages/__init__.py"
    "api_tests/__init__.py"
    "ui_tests/__init__.py"
    "utils/__init__.py"
)

# Create any missing files
echo "Creating missing __init__.py files..."
for file in "${INIT_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "  Creating: $file"
        touch "$file"
    else
        echo "  ✓ Exists: $file"
    fi
done

echo ""
echo "All __init__.py files are present."
echo ""

# Check if we're in a git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Git repository detected. Checking git status..."
    echo ""
    
    # Check which files are untracked or modified
    UNTRACKED=$(git ls-files --others --exclude-standard "${INIT_FILES[@]}" 2>/dev/null || true)
    MODIFIED=$(git diff --name-only "${INIT_FILES[@]}" 2>/dev/null || true)
    
    if [ -n "$UNTRACKED" ] || [ -n "$MODIFIED" ]; then
        echo "The following __init__.py files need to be committed:"
        [ -n "$UNTRACKED" ] && echo "  Untracked: $UNTRACKED"
        [ -n "$MODIFIED" ] && echo "  Modified: $MODIFIED"
        echo ""
        echo "To commit them, run:"
        echo "  git add ${INIT_FILES[*]}"
        echo "  git commit -m 'Add __init__.py files for Python package imports'"
    else
        echo "✓ All __init__.py files are already tracked in git."
    fi
else
    echo "Not a git repository. Files created but not committed."
    echo "If this is a git repo, ensure __init__.py files are committed."
fi

echo ""
echo "✅ Done!"

