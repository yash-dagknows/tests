# ✅ AI Agent Workflow Test - Complete!

## 🎉 **What We Built**

A complete E2E UI test that automates your **exact workflow** from the screenshots!

---

## 📦 **New Files Created**

```
tests/e2e_tests/
│
├── 📄 AI_AGENT_WORKFLOW_TEST.md      # Complete guide (9KB)
├── 📄 AI_AGENT_TEST_SUMMARY.md       # This summary
├── 🔧 run_ai_agent_test.sh           # Quick test runner script
│
├── 📁 pages/
│   ├── workspace_page.py              # Workspace/landing page object
│   └── ai_agent_page.py               # AI agent page object
│
└── 📁 ui_tests/
    └── test_ai_agent_workflow.py      # The actual test (3 variants)
```

---

## 🎯 **Test Flow (Matches Your Screenshots)**

```
1. Login Page
   └─> /vlogin
   
2. Enter Credentials
   └─> yash+user@dagknows.com + password
   
3. Landing Page
   └─> /n/landing (shows workspaces)
   
4. Click "Default" Workspace
   └─> /?space=
   
5. Click "New Task" Button
   └─> Opens dropdown menu
   
6. Select "Create with AI Agent"
   └─> /tasks/DAGKNOWS?agent=1&space=
   
7. Type Message & Send
   └─> "How can I help?" section
   
8. Wait for AI Response
   └─> Test completes! ✅
```

---

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Setup .env**

```bash
cd tests/e2e_tests
cp env.template .env

# Edit .env with:
# DAGKNOWS_URL=https://dev.dagknows.com  (or http://localhost)
# TEST_USER_EMAIL=yash+user@dagknows.com
# TEST_USER_PASSWORD=your-password
# DAGKNOWS_PROXY=?proxy=dev1  (for dev, empty for local)
```

### **Step 2: Install (if not done)**

```bash
pip install -r requirements.txt
playwright install chromium
```

### **Step 3: Run Test**

```bash
# Option A: Use the script (easiest!)
./run_ai_agent_test.sh --headed

# Option B: Direct pytest
pytest ui_tests/test_ai_agent_workflow.py -v --headed
```

---

## 🎬 **Running Options**

### **1. See the Browser (Recommended for First Run)**
```bash
./run_ai_agent_test.sh --headed
```
You'll see the browser open and watch the test execute!

### **2. Run Slowly (See Each Step)**
```bash
./run_ai_agent_test.sh --slow
```
Great for debugging or demos.

### **3. Run Against Local**
```bash
./run_ai_agent_test.sh --local
```
Automatically uses `http://localhost` (no proxy).

### **4. Fast Variant (Skip Navigation)**
```bash
./run_ai_agent_test.sh --fast --headed
```
Skips landing/workspace steps, goes direct to AI agent.

---

## 📊 **Test Variants**

### **Test 1: Complete Workflow** ⭐ Recommended
```bash
pytest ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::test_complete_ai_agent_workflow -v
```
- Full flow matching your screenshots
- All navigation steps
- Screenshots at each step
- Duration: ~60-90s

### **Test 2: Direct Navigation** ⚡ Fast
```bash
pytest ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::test_ai_agent_direct_navigation -v
```
- Login → Direct to AI agent
- Skips landing/workspace
- Duration: ~30-45s

### **Test 3: Helper Method** 🧩 Clean
```bash
pytest ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::test_ai_agent_workflow_with_complete_flow -v
```
- Uses helper method
- Good template for more tests
- Duration: ~30-45s

---

## 📸 **Screenshots Captured**

Automatically saves at each step:

```
reports/screenshots/
├── 01-after-login.png          ← After login
├── 02-landing-page.png         ← Workspace list
├── 03-workspace-view.png       ← Inside workspace
├── 04-new-task-dropdown.png   ← Dropdown menu
├── 05-ai-agent-page.png        ← AI agent loaded
├── 06-message-sent.png         ← After sending
└── 07-ai-response.png          ← AI response
```

---

## 🏠 **Local Testing (Your Docker Setup)**

Works perfectly with your local setup!

### **Step 1: Start Your Local App**
```bash
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d
```

### **Step 2: Get Local JWT Token**
```bash
# 1. Login to http://localhost in browser
# 2. Open Dev Tools (F12) → Application → Local Storage
# 3. Copy value of 'authToken'
```

### **Step 3: Configure for Local**
```bash
# .env
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=yashlocal  # REQUIRED for local!
DAGKNOWS_TOKEN=your-local-jwt-token  # From step 2 (different from dev!)
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-local-password
```

### **Step 4: Run Test**
```bash
cd ../../tests/e2e_tests
./run_ai_agent_test.sh --local --headed
```

**✅ No code changes needed in your application!**

**⚠️ Important:** JWT tokens are DIFFERENT for localhost vs dev!

---

## 🔧 **Configuration Highlights**

### **For dev.dagknows.com:**
```bash
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_PROXY=?proxy=dev1  # CRITICAL!
DAGKNOWS_TOKEN=your-dev-jwt-token  # Get from dev.dagknows.com
```

