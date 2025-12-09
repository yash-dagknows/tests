#!/bin/bash
# Setup script for E2E tests
# Ensures all required files are in place

set -e

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

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure virtual environment is activated: source venv/bin/activate"
echo "2. Run tests: pytest ui_tests/test_ai_agent_workflow.py -v"
echo "   OR use: ./run_ai_agent_test.sh --headed"

