#!/bin/bash
# Quick fix for ModuleNotFoundError
# Copy-paste this entire block into your terminal!

cd /home/ubuntu/tests/e2e_tests

echo "Creating required __init__.py files..."

# Create all __init__.py files
touch __init__.py
touch config/__init__.py
touch fixtures/__init__.py
touch pages/__init__.py
touch api_tests/__init__.py
touch ui_tests/__init__.py
touch utils/__init__.py

# Create reports directory
mkdir -p reports/screenshots

echo "✓ All files created"
echo ""
echo "Now run tests:"
echo "  source venv/bin/activate"
echo "  pytest ui_tests/test_ai_agent_workflow.py -v"
echo ""
echo "Or use the test runner:"
echo "  ./run_ai_agent_test.sh --headed"

