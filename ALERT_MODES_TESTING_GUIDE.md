# Comprehensive Alert Modes Testing Guide

Complete guide for testing all three incident response modes for alert handling.

---

## 🎯 **Three Alert Handling Modes**

DagKnows supports three modes for handling incoming alerts:

| Mode | Description | When Used | AI Required |
|------|-------------|-----------|-------------|
| **Deterministic** | Tasks explicitly configured with `trigger_on_alerts` | Production, known issues | No |
| **AI-Selected** | AI searches for similar tooltasks and selects best match | Semi-automated | Yes |
| **Autonomous** | AI launches full investigation and troubleshooting | Fully automated | Yes |

---

## 🔧 **Configuration**

### **Setting the Mode**

The incident response mode is stored in admin settings and can be configured via:

1. **UI** (Admin Settings page):
   ```
   Settings → Incident Response Mode → Select mode → Save
   ```

2. **API** (programmatic):
   ```bash
   curl -X POST https://44.224.1.45/setFlags \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
     -d '{"incident_response_mode": "deterministic"}'
   ```

3. **Python Test Client**:
   ```python
   req_router_client.set_incident_response_mode('ai_selected')
   ```

### **Valid Mode Values**

- `"deterministic"` - Default mode, requires pre-configured tasks
- `"ai_selected"` - AI searches and selects best task
- `"autonomous"` - AI launches full troubleshooting

---

## 📁 **Test Files**

### **New Comprehensive Test Suite**

**`tests/unit/taskservice/test_alert_modes_comprehensive.py`**
- ✅ Properly sets incident_response_mode before each test class
- ✅ Tests all three modes with realistic scenarios
- ✅ Verifies mode switching works correctly
- ✅ Handles cleanup properly
- ✅ Uses class-scoped fixtures for mode setup

**Test Classes**:
1. `TestDeterministicMode` - Tests deterministic alert matching
2. `TestAISelectedMode` - Tests AI task selection (AI required)
3. `TestAutonomousMode` - Tests autonomous troubleshooting (AI required)
4. `TestModeConfiguration` - Tests mode configuration API
5. `TestModeSwitching` - Tests switching between modes

---

## 🚀 **Running the Tests**

### **Prerequisites**

1. **For Deterministic Mode Tests**:
   - DagKnows deployment (local or remote)
   - Bearer token (if remote)
   - No AI/LLM required

2. **For AI-Selected Mode Tests**:
   - Valid OpenAI API key or LLM configuration
   - LLM model accessible (e.g., gpt-4o)
   - Mark: `@pytest.mark.ai_required`

3. **For Autonomous Mode Tests**:
   - Valid OpenAI API key or LLM configuration
   - Sufficient LLM quota
   - Mark: `@pytest.mark.ai_required` + `@pytest.mark.slow`

### **Run All Tests**

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Local Docker
docker-compose -f docker-compose-local.yml run --rm test-runner \
  pytest unit/taskservice/test_alert_modes_comprehensive.py -v

# Remote Deployment
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-token"
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py -v
```

### **Run by Mode**

```bash
# Deterministic mode only (no AI required)
pytest unit/taskservice/test_alert_modes_comprehensive.py::TestDeterministicMode -v

# AI-Selected mode
pytest unit/taskservice/test_alert_modes_comprehensive.py::TestAISelectedMode -v -m ai_required

# Autonomous mode
pytest unit/taskservice/test_alert_modes_comprehensive.py::TestAutonomousMode -v -m "ai_required and slow"

# Configuration tests
pytest unit/taskservice/test_alert_modes_comprehensive.py::TestModeConfiguration -v
```

### **Skip AI Tests**

```bash
# Run only deterministic tests (no AI)
pytest unit/taskservice/test_alert_modes_comprehensive.py -v -m "not ai_required"
```

### **Run with Detailed Logging**

```bash
pytest unit/taskservice/test_alert_modes_comprehensive.py -v -s --log-cli-level=INFO
```

---

## 📊 **Test Scenarios**

### **1. Deterministic Mode**

**Scenario A: Matching Alert Triggers Task**
```
Setup:
  - Mode: deterministic
  - Task configured: alert_source="Grafana", alert_name="CPUHighAlert"

