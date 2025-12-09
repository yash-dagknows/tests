#!/bin/bash
# Run AI Agent Workflow E2E Test
# 
# Usage:
#   ./run_ai_agent_test.sh              # Run with default options
#   ./run_ai_agent_test.sh --headed     # Run with visible browser
#   ./run_ai_agent_test.sh --local      # Run against localhost

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  AI Agent Workflow E2E Test Runner${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found${NC}"
    echo "Creating from template..."
    cp env.template .env
    echo -e "${YELLOW}Please edit .env file with your credentials${NC}"
    exit 1
fi

# Load .env
source .env 2>/dev/null || true

# Check configuration
echo "Configuration:"
echo "  URL: ${DAGKNOWS_URL}"
echo "  User: ${TEST_USER_EMAIL}"
echo

# Parse arguments
PYTEST_ARGS=""
TEST_NAME="test_complete_ai_agent_workflow"

while [[ $# -gt 0 ]]; do
    case $1 in
        --headed)
            PYTEST_ARGS="$PYTEST_ARGS --headed"
            shift
            ;;
        --slow)
            PYTEST_ARGS="$PYTEST_ARGS --headed --slowmo=1000"
            shift
            ;;
        --local)
            export DAGKNOWS_URL="http://localhost"
            export DAGKNOWS_PROXY="?proxy=yashlocal"
            echo -e "${YELLOW}→ Running against localhost with proxy=yashlocal${NC}"
            shift
            ;;
        --fast)
            TEST_NAME="test_ai_agent_direct_navigation"
            echo -e "${YELLOW}→ Running fast variant (direct navigation)${NC}"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if dependencies installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}✗ pytest not found${NC}"
    echo "Install dependencies: pip install -r requirements.txt"
    exit 1
fi

# Check if playwright installed
if ! python -c "import playwright" 2>/dev/null; then
    echo -e "${RED}✗ playwright not found${NC}"
    echo "Install: pip install -r requirements.txt && playwright install chromium"
    exit 1
fi

# Create reports directory
mkdir -p reports/screenshots

# Run test
echo -e "${GREEN}Running AI Agent Workflow Test...${NC}"
echo

pytest \
    ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::${TEST_NAME} \
    -v \
    $PYTEST_ARGS \
    --html=reports/ai_agent_test_report.html \
    --self-contained-html

EXIT_CODE=$?

echo
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✅ TEST PASSED${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo
    echo "📊 HTML Report: reports/ai_agent_test_report.html"
    echo "📸 Screenshots: reports/screenshots/"
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  ✗ TEST FAILED${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo
    echo "📸 Check screenshots: reports/screenshots/"
    echo "📊 HTML Report: reports/ai_agent_test_report.html"
fi

exit $EXIT_CODE

