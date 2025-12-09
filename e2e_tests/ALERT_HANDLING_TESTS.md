# 🚨 Alert Handling E2E Tests

Complete UI-based end-to-end tests for Alert Handling modes configuration and alert processing.

---

## 📋 **Test Overview**

### **Three Alert Handling Mode Tests**

| Test | Mode | Flow | Duration |
|------|------|------|----------|
| 1. Deterministic | Pre-configured task execution | Full UI + API | ~90-120s |
| 2. AI-Selected | AI selects best task | Full UI + API | ~90-120s |
| 3. Autonomous | AI creates new task | Full UI + API | ~90-120s |

---

## 🎯 **Test Flow - Deterministic Mode Example**

### **Step-by-Step**

1. **Login** at `/vlogin`
2. Navigate to **landing page** (`/n/landing`)
3. Click **"Default" workspace**
4. Navigate to workspace view (`/?space=Default`)
5. Click **Settings** in left navigation bar
6. Navigate to **Settings page** (`/vsettings`)
7. Click **"AI" tab** in horizontal tab strip
8. View **AI Configuration** section
9. Scroll to **"Incident Response"** section
10. Select **"Deterministic"** mode (radio button)
11. Settings auto-save (or click Save if present)
12. Send **Grafana alert** via API (`/processAlert`)
13. Verify **task execution** from API response

---

## 🚀 **Running the Tests**

### **Run All Alert Handling Tests**

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_alert_handling_modes.py -v
```

### **Run Specific Mode Tests**

```bash
# Deterministic mode only
pytest ui_tests/test_alert_handling_modes.py::TestAlertHandlingModesE2E::test_deterministic_mode_alert_handling -v

# AI-Selected mode only
pytest ui_tests/test_alert_handling_modes.py::TestAlertHandlingModesE2E::test_ai_selected_mode_alert_handling -v

# Autonomous mode only
pytest ui_tests/test_alert_handling_modes.py::TestAlertHandlingModesE2E::test_autonomous_mode_alert_handling -v
```

### **Run with Markers**

```bash
# Run all alert handling tests
pytest -m alert_handling -v

