# Alert Handling Modes Testing 🚀

Complete automated testing for DagKnows alert handling in all three modes.

---

## 🎯 **Quick Start**

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-token"

# Run deterministic mode tests (no AI required)
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestDeterministicMode -v
```

**Expected**: 2 tests pass in ~5 seconds ✅

---

## 📚 **Documentation**

| File | Purpose | Read Time |
|------|---------|-----------|
| **`QUICK_START_ALERT_MODES.md`** | Get started in 5 minutes | 3 min |
| **`ALERT_MODES_TESTING_GUIDE.md`** | Complete guide with all details | 15 min |
| **`MANUAL_ALERT_TESTING.md`** | Manual testing with curl | 10 min |
| **`ALERT_MODES_IMPLEMENTATION_SUMMARY.md`** | Implementation details | 5 min |

**Start here** → `QUICK_START_ALERT_MODES.md`

---

## 🧪 **What's Tested**

### **1. Deterministic Mode** (No AI required)
- ✅ Pre-configured tasks trigger on specific alerts
- ✅ Non-matching alerts don't execute

### **2. AI-Selected Mode** (AI required)
- ✅ AI finds and selects similar tooltask
- ✅ No execution when no similar task exists

### **3. Autonomous Mode** (AI required)
- ✅ AI launches full troubleshooting session
- ✅ Creates runbook and investigation tasks

### **4. Configuration** (No AI required)
- ✅ Set and get incident_response_mode
- ✅ Invalid modes are rejected

### **5. Mode Switching** (No AI required)
- ✅ Switching modes changes behavior

---

## 🏃 **Run Commands**

```bash
# All tests (8 tests)
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py -v

# Deterministic only (2 tests, no AI)
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestDeterministicMode -v

# AI-Selected (2 tests, AI required)
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestAISelectedMode -v

# Autonomous (1 test, AI required)
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestAutonomousMode -v

# Configuration (2 tests, no AI)
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestModeConfiguration -v

# Mode switching (1 test, no AI)
./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py::TestModeSwitching -v
```

---

## 🎓 **Example Output**

```bash
$ ./run_remote_tests.sh unit/taskservice/test_alert_modes_comprehensive.py -v

test_alert_modes_comprehensive.py::TestDeterministicMode::test_matching_alert_triggers_task PASSED
test_alert_modes_comprehensive.py::TestDeterministicMode::test_non_matching_alert_no_execution PASSED
test_alert_modes_comprehensive.py::TestAISelectedMode::test_ai_finds_similar_task PASSED
test_alert_modes_comprehensive.py::TestAISelectedMode::test_ai_mode_no_similar_task PASSED
test_alert_modes_comprehensive.py::TestAutonomousMode::test_autonomous_troubleshoot_session_launches PASSED
test_alert_modes_comprehensive.py::TestModeConfiguration::test_set_and_get_incident_response_mode PASSED
test_alert_modes_comprehensive.py::TestModeConfiguration::test_invalid_mode_rejected PASSED
test_alert_modes_comprehensive.py::TestModeSwitching::test_mode_affects_alert_handling PASSED

======================== 8 passed in 45.2s =========================
```

---

## 🛠️ **How It Works**

1. **Test Class Sets Mode**
   - Each test class configures its required mode via `setFlags` API
   - Mode is set before tests run
   - Mode is restored after tests complete

2. **Tests Run**
   - Create tasks with alert configurations
   - Send alerts to `/processAlert` endpoint
   - Verify correct mode and behavior
   - Clean up tasks

3. **Results Validated**
   - Check `incident_response_mode` in response
   - Verify task execution counts
   - Validate AI metadata when applicable

---

## 🔑 **Key Features**

- ✅ **Proper Mode Configuration** - Each test class sets its mode
- ✅ **Alert Source Capitalization** - Handles `.title()` capitalization
- ✅ **Clean Setup/Teardown** - Proper cleanup even on failure
- ✅ **Detailed Validation** - Checks all response fields
- ✅ **Markers for Filtering** - `ai_required`, `slow` markers
- ✅ **Works Local & Remote** - Docker or remote deployment

---

## 🐛 **Troubleshooting**

| Problem | Solution |
|---------|----------|
| Mode not setting | Check bearer token has admin permissions |
| Task not executing | Check alert source capitalization |
| AI tests failing | Verify OpenAI API key configured |
| Connection refused | Verify `DAGKNOWS_URL` is correct |

**Need more help?** → See `ALERT_MODES_TESTING_GUIDE.md`

---

## 📋 **Files Created**

- ✅ `test_alert_modes_comprehensive.py` - Complete test suite (8 tests)
- ✅ `ALERT_MODES_TESTING_GUIDE.md` - Comprehensive guide
- ✅ `QUICK_START_ALERT_MODES.md` - Quick start (5 min)
- ✅ `ALERT_MODES_IMPLEMENTATION_SUMMARY.md` - Implementation details
- ✅ `README_ALERT_MODES.md` - This file

---

## ✨ **Benefits**

- **Automated** - No manual configuration needed
- **Repeatable** - Tests set their own mode
- **Comprehensive** - All 3 modes covered
- **Production-Ready** - Proper error handling
- **Well-Documented** - Multiple guides included

---

## 🚦 **Next Steps**

1. ✅ Read `QUICK_START_ALERT_MODES.md` (3 min)
2. ✅ Run deterministic tests (5 min)
3. ✅ If passing, run all tests (1 min)
4. ✅ If AI configured, verify AI tests pass
5. ✅ Add to CI/CD pipeline

---

## 📖 **Learn More**

- **Alert Payloads** → `MANUAL_ALERT_TESTING.md`
- **Troubleshooting** → `ALERT_MODES_TESTING_GUIDE.md` (section 🐛)
- **Test Details** → `ALERT_MODES_IMPLEMENTATION_SUMMARY.md`
- **Quick Test Script** → `QUICK_ALERT_TEST.sh`

---

**Ready to test?** Start with `QUICK_START_ALERT_MODES.md` 🎯

