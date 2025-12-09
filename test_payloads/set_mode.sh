#!/bin/bash
# Set Incident Response Mode
# Usage: ./set_mode.sh [deterministic|ai_selected|autonomous]

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Load environment
if [ -f "$(dirname "$0")/.env" ]; then
    export $(grep -v '^#' "$(dirname "$0")/.env" | xargs)
fi

BASE_URL="${DAGKNOWS_URL:-https://dev.dagknows.com}"
TOKEN="${DAGKNOWS_TOKEN:-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJ5YXNoQGRhZ2tub3dzLmNvbSIsIm5iZiI6MTc2MTE0NjUxMSwiZXhwIjoxNzkyNjgyNjkxLCJqdGkiOiJZMENWR055N01CQzlKYjNQIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoiYWRtaW4iLCJ1c2VyX2NsYWltcyI6eyJ1aWQiOiIzOSIsInVuYW1lIjoieWFzaEBkYWdrbm93cy5jb20iLCJvcmciOiJkYWdrbm93cyIsImZpcnN0X25hbWUiOiJZYXNoIiwibGFzdF9uYW1lIjoiWWFkYXYiLCJyb2xlIjoiQWRtaW4iLCJhZXNfa2V5IjoiY1Q0RTU2aWxDOTlVXG4tcTZ1dlRBcU15VTBwMEFcbnFJWSIsIm9mc3QiOlszNzIsMTUwLDM0Miw0MzEsMTg3LDM5MSwzOTAsMTc0LDIzMywyNzksMjQ2LDQzNiw5MSw0MjYsMjU3LDIxNiwxNzEsMzMzLDExOCwzNjMsMjc0LDE1MiwzNzEsNDM2LDEzNiwyMjAsMTI3LDY3LDQyNSwzNzMsNDM5LDMyMF19fQ.IvHXxMMm4th-jm7IyektCTW3SXxlq4olv6gByzAliuFk1y2zbr91QBY_zdifz5_KnYNk4ruVr9xLrlahC3h7rGJaFU98OiiiLAQ49CFxgUO2iqyr6XcT3GgO5ptobTtOZNV4rmrPE_6hnjPRImernp5M6FhHhCZWktL9xQqZs9N9m2az1Jk-mi0yZLaNIA25pHWcqgdiF1xCbt5STWqFG2nmt1eq7x-FXnoryEqo1HvfOg74crBcubFORpTZ5AhNRpSdqemcpDd_6t0UliPuAg3VlwIedew9RBRvytr2j9GbBC_jgCh7YJ5oQqFjVItolhSMzuKHLRRHZib8Ikz6fA}"

# Get mode from argument
MODE="$1"

if [ -z "$MODE" ]; then
    echo "Usage: $0 [deterministic|ai_selected|autonomous]"
    echo ""
    echo "Modes:"
    echo "  deterministic - Tasks execute based on trigger_on_alerts configuration"
    echo "  ai_selected   - AI searches for and selects similar tooltasks"
    echo "  autonomous    - AI launches full troubleshooting investigation"
    exit 1
fi

# Validate mode
if [ "$MODE" != "deterministic" ] && [ "$MODE" != "ai_selected" ] && [ "$MODE" != "autonomous" ]; then
    echo -e "${RED}❌ Invalid mode: ${MODE}${NC}"
    echo "Valid modes: deterministic, ai_selected, autonomous"
    exit 1
fi

echo "Setting incident_response_mode to: ${MODE}"

# Set mode
RESPONSE=$(curl -s -X POST "${BASE_URL}/setFlags" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d "{\"incident_response_mode\": \"${MODE}\"}")

STATUS=$(echo "$RESPONSE" | jq -r '.responsecode // "unknown"')

if [ "$STATUS" = "True" ]; then
    echo -e "${GREEN}✓ Mode set successfully to: ${MODE}${NC}"
    echo "$RESPONSE" | jq '.admin_settings.incident_response_mode // empty' 2>/dev/null
    exit 0
else
    echo -e "${RED}✗ Failed to set mode${NC}"
    echo "Response: $(echo "$RESPONSE" | jq -r '.msg // "Unknown error"')"
    echo ""
    echo "Possible issues:"
    echo "  • Token doesn't have admin permissions"
    echo "  • URL is incorrect"
    echo "  • Service is down"
    exit 1
fi

