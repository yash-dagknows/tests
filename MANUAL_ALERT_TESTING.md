# Manual Alert Testing Guide

## 🎯 Testing Deterministic Alert Mapping

This guide shows you how to manually test deterministic alert mapping without running automated tests.

---

## 📍 **Where Alerts Are Sent**

**Endpoint**: `/processAlert`

```
Local Docker:   http://req-router:8888/processAlert
Remote:         https://44.224.1.45/processAlert
```

---

## 🔑 **Key Concept: Alert Source Capitalization**

⚠️ **IMPORTANT**: Req-router capitalizes alert sources using `.title()`

```
You send:       "grafana"     → Req-router sees: "Grafana"
You send:       "cloudwatch"  → Req-router sees: "Cloudwatch"
You send:       "mysource"    → Req-router sees: "Mysource"
You send:       "my_source"   → Req-router sees: "My_Source"  ⚠️ Problematic!
```

**Best Practice**: Use simple lowercase names without underscores or special chars:
- ✅ Good: `"grafana"`, `"cloudwatch"`, `"mysource123"`
- ❌ Avoid: `"my_source"`, `"test-source"`, `"Source_123"`

---

## 📝 **Step-by-Step Manual Testing**

### Step 1: Create a Task with Alert Trigger

**Using the UI or API, create a task with `trigger_on_alerts`:**

```json
{
  "title": "CPU High Alert Handler",
  "description": "Handles high CPU alerts",
  "script_type": "python",
  "script": "print('Handling CPU alert')",
  "trigger_on_alerts": [
    {
      "alert_source": "Grafana",
      "alert_name": "HighCPUAlert",
      "dedup_interval": 300
    }
  ]
}
```

**Key Points**:
- `alert_source`: Capitalized (e.g., "Grafana", not "grafana")
- `alert_name`: Exact match required
- `dedup_interval`: Seconds between executions (300 = 5 minutes)

**Create via curl**:
```bash
curl -X POST http://taskservice:2235/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -H "dk-user-info: $(python3 -c 'import urllib.parse, json; print(urllib.parse.quote(json.dumps({"uid":"1","uname":"test@dagknows.com","org":"avengers","role":"Admin"})))')" \
  -d '{
    "task": {
      "title": "CPU High Alert Handler",
      "description": "Handles high CPU alerts",
      "script_type": "python",
      "script": "print(\"Handling CPU alert\")",
      "trigger_on_alerts": [
        {
          "alert_source": "Grafana",
          "alert_name": "HighCPUAlert",
          "dedup_interval": 300
        }
      ]
    }
  }'
```

**Or using remote deployment**:
```bash
curl -X POST https://44.224.1.45/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
  -d '{
    "task": {
      "title": "CPU High Alert Handler",
      "description": "Handles high CPU alerts",
      "script_type": "python",
      "script": "print(\"Handling CPU alert\")",
      "trigger_on_alerts": [
        {
          "alert_source": "Grafana",
          "alert_name": "HighCPUAlert",
          "dedup_interval": 300
        }
      ]
    }
  }'
```

---

### Step 2: Send a Matching Alert

**Grafana Alert Payload**:

```json
{
  "receiver": "DagKnows_Alert_Endpoint",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "HighCPUAlert",
        "grafana_folder": "production",
        "instance": "server-01",
        "job": "node-exporter",
        "severity": "critical"
      },
      "annotations": {
        "description": "CPU usage has exceeded 90% for 5 minutes",
        "summary": "High CPU Usage on server-01"
      },
      "startsAt": "2025-12-08T14:00:00Z",
      "endsAt": "0001-01-01T00:00:00Z",
      "generatorURL": "http://grafana:3000/alerting/grafana/abc123/view",
      "fingerprint": "alert12345",
      "values": {
        "A": 95.5
      }
    }
  ],
  "groupLabels": {
    "alertname": "HighCPUAlert",
    "grafana_folder": "production"
  },
  "commonLabels": {
    "alertname": "HighCPUAlert",
    "grafana_folder": "production",
    "instance": "server-01",
    "job": "node-exporter",
    "severity": "critical"
  },
  "commonAnnotations": {
    "description": "CPU usage has exceeded 90% for 5 minutes",
    "summary": "High CPU Usage on server-01"
  },
  "externalURL": "http://grafana:3000/",
  "version": "1",
  "title": "[FIRING:1] HighCPUAlert production (server-01 node-exporter)",
  "state": "alerting",
  "message": "**Firing**\n\nValue: A=95.5\nLabels:\n - alertname = HighCPUAlert\n - instance = server-01"
}
```

