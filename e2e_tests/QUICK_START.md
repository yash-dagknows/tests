# E2E Tests - Quick Start Guide

Get started with E2E testing in **5 minutes**!

---

## 🚀 **Quick Setup (5 Steps)**

### **Step 1: Install Dependencies**

```bash
cd tests/e2e_tests

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### **Step 2: Configure Environment**

```bash
# Copy template
cp env.template .env

# Edit .env and fill in:
# - DAGKNOWS_URL=https://dev.dagknows.com
# - DAGKNOWS_TOKEN=your-jwt-token
# - TEST_USER_EMAIL=your-email
# - TEST_USER_PASSWORD=your-password
```

**Get Your JWT Token:**
1. Login to DagKnows in browser
2. Open Dev Tools (F12)
3. Go to Application → Local Storage
4. Copy `authToken` value
5. Paste into `.env` as `DAGKNOWS_TOKEN`

### **Step 3: Verify Configuration**

```bash
# Test that config loads
python -c "from config.env import config; print(f'URL: {config.BASE_URL}')"
```

### **Step 4: Run Your First Test**

```bash
# Run a simple API test (Task CRUD)
pytest api_tests/test_task_crud_api.py::TestTaskCRUDE2E::test_task_full_lifecycle_via_api -v

# Or run a UI test (Login)
pytest ui_tests/test_login_flow.py::TestLoginFlowE2E::test_successful_login_and_logout -v
```

### **Step 5: Run All Tests**

```bash
# Run all E2E tests
pytest -v

# Run only API tests
pytest api_tests/ -v

# Run only UI tests
pytest ui_tests/ -v

# Generate HTML report
pytest --html=reports/report.html
```

---

## 📊 **Test Suites**

### **API-Based E2E Tests** (`api_tests/`)

| Test | Description | Duration |
|------|-------------|----------|
| `test_task_crud_api.py` | Full task lifecycle (Create → Read → Update → Delete) | ~10s |
| `test_task_lifecycle.py` | Create → Update → Execute → Delete task | ~15s |
| `test_alert_workflow.py` | Alert → Task execution | ~15s |
| `test_role_management_api.py` | Create role and assign privileges via API | ~10s |
| `test_user_role_assignment_api.py` | Assign role to user for workspace via API | ~10s |

**Run API tests:**
```bash
pytest api_tests/ -v

# Run specific test
pytest api_tests/test_task_crud_api.py::TestTaskCRUDE2E::test_task_full_lifecycle_via_api -v
```

### **UI-Based E2E Tests** (`ui_tests/`)

| Test | Description | Duration |
|------|-------------|----------|
| `test_login_flow.py` | Login/logout workflow | ~15s |
| `test_task_creation.py` | Create tasks via UI | ~30s |
| `test_task_crud.py` | Task CRUD operations via UI | ~30s |
| `test_workspace_management.py` | Create and navigate to workspace | ~20s |
| `test_role_management.py` | Create role and assign privileges | ~30s |
| `test_user_role_assignment.py` | Assign role to user for workspace | ~30s |
| `test_ai_chat_session.py` | AI chat interaction | ~60s |
| `test_ai_agent_workflow.py` | Complete AI agent workflow | ~90s |
| `test_alert_handling_modes.py` | Alert handling in different modes | ~60s |

**Run UI tests:**
```bash
pytest ui_tests/ -v

# Run specific test
pytest ui_tests/test_login_flow.py::TestLoginFlowE2E::test_successful_login_and_logout -v
```

---

## 🎯 **Common Use Cases**

### **Test Against dev.dagknows.com**

```bash
# .env
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_TOKEN=eyJhbGci...
DAGKNOWS_PROXY=?proxy=dev1  # CRITICAL for dev!

# Run tests
pytest -v
```

### **Test Against Local Deployment**

```bash
# .env
DAGKNOWS_URL=http://localhost
DAGKNOWS_TOKEN=your-local-token
DAGKNOWS_PROXY=  # Empty for local

# Run tests
pytest -v
```

### **Test Specific Workflow**

```bash
# Test task CRUD via API
pytest api_tests/test_task_crud_api.py::TestTaskCRUDE2E::test_task_full_lifecycle_via_api -v

# Test task lifecycle (create, update, execute, delete)
pytest api_tests/test_task_lifecycle.py::TestTaskLifecycleE2E::test_create_update_execute_delete_task -v

# Test login flow
pytest ui_tests/test_login_flow.py::TestLoginFlowE2E::test_successful_login_and_logout -v

# Test workspace management
pytest ui_tests/test_workspace_management.py::TestWorkspaceManagementE2E::test_create_and_navigate_to_workspace -v

# Test role management
pytest ui_tests/test_role_management.py::TestRoleManagementE2E::test_create_role_and_assign_privileges -v

