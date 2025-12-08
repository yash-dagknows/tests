# Quick Start: Testing Alert Handling Modes

**Get testing in 5 minutes!** 🚀

---

## 🎯 **What You'll Test**

Three alert handling modes:
1. **Deterministic** - Pre-configured tasks trigger on specific alerts (no AI)
2. **AI-Selected** - AI finds and selects best tooltask (requires AI)
3. **Autonomous** - AI launches full investigation (requires AI)

---

## ⚡ **Quick Start (3 Steps)**

### **Step 1: Set Environment**

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# For remote testing
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-bearer-token-here"
```

### **Step 2: Run Tests**

**Option A: All Modes (requires AI)**
```bash
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py -v
```

**Option B: Deterministic Only (no AI)**
```bash
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestDeterministicMode -v
```

### **Step 3: Check Results**

```
✅ PASSED = Mode works correctly
❌ FAILED = See troubleshooting below
⏭️  SKIPPED = Missing AI configuration (for AI tests)
```

---

## 🎓 **Example Run**

```bash
$ ./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestDeterministicMode -v

test_alert_modes_comprehensive.py::TestDeterministicMode::test_matching_alert_triggers_task PASSED
test_alert_modes_comprehensive.py::TestDeterministicMode::test_non_matching_alert_no_execution PASSED

======================== 2 passed in 5.3s =========================
```

---

## 🔍 **Test Breakdown**

### **Deterministic Mode Tests** (No AI Required)
```bash
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestDeterministicMode -v

# Tests:
# ✓ Alert with configured task → Task executes
# ✓ Alert with no matching task → No execution
```

### **AI-Selected Mode Tests** (AI Required)
```bash
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestAISelectedMode -v -m ai_required

# Tests:
# ✓ AI finds similar tooltask → Task executes
# ✓ No similar tooltask exists → No execution
```

### **Autonomous Mode Tests** (AI Required, Slow)
```bash
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestAutonomousMode -v -m "ai_required and slow"

# Tests:
# ✓ AI launches full troubleshooting session
# ✓ Creates runbook and child tasks
```

### **Configuration Tests** (No AI Required)
```bash
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestModeConfiguration -v

# Tests:
# ✓ Set and get incident_response_mode
# ✓ Invalid mode values rejected
```

### **Mode Switching Tests** (No AI Required)
```bash
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestModeSwitching -v

# Tests:
# ✓ Switching modes changes alert handling behavior
```

---

## 🐛 **Troubleshooting**

### **Problem: "Mode Not Set"**
```
AssertionError: Expected ai_selected mode, got: deterministic
```

**Fix**: Check bearer token has admin permissions
```bash
# Verify token
curl -X POST $DAGKNOWS_URL/getAdminSettingsFlags \
  -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
  -d '{}' | jq '.admin_settings.incident_response_mode'
```

### **Problem: "Task Not Executed"**
```
AssertionError: Expected task to execute, but tasks_executed=0
```

**Fix**: Check alert source capitalization
- Task configured with: `"Grafana"` (capitalized)
- Alert sent with: `"grafana"` → req-router capitalizes to `"Grafana"` ✓
- These should match!

### **Problem: "AI Tests Skipped"**
```
SKIPPED [1] ... AI configuration required
```

**Fix**: Configure OpenAI API key
```bash
# Check if LLM is configured
curl -X GET $DAGKNOWS_URL/api/health | jq '.llm_configured'

# Should return: true
```

### **Problem: "Connection Refused"**
```
requests.exceptions.ConnectionError: ... Connection refused
```

**Fix**: Verify URL is correct
```bash
# Check URL
echo $DAGKNOWS_URL

# Test connectivity
curl $DAGKNOWS_URL/api/health
```

---

## 📊 **What Each Test Does**

### **1. Deterministic - Matching Alert**
```
1. Creates task with trigger_on_alerts config
2. Sends alert that matches configuration
3. Verifies task executes
```

### **2. Deterministic - No Match**
```
1. Sends alert with no matching task
2. Verifies no task executes
```

### **3. AI-Selected - Similar Task**
```
1. Creates tooltask about "CPU investigation"
2. Sends alert about "CPU high usage"
3. AI finds task via similarity search
4. Verifies task executes
```

### **4. AI-Selected - No Similar Task**
```
1. Sends alert with unique description
2. AI searches but finds nothing
3. Verifies no task executes
```

### **5. Autonomous - Launch Session**
```
1. Sends alert with no deterministic match
2. AI launches troubleshooting session
3. Verifies runbook and child tasks created
```

### **6. Configuration - Set Mode**
```
1. Sets mode to each value
2. Verifies each mode can be configured
```

### **7. Mode Switching - Behavior Changes**
```
1. Tests same alert in different modes
2. Verifies mode affects behavior
```

---

## 🎯 **Common Commands**

```bash
# Set environment
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-token"

# Run deterministic tests (no AI)
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestDeterministicMode -v

# Run all tests with AI
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py -v

# Run with detailed output
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py -v -s --log-cli-level=INFO

# Skip AI tests
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py -v -m "not ai_required"
```

---

## 📚 **Next Steps**

1. ✅ Run deterministic tests first (simplest, no AI)
2. ✅ Verify alert handling works
3. ✅ Run configuration tests
4. ✅ If AI is configured, run AI-selected tests
5. ✅ If AI quota available, run autonomous tests

---

## 🔗 **More Information**

- **`ALERT_MODES_TESTING_GUIDE.md`** - Complete guide with all details
- **`MANUAL_ALERT_TESTING.md`** - Manual testing with curl commands
- **`QUICK_ALERT_TEST.sh`** - Quick bash script for deterministic testing

---

**Last Updated**: December 8, 2025

**Questions?** Check the comprehensive guide at `ALERT_MODES_TESTING_GUIDE.md`

