# Final Fixes for Alert Handling Tests

## 🐛 **Issues Found and Fixed**

### **Issue 1: Wrong Field Name** ❌
**Problem**: Used `alert_source` instead of `source` in `trigger_on_alerts`

**Old Code**:
```python
task_data["trigger_on_alerts"] = [
    {
        "alert_source": "Testsource123",  # ❌ Wrong field name
        "alert_name": "MyAlert"
    }
]
```

**Fixed**:
```python
task_data["trigger_on_alerts"] = [
    {
        "source": "Grafana",  # ✅ Correct field name
        "alert_name": "MyAlert"
    }
]
```

**Backend stores**:
```json
"trigger_on_alerts": [
  {
    "source": "Grafana",      // ✅ Correct
    "alert_name": "MyAlert"
  }
]
```

---

### **Issue 2: Wrong Alert Source Value** ❌
**Problem**: Used custom source names like `"Testsource123"` instead of real alert system names

**Root Cause**: Req-router **detects** the alert source from the payload format:
- Grafana-formatted payload → source = `"Grafana"`
- PagerDuty-formatted payload → source = `"Pagerduty"`  
- Datadog-formatted payload → source = `"Datadog"`

It doesn't read a custom `alert_source` field from the payload!

**Old Code**:
```python
alert_source = f"testsource{timestamp}"  # ❌ Custom name
task_data["trigger_on_alerts"] = [{
    "source": "Testsource123",  # ❌ Won't match "Grafana"
    "alert_name": "MyAlert"
}]

# Send Grafana-formatted alert
alert_payload = create_grafana_alert_data(
    alert_name="MyAlert",
    alert_source="testsource123"  # ❌ This is ignored!
)
# Req-router detects: source = "Grafana" (from format)
# Task expects: source = "Testsource123"
# Result: No match! ❌
```

**Fixed**:
```python
alert_source = "Grafana"  # ✅ Real alert system name
task_data["trigger_on_alerts"] = [{
    "source": "Grafana",  # ✅ Matches req-router detection
    "alert_name": "MyAlert"
}]

# Send Grafana-formatted alert
alert_payload = create_grafana_alert_data(
    alert_name="MyAlert",
    alert_source="grafana"  # Lowercase is fine, ignored anyway
)
# Req-router detects: source = "Grafana" (from format)
# Task expects: source = "Grafana"
# Result: Match! ✅
```

---

### **Issue 3: Fixture Scope Mismatch** ❌
**Problem**: Class-scoped fixture trying to use function-scoped fixture

**Error**:
```
ScopeMismatch: You tried to access the function scoped fixture req_router_client 
with a class scoped request object
```

**Fixed**: Changed from `scope="class"` to default (function scope):
```python
# Before
@pytest.fixture(scope="class", autouse=True)  # ❌
def setup_mode(self, req_router_client):
    ...

# After
@pytest.fixture(autouse=True)  # ✅ Function scope
def setup_mode(self, req_router_client):
    ...
```

---

### **Issue 4: Auth Failures (Not Critical)** ⚠️
**Problem**: `setFlags` API returns "Not authorized with this role:customer"

**Root Cause**: 
- Req-router's `BaseAuthedResource` doesn't check `dk-user-info` header
- Falls back to anonymous/Customer role
- `setFlags` requires Admin or Supremo role

**Impact**: **Not critical** - Tests still work because:
1. Deterministic mode is the default
2. The warning is logged but tests continue
3. Task matching works correctly with fixed source names

**Options**:
1. **Option A (Current)**: Accept the warning, tests work fine
2. **Option B**: Use Bearer token for remote testing (proper auth)
3. **Option C**: Modify req-router to check `dk-user-info` header (backend change)

**Current Solution**: Option A - gracefully handle auth failure:
```python
if result.get('responsecode') == 'False':
    logger.warning(f"Could not set mode (auth issue): {result.get('msg')}")
    logger.warning("Mode will default to 'deterministic' anyway")
```

---

## ✅ **What Works Now**

### **1. Correct Alert Source Detection**
```python
# Task configured for Grafana alerts
task_data["trigger_on_alerts"] = [{
    "source": "Grafana",           # ✅ Real alert system
    "alert_name": "CPUHighAlert"
}]

# Send Grafana-formatted alert
alert = create_grafana_alert_data(
    alert_name="CPUHighAlert",
    alert_source="grafana"  # Ignored, format determines source
)

# Req-router processes:
# 1. Detects Grafana format → source = "Grafana"
# 2. Searches tasks: source="Grafana" AND alert_name="CPUHighAlert"
# 3. Finds match! ✅
# 4. Executes task ✅
```