Action:
  - Send alert: alertname="CPUHighAlert", source=grafana

Expected:
  ✓ Task executes
  ✓ incident_response_mode="deterministic"
  ✓ tasks_executed >= 1
```

**Scenario B: Non-Matching Alert**
```
Setup:
  - Mode: deterministic
  - No matching task configured

Action:
  - Send alert: alertname="UnknownAlert"

Expected:
  ✓ No task executes
  ✓ incident_response_mode="deterministic"
  ✓ tasks_executed = 0
```

---

### **2. AI-Selected Mode**

**Scenario A: AI Finds Similar Task**
```
Setup:
  - Mode: ai_selected
  - Tooltask exists about "CPU performance investigation"
  - No deterministic match

Action:
  - Send alert: "Server CPU at 95%, causing slowness"

Expected:
  ✓ AI searches for similar tasks (KNN search)
  ✓ AI selects most relevant task
  ✓ Task executes
  ✓ incident_response_mode="ai_selected"
  ✓ ai_selection_attempted=true
  ✓ Response includes AI reasoning
```

**Scenario B: No Similar Task Found**
```
Setup:
  - Mode: ai_selected
  - No similar tooltasks exist

Action:
  - Send alert with unique description

Expected:
  ✓ AI searches but finds nothing (similarity < 0.7)
  ✓ No task executes
  ✓ incident_response_mode="ai_selected"
  ✓ ai_selection_attempted=true
```

---

### **3. Autonomous Mode**

**Scenario: AI Launches Investigation**
```
Setup:
  - Mode: autonomous
  - No deterministic match

Action:
  - Send alert: "Database query slow, 400% degradation"

Expected:
  ✓ AI analyzes alert
  ✓ AI creates runbook task
  ✓ AI creates child investigation task
  ✓ AI starts troubleshooting session
  ✓ incident_response_mode="autonomous"
  ✓ Response includes runbook_task_id and child_task_id
```

---

## 🎯 **Key Test Validations**

Each test validates:

1. **Mode Configuration**: `incident_response_mode` is correctly set
2. **Alert Processing**: Alert is accepted and processed
3. **Task Execution**: Correct tasks execute (or don't execute)
4. **Response Structure**: Proper fields in response
5. **Cleanup**: Tasks and alerts cleaned up properly

---

## 🔑 **Alert Source Capitalization**

⚠️ **CRITICAL**: Req-router capitalizes alert sources using `.title()`

```python
# What you send
alert_source = "grafana"

# What req-router sees
alert_source = "Grafana"

# Task configuration MUST match
trigger_on_alerts = [{
    "alert_source": "Grafana",  # ✅ Capitalized
    "alert_name": "MyAlert"
}]
```

**Best Practice**:
- Use simple, lowercase source names: `"grafana"`, `"datadog"`, `"cloudwatch"`
- Avoid underscores: `"my_source"` → `"My_Source"` (problematic!)
- Configure tasks with `.title()` capitalization

---

## 🐛 **Troubleshooting**

### **Tests Failing**

1. **Mode Not Set**
   ```
   Error: Expected ai_selected mode, got: deterministic
   
   Fix: Check that setFlags API is accessible
   - Verify bearer token has admin permissions
   - Check req-router logs for setFlags calls
   ```

2. **AI Tests Failing**
   ```
   Error: No task executed in AI-selected mode
   
   Fix: Verify AI/LLM is configured
   - Check OpenAI API key in environment
   - Verify LLM model is available (gpt-4o)
   - Check req-router logs for LLM calls
   ```

3. **Tasks Not Executing in Deterministic Mode**
   ```
   Error: tasks_executed=0 but task is configured
   
   Fix: Check alert source capitalization
   - Task config: "Grafana"
   - Alert sent: "grafana" → becomes "Grafana" ✓
   - Verify exact alert_name match
   ```

4. **Autonomous Mode Not Launching**
   ```
   Error: No runbook_task_id in response
   
   Fix: Check troubleshoot endpoint
   - Verify /api/v1/tasks/troubleshoot is accessible
   - Check req-router logs for troubleshoot calls
   - Verify AI quota not exceeded
   ```

### **Checking Current Mode**

```bash
# Via API
curl -X POST https://44.224.1.45/getAdminSettingsFlags \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
  -d '{}' | jq '.admin_settings.incident_response_mode'

