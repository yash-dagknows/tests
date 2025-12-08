# Alert Handling Mode Tests

## 📋 Overview

This test suite validates the three alert handling modes in the DagKnows incident response system:

1. **Deterministic Mode** - Pre-configured tasks trigger on specific alerts
2. **AI-Selected Mode** - AI selects best task via similarity search + LLM
3. **Autonomous Mode** - AI launches full troubleshooting session

---

## 🎯 What Gets Tested

### Deterministic Mode
- ✅ Task execution when alert matches `trigger_on_alerts` configuration
- ✅ Alert stored with `selection_mode="deterministic"`
- ✅ Task linkage (`runbook_task_id`) properly recorded
- ✅ No execution when no matching task configured

### AI-Selected Mode  
- ✅ AI finds similar tooltasks via vector search
- ✅ LLM selects best task from candidates
- ✅ Alert stored with `selection_mode="ai_selected"`
- ✅ AI confidence, reasoning, and candidate tooltasks recorded
- ✅ Handling when no suitable task found

### Autonomous Mode
- ✅ AI troubleshooting session launched when no match
- ✅ Alert stored with `selection_mode="autonomous"`
- ✅ Runbook task and child task IDs captured
- ✅ High AI confidence recorded (full investigation)

### Alert Search & Stats
- ✅ Filtering alerts by `selection_mode`
- ✅ Statistics aggregation by selection mode
- ✅ Alert search by source, severity, status

---

## 🚀 Running the Tests

### Prerequisites

1. **Services Running**:
   ```bash
   # From dagknows_src/tests directory
   docker-compose -f docker-compose-local.yml up -d
   ```

2. **Configuration Required**:
   - Req-router must have `incident_response_mode` set
   - For AI-selected tests: `incident_response_mode = 'ai_selected'`
   - For autonomous tests: `incident_response_mode = 'autonomous'`

### Run All Alert Tests

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py -v
```

### Run Specific Test Classes

**Deterministic Mode Only**:
```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingDeterministic -v
```

**AI-Selected Mode Only**:
```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAISelected -v -m ai_required
```

**Autonomous Mode Only**:
```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAutonomous -v -m "ai_required and slow"
```

**Alert Search & Stats**:
```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertSearchAndStats -v
```

### Run Individual Tests

```bash
# Deterministic: Task execution on matching alert
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingDeterministic::test_deterministic_alert_triggers_configured_task -v

# AI-Selected: AI finds and executes task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAISelected::test_ai_selected_mode_finds_and_executes_task -v

# Autonomous: Full troubleshoot session
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAutonomous::test_autonomous_mode_launches_troubleshoot_session -v
```

---

## 📊 Test Markers

Tests use pytest markers for organization:

- **`@pytest.mark.ai_required`** - Tests that require AI/LLM integration
- **`@pytest.mark.slow`** - Tests that take longer (autonomous mode)

### Skip Tests Without AI

```bash
# Run only non-AI tests (deterministic mode)
pytest unit/taskservice/test_alert_handling_modes.py -v -m "not ai_required"
```

### Run Only AI Tests

```bash
# Run all AI-dependent tests
pytest unit/taskservice/test_alert_handling_modes.py -v -m "ai_required"
```

---

## 🔍 Understanding the Alert Flow

### Deterministic Mode Flow

```
1. Alert arrives at /processAlert endpoint
   ↓
2. Req-router searches for tasks with matching trigger_on_alerts
   ↓
3. If match found:
   → Execute configured task
   → Store alert with selection_mode="deterministic"
   ↓
4. If no match:
   → Check incident_response_mode (ai_selected or autonomous)
```

### AI-Selected Mode Flow

```
1. Alert arrives with no deterministic match
   ↓
2. incident_response_mode = 'ai_selected'
   ↓
3. Search for tooltasks with similarity >= 0.7
   ↓
4. If tooltasks found:
   → LLM selects best task
   → LLM generates input parameters
   → Execute selected task
   → Store alert with selection_mode="ai_selected"
   ↓
5. If no suitable tooltask:
   → Store alert with selection_mode="none"
```

### Autonomous Mode Flow

```
1. Alert arrives with no deterministic match
   ↓
2. incident_response_mode = 'autonomous'
   ↓
3. Launch AI troubleshooting session
   → AI investigates issue
   → AI generates resolution steps
   → AI executes remediation
   ↓
4. Store alert with selection_mode="autonomous"
```

---

## 🛠️ Test Data Helpers

### Creating Alerts

```python
# Grafana-style alert
alert = test_data_factory.create_grafana_alert_data(
    alert_name="HighCPU",
    alert_source="grafana",
    status="firing",
    severity="critical",
    description="CPU usage over 90%"
)

# PagerDuty-style alert
alert = test_data_factory.create_pagerduty_alert_data(
    alert_name="ServiceDown",
    alert_source="pagerduty",
    event_type="incident.triggered",
    urgency="high"
)
```

### Sending Alerts

```python
# Process alert through req-router
response = req_router_client.process_alert(alert)

# Search for alerts
alerts = req_router_client.search_alerts(
    params={
        "source": "grafana",
        "selection_mode": "deterministic",
        "severity": "critical"
    }
)

# Get alert stats
stats = req_router_client.get_alert_stats()
```

### Creating Tasks with Alert Triggers

```python
# Task that triggers on specific alert
task_data = test_data_factory.create_task_data(
    title="CPU Remediation",
    script_type="python"
)

