#!/bin/bash
# Test All Alert Handling Modes
# Runs all three mode tests sequentially with comprehensive reporting.

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load environment
if [ -f "${SCRIPT_DIR}/.env" ]; then
    export $(grep -v '^#' "${SCRIPT_DIR}/.env" | xargs)
fi

BASE_URL="${DAGKNOWS_URL:-https://dev.dagknows.com}"
TOKEN="${DAGKNOWS_TOKEN:-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJ5YXNoQGRhZ2tub3dzLmNvbSIsIm5iZiI6MTc2MTE0NjUxMSwiZXhwIjoxNzkyNjgyNjkxLCJqdGkiOiJZMENWR055N01CQzlKYjNQIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoiYWRtaW4iLCJ1c2VyX2NsYWltcyI6eyJ1aWQiOiIzOSIsInVuYW1lIjoieWFzaEBkYWdrbm93cy5jb20iLCJvcmciOiJkYWdrbm93cyIsImZpcnN0X25hbWUiOiJZYXNoIiwibGFzdF9uYW1lIjoiWWFkYXYiLCJyb2xlIjoiQWRtaW4iLCJhZXNfa2V5IjoiY1Q0RTU2aWxDOTlVXG4tcTZ1dlRBcU15VTBwMEFcbnFJWSIsIm9mc3QiOlszNzIsMTUwLDM0Miw0MzEsMTg3LDM5MSwzOTAsMTc0LDIzMywyNzksMjQ2LDQzNiw5MSw0MjYsMjU3LDIxNiwxNzEsMzMzLDExOCwzNjMsMjc0LDE1MiwzNzEsNDM2LDEzNiwyMjAsMTI3LDY3LDQyNSwzNzMsNDM5LDMyMF19fQ.IvHXxMMm4th-jm7IyektCTW3SXxlq4olv6gByzAliuFk1y2zbr91QBY_zdifz5_KnYNk4ruVr9xLrlahC3h7rGJaFU98OiiiLAQ49CFxgUO2iqyr6XcT3GgO5ptobTtOZNV4rmrPE_6hnjPRImernp5M6FhHhCZWktL9xQqZs9N9m2az1Jk-mi0yZLaNIA25pHWcqgdiF1xCbt5STWqFG2nmt1eq7x-FXnoryEqo1HvfOg74crBcubFORpTZ5AhNRpSdqemcpDd_6t0UliPuAg3VlwIedew9RBRvytr2j9GbBC_jgCh7YJ5oQqFjVItolhSMzuKHLRRHZib8Ikz6fA}"

echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                    ║${NC}"
echo -e "${CYAN}║         DagKnows Alert Handling Modes - Complete Test Suite       ║${NC}"
echo -e "${CYAN}║                                                                    ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Target: $BASE_URL"
echo "Time: $(date)"
echo ""

# Track results
DETERMINISTIC_RESULT=""
AI_SELECTED_RESULT=""
AUTONOMOUS_RESULT=""

# Test 1: Deterministic Mode
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  TEST 1/3: DETERMINISTIC MODE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

if bash "${SCRIPT_DIR}/test_deterministic_mode.sh"; then
    DETERMINISTIC_RESULT="PASS"
    echo ""
else
    DETERMINISTIC_RESULT="FAIL"
    echo ""
fi

sleep 2

# Test 2: AI-Selected Mode
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  TEST 2/3: AI-SELECTED MODE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

if bash "${SCRIPT_DIR}/test_ai_selected_mode.sh"; then
    AI_SELECTED_RESULT="PASS"
    echo ""
else
    AI_SELECTED_RESULT="FAIL"
    echo ""
fi

sleep 2

# Test 3: Autonomous Mode
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  TEST 3/3: AUTONOMOUS MODE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

if bash "${SCRIPT_DIR}/test_autonomous_mode.sh"; then
    AUTONOMOUS_RESULT="PASS"
    echo ""
else
    AUTONOMOUS_RESULT="FAIL"
    echo ""
fi

# Summary Report
echo ""
echo -e "${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                      TEST SUMMARY REPORT                           ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Print results
echo "┌────────────────────────────────────┬──────────┐"
echo "│ Test                               │ Result   │"
echo "├────────────────────────────────────┼──────────┤"

if [ "$DETERMINISTIC_RESULT" = "PASS" ]; then
    echo -e "│ 1. Deterministic Mode              │ ${GREEN}✅ PASS${NC}  │"
else
    echo -e "│ 1. Deterministic Mode              │ ${RED}❌ FAIL${NC}  │"
fi

if [ "$AI_SELECTED_RESULT" = "PASS" ]; then
    echo -e "│ 2. AI-Selected Mode                │ ${GREEN}✅ PASS${NC}  │"
else
    echo -e "│ 2. AI-Selected Mode                │ ${RED}❌ FAIL${NC}  │"
fi

if [ "$AUTONOMOUS_RESULT" = "PASS" ]; then
    echo -e "│ 3. Autonomous Mode                 │ ${GREEN}✅ PASS${NC}  │"
else
    echo -e "│ 3. Autonomous Mode                 │ ${RED}❌ FAIL${NC}  │"
fi

echo "└────────────────────────────────────┴──────────┘"
echo ""

# Calculate pass rate
TOTAL=3
PASSED=0
[ "$DETERMINISTIC_RESULT" = "PASS" ] && PASSED=$((PASSED + 1))
[ "$AI_SELECTED_RESULT" = "PASS" ] && PASSED=$((PASSED + 1))
[ "$AUTONOMOUS_RESULT" = "PASS" ] && PASSED=$((PASSED + 1))

echo "Total: ${PASSED}/${TOTAL} tests passed"
echo ""

# Final verdict
if [ "$PASSED" -eq "$TOTAL" ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ ALL TESTS PASSED - Alert handling is working perfectly!       ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════╝${NC}"
    exit 0
elif [ "$PASSED" -gt 0 ]; then
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  ⚠️  PARTIAL SUCCESS - Some modes working, some need attention    ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ ALL TESTS FAILED - Alert handling needs investigation         ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi

