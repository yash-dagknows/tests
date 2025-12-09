# 🧪 Complete E2E Test Suite - All Tests Guide

## 📋 Available Tests

### **1. AI Agent Workflow Test** 🤖
**Test:** Create task using AI Agent chat interface  
**File:** `ui_tests/test_ai_agent_workflow.py`  
**Duration:** 90-120 seconds (AI code generation)  
**Runner:** `./run_ai_agent_test.sh`

**What it tests:**
- Login → Landing → Default workspace
- Click "New Task" → "Create with AI Agent"
- Type prompt → Send → Wait for AI code generation

---

### **2. Alert Handling Tests** 🚨
**Test:** Configure alert modes and send alerts  
**File:** `ui_tests/test_alert_handling_modes.py`  
**Duration:** 60-180 seconds (autonomous is slowest)  
**Runner:** `./run_alert_tests.sh`

**What it tests:**
- **Deterministic:** Pre-configured task execution
- **AI-Selected:** AI selects best task from library
- **Autonomous:** AI creates NEW task dynamically

---

### **3. Workspace Creation Test** 📁
**Test:** Create and navigate to new workspace  
**File:** `ui_tests/test_workspace_management.py`  
**Duration:** 60-90 seconds  
**Runner:** `./run_workspace_test.sh`

**What it tests:**
- Settings → Workspaces tab
- Create workspace → Verify in list
- Navigate directly via URL

---

### **4. Task CRUD Test** 📝
**Test:** Create task using form-based interface  
**File:** `ui_tests/test_task_crud.py`  
**Duration:** 60-80 seconds  
**Runner:** `./run_task_crud_test.sh`

**What it tests:**
- Click "New Task" → "Create from Form"
- Fill title, description, code
- Scroll and click Save
- Verify task creation

---

## 🚀 Quick Run Commands

### **Run All Tests:**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/ -v
```

### **Run Individual Test Suites:**

```bash
# AI Agent Test
./run_ai_agent_test.sh

# Alert Tests (all 3 modes)
./run_alert_tests.sh

# Deterministic mode only
./run_alert_tests.sh --deterministic

# AI-Selected mode only
./run_alert_tests.sh --ai-selected

# Autonomous mode only
./run_alert_tests.sh --autonomous

# Workspace Creation Test
./run_workspace_test.sh

# Task CRUD Test
./run_task_crud_test.sh
```

### **With Browser Visible (Headed Mode):**
```bash
./run_ai_agent_test.sh --headed
./run_alert_tests.sh --deterministic --headed
./run_workspace_test.sh --headed
```

### **Slow Motion (for debugging):**
```bash
./run_ai_agent_test.sh --headed --slow
./run_alert_tests.sh --autonomous --headed --slow
./run_workspace_test.sh --headed --slow
```

---

## 📊 Test Matrix

| Test | Duration | API Calls | Cleanup | Best Use Case |
|------|----------|-----------|---------|---------------|
| **AI Agent** | 90-120s | Minimal | No | Test AI code generation |
| **Deterministic** | 60s | Yes (alert) | No | Test fixed task execution |
| **AI-Selected** | 70s | Yes (alert) | No | Test AI task selection |
| **Autonomous** | 120-180s | Yes (alert) | No | Test AI task creation |
| **Workspace** | 60-90s | Minimal | No | Test workspace management |
| **Task CRUD** | 60-80s | Minimal | No | Test task form creation |

---

## 🎯 Run By Test Marker

### **All UI Tests:**
```bash
pytest -m ui -v
```

### **All E2E Tests:**
```bash
pytest -m e2e -v
```

### **Alert Handling Tests Only:**
```bash
pytest -m alert_handling -v
```

### **Workspace Tests Only:**
```bash
pytest -m workspace_management -v
```

### **Combine Markers:**
```bash
pytest -m "ui and alert_handling" -v
pytest -m "e2e and not slow" -v
```

---

## 📸 Screenshots

All tests save screenshots to: `reports/screenshots/`

### **Screenshot Naming:**
- **AI Agent:** `01-after-login.png`, `07-ai-generated-task.png`
- **Alert Tests:** `autonomous-mode-selected.png`, `after-ai-tab-click.png`
- **Workspace:** `06-workspace-created.png`, `09-workspace-folder-dropdown-open.png`

---

## 📄 HTML Report

After any test run:
```bash
# View HTML report
open reports/report.html  # macOS
xdg-open reports/report.html  # Linux
```

---

## 🔧 Environment Setup

### **First Time Setup:**
```bash
cd /home/ubuntu/tests/e2e_tests

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Install system dependencies (Ubuntu)
sudo apt-get install -y \
  libnss3 \
  libxss1 \
  libasound2t64 \
  libatk-bridge2.0-0t64 \
  libgtk-3-0 \
  libgbm1

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### **Before Each Test Run:**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## 🌐 Environment Selection

### **Default: dev.dagknows.com**
```bash
export DAGKNOWS_URL="https://dev.dagknows.com"
export DAGKNOWS_PROXY="?proxy=dev1"
export DAGKNOWS_TOKEN="<dev_jwt_token>"
./run_ai_agent_test.sh
```

### **Local Docker:**
```bash
export DAGKNOWS_URL="http://localhost:8000"
export DAGKNOWS_PROXY="?proxy=yashlocal"
export DAGKNOWS_TOKEN="<local_jwt_token>"
./run_ai_agent_test.sh --local
```

