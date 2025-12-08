#!/bin/bash
# Script to run tests against remote DagKnows deployment
# Usage: ./run_remote_tests.sh [pytest args]
# Example: ./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v

# Load environment variables from .env.local if it exists
if [ -f ".env.local" ]; then
    echo "Loading environment from .env.local..."
    export $(grep -v '^#' .env.local | xargs)
fi

# Set defaults if not already set
: ${DAGKNOWS_URL:="https://44.224.1.45"}

# Check if DAGKNOWS_TOKEN is set
if [ -z "$DAGKNOWS_TOKEN" ]; then
    echo "❌ Error: DAGKNOWS_TOKEN environment variable is not set"
    echo "Please set it in .env.local or export it:"
    echo "  export DAGKNOWS_TOKEN='your-token-here'"
    exit 1
fi

echo "🌐 Testing against: $DAGKNOWS_URL"
echo "👤 User: ironman@avengers.com (Supremo)"
echo "🔑 Token: ${DAGKNOWS_TOKEN:0:50}..." # Show first 50 chars
echo "---"

# Run pytest with all provided arguments
python -m pytest "$@"

