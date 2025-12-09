# AI Agent Workflow E2E Test

Complete UI test for the AI Agent task creation workflow.

---

## 🎯 **What This Test Does**

This test automates the exact workflow you showed in the screenshots:

1. ✅ Navigate to login page (`/vlogin`)
2. ✅ Login with `yash+user@dagknows.com`
3. ✅ Navigate to landing page (`/n/landing`)
4. ✅ Click "Default" workspace
5. ✅ Navigate to tasks page (`/?space=`)
6. ✅ Click "New Task" button
7. ✅ Select "Create with AI Agent" from dropdown
8. ✅ Navigate to AI agent page (`/tasks/DAGKNOWS?agent=1&space=`)
9. ✅ Type message in "How can I help?" section
10. ✅ Send message (click or press Enter)
11. ✅ Wait for AI response

---

## 🚀 **Quick Start**

### **For Remote Testing (dev.dagknows.com)**

```bash
cd tests/e2e_tests

# 1. Setup .env
cp env.template .env

# Edit .env:
# DAGKNOWS_URL=https://dev.dagknows.com
# DAGKNOWS_TOKEN=your-jwt-token
# DAGKNOWS_PROXY=?proxy=dev1
# TEST_USER_EMAIL=yash+user@dagknows.com
# TEST_USER_PASSWORD=your-password

# 2. Install dependencies (if not done)
pip install -r requirements.txt
playwright install chromium

# 3. Run the test
pytest ui_tests/test_ai_agent_workflow.py -v
```

### **For Local Testing (Your Local Docker Setup)**

```bash
cd tests/e2e_tests

# 1. Start your local application
cd ../../app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d
cd ../../tests/e2e_tests

# 2. Setup .env for local
cp env.template .env

# Edit .env:
# DAGKNOWS_URL=http://localhost
# DAGKNOWS_PROXY=?proxy=yashlocal  # IMPORTANT: Required for local!
# DAGKNOWS_TOKEN=your-local-jwt-token  # Get from localhost (different from dev!)
# TEST_USER_EMAIL=yash+user@dagknows.com
# TEST_USER_PASSWORD=your-local-password

# 3. Install dependencies (if not done)
pip install -r requirements.txt
playwright install chromium

# 4. Run the test
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 📊 **Test Variants**

The file includes **3 test variants**:

### **1. Complete Workflow Test** (Recommended)
```bash
pytest ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::test_complete_ai_agent_workflow -v
```

**What it does:**
- Full workflow from login to AI interaction
- Follows exact user journey with all navigation steps
- Takes screenshots at each step
- Most comprehensive test

**Duration:** ~60-90 seconds

---

### **2. Direct Navigation Test** (Faster)
```bash
pytest ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::test_ai_agent_direct_navigation -v
```

**What it does:**
- Login → Direct navigation to AI agent page
- Skips landing/workspace navigation
- Faster for repeated testing

**Duration:** ~30-45 seconds

---

### **3. Complete Flow Helper Test** (Cleanest)
```bash
pytest ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::test_ai_agent_workflow_with_complete_flow -v
```

**What it does:**
- Uses helper method for clean code
- Good example for writing more tests
- Demonstrates reusable patterns

**Duration:** ~30-45 seconds

---

## 🎬 **Run Options**

### **Run with visible browser (see what's happening)**
```bash
pytest ui_tests/test_ai_agent_workflow.py --headed -v
```

### **Run slowly (see each step)**
```bash
pytest ui_tests/test_ai_agent_workflow.py --headed --slowmo=1000 -v
```

### **Run with full output**
```bash
pytest ui_tests/test_ai_agent_workflow.py -v -s
```

### **Generate HTML report**
```bash
pytest ui_tests/test_ai_agent_workflow.py --html=reports/ai_agent_test.html
```

### **Keep browser open on failure**
```bash
pytest ui_tests/test_ai_agent_workflow.py --headed --pause-on-failure
```

---

## 📸 **Screenshots**

Tests automatically capture screenshots at key points:

```
reports/screenshots/
├── 01-after-login.png           # After successful login
├── 02-landing-page.png          # Landing page with workspaces
├── 03-workspace-view.png        # Inside Default workspace
├── 04-new-task-dropdown.png    # New Task dropdown menu
├── 05-ai-agent-page.png         # AI Agent page loaded
├── 06-message-sent.png          # After sending message
└── 07-ai-response.png           # AI response (or timeout)
```

---

## 🔧 **Configuration**

### **Required Environment Variables**

```bash
# Base URL
DAGKNOWS_URL=https://dev.dagknows.com  # or http://localhost

# JWT Token (DIFFERENT for each environment!)
DAGKNOWS_TOKEN=your-token-here

# Proxy (CRITICAL - different for each environment!)
# For dev.dagknows.com: ?proxy=dev1
# For localhost: ?proxy=yashlocal
DAGKNOWS_PROXY=?proxy=dev1

