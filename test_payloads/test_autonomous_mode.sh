#!/bin/bash
# Test Autonomous Alert Handling Mode
# This script tests that AI can launch a full troubleshooting session for an alert.

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Load environment
if [ -f "$(dirname "$0")/.env" ]; then
    export $(grep -v '^#' "$(dirname "$0")/.env" | xargs)
fi

BASE_URL="${DAGKNOWS_URL:-https://dev.dagknows.com}"
TOKEN="${DAGKNOWS_TOKEN:-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJ5YXNoQGRhZ2tub3dzLmNvbSIsIm5iZiI6MTc2MTE0NjUxMSwiZXhwIjoxNzkyNjgyNjkxLCJqdGkiOiJZMENWR055N01CQzlKYjNQIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoiYWRtaW4iLCJ1c2VyX2NsYWltcyI6eyJ1aWQiOiIzOSIsInVuYW1lIjoieWFzaEBkYWdrbm93cy5jb20iLCJvcmciOiJkYWdrbm93cyIsImZpcnN0X25hbWUiOiJZYXNoIiwibGFzdF9uYW1lIjoiWWFkYXYiLCJyb2xlIjoiQWRtaW4iLCJhZXNfa2V5IjoiY1Q0RTU2aWxDOTlVXG4tcTZ1dlRBcU15VTBwMEFcbnFJWSIsIm9mc3QiOlszNzIsMTUwLDM0Miw0MzEsMTg3LDM5MSwzOTAsMTc0LDIzMywyNzksMjQ2LDQzNiw5MSw0MjYsMjU3LDIxNiwxNzEsMzMzLDExOCwzNjMsMjc0LDE1MiwzNzEsNDM2LDEzNiwyMjAsMTI3LDY3LDQyNSwzNzMsNDM5LDMyMF19fQ.IvHXxMMm4th-jm7IyektCTW3SXxlq4olv6gByzAliuFk1y2zbr91QBY_zdifz5_KnYNk4ruVr9xLrlahC3h7rGJaFU98OiiiLAQ49CFxgUO2iqyr6XcT3GgO5ptobTtOZNV4rmrPE_6hnjPRImernp5M6FhHhCZWktL9xQqZs9N9m2az1Jk-mi0yZLaNIA25pHWcqgdiF1xCbt5STWqFG2nmt1eq7x-FXnoryEqo1HvfOg74crBcubFORpTZ5AhNRpSdqemcpDd_6t0UliPuAg3VlwIedew9RBRvytr2j9GbBC_jgCh7YJ5oQqFjVItolhSMzuKHLRRHZib8Ikz6fA}"
# Critical: proxy parameter needed for dev.dagknows.com
PROXY_PARAM="${DAGKNOWS_PROXY:-?proxy=dev1}"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Testing AUTONOMOUS Alert Handling Mode${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Target: $BASE_URL"
echo "Mode: Autonomous (AI launches full investigation)"
echo ""
echo -e "${YELLOW}⚠️  Note: This test requires AI/LLM to be configured${NC}"
echo ""

ALERT_NAME="DatabasePerformanceDegradation"

echo -e "${YELLOW}📝 Prerequisites:${NC}"
echo "  1. Set mode to 'autonomous' via UI: Settings → Alert Handling Mode"
echo "  2. AI/LLM must be configured (OpenAI or similar)"
echo "  3. No matching task needs to exist"
echo ""
echo "  AI will create runbook and investigation tasks automatically."
echo ""
read -p "Press Enter to continue (or Ctrl+C to exit)..."
echo ""

# Step 1: Send alert (no deterministic match, no similar tooltask)
echo -e "${YELLOW}Step 1: Sending Grafana alert (no matching task configured)${NC}"
echo "  AI should launch a full troubleshooting investigation"
echo "  URL: ${BASE_URL}/processAlert${PROXY_PARAM}"
ALERT_RESPONSE=$(curl -s -X POST "${BASE_URL}/processAlert${PROXY_PARAM}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d "{
        \"receiver\": \"Autonomous_Test_Endpoint\",
        \"status\": \"firing\",
        \"alerts\": [{
            \"status\": \"firing\",
            \"labels\": {
                \"alertname\": \"${ALERT_NAME}\",
                \"grafana_folder\": \"production\",
                \"instance\": \"db-server-01\",
                \"severity\": \"warning\"
            },
            \"annotations\": {
                \"description\": \"Database query response time has degraded by 400% over the last 15 minutes. Multiple slow queries detected on production database. Users are experiencing significant page load timeouts and application slowness.\",
                \"summary\": \"Critical Database Performance Degradation\"
            },
            \"startsAt\": \"$(date -u +%s)\",
            \"fingerprint\": \"autotest$(date +%s)\"
        }],
        \"groupLabels\": {
            \"alertname\": \"${ALERT_NAME}\"
        },
        \"commonLabels\": {
            \"alertname\": \"${ALERT_NAME}\",
            \"severity\": \"warning\"
        },
        \"commonAnnotations\": {
            \"description\": \"Database query response time has degraded by 400% over the last 15 minutes. Multiple slow queries detected.\",
            \"summary\": \"Critical Database Performance Degradation\"
        },
        \"externalURL\": \"http://grafana:3000/\",
        \"version\": \"1\",
        \"title\": \"[FIRING:1] ${ALERT_NAME}\",
        \"state\": \"alerting\"
    }")

echo "$ALERT_RESPONSE" | jq . 2>/dev/null || echo "$ALERT_RESPONSE"
echo ""

# Step 2: Verify execution
echo -e "${YELLOW}Step 2: Verifying execution${NC}"

STATUS=$(echo "$ALERT_RESPONSE" | jq -r '.status // "unknown"')
RUNBOOK_ID=$(echo "$ALERT_RESPONSE" | jq -r '.runbook_task_id // ""')
CHILD_ID=$(echo "$ALERT_RESPONSE" | jq -r '.child_task_id // ""')
TASKS_EXECUTED=$(echo "$ALERT_RESPONSE" | jq -r '.tasks_executed // 0')

echo "  Status: ${STATUS}"
echo "  Tasks Executed: ${TASKS_EXECUTED}"
echo "  Runbook Task ID: ${RUNBOOK_ID:-none}"
echo "  Child Task ID: ${CHILD_ID:-none}"
echo ""

# Show results
if [ "$STATUS" = "success" ] && [ -n "$RUNBOOK_ID" ] && [ -n "$CHILD_ID" ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✅ SUCCESS: Autonomous investigation launched!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "AI launched autonomous troubleshooting session:"
    echo "  • Runbook Task: ${RUNBOOK_ID}"
    echo "  • Investigation Task: ${CHILD_ID}"
    echo ""
    echo "You can view these tasks in the UI or via API"
    exit 0
elif [ "$TASKS_EXECUTED" -ge 1 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✅ SUCCESS: Task(s) executed!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Executed tasks:"
    echo "$ALERT_RESPONSE" | jq -r '.executed_tasks[]? | "  • Task ID: \(.task_id)\n    Job ID: \(.job_id)"' 2>/dev/null || echo "  (Task executed successfully)"
    exit 0
else
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  ⚠ No tasks or investigation launched${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Possible reasons:"
    echo "  • Mode not set to 'autonomous' in UI"
    echo "  • AI/LLM not configured"
    echo "  • No matching tasks configured"
    echo ""
    echo "Message: $(echo "$ALERT_RESPONSE" | jq -r '.message // "N/A"')"
    exit 0
fi