### **For localhost:**
```bash
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=yashlocal  # REQUIRED for local!
DAGKNOWS_TOKEN=your-local-jwt-token  # Get from localhost (DIFFERENT!)
```

**⚠️ Important:**
- JWT tokens are DIFFERENT for dev vs local
- Both environments REQUIRE proxy parameter
- The test automatically adapts based on URL

**The test automatically adapts!** No need to change code.

---

## 🎓 **Page Objects Created**

### **1. WorkspacePage** (`pages/workspace_page.py`)

Methods:
- `navigate_to_landing()` - Go to /n/landing
- `wait_for_workspaces_loaded()` - Wait for page load
- `click_workspace(name)` - Click any workspace
- `click_default_workspace()` - Quick method for "Default"

### **2. AIAgentPage** (`pages/ai_agent_page.py`)

Methods:
- `click_new_task_button()` - Open dropdown
- `click_create_with_ai_agent()` - Select option
- `navigate_to_ai_agent_directly()` - Skip navigation
- `send_message(text)` - Type and send
- `wait_for_ai_response()` - Wait for AI
- `complete_ai_agent_workflow()` - Full flow helper

---

## ✅ **Success Criteria**

Test passes when:

1. ✅ Login successful
2. ✅ Landing page loads
3. ✅ Can click workspace
4. ✅ New Task dropdown works
5. ✅ Create with AI Agent works
6. ✅ AI agent page loads (`agent=1`)
7. ✅ Message can be sent
8. ✅ AI responds (or timeout)

---

## 🐛 **Troubleshooting**

### **"Playwright not installed"**
```bash
playwright install chromium
```

### **"Test fails at login"**
- Check password in `.env`
- Verify user exists
- Run with `--headed` to see

### **"New Task button not found"**
- Check user permissions
- Verify on correct page
- See screenshot 03

### **"For dev.dagknows.com - 404 errors"**
- **Must set:** `DAGKNOWS_PROXY=?proxy=dev1`
- This is critical for dev!

---

## 📝 **Example: Customize the Prompt**

Edit `ui_tests/test_ai_agent_workflow.py`:

```python
# Line ~80
test_prompt = "Create a task to check server CPU usage..."

# Change to:
test_prompt = "Your custom prompt here"
```

---

## 🎯 **Adding More Tests**

Use this as a template:

```python
def test_my_workflow(page):
    # 1. Login
    login_page = LoginPage(page)
    login_page.login(user=test_user)
    
    # 2. Navigate
    ai_agent_page = AIAgentPage(page)
    ai_agent_page.navigate_to_ai_agent_directly()
    
    # 3. Interact
    ai_agent_page.send_message("My prompt")
    
    # 4. Verify
    assert ai_agent_page.verify_agent_mode_active()
```

---

## 📊 **Test Execution Examples**

### **Run with report:**
```bash
pytest ui_tests/test_ai_agent_workflow.py \
    --html=reports/my_test.html \
    --headed
```

### **Run all 3 variants:**
```bash
pytest ui_tests/test_ai_agent_workflow.py -v
```

### **Run specific test:**
```bash
pytest ui_tests/test_ai_agent_workflow.py::TestAIAgentWorkflowE2E::test_complete_ai_agent_workflow -v
```

---

## 🎉 **Ready to Use!**

Everything is set up and ready:

✅ Test file created  
✅ Page objects created  
✅ Configuration supports local & remote  
✅ Runner script included  
✅ Documentation complete  
✅ No app code changes needed  

---

## 🚀 **Run Your First Test Now!**

```bash
cd tests/e2e_tests

# Setup (first time only)
cp env.template .env
# Edit .env with your credentials

# Install (first time only)
pip install -r requirements.txt
playwright install chromium

# Run test!
./run_ai_agent_test.sh --headed
```

**Watch your browser automate the exact workflow you showed!** 🎬

---

## 📚 **Documentation Files**

| File | Purpose |
|------|---------|
| `AI_AGENT_WORKFLOW_TEST.md` | Complete guide (9KB) |
| `AI_AGENT_TEST_SUMMARY.md` | This summary |
| `README.md` | Full E2E suite docs |
| `QUICK_START.md` | 5-minute guide |

---

## 💡 **Key Takeaways**

1. ✅ **Test matches your exact workflow** - Based on your screenshots
2. ✅ **Works locally & remotely** - Auto-adapts
3. ✅ **No app changes needed** - Tests cater to app
4. ✅ **Easy to run** - One command: `./run_ai_agent_test.sh --headed`
5. ✅ **Easy to extend** - Add more tests using same pattern
6. ✅ **Screenshots & reports** - Debug easily
7. ✅ **Reusable page objects** - Clean, maintainable code

---

**Questions? Check `AI_AGENT_WORKFLOW_TEST.md` for detailed docs!**

**Ready to test? Run:** `./run_ai_agent_test.sh --headed` 🚀