# Test with screenshots
pytest ui_tests/ -v --screenshot=on
```

### **Debug Failing Test**

```bash
# Run with full output
pytest api_tests/test_task_crud_api.py -v -s

# Run with Playwright headed mode (see browser)
pytest ui_tests/test_login_flow.py --headed

# Keep browser open on failure
pytest ui_tests/ --headed --slowmo=1000
```

---

## 📁 **Project Structure**

```
e2e_tests/
├── api_tests/          # API-based E2E tests
│   ├── test_task_crud_api.py
│   ├── test_task_lifecycle.py
│   ├── test_alert_workflow.py
│   ├── test_role_management_api.py
│   └── test_user_role_assignment_api.py
│
├── ui_tests/           # UI-based E2E tests  
│   ├── test_login_flow.py
│   ├── test_task_creation.py
│   ├── test_task_crud.py
│   ├── test_workspace_management.py
│   ├── test_role_management.py
│   ├── test_user_role_assignment.py
│   ├── test_ai_chat_session.py
│   ├── test_ai_agent_workflow.py
│   └── test_alert_handling_modes.py
│
├── pages/              # Page Object Model
│   ├── login_page.py
│   ├── task_page.py
│   ├── settings_page.py
│   └── chat_page.py
│
├── fixtures/           # Reusable test fixtures
│   ├── api_client.py
│   └── auth.py
│
├── config/             # Configuration
│   ├── env.py
│   └── test_users.py
│
└── conftest.py         # Pytest fixtures
```

---

## 🔧 **Configuration Options**

### **Environment Variables**

| Variable | Description | Example |
|----------|-------------|---------|
| `DAGKNOWS_URL` | Base URL | `https://dev.dagknows.com` |
| `DAGKNOWS_TOKEN` | JWT token | `eyJhbGci...` |
| `DAGKNOWS_PROXY` | Proxy param | `?proxy=dev1` |
| `TEST_USER_EMAIL` | Test user | `test@dagknows.com` |
| `TEST_USER_PASSWORD` | Password | `password123` |

### **Pytest Options**

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Run specific test
pytest api_tests/test_task_crud_api.py::TestTaskCRUDE2E::test_task_full_lifecycle_via_api

# Run tests matching pattern
pytest -k "login"

# Run with markers
pytest -m "api"  # Only API tests
pytest -m "ui"   # Only UI tests

# Generate reports
pytest --html=reports/report.html
pytest --junitxml=reports/junit.xml

# Parallel execution
pytest -n 4  # Run with 4 workers
```

---

## 🐛 **Troubleshooting**

### **Issue: Playwright browsers not found**

```bash
playwright install chromium
```

### **Issue: Authentication fails (401)**

- Check JWT token is not expired
- Verify token has correct permissions
- For dev.dagknows.com, ensure `DAGKNOWS_PROXY=?proxy=dev1`

### **Issue: UI test can't find elements**

- Check if page loaded: add `page.wait_for_timeout(5000)`
- Verify selectors match current UI
- Take screenshot: `page.screenshot(path="debug.png")`
- Run in headed mode: `pytest --headed`

### **Issue: API test times out**

- Increase timeout in `.env`: `TEST_TIMEOUT=60`
- Check network connectivity
- Verify URL is correct

### **Issue: Tests pass locally but fail in CI**

- Ensure all dependencies in `requirements.txt`
- Set environment variables in CI
- Use `--screenshot=only-on-failure` for debugging

---

## 📚 **Next Steps**

1. **Read Full Documentation**: See `README.md` for comprehensive guide
2. **Add Your Own Tests**: Use existing tests as templates
3. **Customize Page Objects**: Add methods for your workflows
4. **Integrate with CI/CD**: See `README.md` CI/CD section

---

## ✅ **Verification Checklist**

Before running tests, verify:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed (`playwright install`)
- [ ] `.env` file configured with valid credentials
- [ ] JWT token is not expired
- [ ] Test user has appropriate permissions
- [ ] For dev.dagknows.com: `DAGKNOWS_PROXY=?proxy=dev1` is set

---

## 🎓 **Test Examples**

### **API Test Example**

```python
def test_create_task(api_client):
    # Create task
    task_data = {"title": "Test Task", "script_type": "command"}
    response = api_client.create_task(task_data)
    task = response["task"]
    
    # Verify
    assert task["title"] == "Test Task"
    
    # Cleanup
    api_client.delete_task(task["id"])
```

### **UI Test Example**

```python
def test_login(page):
    # Use page object
    login_page = LoginPage(page)
    login_page.login(email="test@example.com", password="password")
    
    # Verify
    assert login_page.is_logged_in()
```

---

**Ready to run tests? Start with Step 1!** 🚀

**Questions?** Check `README.md` or review existing tests for examples.