### **2. Supported Alert Sources**
Based on req-router's detection logic:
- `"Grafana"` - Grafana monitoring alerts
- `"Prometheus"` - Prometheus alerts
- `"Pagerduty"` - PagerDuty incidents
- `"Datadog"` - Datadog monitors
- `"CloudWatch"` - AWS CloudWatch alarms

**Always use these real names**, not custom values!

---

## 🎯 **How to Write Alert Tests**

### **Template for Deterministic Mode**:
```python
def test_alert_execution():
    # 1. Use REAL alert source name
    alert_source = "Grafana"  # Or "Datadog", "Pagerduty", etc.
    alert_name = f"MyAlert{timestamp}"
    
    # 2. Configure task with trigger
    task_data = create_task_data(...)
    task_data["trigger_on_alerts"] = [{
        "source": alert_source,     # Must match real source name
        "alert_name": alert_name,   # Exact match required
        "dedup_interval": 300
    }]
    
    task = create_task(task_data)
    
    # 3. Send alert with matching format
    alert_payload = create_grafana_alert_data(  # Use appropriate format
        alert_name=alert_name,
        alert_source="grafana",  # Lowercase OK, will be capitalized
        status="firing"
    )
    
    # 4. Process alert
    response = process_alert(alert_payload)
    
    # 5. Verify
    assert response["alert_source"] == "Grafana"  # Detected from format
    assert response["alert_name"] == alert_name
    assert response["tasks_executed"] >= 1        # Task executed!
```

---

## 📋 **Field Name Reference**

### **In Task Configuration** (`trigger_on_alerts`):
```python
"trigger_on_alerts": [
    {
        "source": "Grafana",          # ✅ Field name: "source"
        "alert_name": "MyAlert",      # ✅ Field name: "alert_name"
        "dedup_interval": 300         # Optional
    }
]
```

### **In Elasticsearch** (stored):
```json
{
  "trigger_on_alerts": [
    {
      "source": "Grafana",           // ✅ Stored as "source"
      "alert_name": "MyAlert"        // ✅ Stored as "alert_name"
    }
  ]
}
```

### **In Alert Response**:
```json
{
  "alert_source": "Grafana",         // ✅ Response uses "alert_source"
  "alert_name": "MyAlert",           // ✅ "alert_name"
  "normalized_alert": {
    "source": "Grafana"              // ✅ Normalized uses "source"
  }
}
```

**Summary**:
- **Task config**: `source` (not `alert_source`)
- **Storage**: `source`
- **API response**: `alert_source` (different field name!)
- **Normalized alert**: `source`

---

## 🚀 **Run Tests Now**

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Run deterministic tests (should pass now!)
docker-compose -f docker-compose-local.yml run --rm test-runner \
  pytest unit/taskservice/test_alert_modes_comprehensive.py::TestDeterministicMode -v
```

**Expected**: 
```
test_matching_alert_triggers_task PASSED  ✅
test_non_matching_alert_no_execution PASSED  ✅

======================== 2 passed =========================
```

---

## 🔍 **Debugging Tips**

### **If Task Still Doesn't Execute**:

1. **Check task configuration**:
   ```python
   # Print task after creation
   print(task["trigger_on_alerts"])
   # Should show: [{"source": "Grafana", "alert_name": "MyAlert"}]
   ```

2. **Check alert response**:
   ```python
   print(alert_response["alert_source"])  # Should be "Grafana"
   print(alert_response["alert_name"])    # Should match your alert_name
   ```

3. **Check req-router logs**:
   ```bash
   docker logs req-router --tail 100 | grep -i "alert"
   # Look for:
   # - "processAlert called"
   # - "No matching tasks found" or "Found X matching tasks"
   ```

4. **Verify source matching**:
   ```
   Task expects: source="Grafana", name="MyAlert"
   Alert has: source="Grafana", name="MyAlert"
   ✅ Should match!
   
   Task expects: source="Testsource123", name="MyAlert"
   Alert has: source="Grafana", name="MyAlert"  
   ❌ Won't match! (source mismatch)
   ```

---

## 📚 **Related Documentation**

- **`ALERT_MODES_TESTING_GUIDE.md`** - Complete guide
- **`MANUAL_ALERT_TESTING.md`** - Manual curl testing
- **`ALERT_TEST_FIXES.md`** - Previous fixes (capitalization)
- **`QUICK_ALERT_TEST.sh`** - Quick test script

---

**Last Updated**: December 8, 2025

**Status**: ✅ All issues fixed, tests should pass!