task_data["trigger_on_alerts"] = [
    {
        "alert_source": "grafana",
        "alert_name": "HighCPU",
        "dedup_interval": 300  # 5 minutes
    }
]

task = taskservice_client.create_task(task_data)
```

---

## 📝 Alert Fields Reference

### Key Alert Fields

| Field | Type | Description |
|-------|------|-------------|
| `selection_mode` | string | How task was selected: `deterministic`, `ai_selected`, `autonomous`, `none` |
| `incident_response_mode` | string | Configured mode: `deterministic`, `ai_selected`, `autonomous` |
| `runbook_task_id` | string | ID of executed task |
| `primary_job_id` | string | ID of job execution |
| `ai_selected` | boolean | Whether AI was used for selection |
| `ai_confidence` | float | AI confidence score (0-1) |
| `ai_reasoning` | string | AI's reasoning for task selection |
| `ai_candidate_tooltasks` | array | Tasks AI considered |
| `execution_status` | string | Job execution status |
| `status` | string | Alert status: `firing`, `resolved` |
| `severity` | string | Alert severity: `critical`, `warning`, `info` |
| `source` | string | Alert source system |

---

## 🎨 Expected Test Output

### Successful Deterministic Test

```
unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingDeterministic::test_deterministic_alert_triggers_configured_task 
INFO Created task ABC123 for deterministic alert handling
INFO Alert response: {'status': 'success', 'tasks_executed': 1, ...}
INFO ✅ Deterministic mode test passed: task ABC123 triggered by alert
PASSED [100%]
```

### Successful AI-Selected Test

```
unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAISelected::test_ai_selected_mode_finds_and_executes_task 
INFO Created tooltask XYZ789 for AI selection
INFO Alert response (AI-selected): {'status': 'success', ...}
INFO Selection mode: ai_selected
INFO ✅ AI-selected mode test passed: AI selected task with 0.85 confidence
PASSED [100%]
```

### Skipped Test (Mode Not Configured)

```
unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAISelected::test_ai_selected_mode_finds_and_executes_task 
WARNING AI-selected mode not used (mode: none). This may indicate incident_response_mode is not set to 'ai_selected'
SKIPPED [100%]
```

---

## ⚠️ Common Issues & Solutions

### Issue: Tests Skip with "Mode Not Configured"

**Problem**: `incident_response_mode` not set correctly in req-router

**Solution**:
```bash
# Check req-router configuration
docker logs req-router | grep incident_response_mode

# Or check environment variables
docker exec req-router env | grep INCIDENT_RESPONSE_MODE
```

### Issue: AI Tests Fail with "No LLM Available"

**Problem**: LLM service not accessible or API keys not set

**Solution**:
```bash
# Check if LLM service is configured
docker logs req-router | grep -i "llm\|openai\|anthropic"

# Verify API keys are set
docker exec req-router env | grep -i "api_key\|openai\|anthropic"
```

### Issue: Alerts Not Found in Search

**Problem**: Elasticsearch indexing delay

**Solution**: Tests already include `time.sleep(2)` waits. If still failing, increase sleep time or check Elasticsearch health:
```bash
curl http://localhost:9200/_cluster/health
```

### Issue: DELETE Cleanup Fails

**Problem**: Known backend issue (see `BACKEND_DELETE_BUG.md`)

**Solution**: Tests handle cleanup failures gracefully with try/except. Cleanup failures don't fail the test.

---

## 📈 Success Criteria

### Deterministic Mode
- ✅ Task executes when alert matches `trigger_on_alerts`
- ✅ `selection_mode="deterministic"` in stored alert
- ✅ `runbook_task_id` links to executed task
- ✅ No false positives (unmatched alerts don't execute)

### AI-Selected Mode
- ✅ AI finds tooltasks with similarity >= 0.7
- ✅ LLM successfully selects best task
- ✅ `selection_mode="ai_selected"` in stored alert
- ✅ AI fields populated (confidence, reasoning, candidates)
- ✅ Selected task executes successfully

### Autonomous Mode
- ✅ Troubleshoot session launches
- ✅ `selection_mode="autonomous"` in stored alert
- ✅ `runbook_task_id` and `child_task_id` created
- ✅ AI confidence >= 0.9 (full investigation)

---

## 🔗 Related Documentation

- **`TEST_COMMANDS_REFERENCE.md`** - Complete test command reference
- **`LOCAL_TESTING_GUIDE.md`** - Setup and configuration guide
- **`BACKEND_DELETE_BUG.md`** - Known DELETE endpoint issue
- **`tests/utils/fixtures.py`** - Test data factory methods
- **`tests/utils/api_client.py`** - API client methods

---

## 📞 Support

For questions about alert handling modes:
1. Check req-router logs: `docker logs req-router --tail 100`
2. Check taskservice logs: `docker logs taskservice --tail 100`
3. Verify Elasticsearch health: `curl http://localhost:9200/_cluster/health`
4. Review alert processing flow in `/Users/yashyaadav/dag_workspace/dagknows_src/req_router/src/req_router.py` (lines 2493-2850)

---

**Last Updated**: December 8, 2025
**Test File**: `tests/unit/taskservice/test_alert_handling_modes.py`
**Test Count**: 8 tests across 3 modes

