#!/bin/bash
# Quick runner for Alert Handling E2E Tests

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Alert Handling E2E Tests Runner${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Source environment setup (creates __init__.py files and sets PYTHONPATH)
if [ -f "setup_env.sh" ]; then
    source setup_env.sh
else
    # Fallback: manual setup
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    touch __init__.py config/__init__.py fixtures/__init__.py pages/__init__.py \
          api_tests/__init__.py ui_tests/__init__.py utils/__init__.py 2>/dev/null || true
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment not found${NC}"
    echo "Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate venv
source venv/bin/activate

# PYTHONPATH is already set by setup_env.sh above, but ensure it's set
if [[ ":$PYTHONPATH:" != *":$(pwd):"* ]]; then
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
fi

# Parse arguments
TEST_MODE="all"
HEADED=false
SLOW_MO=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --deterministic)
            TEST_MODE="deterministic"
            shift
            ;;
        --ai-selected)
            TEST_MODE="ai_selected"
            shift
            ;;
        --autonomous)
            TEST_MODE="autonomous"
            shift
            ;;
        --headed)
            HEADED=true
            shift
            ;;
        --slow)
            SLOW_MO=1000
            shift
            ;;
        --fast)
            SLOW_MO=0
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--deterministic|--ai-selected|--autonomous] [--headed] [--slow|--fast]"
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="pytest ui_tests/test_alert_handling_modes.py -v"

# Add specific test if requested
if [ "$TEST_MODE" == "deterministic" ]; then
    PYTEST_CMD="pytest ui_tests/test_alert_handling_modes.py::TestAlertHandlingModesE2E::test_deterministic_mode_alert_handling -v"
    echo -e "${YELLOW}Running: Deterministic Mode Test${NC}"
elif [ "$TEST_MODE" == "ai_selected" ]; then
    PYTEST_CMD="pytest ui_tests/test_alert_handling_modes.py::TestAlertHandlingModesE2E::test_ai_selected_mode_alert_handling -v"
    echo -e "${YELLOW}Running: AI-Selected Mode Test${NC}"
elif [ "$TEST_MODE" == "autonomous" ]; then
    PYTEST_CMD="pytest ui_tests/test_alert_handling_modes.py::TestAlertHandlingModesE2E::test_autonomous_mode_alert_handling -v"
    echo -e "${YELLOW}Running: Autonomous Mode Test${NC}"
else
    echo -e "${YELLOW}Running: All Alert Handling Tests${NC}"
fi

# Add headed mode if requested
if [ "$HEADED" == true ]; then
    PYTEST_CMD="$PYTEST_CMD --headed"
    echo -e "${YELLOW}Mode: Headed (visible browser)${NC}"
fi

# Add slow-mo if requested
if [ "$SLOW_MO" -gt 0 ]; then
    PYTEST_CMD="$PYTEST_CMD --slowmo $SLOW_MO"
    echo -e "${YELLOW}Slow-mo: ${SLOW_MO}ms${NC}"
fi

echo

# Run tests
echo -e "${GREEN}Starting tests...${NC}"
echo -e "${BLUE}Command: $PYTEST_CMD${NC}"
echo

$PYTEST_CMD

# Show results
echo
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Tests completed!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo "📸 Screenshots saved in: reports/screenshots/"
echo "📄 HTML report: reports/report.html"
echo

# Show deterministic screenshots if that test ran
if [ "$TEST_MODE" == "deterministic" ] || [ "$TEST_MODE" == "all" ]; then
    echo "📸 Deterministic test screenshots:"
    ls -1 reports/screenshots/ | grep "deterministic" || echo "  (no deterministic screenshots found)"
    echo
fi

