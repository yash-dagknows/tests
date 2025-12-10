#!/bin/bash
# Setup script for E2E tests
# Ensures all required files are in place and sets up environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Setting up E2E test environment..."

# Create __init__.py files if they don't exist
echo "Creating __init__.py files..."
touch __init__.py
touch config/__init__.py
touch fixtures/__init__.py
touch pages/__init__.py
touch api_tests/__init__.py
touch ui_tests/__init__.py
touch utils/__init__.py

echo "✓ All __init__.py files created"

# Create reports directory
echo "Creating reports directory..."
mkdir -p reports/screenshots

echo "✓ Reports directory created"

# Set PYTHONPATH
echo "Setting PYTHONPATH..."
export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}"
echo "✓ PYTHONPATH set to: ${PYTHONPATH}"

echo ""
echo "✅ Setup complete!"
echo ""
echo "IMPORTANT: PYTHONPATH is set for this session only."
echo ""
echo "To make it persistent, add this to your ~/.bashrc or ~/.zshrc:"
echo "  export PYTHONPATH=\"\${PYTHONPATH}:${SCRIPT_DIR}\""
echo ""
echo "Or source the setup_env.sh script before running tests:"
echo "  source setup_env.sh"
echo ""
echo "Next steps:"
echo "1. Make sure virtual environment is activated: source venv/bin/activate"
echo "2. Source environment: source setup_env.sh (or run this script)"
echo "3. Run tests: pytest ui_tests/test_task_crud.py -v"
echo "   OR use: ./run_task_crud_test.sh"