Or use `--local` flag:
```bash
./run_ai_agent_test.sh --local
./run_alert_tests.sh --deterministic --local
./run_workspace_test.sh --local
```

---

## ⏱️ Timing Considerations

### **Slow Tests:**
- **AI Agent (code generation):** 90-120s
- **Autonomous Mode:** 120-180s (AI generates task + executes)

### **Medium Tests:**
- **Workspace Creation:** 60-90s
- **AI-Selected Mode:** 70s

### **Fast Tests:**
- **Deterministic Mode:** 60s

### **Total Suite Runtime:**
```bash
# All tests together: ~8-10 minutes
pytest ui_tests/ -v
```

---

## 🐛 Common Issues

### **Issue 1: Module not found**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### **Issue 2: Browser dependencies missing**
```bash
sudo apt-get install -y libnss3 libxss1 libasound2t64 \
  libatk-bridge2.0-0t64 libgtk-3-0 libgbm1
```

### **Issue 3: Login fails**
- Check JWT token is valid
- Verify `DAGKNOWS_URL` is correct
- Check screenshots: `reports/screenshots/login-*.png`

### **Issue 4: Test timeout**
- Increase timeout in `pytest.ini`: `timeout = 600`
- Use `--slowmo` to slow down execution
- Check if application is responsive

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `QUICK_SETUP_GUIDE.md` | Setup instructions |
| `AI_AGENT_WORKFLOW_TEST.md` | AI Agent test details |
| `ALERT_HANDLING_TESTS.md` | Alert test details |
| `AUTONOMOUS_MODE_EXPLAINED.md` | Autonomous mode explanation |
| `WORKSPACE_TEST_SUMMARY.md` | Workspace test details |
| `ALL_TESTS_GUIDE.md` | This file (comprehensive guide) |
| `TROUBLESHOOTING.md` | Common issues |

---

## ✅ Pre-Flight Checklist

Before running tests, verify:

- [ ] Virtual environment activated: `source venv/bin/activate`
- [ ] PYTHONPATH set: `export PYTHONPATH="${PYTHONPATH}:$(pwd)"`
- [ ] Environment variables set (URL, PROXY, TOKEN)
- [ ] Dependencies installed: `pip list | grep playwright`
- [ ] Browsers installed: `playwright --version`
- [ ] Application is running (if testing locally)

---

## 🎯 Test Scenarios by Use Case

### **Scenario 1: Quick Smoke Test**
```bash
# Run deterministic mode (fastest)
./run_alert_tests.sh --deterministic
```

### **Scenario 2: Full Alert Flow**
```bash
# Run all 3 alert modes
./run_alert_tests.sh
```

### **Scenario 3: AI Features**
```bash
# AI Agent + Autonomous Mode
./run_ai_agent_test.sh
./run_alert_tests.sh --autonomous
```

### **Scenario 4: Complete E2E**
```bash
# All tests
pytest ui_tests/ -v
```

### **Scenario 5: Debug Specific Test**
```bash
# Headed + Slow + Screenshots
./run_workspace_test.sh --headed --slow
```

---

## 📊 Test Coverage

### **UI Features Tested:**
✅ Login & Authentication  
✅ Workspace Navigation  
✅ Settings Management  
✅ AI Agent Chat Interface  
✅ Alert Mode Configuration  
✅ Workspace Creation  
✅ Dropdown Navigation  

### **API Features Tested:**
✅ Alert Processing (`/processAlert`)  
✅ Deterministic Mode  
✅ AI-Selected Mode  
✅ Autonomous Mode  

### **Not Yet Tested:**
- Task CRUD operations (create, edit, delete)
- User management
- Proxies configuration
- Authentication tools
- Task execution monitoring

---

## 🚀 Next Test Ideas

1. **Task Library Management:**
   - Create task via form (not AI)
   - Edit existing task
   - Delete task
   - Duplicate task

2. **User Management:**
   - Create new user
   - Assign roles
   - Manage permissions

3. **Alert Management:**
   - View alert history
   - Configure alert routing
   - Test PagerDuty alerts

4. **Execution Monitoring:**
   - View job logs
   - Monitor task execution
   - Check task status

---

## 📞 Help & Support

### **Check Logs:**
```bash
# Test output
cat reports/report.html

# Screenshots
ls -lh reports/screenshots/

# Pytest cache
cat .pytest_cache/v/cache/lastfailed
```

### **Debug Mode:**
```bash
# Run with verbose output
pytest ui_tests/test_ai_agent_workflow.py -v -s

# Run with headed + slow
./run_ai_agent_test.sh --headed --slow
```

### **Clean Start:**
```bash
# Remove old reports
rm -rf reports/screenshots/*.png
rm -f reports/report.html

# Clear pytest cache
rm -rf .pytest_cache/
```

---

## ✅ Summary

### **Total Tests Created:** 9
- AI Agent Workflow (3 variants)
- Alert Handling (3 modes)
- Workspace Creation (1)
- Task CRUD (2 tests)

### **Total Duration:** ~10-12 minutes for all

### **Total Screenshots:** ~50-60 per full run

### **Ready to Run:**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run one test
./run_workspace_test.sh

# Run all tests
pytest ui_tests/ -v
```

---

**All tests are ready!** 🚀 Pick a test and run it!