# Run all UI tests
pytest -m ui -v
```

---

## 📸 **Screenshots Captured**

Each test captures detailed screenshots:

### **Deterministic Mode Test Screenshots:**
```
01-deterministic-after-login.png         # After successful login
02-deterministic-landing-page.png        # Landing page with workspaces
03-deterministic-workspace-view.png      # Inside Default workspace
04-deterministic-settings-page.png       # Settings page (General tab)
05-deterministic-ai-tab.png              # AI tab with AI Configuration
06-deterministic-mode-selected.png       # After selecting Deterministic mode
07-deterministic-alert-sent.png          # After sending alert
```

Additional debugging screenshots:
- `before-settings-click.png` - Before clicking Settings
- `after-settings-navigation.png` - After navigating to Settings
- `before-ai-tab-click.png` - Before clicking AI tab
- `after-ai-tab-click.png` - After AI tab loads
- `before-deterministic-selection.png` - Before selecting mode
- `after-deterministic-selection.png` - After mode selection

---

## 🔧 **Prerequisites**

### **For Successful Task Execution**

The tests will **send alerts**, but tasks will only execute if you have:

1. **A pre-configured task** with alert trigger:
   ```json
   {
     "trigger_on_alerts": [{
       "source": "Grafana",
       "alert_name": "HighCPUUsage"
     }]
   }
   ```

2. **Correct mode selected** in Settings → AI → Incident Response

### **Alert Payloads Used**

#### **Grafana Alert:**
- **Alert Name:** `HighCPUUsage`
- **Source:** Grafana
- **Severity:** Critical
- **Description:** CPU usage exceeded 90% on test server

#### **PagerDuty Alert:**
- **Event:** incident.triggered
- **Title:** Database Connection Failure
- **Urgency:** High

---

## ✅ **Expected Results**

### **Test Pass Criteria:**

1. ✅ Login successful
2. ✅ Navigation to Settings works
3. ✅ AI tab loads
4. ✅ Deterministic mode can be selected
5. ✅ Alert sent successfully (returns 200)
6. ⚠️ **Task execution**: May or may not execute (depends on pre-configured tasks)

### **Success Indicators:**

```python
# API Response when task executes:
{
  "status": "success",
  "tasks_executed": 1,
  "executed_tasks": [{
    "task_id": "abc123",
    "job_id": "job456",
    "status": "SUBMITTED"
  }]
}
```

### **No Task Execution (Still Valid):**

```python
# API Response when no matching task:
{
  "status": "success",
  "tasks_executed": 0,
  "message": "No matching tasks found"
}
```

**Note:** The test verifies the **UI flow** and **alert sending**. Task execution depends on your task configuration.

---

## 🆚 **Three Alert Handling Modes**

### **1. Deterministic Mode**
- **Behavior:** Executes pre-configured tasks only
- **Use Case:** Fixed, predictable alert response
- **Test:** Verifies UI selection + alert sent

### **2. AI-Selected Mode**
- **Behavior:** AI selects best matching task from library
- **Use Case:** Intelligent task selection
- **Test:** Verifies UI selection + alert sent

### **3. Autonomous Mode**
- **Behavior:** AI creates new task on-the-fly
- **Use Case:** Dynamic, adaptive responses
- **Test:** Verifies UI selection + alert sent

---

## 🐛 **Troubleshooting**

### **Issue: Settings link not found**

**Solution:** Check that Settings is visible in left nav:
```bash
# Take screenshot manually
pytest ui_tests/test_alert_handling_modes.py::test_deterministic_mode_alert_handling -v -k "deterministic" --capture=no
```

### **Issue: AI tab not found**

**Solution:** Verify tab structure in screenshot `04-deterministic-settings-page.png`

### **Issue: Deterministic option not found**

**Solution:** Check screenshot `05-deterministic-ai-tab.png` to see Incident Response section

### **Issue: Alert sending fails (401)**

**Solution:** Check JWT token in `config/env.py` or `.env` file

### **Issue: No tasks executed**

**This is OK!** The test verifies UI flow. To see task execution:
1. Create a task with alert trigger matching `HighCPUUsage`
2. Set source to `Grafana`
3. Run test again

---

## 📊 **Comparison with Bash Scripts**

### **Old Bash Scripts** (`test_payloads/`)
- ✅ Fast (~5 seconds)
- ✅ Direct API calls
- ❌ No UI testing
- ❌ Assumes mode already set
- ❌ No visual verification

### **New E2E Tests** (`e2e_tests/ui_tests/`)
- ✅ Full user flow
- ✅ UI verification with screenshots
- ✅ Mode configuration tested
- ✅ Visual debugging
- ⏱️ Slower (~90 seconds)
- ✅ Catches UI bugs

**Recommendation:** Use both!
- **Bash scripts:** Quick API testing
- **E2E tests:** Full UI validation

---

## 🎓 **Page Objects Used**

### **LoginPage** (`pages/login_page.py`)
- Login flow
- Logout
- Session management

### **WorkspacePage** (`pages/workspace_page.py`)
- Landing page navigation
- Workspace selection

### **SettingsPage** (`pages/settings_page.py`) ⭐ **NEW**
- Navigate to Settings
- Click AI tab
- Select alert handling modes
- Save settings

---

## 📝 **Configuration Files**

### **Environment Variables** (`.env`)
```bash
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_PROXY=?proxy=dev1
DAGKNOWS_TOKEN=eyJhbGc...  # Your JWT token
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=1Hey2Yash*
TEST_ORG=dagknows
```

### **Test Markers** (`pytest.ini`)
```ini
markers =
    alert_handling: Tests for alert handling and incident response
    ui: UI-based E2E tests
    e2e: End-to-end tests
```

---

## 🚀 **Quick Start**

```bash
# 1. Activate venv
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate

# 2. Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 3. Run all alert handling tests
pytest ui_tests/test_alert_handling_modes.py -v

# 4. Check screenshots
ls -lah reports/screenshots/ | grep deterministic
```

---

## 📚 **Related Documentation**

- [AI Agent Workflow Tests](AI_AGENT_WORKFLOW_TEST.md)
- [Quick Setup Guide](QUICK_SETUP_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Configuration Guide](LOCAL_VS_DEV_CONFIG.md)

---

**Your alert handling E2E tests are ready!** 🎉

Run them to verify the complete Settings → AI → Incident Response workflow.

