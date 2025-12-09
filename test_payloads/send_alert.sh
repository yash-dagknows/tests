#!/bin/bash
# Send Alert Payload to DagKnows
# Usage: ./send_alert.sh <payload_file.json>

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
# Critical: proxy parameter needed for dev.dagknows.com
PROXY_PARAM="${DAGKNOWS_PROXY:-?proxy=dev1}"

# Get payload file
PAYLOAD_FILE="$1"

if [ -z "$PAYLOAD_FILE" ]; then
    echo "Usage: $0 <payload_file.json>"
    echo ""
    echo "Available payloads:"
    ls -1 "$(dirname "$0")"/*.json 2>/dev/null | xargs -n1 basename
    exit 1
fi

# Check if file exists
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -f "${SCRIPT_DIR}/${PAYLOAD_FILE}" ] && [ ! -f "${PAYLOAD_FILE}" ]; then
    echo -e "${RED}❌ Payload file not found: ${PAYLOAD_FILE}${NC}"
    exit 1
fi

# Use full path if relative
if [ -f "${SCRIPT_DIR}/${PAYLOAD_FILE}" ]; then
    PAYLOAD_FILE="${SCRIPT_DIR}/${PAYLOAD_FILE}"
fi

echo "Sending alert to: ${BASE_URL}/processAlert${PROXY_PARAM}"
echo "Payload file: $(basename "$PAYLOAD_FILE")"
echo ""

# Send alert
RESPONSE=$(curl -s -X POST "${BASE_URL}/processAlert${PROXY_PARAM}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d @"${PAYLOAD_FILE}")

# Parse response
STATUS=$(echo "$RESPONSE" | jq -r '.status // "unknown"')
TASKS_EXECUTED=$(echo "$RESPONSE" | jq -r '.tasks_executed // 0')
MODE=$(echo "$RESPONSE" | jq -r '.incident_response_mode // "unknown"')
ALERT_SOURCE=$(echo "$RESPONSE" | jq -r '.alert_source // "unknown"')
ALERT_NAME=$(echo "$RESPONSE" | jq -r '.alert_name // "unknown"')

# Display response
echo -e "${YELLOW}Response:${NC}"
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
echo ""

# Summary
echo -e "${YELLOW}Summary:${NC}"
echo "  Status: ${STATUS}"
echo "  Mode: ${MODE}"
echo "  Alert Source: ${ALERT_SOURCE}"
echo "  Alert Name: ${ALERT_NAME}"
echo "  Tasks Executed: ${TASKS_EXECUTED}"
echo ""

if [ "$TASKS_EXECUTED" -ge 1 ]; then
    echo -e "${GREEN}✅ Alert processed and task(s) executed!${NC}"
    exit 0
elif [ "$STATUS" = "success" ]; then
    echo -e "${YELLOW}⚠️  Alert processed but no tasks executed${NC}"
    echo "This is expected if no matching tasks are configured"
    exit 0
else
    echo -e "${RED}❌ Alert processing failed${NC}"
    exit 1
fi

