#!/bin/bash
# Test AI-Selected Alert Handling Mode
# This script tests that AI can find and select a similar task when an alert is received.

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
echo -e "${BLUE}  Testing AI-SELECTED Alert Handling Mode${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Target: $BASE_URL"
echo "Mode: AI-Selected (AI finds and selects best task)"
echo ""

ALERT_NAME="CPUPerformanceAlert"

echo -e "${YELLOW}📝 Prerequisites:${NC}"
echo "  1. Set mode to 'ai_selected' via UI: Settings → Alert Handling Mode"
echo "  2. Have a tooltask about CPU performance (NO trigger configured):"
echo "     • Title: 'CPU Performance Investigation'"
echo "     • Description: 'Investigate high CPU usage, analyze processes...'"
echo "     • Tags: cpu, performance"
echo "     • NO trigger_on_alerts configured"
echo ""
echo "  AI will search for similar tasks using KNN vector search."
echo ""
read -p "Press Enter to continue (or Ctrl+C to exit)..."
echo ""

# Step 1: Send alert about CPU issues (no deterministic match)
echo -e "${YELLOW}Step 1: Sending Grafana alert about CPU performance${NC}"
echo "  (Alert has NO deterministic match, AI must search for similar tasks)"
echo "  URL: ${BASE_URL}/processAlert${PROXY_PARAM}"
ALERT_RESPONSE=$(curl -s -X POST "${BASE_URL}/processAlert${PROXY_PARAM}" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d "{
        \"receiver\": \"AI_Test_Endpoint\",
        \"status\": \"firing\",
        \"alerts\": [{
            \"status\": \"firing\",
            \"labels\": {
                \"alertname\": \"${ALERT_NAME}\",
                \"grafana_folder\": \"production\",
                \"instance\": \"prod-server-03\",
                \"severity\": \"critical\"
            },
            \"annotations\": {
                \"description\": \"Server CPU utilization has reached 95% and is causing application performance degradation. Immediate investigation of resource consumption is needed.\",
                \"summary\": \"Critical CPU Usage Spike Detected\"
            },
            \"startsAt\": \"$(date -u +%s)\",
            \"fingerprint\": \"aitest$(date +%s)\"
        }],
        \"groupLabels\": {
            \"alertname\": \"${ALERT_NAME}\"
        },
        \"commonLabels\": {
            \"alertname\": \"${ALERT_NAME}\",
            \"severity\": \"critical\"
        },
        \"commonAnnotations\": {
            \"description\": \"Server CPU utilization has reached 95% and is causing application performance degradation. Immediate investigation of resource consumption is needed.\",
            \"summary\": \"Critical CPU Usage Spike Detected\"
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
TASKS_EXECUTED=$(echo "$ALERT_RESPONSE" | jq -r '.tasks_executed // 0')

echo "  Status: ${STATUS}"
echo "  Tasks Executed: ${TASKS_EXECUTED}"
echo ""

# Show results
if [ "$TASKS_EXECUTED" -ge 1 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✅ SUCCESS: Task(s) executed!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Executed tasks:"
    echo "$ALERT_RESPONSE" | jq -r '.executed_tasks[]? | "  • Task ID: \(.task_id)\n    Job ID: \(.job_id)\n    AI Selected: \(.ai_selected // false)\n    AI Confidence: \(.ai_confidence // "N/A")\n    AI Reasoning: \(.ai_reasoning // "N/A")"' 2>/dev/null || echo "  (Task executed successfully)"
    exit 0
else
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  ⚠ No tasks executed${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "This can happen if:"
    echo "  • No matching tasks are configured"
    echo "  • Mode is not set to 'ai_selected' in UI"
    echo "  • No similar tooltasks exist"
    echo "  • Alert doesn't match any task criteria"
    exit 0
fi

