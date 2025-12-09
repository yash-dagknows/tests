# End-to-End (E2E) Test Suite

Comprehensive E2E testing for DagKnows application covering both API and UI testing.

## 🎯 **Overview**

This test suite focuses on **End-to-End workflows** rather than isolated unit tests. It validates complete user journeys from start to finish.

### **Test Coverage:**
- ✅ **5+ API-based E2E tests** - Testing backend workflows via API
- ✅ **5+ UI-based E2E tests** - Testing user workflows via UI automation
- ✅ **Reusable modules** - Login, authentication, common actions
- ✅ **Page Object Model** - Maintainable UI test structure
- ✅ **Real authentication** - Uses actual JWT tokens

---

## 📁 **Directory Structure**

```
e2e_tests/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── package.json           # Playwright dependencies
├── playwright.config.js   # Playwright configuration
├── pytest.ini             # Pytest configuration
│
├── config/
│   ├── env.py            # Environment configuration (URLs, tokens)
│   └── test_users.py     # Test user credentials
│
├── fixtures/
│   ├── api_client.py     # Reusable API client
│   ├── auth.py           # Authentication helpers
│   └── test_data.py      # Test data generators
│
├── pages/                 # Page Object Model for UI tests
│   ├── base_page.py      # Base page class
│   ├── login_page.py     # Login page
│   ├── dashboard_page.py # Dashboard/home page
│   ├── task_page.py      # Task creation/management
│   └── chat_page.py      # AI chat session
│
├── api_tests/             # API-based E2E tests
│   ├── test_task_lifecycle.py
│   ├── test_alert_workflow.py
│   ├── test_user_management.py
│   ├── test_workspace_operations.py
│   └── test_incident_response.py
│
├── ui_tests/              # UI-based E2E tests
│   ├── test_login_flow.py
│   ├── test_task_creation.py
│   ├── test_ai_chat_session.py
│   ├── test_runbook_execution.py
│   └── test_alert_management_ui.py
│
├── utils/
│   ├── helpers.py        # Common utility functions
│   ├── wait_conditions.py # Custom wait conditions
│   └── api_helpers.py    # API utility functions
│
└── reports/              # Test reports (generated)
    └── screenshots/      # Test screenshots
```

---

## 🚀 **Quick Start**

### **⚡ One-Command Installation (Recommended)**

```bash
cd tests/e2e_tests
./install.sh
```

This installs everything: system dependencies, Python packages, Playwright browsers, and project structure.  
📖 See [ONE_COMMAND_INSTALL.md](ONE_COMMAND_INSTALL.md) for details.

### **1. Manual Installation (Alternative)**

```bash
cd tests/e2e_tests

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y $(cat system_requirements.txt | grep -v '^#')

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Setup project structure
./setup.sh
```

### **2. Configure Environment**

The `.env` file is **auto-created** by `install.sh` and pre-configured for `dev.dagknows.com`.

If you need to modify it:

```bash
# .env (already configured)
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_PROXY=?proxy=dev1
DAGKNOWS_TOKEN=<auto-set-with-valid-jwt>
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=<auto-set>
TEST_ORG=dagknows
```

📖 See [LOCAL_VS_DEV_CONFIG.md](LOCAL_VS_DEV_CONFIG.md) for local setup details.

### **3. Run Tests**

```bash
# Activate virtual environment first!
source venv/bin/activate

# Quick test - AI Agent workflow (recommended)
./run_ai_agent_test.sh

# Run all UI tests
pytest ui_tests/ -v

# Run all API tests
pytest api_tests/ -v

# Run specific test
pytest ui_tests/test_ai_agent_workflow.py -v

# Run with headed browser (for debugging)
pytest ui_tests/ --headed --slowmo 1000

# Run and generate HTML report
pytest --html=reports/report.html
```

📖 Quick guides: [RUN_NOW.md](RUN_NOW.md) | [QUICK_SETUP_GUIDE.md](QUICK_SETUP_GUIDE.md)

---

## 🎯 **API-based E2E Tests**

### **Test 1: Task Lifecycle**
**File:** `api_tests/test_task_lifecycle.py`
**Flow:**
1. Create a task via API
2. Update task details
3. Add child tasks
4. Execute the task
5. Verify execution status
6. Delete task

### **Test 2: Alert to Task Execution Workflow**
**File:** `api_tests/test_alert_workflow.py`
**Flow:**
1. Create task with alert trigger
2. Send alert via processAlert API
3. Verify task is triggered
4. Check job execution status
5. Verify job completion

### **Test 3: User Management Workflow**
**File:** `api_tests/test_user_management.py`
**Flow:**
1. Create new user
2. Assign roles/permissions
3. User logs in
4. User creates workspace
5. User invites team member

### **Test 4: Workspace Operations**
**File:** `api_tests/test_workspace_operations.py`
**Flow:**
1. Create workspace
2. Add members
3. Create tasks in workspace
4. Share tasks
5. Delete workspace

### **Test 5: Incident Response Workflow**
**File:** `api_tests/test_incident_response.py`
**Flow:**
1. Set incident response mode
2. Trigger alert
3. Verify automated response
4. Check investigation tasks created
5. Validate incident closure

---

## 🖥️ **UI-based E2E Tests**

### **Test 1: Complete Login Flow**
**File:** `ui_tests/test_login_flow.py`
**Flow:**
1. Navigate to login page
2. Enter credentials
3. Verify redirect to dashboard
4. Verify user menu visible
5. Logout

