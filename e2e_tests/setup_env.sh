#!/bin/bash
# Environment setup script for E2E tests
# Source this file to set up PYTHONPATH and create __init__.py files
# Usage: source setup_env.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Create __init__.py files if they don't exist
touch __init__.py
touch config/__init__.py 2>/dev/null || true
touch fixtures/__init__.py 2>/dev/null || true
touch pages/__init__.py 2>/dev/null || true
touch api_tests/__init__.py 2>/dev/null || true
touch ui_tests/__init__.py 2>/dev/null || true
touch utils/__init__.py 2>/dev/null || true

# Create reports directory
mkdir -p reports/screenshots

# Set PYTHONPATH (add to existing, don't replace)
if [[ ":$PYTHONPATH:" != *":$SCRIPT_DIR:"* ]]; then
    export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}"
fi

echo "✓ E2E test environment ready"
echo "  PYTHONPATH: ${PYTHONPATH}"
echo "  Working directory: ${SCRIPT_DIR}"