# Test User Credentials
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-password
TEST_ORG=dagknows
```

### **Local Testing Configuration**

For local testing with `local-docker-c-backup-bfr-reorder.yml`:

```bash
# .env
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=yashlocal  # REQUIRED for local!
DAGKNOWS_TOKEN=your-local-jwt-token  # Get from localhost browser
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-local-password
```

**Important Notes:**
- ⚠️ **JWT tokens are DIFFERENT** - Get from localhost, not dev!
- ⚠️ **Proxy IS required** - Use `?proxy=yashlocal` for localhost
- ✅ Tests adapt automatically to local/remote URLs
- ✅ No code changes needed in your application
- ✅ Tests cater to existing application behavior

**How to get local JWT token:**
1. Login to http://localhost in your browser
2. Open Dev Tools (F12)
3. Go to Application → Local Storage
4. Copy value of `authToken`
5. Paste into `.env` as `DAGKNOWS_TOKEN`

---

## 🐛 **Troubleshooting**

### **Issue: Test fails at login**

**Solution:**
1. Check password is correct in `.env`
2. Verify user exists in your deployment
3. Run with `--headed` to see what's happening

```bash
pytest ui_tests/test_ai_agent_workflow.py --headed -v
```

---

### **Issue: "New Task" button not found**

**Solution:**
1. Verify user has permissions to create tasks
2. Check if on correct workspace
3. Take screenshot to debug

The test automatically screenshots if this happens.

---

### **Issue: AI agent page not loading**

**Solution:**
1. For dev.dagknows.com: Ensure `DAGKNOWS_PROXY=?proxy=dev1`
2. For localhost: Ensure proxy is empty
3. Check URL in error message
4. Verify agent mode is enabled for user

---

### **Issue: Chat input not found**

**Solution:**
1. Page may not be fully loaded - test has 10s timeout
2. AI features may not be enabled
3. Check screenshot: `05-ai-agent-page.png`

The test tries multiple selectors for the chat input.

---

### **Issue: Playwright not installed**

```bash
playwright install chromium
```

---

## 📝 **Customizing the Test**

### **Change the prompt**

Edit the test file:

```python
# In test_ai_agent_workflow.py
test_prompt = "Your custom prompt here"
```

### **Test with different user**

```python
test_user = get_test_user("Admin")
test_user.email = "your-user@example.com"  # Change this
```

### **Test different workspace**

```python
workspace_page.click_workspace("Agent")  # Instead of "Default"
```

---

## 🎓 **Understanding the Code**

### **Page Objects Used**

1. **LoginPage** (`pages/login_page.py`)
   - Handles login flow
   - Methods: `login()`, `is_logged_in()`

2. **WorkspacePage** (`pages/workspace_page.py`)
   - Handles workspace selection
   - Methods: `click_workspace()`, `click_default_workspace()`

3. **AIAgentPage** (`pages/ai_agent_page.py`)
   - Handles AI agent interaction
   - Methods: `click_new_task_button()`, `click_create_with_ai_agent()`, `send_message()`

### **Key Test Patterns**

```python
# 1. Page Object pattern
login_page = LoginPage(page)
login_page.login(user=test_user)

# 2. Explicit assertions
assert login_page.is_logged_in(), "Should be logged in"

# 3. Screenshots at key points
login_page.screenshot("01-after-login")

# 4. Logging for debugging
logger.info("✓ Login successful")
```

---

## ✅ **Success Criteria**

Test passes when:

1. ✅ Login completes successfully
2. ✅ Landing page loads with workspaces
3. ✅ Default workspace can be selected
4. ✅ New Task dropdown appears
5. ✅ Create with AI Agent option is clickable
6. ✅ AI agent page loads (`agent=1` in URL)
7. ✅ Message can be typed and sent
8. ✅ AI response received (or 60s timeout)

---

## 🔄 **Adding Cleanup (Future)**

To add cleanup in the future:

```python
try:
    # Test code here
    ai_agent_page.send_message(prompt)
finally:
    # Cleanup code
    # e.g., delete created task via API
    pass
```

---

## 📚 **Related Files**

| File | Purpose |
|------|---------|
| `pages/login_page.py` | Login page object |
| `pages/workspace_page.py` | Workspace/landing page |
| `pages/ai_agent_page.py` | AI agent page |
| `config/env.py` | Environment configuration |
| `config/test_users.py` | Test user definitions |
| `conftest.py` | Pytest fixtures |

---

## 🎯 **Next Steps**

1. ✅ **Run the test** - Start with complete workflow test
2. 📸 **Check screenshots** - Review what happened at each step
3. 🔧 **Customize** - Adjust prompt, user, or workspace as needed
4. 📝 **Add more tests** - Use this as template for other workflows
5. 🧹 **Add cleanup** - Implement task deletion if needed

---

## 💡 **Tips**

- Use `--headed` during development to see the browser
- Use `-v` for verbose output
- Screenshots are automatically saved on failure
- Tests work with both local and remote deployments
- No application code changes needed!

---

**Ready to test? Run:**

```bash
pytest ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::test_complete_ai_agent_workflow -v --headed
```

This will run the test with a visible browser so you can see exactly what's happening! 🚀

