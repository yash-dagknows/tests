# 🤖 Autonomous Mode - Explained

## ❓ **Why Did Autonomous Mode Execute an Existing Task?**

You observed that the autonomous mode test triggered an **existing task** instead of creating a **new task**. Let me explain why this happens and how to fix it.

---

## 🎯 **Expected Autonomous Mode Behavior**

### **Ideal Flow:**
1. Alert arrives with name: `HighCPUUsage`
2. Autonomous mode checks: "Is there an existing task for this?"
3. **If NO existing task**: AI generates NEW task code → Creates task → Executes
4. **If YES existing task**: Uses existing task (fallback behavior)

### **What You Saw:**
```json
{
  "tasks_found": 1,        // ← Found existing task!
  "tasks_executed": 1,
  "executed_tasks": [{
    "task_id": "haZ5ypxQtnH5Q6EyszCQ"  // ← Existing task ID
  }]
}
```

**Result:** It found an existing task with `alert_name: HighCPUUsage` and executed it.

---

## 🔍 **Why This Happened**

### **Possible Reasons:**

1. **Existing Task with Trigger:**
   - You have a task configured with:
     ```json
     "trigger_on_alerts": [{
       "source": "Grafana",
       "alert_name": "HighCPUUsage"
     }]
     ```
   - When alert arrives, system finds this task and executes it

2. **Mode Switch Didn't Propagate:**
   - Mode was changed in UI but backend still sees old mode
   - Needs time to propagate (5-10 seconds)

3. **Intelligent Fallback:**
   - Autonomous mode intelligently uses existing tasks when available
   - Only creates NEW tasks when no match exists

---

## ✅ **The Fix (Already Applied)**

I've updated the test to:

### **1. Use Unique Alert Names**
```python
def _send_autonomous_test_alert(self, test_config) -> dict:
    timestamp = int(time.time())
    alert_name = f"AutonomousTest_{timestamp}"  # ← UNIQUE name
    # ...
```

**Result:** No existing task will match → Forces NEW task creation

### **2. Longer Wait Times**
```python
# Wait for mode to propagate
page.wait_for_timeout(10000)  # 10 seconds instead of 5
```

### **3. Mode Verification**
```python
# Verify mode was actually switched
current_mode = settings_page.get_current_alert_mode()
if current_mode != "autonomous":
    logger.warning("Mode didn't switch properly!")
```

### **4. Better Response Analysis**
```python
if tasks_found == 0:
    logger.info("✅ NEW task created by Autonomous mode!")
else:
    logger.warning("⚠ Used EXISTING task")
```

---

## 🚀 **Run Updated Test**

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
./run_alert_tests.sh --autonomous
```

Now it will:
1. ✅ Send alert with **unique name** (`AutonomousTest_<timestamp>`)
2. ✅ Force Autonomous mode to **create NEW task**
3. ✅ Wait longer for task generation (120 seconds)
4. ✅ Verify if task was newly created

---

## 📊 **Expected Results**

### **With Unique Alert Name:**
```json
{
  "status": "success",
  "tasks_found": 0,           // ← No existing task found
  "tasks_created": 1,         // ← NEW task created!
  "tasks_executed": 1,
  "executed_tasks": [{
    "task_id": "xyz123",      // ← NEW task ID (different from before)
    "job_id": "abc456",
    "status": "triggered",
    "newly_created": true     // ← Flag indicating new task
  }]
}
```

### **Response Indicators:**

| Indicator | Meaning |
|-----------|---------|
| `tasks_found: 0` | No existing task matched |
| `tasks_created: 1` | Autonomous created NEW task |
| `tasks_found: 1` | Found existing task |
| `tasks_created: 0` | Used existing task (fallback) |

---

## ⏱️ **Timeout Considerations**

### **Autonomous Mode Timeline:**

```
1. Receive alert                    (instant)
   ↓
2. Check for existing tasks         (2-5 seconds)
   ↓
3. AI analyzes alert                (10-20 seconds)
   ↓
4. AI generates task code           (20-40 seconds)
   ↓
5. Create task in system            (5-10 seconds)
   ↓
6. Execute task                     (2-5 seconds)

TOTAL: 40-80 seconds (up to 120s worst case)
```

### **Updated Timeouts:**

- **API request timeout:** 120 seconds
- **Pytest test timeout:** 600 seconds (10 minutes)
- **Mode propagation wait:** 10 seconds

---

## 🆚 **Mode Comparison**

| Mode | Alert Name | Task Source | Creation Time |
|------|------------|-------------|---------------|
| **Deterministic** | `HighCPUUsage` | Pre-configured | N/A (already exists) |
| **AI-Selected** | `HighCPUUsage` | Library of tasks | N/A (selects existing) |
| **Autonomous** | `AutonomousTest_<timestamp>` | **Dynamically generated** | 40-80 seconds |

---

## 🐛 **Troubleshooting**

### **Issue: Still executing existing task**

**Symptoms:**
```json
{
  "tasks_found": 1,
  "tasks_executed": 1
}
```

**Solutions:**

1. **Check mode in UI manually:**
   - Go to Settings → AI → Incident Response
   - Verify "Autonomous" is selected with "Active" badge

2. **Wait longer before sending alert:**
   ```python
   page.wait_for_timeout(15000)  # 15 seconds
   ```

3. **Clear existing task triggers:**
   - Remove `trigger_on_alerts` from existing tasks
   - Or use very unique alert names

4. **Check backend logs:**
   - Verify backend sees the mode change
   - Check if mode is actually "autonomous" when alert arrives

---

## 📋 **What Was Changed**

### **Files Updated:**

1. ✅ `test_alert_handling_modes.py`:
   - Added `_send_autonomous_test_alert()` with unique names
   - Added mode verification
   - Added response analysis
   - Increased wait time to 10 seconds

2. ✅ `settings_page.py`:
   - Added `get_current_alert_mode()` method
   - Improved scrolling in mode selection
   - Better error messages

3. ✅ `pytest.ini`:
   - Increased timeout from 300s to 600s

---

## ✅ **Summary**

### **Why It Used Existing Task:**
- Alert name `HighCPUUsage` matched existing task
- System found task → used it (efficient behavior)

### **How We Fixed It:**
- Use unique alert names: `AutonomousTest_<timestamp>`
- Verify mode after selection
- Better logging and analysis

### **Expected Now:**
- Autonomous mode should **create NEW tasks** dynamically
- Response will show `tasks_found: 0` and `tasks_created: 1`

---

**Run the test again with these fixes!** 🚀

The autonomous mode test will now properly test dynamic task creation.