### **Test 2: Task Creation and Management**
**File:** `ui_tests/test_task_creation.py`
**Flow:**
1. Login
2. Click "Create Runbook"
3. Fill task details
4. Add description
5. Add child tasks
6. Verify task created
7. Edit task
8. Delete task

### **Test 3: AI Chat Session**
**File:** `ui_tests/test_ai_chat_session.py`
**Flow:**
1. Login
2. Navigate to AI chat
3. Start new session
4. Send prompt
5. Verify AI response
6. Continue conversation
7. Save/export chat

### **Test 4: Runbook Execution**
**File:** `ui_tests/test_runbook_execution.py`
**Flow:**
1. Login
2. Open existing runbook
3. Click execute
4. Monitor execution progress
5. Verify task completion
6. Check execution logs

### **Test 5: Alert Management UI**
**File:** `ui_tests/test_alert_management_ui.py`
**Flow:**
1. Login
2. Navigate to alerts page
3. View incoming alerts
4. Configure alert routing
5. Test alert handling
6. Verify task execution

---

## 🔧 **Configuration**

### **Environment Variables**

| Variable | Description | Example |
|----------|-------------|---------|
| `DAGKNOWS_URL` | Base URL of deployment | `https://dev.dagknows.com` |
| `DAGKNOWS_TOKEN` | JWT access token | `eyJhbGci...` |
| `TEST_USER_EMAIL` | Test user email | `test@dagknows.com` |
| `TEST_USER_PASSWORD` | Test user password | `password123` |
| `TEST_ORG` | Organization name | `dagknows` |
| `PROXY_PARAM` | Proxy parameter for dev | `?proxy=dev1` |

### **Test User Setup**

Test users should have:
- ✅ Admin/Supremo role
- ✅ Access to test workspace
- ✅ Permissions for all operations
- ✅ Valid JWT token with long expiry

---

## 🧩 **Reusable Modules**

### **Authentication Module**
```python
from fixtures.auth import AuthHelper

auth = AuthHelper()
auth.login(email, password)
token = auth.get_token()
```

### **API Client Module**
```python
from fixtures.api_client import DagKnowsAPIClient

client = DagKnowsAPIClient(base_url, token)
response = client.create_task(task_data)
```

### **Page Objects**
```python
from pages.login_page import LoginPage

login_page = LoginPage(page)
login_page.login(email, password)
```

---

## 📊 **Test Reports**

### **Generate Reports**

```bash
# HTML report
pytest --html=reports/report.html --self-contained-html

# JUnit XML (for CI/CD)
pytest --junitxml=reports/junit.xml

# Allure report
pytest --alluredir=reports/allure
allure serve reports/allure
```

### **Screenshots**

Screenshots are automatically captured:
- ✅ On test failure
- ✅ At key checkpoints
- ✅ Saved in `reports/screenshots/`

---

## 🎓 **Best Practices**

### **1. Tests Match Real UI Behavior**
```python
# ✅ GOOD: Match how UI actually works
client.update_task(
    task_id=task_id,
    data=full_task_object,  # Send all fields
    update_mask=["title", "description", "script"]  # Like UI does
)

# ❌ BAD: Minimal update that doesn't match UI
client.update_task(
    task_id=task_id,
    data={"title": "New Title"},  # Too minimal
    update_mask=["title"]
)
```

### **2. Use Page Object Model**
```python
# ✅ GOOD: Use page objects
task_page.create_task(title, description)

# ❌ BAD: Direct element interaction
page.fill("#task-title", title)
page.fill("#task-desc", description)
```

### **3. Test Complete Workflows**
```python
# ✅ GOOD: End-to-end flow
def test_alert_to_task_execution():
    # Create task with trigger
    # Send alert
    # Verify execution
    # Check results

# ❌ BAD: Testing single operation
def test_create_task():
    create_task()  # Too isolated
```

### **4. Clean Up After Tests**
```python
@pytest.fixture
def task(client):
    task = client.create_task(...)
    yield task
    client.delete_task(task.id)  # Cleanup
```

---

## 🐛 **Troubleshooting**

### **Issue: Playwright browsers not installed**
```bash
playwright install
```

### **Issue: Authentication fails**
- Check token is not expired
- Verify token has correct permissions
- Ensure `?proxy=dev1` is used for dev.dagknows.com

### **Issue: UI tests fail to find elements**
- Check if page has loaded completely
- Verify selectors match current UI
- Add explicit waits for dynamic content

### **Issue: API tests timeout**
- Increase timeout in pytest.ini
- Check network connectivity
- Verify URL is correct

---

## 🔄 **CI/CD Integration**

### **GitHub Actions Example**

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd tests/e2e_tests
          pip install -r requirements.txt
          playwright install
      
      - name: Run E2E tests
        env:
          DAGKNOWS_URL: ${{ secrets.DAGKNOWS_URL }}
          DAGKNOWS_TOKEN: ${{ secrets.DAGKNOWS_TOKEN }}
        run: |
          cd tests/e2e_tests
          pytest --html=reports/report.html
      
      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: tests/e2e_tests/reports/
```

---

## 📚 **Additional Resources**

- **Playwright Docs**: https://playwright.dev/python/
- **Pytest Docs**: https://docs.pytest.org/
- **Page Object Model**: https://playwright.dev/python/docs/pom
- **DagKnows API Docs**: Check `/api/docs` endpoint

---

## 🎯 **Test Philosophy**

> **"Test the application as users use it, not as developers built it."**

- Focus on **user journeys**, not implementation details
- Tests should **match UI behavior** exactly
- Prefer **E2E flows** over isolated operations
- **Don't change code** to fit tests - adapt tests to code

---

**Ready to test? Start with the Quick Start section!** 🚀