**Send via curl (Local)**:
```bash
curl -X POST http://req-router:8888/processAlert \
  -H "Content-Type: application/json" \
  -H "dk-user-info: $(python3 -c 'import urllib.parse, json; print(urllib.parse.quote(json.dumps({"uid":"1","uname":"test@dagknows.com","org":"avengers","role":"Admin"})))')" \
  -d '{
    "receiver": "DagKnows_Alert_Endpoint",
    "status": "firing",
    "alerts": [
      {
        "status": "firing",
        "labels": {
          "alertname": "HighCPUAlert",
          "grafana_folder": "production",
          "instance": "server-01",
          "job": "node-exporter",
          "severity": "critical"
        },
        "annotations": {
          "description": "CPU usage has exceeded 90% for 5 minutes",
          "summary": "High CPU Usage on server-01"
        },
        "startsAt": "2025-12-08T14:00:00Z",
        "endsAt": "0001-01-01T00:00:00Z",
        "generatorURL": "http://grafana:3000/alerting/grafana/abc123/view",
        "fingerprint": "alert12345",
        "values": {
          "A": 95.5
        }
      }
    ],
    "groupLabels": {
      "alertname": "HighCPUAlert",
      "grafana_folder": "production"
    },
    "commonLabels": {
      "alertname": "HighCPUAlert",
      "grafana_folder": "production",
      "instance": "server-01",
      "job": "node-exporter",
      "severity": "critical"
    },
    "commonAnnotations": {
      "description": "CPU usage has exceeded 90% for 5 minutes",
      "summary": "High CPU Usage on server-01"
    },
    "externalURL": "http://grafana:3000/",
    "version": "1",
    "title": "[FIRING:1] HighCPUAlert production (server-01 node-exporter)",
    "state": "alerting"
  }'
```

**Send via curl (Remote)**:
```bash
curl -X POST https://44.224.1.45/processAlert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
  -d '{
    "receiver": "DagKnows_Alert_Endpoint",
    "status": "firing",
    "alerts": [
      {
        "status": "firing",
        "labels": {
          "alertname": "HighCPUAlert",
          "grafana_folder": "production",
          "instance": "server-01",
          "job": "node-exporter",
          "severity": "critical"
        },
        "annotations": {
          "description": "CPU usage has exceeded 90% for 5 minutes",
          "summary": "High CPU Usage on server-01"
        },
        "startsAt": "2025-12-08T14:00:00Z",
        "endsAt": "0001-01-01T00:00:00Z",
        "generatorURL": "http://grafana:3000/alerting/grafana/abc123/view",
        "fingerprint": "alert12345",
        "values": {
          "A": 95.5
        }
      }
    ],
    "groupLabels": {
      "alertname": "HighCPUAlert"
    },
    "commonLabels": {
      "alertname": "HighCPUAlert",
      "instance": "server-01",
      "severity": "critical"
    },
    "commonAnnotations": {
      "description": "CPU usage has exceeded 90% for 5 minutes",
      "summary": "High CPU Usage on server-01"
    },
    "externalURL": "http://grafana:3000/",
    "version": "1",
    "title": "[FIRING:1] HighCPUAlert",
    "state": "alerting"
  }'
```

---

### Step 3: Verify Task Execution

**Expected Response**:
```json
{
  "status": "success",
  "message": "Alert processed successfully",
  "alert_source": "Grafana",
  "alert_name": "HighCPUAlert",
  "tasks_executed": 1,
  "incident_response_mode": "deterministic",
  "executed_tasks": [
    {
      "task_id": "abc123...",
      "task_title": "CPU High Alert Handler",
      "job_id": "job_xyz789",
      "execution_status": "started"
    }
  ]
}
```

**Key Fields**:
- `tasks_executed: 1` → Task was found and executed ✅
- `incident_response_mode: "deterministic"` → Used deterministic matching ✅
- `executed_tasks` → Array of executed tasks with job IDs

---

## 🧪 **Testing Different Scenarios**

### Scenario 1: Match Found (Deterministic)

**Task Configuration**:
```json
{
  "trigger_on_alerts": [
    {
      "alert_source": "Grafana",
      "alert_name": "DiskSpaceLow"
    }
  ]
}
```

**Alert Sent**:
```json
{
  "alerts": [
    {
      "labels": {
        "alertname": "DiskSpaceLow"  // Matches!
      }
    }
  ]
}
```

**Expected**: Task executes ✅

---

### Scenario 2: No Match (Deterministic)

**Task Configuration**:
```json
{
  "trigger_on_alerts": [
    {
      "alert_source": "Grafana",
      "alert_name": "CPUHigh"
    }
  ]
}
```

**Alert Sent**:
```json
{
  "alerts": [
    {
      "labels": {
        "alertname": "DiskSpaceLow"  // Doesn't match!
      }
    }
  ]
}
```

**Expected**:
```json
{
  "status": "success",
  "message": "No matching tasks found",
  "tasks_executed": 0,
  "incident_response_mode": "deterministic"
}
```

---

### Scenario 3: Source Mismatch (Common Mistake)

**Task Configuration**:
```json
{
  "trigger_on_alerts": [
    {
      "alert_source": "grafana",  // ❌ Lowercase!
      "alert_name": "CPUHigh"
    }
  ]
}
```

