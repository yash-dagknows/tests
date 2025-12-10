#!/bin/bash
# run_role_management_test.sh
# Helper script to run E2E UI test for Role Management (RBAC)

# Get script directory and source environment setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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

# --- Configuration ---
TEST_FILE="ui_tests/test_role_management.py"
TEST_FUNCTION="::TestRoleManagementE2E::test_create_role_and_assign_privileges"
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
    echo "  --headed    Run test in headed browser mode (visible UI)."
    echo "  --slow      Run test in slow motion (1000ms delay)."
    echo "  --local     Run test against local Docker setup."
    echo "  --help      Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 --headed --slow"
    echo "  $0 --local"
}

# --- Argument Parsing ---
for arg in "$@"; do
    case $arg in
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
# PYTHONPATH is already set by setup_env.sh above, but ensure it's set
if [[ ":$PYTHONPATH:" != *":$(pwd):"* ]]; then
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
fi

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
echo "  Role Management E2E Test Runner"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -n "$HEADED_MODE" ]; then
    echo "Headed Mode: Enabled"
fi
if [ -n "$SLOW_MO_DELAY" ]; then
    echo "Slow-mo: $(echo "$SLOW_MO_DELAY" | awk '{print $2}')ms"
fi
echo ""
echo "Starting test..."
echo "Command: pytest ${TEST_FILE}${TEST_FUNCTION} -v ${HEADED_MODE} ${SLOW_MO_DELAY}"
echo ""

pytest "${TEST_FILE}${TEST_FUNCTION}" -v ${HEADED_MODE} ${SLOW_MO_DELAY}

