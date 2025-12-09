#!/bin/bash
# run_task_crud_test.sh
# Helper script to run E2E UI tests for Task CRUD Operations

# --- Configuration ---
TEST_FILE="ui_tests/test_task_crud.py"
DEFAULT_TEST_FUNCTION="" # Run all tests in the file by default
HEADED_MODE=""
SLOW_MO_DELAY=""
LOCAL_MODE="" # Flag to indicate local Docker environment
BASE_URL_LOCAL="http://localhost:8000"
PROXY_PARAM_LOCAL="?proxy=yashlocal"
JWT_TOKEN_LOCAL="your_local_jwt_token_here" # Placeholder for local JWT
BASE_URL_DEV="https://dev.dagknows.com"
PROXY_PARAM_DEV="?proxy=dev1"
JWT_TOKEN_DEV="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJ5YXNoQGRhZ2tub3dzLmNvbSIsIm5iZiI6MTc2MTE0NjUxMSwiZXhwIjoxNzkyNjgyNjkxLCJqdGkiOiJZMENWR055N01CQzlKYjNQIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoiYWRtaW4iLCJ1c2VyX2NsYWltcyI6eyJ1aWQiOiIzOSIsInVuYW1lIjoiY29udGFjdEBkYWdrbm93cy5jb20iLCJvcmciOiJkYWdrbm93cyIsImZpcnN0X25hbWUiOiJZYXNoIiwibGFzdF9uYW1lIjoiWWFkYXYiLCJyb2xlIjoiQWRtaW4iLCJhZXNfa2V5IjoiY1Q0RTU2aWxDOTlVXG4tcTZ1dlRBcU15VTBwMEFcbnFJWSIsIm9mc3QiOlszNzIsMTUwLDM0Miw0MzEsMTg3LDM5MSwzOTAsMTc0LDIzMywyNzksMjQ2LDQzNiw5MSw0MjYsMjU3LDIxNiwxNzEsMzMzLDExOCwzNjMsMjc0LDE1MiwzNzEsNDM2LDEzNiwyMjAsMTI3LDY3LDQyNSwzNzMsNDM5LDMyMF19fQ.IvHXxMMm4th-jm7IyektCTW3SXxl4olv6gByzAliuFk1y2zbr91QBY_zdifz5_KnYNk4ruVr9xLrlahC3h7rGJaFU98OiiiLAQ49CFxgUO2iqyr6XcT3GgO5ptobTtOZNV4rmrPE_6hnjPRImernp5M6FhHhCZWktL9xQqZs9N9m2az1Jk-mi0yZLaNIA25pHWcqGdiF1xCbt5STWqFG2nmt1eq7x-FXnoryEqo1HvfOg74crBcubFORpTZ5AhNRpSdqemcpDd_6t0UliPuAg3VlwIedew9RBRvytr2j9GbBC_jgCh7YJ5oQqFjVItolhSMzuKHLRRHZib8Ikz6fA" # Hardcoded dev JWT

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "OPTIONS:"
    echo "  --create-from-form  Run only the create from form test."
    echo "  --minimal           Run only the minimal task creation test."
    echo "  --headed            Run tests in headed browser mode (visible UI)."
    echo "  --slow              Run tests in slow motion (1000ms delay)."
    echo "  --local             Run tests against local Docker setup."
    echo "  --help              Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --create-from-form --headed"
    echo "  $0 --minimal --slow"
    echo "  $0 --local"
}

# --- Argument Parsing ---
for arg in "$@"; do
    case $arg in
        --create-from-form)
            TEST_FUNCTION="::TestTaskCRUDE2E::test_create_task_from_form"
            shift
            ;;
        --minimal)
            TEST_FUNCTION="::TestTaskCRUDE2E::test_create_task_with_minimal_data"
            shift
            ;;
        --headed)
            HEADED_MODE="--headed"
            shift
            ;;
        --slow)
            SLOW_MO_DELAY="--slowmo 1000"
            shift
            ;;
        --local)
            LOCAL_MODE="true"
            shift
            ;;
        --help)
            print_help
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            print_help
            exit 1
            ;;
    esac
done

# --- Environment Setup ---
# Set PYTHONPATH to include the current directory for module imports
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Set environment variables based on mode
if [ "$LOCAL_MODE" == "true" ]; then
    export DAGKNOWS_URL="$BASE_URL_LOCAL"
    export DAGKNOWS_PROXY="$PROXY_PARAM_LOCAL"
    export DAGKNOWS_TOKEN="$JWT_TOKEN_LOCAL"
    echo "Running: Local Docker Mode"
else
    export DAGKNOWS_URL="$BASE_URL_DEV"
    export DAGKNOWS_PROXY="$PROXY_PARAM_DEV"
    export DAGKNOWS_TOKEN="$JWT_TOKEN_DEV"
    echo "Running: dev.dagknows.com Mode"
fi

# --- Execution ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Task CRUD E2E Tests Runner"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -n "$TEST_FUNCTION" ]; then
    TEST_NAME=$(echo "$TEST_FUNCTION" | sed 's/.*:://g' | sed 's/_/ /g' | sed 's/test //g')
    echo "Running: ${TEST_NAME^} Test"
else
    echo "Running: All Task CRUD Tests"
fi

if [ -n "$HEADED_MODE" ]; then
    echo "Headed Mode: Enabled"
fi
if [ -n "$SLOW_MO_DELAY" ]; then
    echo "Slow-mo: $(echo "$SLOW_MO_DELAY" | awk '{print $2}')ms"
fi
echo ""
echo "Starting tests..."
echo "Command: pytest ${TEST_FILE}${TEST_FUNCTION} -v ${HEADED_MODE} ${SLOW_MO_DELAY}"
echo ""

pytest "${TEST_FILE}${TEST_FUNCTION}" -v ${HEADED_MODE} ${SLOW_MO_DELAY}

# --- Post-execution ---
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Tests completed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📸 Screenshots saved in: reports/screenshots/"
echo "📄 HTML report: reports/report.html"
echo ""

