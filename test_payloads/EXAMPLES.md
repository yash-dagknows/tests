# Alert Handling Test Examples

Real-world examples for testing alert handling modes.

---

## 📘 **Example 1: Test Grafana CPU Alert (Deterministic)**

### **Scenario**
Test that a pre-configured task executes when a high CPU alert fires.

### **Steps**

**1. Setup**
```bash
cd tests/test_payloads
export DAGKNOWS_URL="https://dev.dagknows.com"
export DAGKNOWS_TOKEN="your-token"
```

**2. Create task with alert trigger**
```bash
./create_test_task.sh "Grafana" "HighCPUUsage"
```

Expected output:
```
✅ Task created successfully!

Task Details:
  ID: task_abc123
  Title: Handler for HighCPUUsage
  Trigger Source: Grafana
  Trigger Name: HighCPUUsage
```

**3. Send matching alert**
```bash
./send_alert.sh grafana_alert_cpu.json
```

Expected output:
```
Status: success
Mode: deterministic
Alert Source: Grafana
Alert Name: HighCPUUsage
Tasks Executed: 1

✅ Alert processed and task(s) executed!
```

---

## 📗 **Example 2: Test AI Task Selection**

### **Scenario**
Test that AI can find and execute a similar task based on alert description.

### **Steps**

**1. Set AI-selected mode**
```bash
./set_mode.sh ai_selected
```

**2. Create a tooltask about CPU (NO trigger configured)**
```bash
curl -X POST "${DAGKNOWS_URL}/api/v1/tasks/" \
  -H "Authorization: Bearer ${DAGKNOWS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "title": "CPU Performance Investigation",
      "description": "Investigate high CPU usage, check top processes, analyze load average",
      "script_type": "python",
      "script": "import psutil\nprint(f\"CPU: {psutil.cpu_percent()}%\")",
      "tags": ["cpu", "performance"]
    }
  }'
```

**3. Wait for vectorization (5 seconds)**
```bash
sleep 5
```

**4. Send CPU alert (no deterministic match)**
```bash
./send_alert.sh grafana_alert_cpu.json
```

**Expected**: AI finds the similar task and executes it!

```
Status: success
Mode: ai_selected
AI Attempted: true
Tasks Executed: 1
```

---

## 📕 **Example 3: Test Autonomous Investigation**

### **Scenario**
Test that AI launches a full troubleshooting session for an unfamiliar alert.

### **Steps**

**1. Set autonomous mode**
```bash
./set_mode.sh autonomous
```

**2. Send a novel alert (no matching task exists)**
```bash
./send_alert.sh grafana_alert_memory.json
```

**Expected**: AI creates runbook and investigation tasks!

```
Status: success
Mode: autonomous
Runbook Task: runbook_xyz789
Investigation Task: investigation_abc456
```

---

## 📙 **Example 4: Custom Alert Payload**

### **Scenario**
Create and test a custom alert for disk space.

### **Steps**

**1. Create custom alert payload**
```bash
cat > custom_disk_alert.json << 'EOF'
{
  "receiver": "DagKnows",
  "status": "firing",
  "alerts": [{
    "status": "firing",
    "labels": {
      "alertname": "DiskSpaceLow",
      "severity": "warning",
      "instance": "server-03"
    },
    "annotations": {
      "description": "Disk usage is at 92% on /data partition",
      "summary": "Low Disk Space Alert"
    }
  }],
  "commonLabels": {
    "alertname": "DiskSpaceLow"
  }
}
EOF
```

**2. Create task for disk alerts**
```bash
./create_test_task.sh "Grafana" "DiskSpaceLow"
```

**3. Test it**
```bash
./send_alert.sh custom_disk_alert.json
```

---

## 📔 **Example 5: PagerDuty Incident**

### **Scenario**
Test PagerDuty database incident handling.

### **Steps**

**1. Create task for database issues**
```bash
./create_test_task.sh "Pagerduty" "Database Connection Failure"
```

**2. Send PagerDuty incident**
```bash
./send_alert.sh pagerduty_incident_db.json
```

**Expected**:
```
Status: success
Alert Source: Pagerduty
Alert Name: Database Connection Failure
Tasks Executed: 1
```

---

## 📒 **Example 6: Test All Modes in Sequence**

### **Scenario**
Comprehensive test of all three modes.

### **Steps**

```bash
# Run all mode tests
./test_all_modes.sh
```

**Expected output**:
```
╔════════════════════════════════════════════════════════════════════╗
║                      TEST SUMMARY REPORT                           ║
╚════════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────┬──────────┐
│ Test                               │ Result   │
├────────────────────────────────────┼──────────┤
│ 1. Deterministic Mode              │ ✅ PASS  │
│ 2. AI-Selected Mode                │ ✅ PASS  │
│ 3. Autonomous Mode                 │ ✅ PASS  │
└────────────────────────────────────┴──────────┘

Total: 3/3 tests passed

╔════════════════════════════════════════════════════════════════════╗
║  ✅ ALL TESTS PASSED - Alert handling is working perfectly!       ║
╚════════════════════════════════════════════════════════════════════╝
```

---

## 🔧 **Example 7: Multiple Alert Sources**

### **Scenario**
Configure one task to handle alerts from multiple sources.

### **Steps**

