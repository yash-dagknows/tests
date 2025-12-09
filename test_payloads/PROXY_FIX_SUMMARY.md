# Critical Fix: Proxy Parameter for dev.dagknows.com

## 🔴 **The Problem**

Jobs were getting stuck in `SUBMITTED` stage because the test scripts were **missing the critical `?proxy=dev1` parameter** required by dev.dagknows.com deployment.

### **Before Fix:**
```bash
URL: https://dev.dagknows.com/processAlert  ❌
Result: Job ID = null, stuck in SUBMITTED
```

### **After Fix:**
```bash
URL: https://dev.dagknows.com/processAlert?proxy=dev1  ✅
Result: Job ID = Y0KGrmbxo7yDEEN3ffSO, executes properly
```

---

## 🔍 **Root Cause**

The working Python test scripts (`Test_Alert_Dev.py`, `test_alert_webhooks.py`) all had:

```python
QUERY_PARAMS = "?proxy=dev1"
url = f"{base_url}{endpoint}{query_params}"  # Includes ?proxy=dev1
```

But our bash scripts were calling:

```bash
curl -X POST "${BASE_URL}/processAlert"  # Missing ?proxy=dev1
```

---

## ✅ **The Fix**

### **All Scripts Updated:**

1. **test_deterministic_mode.sh**
2. **test_ai_selected_mode.sh**  
3. **test_autonomous_mode.sh**
4. **send_alert.sh**

### **What Changed:**

```bash
# Added proxy parameter
PROXY_PARAM="${DAGKNOWS_PROXY:-?proxy=dev1}"

# Updated all curl calls
curl -s -X POST "${BASE_URL}/processAlert${PROXY_PARAM}" \  # ✅ Now includes ?proxy=dev1
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${TOKEN}" \
    ...
```

---

## 📊 **Test Results**

### **Before Fix:**
```json
{
  "status": "success",
  "tasks_executed": 1,
  "executed_tasks": [{
    "task_id": "haZ5ypxQtnH5Q6EyszCQ",
    "job_id": null,                    // ❌ No job created
    "status": "triggered"
  }]
}
```
**Result**: Job stuck in SUBMITTED, never executes

### **After Fix:**
```json
{
  "status": "success",
  "tasks_executed": 1,
  "executed_tasks": [{
    "task_id": "haZ5ypxQtnH5Q6EyszCQ",
    "job_id": "Y0KGrmbxo7yDEEN3ffSO",  // ✅ Real job ID!
    "status": "triggered"
  }]
}
```
**Result**: Job executes successfully!

---

##  **Why is `?proxy=dev1` Needed?**

The dev.dagknows.com deployment uses a proxy/routing mechanism that requires this parameter to:
1. **Route requests** to the correct backend instance
2. **Create jobs** in the proper execution environment  
3. **Track execution** through the workflow engine

Without it:
- Requests reach the server ✅
- Alerts are normalized ✅
- Tasks are found ✅
- But jobs **never actually execute** ❌

---

## 🎯 **How to Use**

### **Scripts Now Work Out of the Box:**

```bash
cd tests/test_payloads

# No configuration needed - proxy parameter is hardcoded
./test_deterministic_mode.sh   # Uses ?proxy=dev1
./test_ai_selected_mode.sh     # Uses ?proxy=dev1  
./test_autonomous_mode.sh      # Uses ?proxy=dev1
./send_alert.sh grafana_alert_cpu.json  # Uses ?proxy=dev1
```

### **For Different Deployments:**

```bash
# Override proxy for different environment
export DAGKNOWS_PROXY="?proxy=prod1"
./test_deterministic_mode.sh

# Or no proxy for local testing
export DAGKNOWS_PROXY=""
./test_deterministic_mode.sh
```

---

## 📝 **Additional Improvements Made**

1. ✅ **Removed mode checking** - Users set mode via UI
2. ✅ **Removed cleanup logic** - Simpler scripts
3. ✅ **Removed task creation** - Users create tasks once via UI
4. ✅ **Added proxy parameter** - **Critical fix!**
5. ✅ **Better logging** - Shows full URL with proxy

---

## 🔄 **Comparison with Working Scripts**

### **Python Script Pattern (Working):**
```python
BASE_URL = "https://dev.dagknows.com"
ENDPOINT = "/processAlert"
QUERY_PARAMS = "?proxy=dev1"  # ← Always included
BEARER_TOKEN = "eyJhbGci..."

url = f"{BASE_URL}{ENDPOINT}{QUERY_PARAMS}"
# Result: https://dev.dagknows.com/processAlert?proxy=dev1 ✅
```

### **Bash Script Pattern (Now Fixed):**
```bash
BASE_URL="https://dev.dagknows.com"
TOKEN="eyJhbGci..."
PROXY_PARAM="?proxy=dev1"  # ← Now included!

curl -X POST "${BASE_URL}/processAlert${PROXY_PARAM}"
# Result: https://dev.dagknows.com/processAlert?proxy=dev1 ✅
```

---

## ✅ **Verification**

Test the fix:

```bash
cd tests/test_payloads
echo "" | ./test_deterministic_mode.sh
```

**Expected Output:**
```
✅ SUCCESS: Deterministic mode works!
Tasks Executed: 1
Job ID: Y0KGrmbxo7yDEEN3ffSO (actual job, not null!)
```

---

## 📚 **Reference Files**

Working examples that use `?proxy=dev1`:
- `test_payloads/Test_Alert_Dev.py`
- `test_payloads/Test_Alert_Dev_With_Workspace.py`
- `test_payloads/test_alert_webhooks.py`

Updated bash scripts:
- `test_payloads/test_deterministic_mode.sh` ✅
- `test_payloads/test_ai_selected_mode.sh` ✅
- `test_payloads/test_autonomous_mode.sh` ✅
- `test_payloads/send_alert.sh` ✅

---

## 🎉 **Status**

**✅ FIXED** - All test scripts now include the critical `?proxy=dev1` parameter!

Jobs are no longer stuck in SUBMITTED - they execute properly! 🚀

---

**Last Updated**: December 8, 2025  
**Fix Applied**: Added `PROXY_PARAM="?proxy=dev1"` to all test scripts