# Via Python
settings = req_router_client.get_admin_settings()
mode = settings.get("admin_settings", {}).get("incident_response_mode")
print(f"Current mode: {mode}")
```

### **Checking Req-Router Logs**

```bash
# Local Docker
docker logs req-router --tail 100 | grep -i "incident_response_mode"

# Look for:
# - "Incident response mode: deterministic"
# - "AI-selected mode enabled, searching for matching tooltasks"
# - "Autonomous mode enabled, launching troubleshoot session"
```

---

## 📈 **Test Execution Order**

Tests are ordered to minimize interference:

1. ✅ `TestDeterministicMode` (Order 1) - Basic functionality
2. ✅ `TestAISelectedMode` (Order 2) - AI features
3. ✅ `TestAutonomousMode` (Order 3) - Full AI session
4. ✅ `TestModeConfiguration` (Order 4) - Config API
5. ✅ `TestModeSwitching` (Order 5) - Mode transitions

Each test class:
- Sets its required mode in `setup_mode` fixture
- Runs its tests
- Restores to default (deterministic) in teardown

---

## 🎓 **Example Test Run**

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Set up environment
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="eyJhbGci..."

# Run comprehensive tests
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py -v

# Expected Output:
# test_alert_modes_comprehensive.py::TestDeterministicMode::test_matching_alert_triggers_task PASSED
# test_alert_modes_comprehensive.py::TestDeterministicMode::test_non_matching_alert_no_execution PASSED
# test_alert_modes_comprehensive.py::TestAISelectedMode::test_ai_finds_similar_task PASSED
# test_alert_modes_comprehensive.py::TestAISelectedMode::test_ai_mode_no_similar_task PASSED
# test_alert_modes_comprehensive.py::TestAutonomousMode::test_autonomous_troubleshoot_session_launches PASSED
# test_alert_modes_comprehensive.py::TestModeConfiguration::test_set_and_get_incident_response_mode PASSED
# test_alert_modes_comprehensive.py::TestModeConfiguration::test_invalid_mode_rejected PASSED
# test_alert_modes_comprehensive.py::TestModeSwitching::test_mode_affects_alert_handling PASSED
# 
# ======================== 8 passed in 45.2s =========================
```

---

## 📚 **Related Documentation**

- **`MANUAL_ALERT_TESTING.md`** - Manual curl testing
- **`ALERT_TEST_FIXES.md`** - Known issues and fixes
- **`QUICK_START_ALERT_TESTS.md`** - Quick start guide
- **`test_alert_handling_modes.py`** - Original test file (deprecated by comprehensive version)

---

## ✅ **Checklist for Running Tests**

- [ ] DagKnows deployment is running
- [ ] Bearer token is set (`DAGKNOWS_TOKEN`)
- [ ] Base URL is correct (`DAGKNOWS_URL`)
- [ ] For AI tests: OpenAI API key is configured
- [ ] For AI tests: LLM model is accessible
- [ ] Admin permissions on token (for setFlags)
- [ ] Tests directory: `/Users/yashyaadav/dag_workspace/dagknows_src/tests`

---

**Last Updated**: December 8, 2025

