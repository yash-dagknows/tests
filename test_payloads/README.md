# Alert Handling Mode Test Scripts

Manual test scripts for testing all three alert handling modes against any DagKnows deployment.

## 📋 **Quick Start**

### **1. Setup Environment**

Create `.env` file in this directory:

```bash
# .env
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_TOKEN=your-bearer-token-here
```

Or export variables:

```bash
export DAGKNOWS_URL="https://dev.dagknows.com"
export DAGKNOWS_TOKEN="your-bearer-token"
```

### **2. Make Scripts Executable**

```bash
chmod +x *.sh
```

### **3. Run Tests**

```bash
# Test Deterministic Mode
./test_deterministic_mode.sh

# Test AI-Selected Mode
./test_ai_selected_mode.sh

# Test Autonomous Mode
./test_autonomous_mode.sh

# Run all modes
./test_all_modes.sh
```

---

## 🎯 **Test Scripts**

### **1. `test_deterministic_mode.sh`**

**What it does**:
- Creates a task configured with `trigger_on_alerts`
- Sends a matching Grafana alert
- Verifies the task executes
- Cleans up

**Expected**: Task executes immediately when alert matches

**Use case**: Testing pre-configured alert response automation

---

### **2. `test_ai_selected_mode.sh`**

**What it does**:
- Switches to AI-selected mode
- Creates a tooltask about CPU performance
- Sends an alert about CPU issues (no deterministic match)
- AI searches for similar tasks using KNN search
- AI selects and executes the best matching task
- Cleans up

**Expected**: AI finds similar task and executes it

**Use case**: Testing AI-powered task selection

---

### **3. `test_autonomous_mode.sh`**

**What it does**:
- Switches to autonomous mode
- Sends an alert with no deterministic match
- AI launches a full troubleshooting session
- Creates runbook and investigation tasks
- Cleans up

**Expected**: AI creates and executes investigation workflow

**Use case**: Testing fully autonomous AI troubleshooting

---

### **4. `test_all_modes.sh`**

Runs all three mode tests sequentially with detailed reporting.

---

## 📁 **Payload Files**

### **`grafana_alert_cpu.json`**

Example Grafana alert for high CPU usage:
```json
{
  "alerts": [{
    "labels": {
      "alertname": "HighCPUUsage",
      "severity": "critical"
    }
  }]
}
```

### **`grafana_alert_memory.json`**

Example Grafana alert for high memory usage.

### **`pagerduty_incident_db.json`**

Example PagerDuty incident for database issues.

### **`pagerduty_incident_service.json`**

Example PagerDuty incident for service downtime.

---

## 🛠️ **Helper Scripts**

### **`create_test_task.sh`**

Creates a test task with alert triggers.

**Usage**:
```bash
./create_test_task.sh "Grafana" "HighCPUUsage"
```

### **`send_alert.sh`**

Sends an alert to the deployment.

**Usage**:
```bash
./send_alert.sh grafana_alert_cpu.json
```

### **`check_alert_status.sh`**

Checks if an alert was processed and if tasks were executed.

**Usage**:
```bash
./check_alert_status.sh "HighCPUUsage"
```

### **`set_mode.sh`**

Sets the incident response mode.

**Usage**:
```bash
./set_mode.sh deterministic
./set_mode.sh ai_selected
./set_mode.sh autonomous
```

---

## 📊 **Test Scenarios**

### **Scenario 1: Deterministic Match**
```bash
# 1. Create task
./create_test_task.sh "Grafana" "HighCPUUsage"

# 2. Send matching alert
./send_alert.sh grafana_alert_cpu.json

# 3. Verify task executed
./check_alert_status.sh "HighCPUUsage"
```

### **Scenario 2: AI Selection**
```bash
# 1. Set AI mode
./set_mode.sh ai_selected

# 2. Create tooltask (no trigger configured)
# (Task about CPU investigation)

# 3. Send alert
./send_alert.sh grafana_alert_cpu.json

# 4. AI should find and execute similar task
```

### **Scenario 3: Autonomous Investigation**
```bash
# 1. Set autonomous mode
./set_mode.sh autonomous

# 2. Send alert (no matching task)
./send_alert.sh grafana_alert_memory.json

# 3. AI launches investigation
```

---

## 🔍 **Troubleshooting**

### **No Tasks Executed**

**Check**:
1. Alert source matches task config:
   - Grafana alerts → `source: "Grafana"`
   - PagerDuty incidents → `source: "Pagerduty"`

2. Alert name matches exactly (case-sensitive):
   ```bash
   # In task config
   "alert_name": "HighCPUUsage"
   
   # In alert payload
   "labels": {"alertname": "HighCPUUsage"}
   ```

3. Mode is set correctly:
   ```bash
   ./set_mode.sh deterministic
   ```

### **Auth Errors**

**Error**: `401 Unauthorized`

**Fix**: Check your bearer token:
```bash
# Test token
curl -X GET $DAGKNOWS_URL/api/v1/tasks/status \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN"

# Should return: {"status": "ok"} or similar
```

### **Mode Not Changing**

**Error**: Mode doesn't change when running `set_mode.sh`

**Fix**: Token needs admin permissions:
- Ensure token has `Admin` or `Supremo` role
- Check: `curl -X POST $DAGKNOWS_URL/getAdminSettingsFlags ...`

---

## 📖 **Examples**

### **Example 1: Test Grafana High CPU Alert**

```bash
#!/bin/bash
# Complete test of deterministic mode with Grafana alert

export DAGKNOWS_URL="https://dev.dagknows.com"
export DAGKNOWS_TOKEN="eyJhbGci..."

# 1. Create task
TASK_ID=$(curl -s -X POST $DAGKNOWS_URL/api/v1/tasks/ \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task": {
      "title": "Handle High CPU",
      "script": "echo Investigating CPU...",
      "script_type": "command",
      "trigger_on_alerts": [{
        "source": "Grafana",
        "alert_name": "HighCPUUsage",
        "dedup_interval": 300
      }]
    }
  }' | jq -r '.task.id')

echo "Created task: $TASK_ID"

# 2. Send alert
curl -X POST $DAGKNOWS_URL/processAlert \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d @grafana_alert_cpu.json

# 3. Check result
sleep 2
curl -X GET "$DAGKNOWS_URL/api/alerts?alert_name=HighCPUUsage" \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN"

# 4. Cleanup
curl -X DELETE "$DAGKNOWS_URL/api/v1/tasks/$TASK_ID?wsid=__DEFAULT__" \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN"
```

---

## 🎓 **Best Practices**

1. **Always clean up**: Delete test tasks and alerts after testing
2. **Use unique alert names**: Include timestamps to avoid conflicts
3. **Test in order**: Deterministic → AI-Selected → Autonomous
4. **Check logs**: Use `check_alert_status.sh` to verify execution
5. **Restore mode**: Set back to deterministic after testing

---

## 📝 **Notes**

- Scripts use `jq` for JSON parsing (install: `brew install jq` or `apt install jq`)
- All scripts support both `.env` file and environment variables
- Cleanup is automatic in test scripts
- Test tasks are tagged with `test-alert-modes` for easy identification

---

**Last Updated**: December 8, 2025

