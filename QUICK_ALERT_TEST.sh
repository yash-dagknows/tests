#!/bin/bash
# Quick Alert Deterministic Mapping Test
# Usage: ./QUICK_ALERT_TEST.sh

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="${DAGKNOWS_URL:-https://44.224.1.45}"
TOKEN="${DAGKNOWS_TOKEN}"

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Error: DAGKNOWS_TOKEN not set${NC}"
    echo "Please set: export DAGKNOWS_TOKEN='your-token'"
    exit 1
fi

echo -e "${YELLOW}Testing Deterministic Alert Mapping${NC}"
echo "Target: $BASE_URL"
echo "---"

# Generate unique alert name
TIMESTAMP=$(date +%s)
ALERT_NAME="TestAlert${TIMESTAMP}"

# Step 1: Create task with alert trigger
echo -e "${YELLOW}Step 1: Creating task with alert trigger...${NC}"
TASK_RESPONSE=$(curl -s -X POST ${BASE_URL}/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d "{
    \"task\": {
      \"title\": \"Alert Handler ${TIMESTAMP}\",
      \"description\": \"Handles ${ALERT_NAME}\",
      \"script_type\": \"python\",
      \"script\": \"print('Alert ${ALERT_NAME} handled!')\",
      \"trigger_on_alerts\": [
        {
          \"alert_source\": \"Grafana\",
          \"alert_name\": \"${ALERT_NAME}\",
          \"dedup_interval\": 300
        }
      ]
    }
  }")

TASK_ID=$(echo $TASK_RESPONSE | jq -r '.task.id')

if [ -z "$TASK_ID" ] || [ "$TASK_ID" = "null" ]; then
    echo -e "${RED}✗ Failed to create task${NC}"
    echo "Response: $TASK_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✓ Created task: $TASK_ID${NC}"
echo "  Alert Source: Grafana"
echo "  Alert Name: $ALERT_NAME"
echo ""

# Step 2: Send matching alert
echo -e "${YELLOW}Step 2: Sending matching alert...${NC}"
ALERT_RESPONSE=$(curl -s -X POST ${BASE_URL}/processAlert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d "{
    \"receiver\": \"Test_Endpoint\",
    \"status\": \"firing\",
    \"alerts\": [{
      \"status\": \"firing\",
      \"labels\": {
        \"alertname\": \"${ALERT_NAME}\",
        \"grafana_folder\": \"test\",
        \"severity\": \"critical\"
      },
      \"annotations\": {
        \"description\": \"Test alert for deterministic mapping\",
        \"summary\": \"Testing Alert ${ALERT_NAME}\"
      },
      \"startsAt\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
      \"fingerprint\": \"test${TIMESTAMP}\"
    }],
    \"groupLabels\": {
      \"alertname\": \"${ALERT_NAME}\"
    },
    \"commonLabels\": {
      \"alertname\": \"${ALERT_NAME}\",
      \"severity\": \"critical\"
    },
    \"commonAnnotations\": {
      \"description\": \"Test alert for deterministic mapping\",
      \"summary\": \"Testing Alert ${ALERT_NAME}\"
    },
    \"externalURL\": \"http://grafana:3000/\",
    \"version\": \"1\",
    \"title\": \"[FIRING:1] ${ALERT_NAME}\",
    \"state\": \"alerting\"
  }")

echo "$ALERT_RESPONSE" | jq . 2>/dev/null || echo "$ALERT_RESPONSE"
echo ""

# Step 3: Verify execution
echo -e "${YELLOW}Step 3: Verifying task execution...${NC}"

STATUS=$(echo $ALERT_RESPONSE | jq -r '.status')
TASKS_EXECUTED=$(echo $ALERT_RESPONSE | jq -r '.tasks_executed // 0')
MODE=$(echo $ALERT_RESPONSE | jq -r '.incident_response_mode // "unknown"')

echo "  Status: $STATUS"
echo "  Tasks Executed: $TASKS_EXECUTED"
echo "  Response Mode: $MODE"
echo ""

if [ "$TASKS_EXECUTED" -ge 1 ]; then
    echo -e "${GREEN}✓✓✓ SUCCESS ✓✓✓${NC}"
    echo -e "${GREEN}Task was triggered by alert!${NC}"
    echo ""
    
    # Show execution details
    echo "Execution Details:"
    echo "$ALERT_RESPONSE" | jq -r '.executed_tasks[] | "  Task: \(.task_title)\n  Job ID: \(.job_id)\n  Status: \(.execution_status)"' 2>/dev/null || echo "  (Details not available)"
else
    echo -e "${RED}✗✗✗ FAILED ✗✗✗${NC}"
    echo -e "${RED}Task was NOT triggered!${NC}"
    echo ""
    echo "Possible issues:"
    echo "  - Alert source capitalization mismatch"
    echo "  - Alert name doesn't match exactly"
    echo "  - Task not found by req-router"
    echo ""
    echo "Debug info:"
    echo "  Expected source: Grafana"
    echo "  Expected name: $ALERT_NAME"
    echo "  Task ID: $TASK_ID"
fi

echo ""

# Step 4: Cleanup
echo -e "${YELLOW}Step 4: Cleaning up...${NC}"
DELETE_RESPONSE=$(curl -s -X DELETE "${BASE_URL}/api/v1/tasks/${TASK_ID}?wsid=__DEFAULT__" \
  -H "Authorization: Bearer ${TOKEN}")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Task deleted${NC}"
else
    echo -e "${YELLOW}⚠ Task cleanup may have failed (task ID: ${TASK_ID})${NC}"
fi

echo ""
echo "Done!"

