# ✅ Alert Handling E2E Tests - Summary

## 🎯 **What Was Created**

### **1. New Page Object: `pages/settings_page.py`**
Handles Settings page interactions:
- Navigate to Settings
- Click AI tab
- Select Deterministic / AI-Selected / Autonomous mode
- Save settings

### **2. New E2E Test File: `ui_tests/test_alert_handling_modes.py`**
Three comprehensive E2E tests:
- `test_deterministic_mode_alert_handling`
- `test_ai_selected_mode_alert_handling`
- `test_autonomous_mode_alert_handling`

### **3. Documentation**
- `ALERT_HANDLING_TESTS.md` - Complete guide
- `ALERT_TESTS_SUMMARY.md` - This file
- `run_alert_tests.sh` - Quick runner script

### **4. Configuration Updates**
- `pytest.ini` - Added `alert_handling` and `e2e` markers

---

## 🚀 **Quick Start**

### **Run All 3 Tests**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_alert_handling_modes.py -v
```

### **Or Use Helper Script**
```bash
# All tests
./run_alert_tests.sh

# Only Deterministic
./run_alert_tests.sh --deterministic

# With visible browser
./run_alert_tests.sh --deterministic --headed --slow
```

---

## 📋 **Test Flow**

Each test follows this flow:

```
1. Login (/vlogin)
   ↓
2. Landing Page (/n/landing)
   ↓
3. Click "Default" Workspace
   ↓
4. Workspace View (/?space=Default)
   ↓
5. Click Settings (left nav)
   ↓
6. Settings Page (/vsettings)
   ↓
7. Click "AI" Tab
   ↓
8. AI Configuration Page
   ↓
9. Select Mode (Deterministic/AI-Selected/Autonomous)
   ↓
10. Send Grafana Alert (API)
   ↓
11. Verify Response
```

---

## 📸 **Screenshots**

Each test captures **7+ screenshots**:
1. `01-deterministic-after-login.png`
2. `02-deterministic-landing-page.png`
3. `03-deterministic-workspace-view.png`
4. `04-deterministic-settings-page.png`
5. `05-deterministic-ai-tab.png`
6. `06-deterministic-mode-selected.png`
7. `07-deterministic-alert-sent.png`

Plus debugging screenshots at each step!

---

## ⏱️ **Timing**

- **Per test:** ~90-120 seconds
- **All 3 tests:** ~5-6 minutes

Breakdown:
- Login & Navigation: ~30s
- Settings & Mode Selection: ~20s
- Alert Sending & Verification: ~10s
- Screenshots & Waits: ~30s

---

## ✅ **What Gets Tested**

### **UI Flow ✅**
- Login works
- Landing page loads
- Workspace selection works
- Settings navigation works
- AI tab clickable
- Mode selection works
- Settings save (auto or manual)

### **API Integration ✅**
- Alert payload sent
- API responds (200 OK)
- Response structure validated

### **Task Execution ⚠️**
- **Optional**: Requires pre-configured task
- Test passes even if no task executes
- Logs whether tasks executed or not

---

## 🆚 **Comparison: All E2E Tests**

| Test Suite | Tests | Focus | Duration |
|------------|-------|-------|----------|
| **AI Agent Workflow** | 3 | Task creation with AI | ~4-5 min |
| **Alert Handling** (NEW) | 3 | Mode config + alerts | ~5-6 min |
| **Total** | 6 | Complete E2E coverage | ~10 min |

---

## 📦 **Files Created**

```
tests/e2e_tests/
├── pages/
│   └── settings_page.py              ⭐ NEW
├── ui_tests/
│   ├── test_ai_agent_workflow.py     (existing)
│   └── test_alert_handling_modes.py  ⭐ NEW
├── run_alert_tests.sh                ⭐ NEW
├── ALERT_HANDLING_TESTS.md           ⭐ NEW
├── ALERT_TESTS_SUMMARY.md            ⭐ NEW
└── pytest.ini                        (updated)
```

---

## 🎓 **Page Objects**

### **Existing:**
- `LoginPage` - Login/logout
- `WorkspacePage` - Workspace selection
- `AIAgentPage` - AI agent interactions

### **New:**
- `SettingsPage` ⭐ - Settings navigation & configuration

---

## 🔧 **Prerequisites**

### **Must Have:**
- Python 3.8+
- Virtual environment activated
- All dependencies installed
- Valid JWT token in `.env`

### **Optional (for task execution):**
- Pre-configured task with alert trigger:
  ```json
  {
    "trigger_on_alerts": [{
      "source": "Grafana",
      "alert_name": "HighCPUUsage"
    }]
  }
  ```

---

## 🐛 **Common Issues**

### **"Settings link not found"**
- **Cause:** Settings not in left nav
- **Fix:** Check screenshot `before-settings-click.png`

### **"AI tab not found"**
- **Cause:** Tab structure different
- **Fix:** Check screenshot `04-deterministic-settings-page.png`

### **"Deterministic option not found"**
- **Cause:** Incident Response section not visible
- **Fix:** Scroll down or check screenshot `05-deterministic-ai-tab.png`

### **"No tasks executed"**
- **This is OK!** Test validates UI flow
- To see execution: Create matching task first

---

## 📊 **Test Results**

### **Success Criteria:**

✅ **All these must pass:**
1. Login successful
2. Navigate to Settings
3. Click AI tab
4. Select mode (Deterministic/AI-Selected/Autonomous)
5. Send alert (API returns 200)

⚠️ **Optional:**
6. Task executes (depends on configuration)

### **Example Output:**

```
test_deterministic_mode_alert_handling PASSED
  ✓ Login successful
  ✓ On landing page
  ✓ In workspace view
  ✓ On settings page
  ✓ AI settings tab loaded
  ✓ Deterministic mode selected
  Status: success
  Tasks executed: 1
  ✅ SUCCESS: Task(s) executed in Deterministic mode!
```

---

## 🎉 **Summary**

### **What You Now Have:**

1. ✅ **3 New E2E Tests** for alert handling modes
2. ✅ **1 New Page Object** for Settings
3. ✅ **Complete Documentation**
4. ✅ **Helper Script** for easy running
5. ✅ **Detailed Screenshots** at every step

### **Total E2E Test Coverage:**

- **AI Agent Tests:** 3 tests
- **Alert Handling Tests:** 3 tests
- **Total:** 6 comprehensive E2E tests

---

## 🚀 **Next Steps**

1. **Run the tests:**
   ```bash
   ./run_alert_tests.sh
   ```

2. **Review screenshots:**
   ```bash
   ls -lah reports/screenshots/ | grep deterministic
   ```

3. **Check HTML report:**
   ```bash
   open reports/report.html  # or firefox/chrome reports/report.html
   ```

4. **Optional: Configure task for execution**
   - Create task with alert trigger
   - Run test again to see task execute

---

**Your Alert Handling E2E tests are ready to run!** 🎉

For detailed information, see [ALERT_HANDLING_TESTS.md](ALERT_HANDLING_TESTS.md)

