#!/bin/bash
# Create a Test Task with Alert Trigger
# Usage: ./create_test_task.sh <alert_source> <alert_name>
# Example: ./create_test_task.sh "Grafana" "HighCPUUsage"

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

# Get arguments
ALERT_SOURCE="$1"
ALERT_NAME="$2"

if [ -z "$ALERT_SOURCE" ] || [ -z "$ALERT_NAME" ]; then
    echo "Usage: $0 <alert_source> <alert_name>"
    echo ""
    echo "Examples:"
    echo "  $0 Grafana HighCPUUsage"
    echo "  $0 Pagerduty 'Database Connection Failure'"
    echo "  $0 Grafana DiskSpaceLow"
    echo ""
    echo "Valid alert sources:"
    echo "  • Grafana (capital G)"
    echo "  • Pagerduty (capital P, lowercase d)"
    echo "  • Datadog"
    echo "  • Prometheus"
    echo "  • CloudWatch"
    exit 1
fi

TIMESTAMP=$(date +%s)

echo "Creating task with alert trigger:"
echo "  Alert Source: ${ALERT_SOURCE}"
echo "  Alert Name: ${ALERT_NAME}"
echo ""

# Create task using simpler command script
RESPONSE=$(curl -s -X POST "${BASE_URL}/api/v1/tasks/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    -d @- << EOF
{
    "task": {
        "title": "Handler for ${ALERT_NAME}",
        "description": "Automated response handler for ${ALERT_SOURCE} alert: ${ALERT_NAME}",
        "script_type": "command",
        "commands": [
            "echo '🚨 Alert Handler Triggered!'",
            "echo 'Alert Source: ${ALERT_SOURCE}'",
            "echo 'Alert Name: ${ALERT_NAME}'",
            "echo 'Timestamp: '$(date)",
            "echo 'Performing automated response...'",
            "echo '✅ Response completed successfully!'"
        ],
        "tags": ["test-alert-handler", "${ALERT_SOURCE}"],
        "trigger_on_alerts": [
            {
                "source": "${ALERT_SOURCE}",
                "alert_name": "${ALERT_NAME}",
                "dedup_interval": 300
            }
        ]
    }
}
EOF
)

TASK_ID=$(echo "$RESPONSE" | jq -r '.task.id // empty')

if [ -z "$TASK_ID" ]; then
    echo -e "${RED}✗ Failed to create task${NC}"
    echo "Response:"
    echo "$RESPONSE" | jq .
    exit 1
fi

echo -e "${GREEN}✅ Task created successfully!${NC}"
echo ""
echo "Task Details:"
echo "  ID: ${TASK_ID}"
echo "  Title: Handler for ${ALERT_NAME}"
echo "  Trigger Source: ${ALERT_SOURCE}"
echo "  Trigger Name: ${ALERT_NAME}"
echo "  Dedup Interval: 300 seconds (5 minutes)"
echo ""
echo "View in UI: ${BASE_URL}/tasks/${TASK_ID}"
echo ""
echo "To test this task, send an alert:"
echo "  ./send_alert.sh <appropriate_payload.json>"
echo ""
echo "To delete this task:"
echo "  curl -X DELETE '${BASE_URL}/api/v1/tasks/${TASK_ID}?wsid=__DEFAULT__' \\"
echo "    -H 'Authorization: Bearer \$DAGKNOWS_TOKEN'"

