#!/bin/bash

# E2E API Test Runner: Task CRUD Operations
# This script runs the API-based E2E test for task creation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Source environment setup
if [ -f "setup_env.sh" ]; then
    source setup_env.sh
fi

# Default values
HEADED=false
SLOWMO=0
LOCAL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --headed)
            HEADED=true
            shift
            ;;
        --slow)
            SLOWMO=1000
            shift
            ;;
        --local)
            LOCAL=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--headed] [--slow] [--local]"
            exit 1
            ;;
    esac
done

# Set environment variables
if [ "$LOCAL" = true ]; then
    export DAGKNOWS_URL="${DAGKNOWS_URL:-http://localhost:3000}"
    export DAGKNOWS_PROXY="${DAGKNOWS_PROXY:-?proxy=yashlocal}"
    export JWT_TOKEN="${JWT_TOKEN:-your_local_jwt_token_here}"
    echo "Running: Local Docker Mode"
else
    export DAGKNOWS_URL="${DAGKNOWS_URL:-https://dev.dagknows.com}"
    export DAGKNOWS_PROXY="${DAGKNOWS_PROXY:-?proxy=dev1}"
    export JWT_TOKEN="${JWT_TOKEN:-your_dev_jwt_token_here}"
    echo "Running: dev.dagknows.com Mode"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Task CRUD API E2E Test Runner"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Starting test..."
echo "Command: pytest api_tests/test_task_crud_api.py::TestTaskCRUDE2E::test_task_full_lifecycle_via_api -v"

pytest api_tests/test_task_crud_api.py::TestTaskCRUDE2E::test_task_full_lifecycle_via_api -v

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Test completed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