**1. Create multi-source task via API**
```bash
curl -X POST "${DAGKNOWS_URL}/api/v1/tasks/" \
  -H "Authorization: Bearer ${DAGKNOWS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "title": "Multi-Source Alert Handler",
      "script": "echo Handling alert from any source",
      "script_type": "command",
      "trigger_on_alerts": [
        {
          "source": "Grafana",
          "alert_name": "HighCPUUsage",
          "dedup_interval": 300
        },
        {
          "source": "Pagerduty",
          "alert_name": "CPU Critical",
          "dedup_interval": 300
        }
      ]
    }
  }'
```

**2. Test with Grafana alert**
```bash
./send_alert.sh grafana_alert_cpu.json
# Should execute!
```

**3. Test with PagerDuty**
```bash
# (Would need matching PagerDuty payload with alert_name: "CPU Critical")
```

---

## 🎯 **Example 8: Test Mode Switching**

### **Scenario**
Verify mode switching works correctly.

### **Steps**

**1. Start in deterministic mode**
```bash
./set_mode.sh deterministic
./test_deterministic_mode.sh
# Should pass
```

**2. Switch to AI-selected**
```bash
./set_mode.sh ai_selected
# Send an alert - should use AI selection
./send_alert.sh grafana_alert_cpu.json
```

**3. Switch to autonomous**
```bash
./set_mode.sh autonomous
# Send an alert - should launch investigation
./send_alert.sh grafana_alert_memory.json
```

**4. Restore deterministic**
```bash
./set_mode.sh deterministic
```

---

## 💡 **Example 9: Deduplication Testing**

### **Scenario**
Test that dedup_interval prevents duplicate executions.

### **Steps**

**1. Create task with 5-minute dedup**
```bash
./create_test_task.sh "Grafana" "TestDedup"
```

**2. Modify alert payload**
```bash
# Edit grafana_alert_cpu.json to change alertname to "TestDedup"
sed 's/HighCPUUsage/TestDedup/g' grafana_alert_cpu.json > test_dedup.json
```

**3. Send first alert**
```bash
./send_alert.sh test_dedup.json
# Output: Tasks Executed: 1
```

**4. Send duplicate immediately**
```bash
./send_alert.sh test_dedup.json
# Output: Tasks Executed: 0 (deduplicated)
```

**5. Wait 5 minutes and retry**
```bash
sleep 300
./send_alert.sh test_dedup.json
# Output: Tasks Executed: 1 (allowed after dedup window)
```

---

## 🎓 **Example 10: Integration Test Flow**

### **Scenario**
Complete end-to-end test for CI/CD pipeline.

### **Script**
```bash
#!/bin/bash
# integration_test.sh

set -e

# Setup
source .env
PASSED=0
FAILED=0

# Test 1: Deterministic
echo "Testing Deterministic Mode..."
if ./test_deterministic_mode.sh > /dev/null 2>&1; then
    echo "✅ Deterministic: PASS"
    PASSED=$((PASSED + 1))
else
    echo "❌ Deterministic: FAIL"
    FAILED=$((FAILED + 1))
fi

# Test 2: AI-Selected (skip if AI not configured)
echo "Testing AI-Selected Mode..."
if ./test_ai_selected_mode.sh > /dev/null 2>&1; then
    echo "✅ AI-Selected: PASS"
    PASSED=$((PASSED + 1))
else
    echo "⚠️  AI-Selected: SKIP (AI not configured)"
fi

# Test 3: Verify mode persistence
echo "Testing mode persistence..."
./set_mode.sh deterministic
MODE=$(curl -s -X POST "${DAGKNOWS_URL}/getSettings" \
    -H "Authorization: Bearer ${DAGKNOWS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{}' | jq -r '.admin_settings.incident_response_mode')

if [ "$MODE" = "deterministic" ]; then
    echo "✅ Mode persistence: PASS"
    PASSED=$((PASSED + 1))
else
    echo "❌ Mode persistence: FAIL"
    FAILED=$((FAILED + 1))
fi

# Summary
echo ""
echo "Integration Test Summary:"
echo "  Passed: ${PASSED}"
echo "  Failed: ${FAILED}"

exit $FAILED
```

---

## 📋 **Common Patterns**

### **Pattern 1: Create → Test → Cleanup**
```bash
# Create
TASK_ID=$(./create_test_task.sh "Grafana" "TestAlert" | grep "ID:" | awk '{print $2}')

# Test
./send_alert.sh grafana_alert_cpu.json

# Cleanup
curl -X DELETE "${DAGKNOWS_URL}/api/v1/tasks/${TASK_ID}?wsid=__DEFAULT__" \
  -H "Authorization: Bearer ${DAGKNOWS_TOKEN}"
```

### **Pattern 2: Batch Testing**
```bash
# Test multiple alert types
for payload in *.json; do
    echo "Testing $payload..."
    ./send_alert.sh "$payload"
    sleep 2
done
```

### **Pattern 3: Parallel Testing**
```bash
# Test all modes in parallel
./test_deterministic_mode.sh &
./test_ai_selected_mode.sh &
./test_autonomous_mode.sh &
wait
echo "All tests completed"
```

---

## 🎬 **Next Steps**

- Try the **Quick Start**: [QUICK_START.md](./QUICK_START.md)
- Read **Full Docs**: [README.md](./README.md)
- Create **Custom Payloads**: Copy and modify JSON files
- **Integrate with CI/CD**: Use scripts in your pipeline

---

**Happy Testing!** 🚀