**Alert Sent**: `source: "grafana"` → Req-router capitalizes to `"Grafana"`

**Result**: ❌ **NO MATCH** because task has `"grafana"` but req-router looks for `"Grafana"`

**Fix**: Always use capitalized source in task configuration:
```json
{
  "alert_source": "Grafana"  // ✅ Capitalized
}
```

---

## 📋 **Alert Matching Logic**

Req-router matches alerts to tasks using:

```python
# Pseudo-code
alert_source = normalize_source(payload)  # "grafana" → "Grafana"
alert_name = extract_alert_name(payload)  # "HighCPUAlert"

matching_tasks = find_tasks_where(
    task.trigger_on_alerts.alert_source == alert_source AND
    task.trigger_on_alerts.alert_name == alert_name
)

for task in matching_tasks:
    execute_task(task)
```

**Key Points**:
1. **Exact match** required on both `alert_source` and `alert_name`
2. **Case-sensitive** matching
3. **Source is capitalized** by req-router before matching
4. **Multiple tasks** can trigger on the same alert

---

## 🔍 **Debugging Tips**

### Check Task Configuration

```bash
# Get task details
curl http://taskservice:2235/api/v1/tasks/{task_id} \
  -H "dk-user-info: ..."

# Look for trigger_on_alerts field
```

### Check Req-Router Logs

```bash
# Local Docker
docker logs req-router --tail 50

# Look for:
# - "processAlert called"
# - "No matching tasks found" or "Found X matching tasks"
# - Alert source and name after normalization
```

### Check TaskService Logs

```bash
# Check if task was executed
docker logs taskservice --tail 50

# Look for job execution logs
```

### Verify Alert Normalization

The alert you send goes through normalization:

```
Raw Grafana Payload
  ↓
Normalize Alert (extract source, name, severity, etc.)
  ↓
Capitalize Source: "grafana" → "Grafana"
  ↓
Find Matching Tasks
  ↓
Execute Tasks
```

---

## 💡 **Common Issues & Solutions**

| Issue | Cause | Solution |
|-------|-------|----------|
| **No task executes** | Source capitalization mismatch | Use "Grafana" not "grafana" in task config |
| **No task executes** | Alert name mismatch | Check exact spelling in labels.alertname |
| **Multiple executions** | Dedup interval too short | Increase dedup_interval to 300+ |
| **401 Unauthorized** | Missing auth header | Add Bearer token or dk-user-info header |

---

## 📁 **Complete Example Script**

Save this as `test_alert_deterministic.sh`:

```bash
#!/bin/bash

# Configuration
BASE_URL="https://44.224.1.45"
TOKEN="your-token-here"

# Step 1: Create task with alert trigger
echo "Creating task with alert trigger..."
TASK_RESPONSE=$(curl -s -X POST ${BASE_URL}/api/v1/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "task": {
      "title": "Test Alert Handler",
      "description": "Handles test alerts",
      "script_type": "python",
      "script": "print(\"Alert handled!\")",
      "trigger_on_alerts": [
        {
          "alert_source": "Grafana",
          "alert_name": "TestAlert123",
          "dedup_interval": 300
        }
      ]
    }
  }')

TASK_ID=$(echo $TASK_RESPONSE | jq -r '.task.id')
echo "Created task: $TASK_ID"

# Step 2: Send matching alert
echo "Sending alert..."
ALERT_RESPONSE=$(curl -s -X POST ${BASE_URL}/processAlert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "status": "firing",
    "alerts": [{
      "status": "firing",
      "labels": {
        "alertname": "TestAlert123",
        "severity": "critical"
      },
      "annotations": {
        "description": "Test alert for deterministic mapping",
        "summary": "Test Alert"
      }
    }],
    "commonLabels": {
      "alertname": "TestAlert123"
    }
  }')

echo "Alert response:"
echo $ALERT_RESPONSE | jq .

# Check if task executed
TASKS_EXECUTED=$(echo $ALERT_RESPONSE | jq -r '.tasks_executed')
if [ "$TASKS_EXECUTED" -ge 1 ]; then
    echo "✅ SUCCESS: Task executed!"
else
    echo "❌ FAILED: Task did not execute"
fi

# Cleanup
echo "Cleaning up task..."
curl -s -X DELETE "${BASE_URL}/api/v1/tasks/${TASK_ID}?wsid=__DEFAULT__" \
  -H "Authorization: Bearer ${TOKEN}"

echo "Done!"
```

Run it:
```bash
chmod +x test_alert_deterministic.sh
./test_alert_deterministic.sh
```

---

## 📚 **Related Documentation**

- **`ALERT_HANDLING_TESTS.md`** - Automated test details
- **`ALERT_TEST_FIXES.md`** - Known issues and fixes
- **`test_payloads/test_alert_webhooks.py`** - More payload examples

---

**Last Updated**: December 8, 2025

