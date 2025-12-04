#!/bin/bash
# Script to run tests in CI environment
# This can be called from Jenkins, GitHub Actions, or other CI systems

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}DagKnows Test Suite - CI Execution${NC}"
echo -e "${GREEN}=====================================${NC}"

# Change to tests directory
cd "$(dirname "$0")/.."
echo -e "\n${YELLOW}Working directory: $(pwd)${NC}"

# Parse command line arguments
TEST_SUITE="${1:-all}"
RUN_COVERAGE="${2:-true}"

echo -e "\n${YELLOW}Configuration:${NC}"
echo "  Test Suite: $TEST_SUITE"
echo "  Coverage: $RUN_COVERAGE"

# Setup Python environment
echo -e "\n${YELLOW}Setting up Python environment...${NC}"
python3 -m venv venv || true
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p results logs

# Setup environment file
if [ ! -f .env.test ]; then
    echo -e "${YELLOW}Creating .env.test from example...${NC}"
    cp .env.test.example .env.test
fi

# Start services
echo -e "\n${YELLOW}Starting test services...${NC}"
docker-compose -f docker-compose-test.yml up -d

# Wait for services
echo -e "\n${YELLOW}Waiting for services to be ready...${NC}"
./utils/wait-for-services.sh

# Build pytest command
PYTEST_CMD="pytest -v --color=yes --junitxml=results/junit.xml --html=results/report.html --self-contained-html"

# Add coverage if requested
if [ "$RUN_COVERAGE" = "true" ]; then
    echo -e "${YELLOW}Coverage reporting enabled${NC}"
    PYTEST_CMD="$PYTEST_CMD --cov=../taskservice/src --cov=../req_router/src --cov-report=xml:results/coverage.xml --cov-report=html:results/htmlcov --cov-report=term-missing"
fi

# Select test suite
case "$TEST_SUITE" in
    unit)
        echo -e "\n${GREEN}Running unit tests...${NC}"
        PYTEST_CMD="$PYTEST_CMD unit/"
        ;;
    integration)
        echo -e "\n${GREEN}Running integration tests...${NC}"
        PYTEST_CMD="$PYTEST_CMD integration/"
        ;;
    e2e)
        echo -e "\n${GREEN}Running E2E tests...${NC}"
        PYTEST_CMD="$PYTEST_CMD e2e/"
        ;;
    smoke)
        echo -e "\n${GREEN}Running smoke tests...${NC}"
        PYTEST_CMD="$PYTEST_CMD -m smoke"
        ;;
    all)
        echo -e "\n${GREEN}Running all tests...${NC}"
        ;;
    *)
        echo -e "${RED}Unknown test suite: $TEST_SUITE${NC}"
        echo "Valid options: unit, integration, e2e, smoke, all"
        exit 1
        ;;
esac

# Run tests
echo -e "\n${GREEN}Executing tests...${NC}"
echo "Command: $PYTEST_CMD"
set +e  # Don't exit on test failures
$PYTEST_CMD
TEST_EXIT_CODE=$?
set -e

# Stop services
echo -e "\n${YELLOW}Stopping test services...${NC}"
docker-compose -f docker-compose-test.yml down -v

# Report results
echo -e "\n${GREEN}=====================================${NC}"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Tests PASSED${NC}"
else
    echo -e "${RED}✗ Tests FAILED${NC}"
fi
echo -e "${GREEN}=====================================${NC}"

# Generate summary
if [ -f results/junit.xml ]; then
    echo -e "\n${YELLOW}Test Summary:${NC}"
    python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('results/junit.xml')
root = tree.getroot()
tests = int(root.attrib.get('tests', 0))
failures = int(root.attrib.get('failures', 0))
errors = int(root.attrib.get('errors', 0))
skipped = int(root.attrib.get('skipped', 0))
passed = tests - failures - errors - skipped
print(f'  Total: {tests}')
print(f'  Passed: {passed}')
print(f'  Failed: {failures}')
print(f'  Errors: {errors}')
print(f'  Skipped: {skipped}')
" || echo "  (Summary not available)"
fi

# Show coverage summary if available
if [ "$RUN_COVERAGE" = "true" ] && [ -f results/coverage.xml ]; then
    echo -e "\n${YELLOW}Coverage Summary:${NC}"
    echo "  Report: results/htmlcov/index.html"
fi

echo -e "\n${YELLOW}Reports available at:${NC}"
echo "  JUnit: results/junit.xml"
echo "  HTML: results/report.html"
if [ "$RUN_COVERAGE" = "true" ]; then
    echo "  Coverage: results/coverage.xml"
    echo "  Coverage HTML: results/htmlcov/index.html"
fi

exit $TEST_EXIT_CODE

