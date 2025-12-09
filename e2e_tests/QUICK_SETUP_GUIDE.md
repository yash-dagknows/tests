# 🚀 Quick Setup Guide - E2E Tests

Choose your environment and follow the steps!

---

## 📋 **Prerequisites (Both)**

```bash
# 1. Python 3.8+
python --version

# 2. Git repository cloned
cd /Users/yashyaadav/dag_workspace/dagknows_src
```

---

## 🌐 **Option 1: Test Against dev.dagknows.com** (Recommended First)

### **Step 1: Navigate to tests folder**
```bash
cd tests/e2e_tests
```

### **Step 2: Create virtual environment and install dependencies**
```bash
# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

**Note:** Always activate venv before running tests:
```bash
source venv/bin/activate
```

### **Step 3: Run setup script**
```bash
# Creates all required __init__.py files and directories
./setup.sh
```

### **Step 4: Create .env file**
```bash
# Copy template
cp env.template .env
```

The `.env` file is already pre-configured for dev.dagknows.com! ✅

**Verify it looks like this:**
```bash
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_PROXY=?proxy=dev1
DAGKNOWS_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJ5YXNoQGRhZ2tub3dzLmNvbSIsIm5iZiI6MTc2MTE0NjUxMSwiZXhwIjoxNzkyNjgyNjkxLCJqdGkiOiJZMENWR055N01CQzlKYjNQIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoiYWRtaW4iLCJ1c2VyX2NsYWltcyI6eyJ1aWQiOiIzOSIsInVuYW1lIjoieWFzaEBkYWdrbm93cy5jb20iLCJvcmciOiJkYWdrbm93cyIsImZpcnN0X25hbWUiOiJZYXNoIiwibGFzdF9uYW1lIjoiWWFkYXYiLCJyb2xlIjoiQWRtaW4iLCJhZXNfa2V5IjoiY1Q0RTU2aWxDOTlVXG4tcTZ1dlRBcU15VTBwMEFcbnFJWSIsIm9mc3QiOlszNzIsMTUwLDM0Miw0MzEsMTg3LDM5MSwzOTAsMTc0LDIzMywyNzksMjQ2LDQzNiw5MSw0MjYsMjU3LDIxNiwxNzEsMzMzLDExOCwzNjMsMjc0LDE1MiwzNzEsNDM2LDEzNiwyMjAsMTI3LDY3LDQyNSwzNzMsNDM5LDMyMF19fQ.IvHXxMMm4th-jm7IyektCTW3SXxlq4olv6gByzAliuFk1y2zbr91QBY_zdifz5_KnYNk4ruVr9xLrlahC3h7rGJaFU98OiiiLAQ49CFxgUO2iqyr6XcT3GgO5ptobTtOZNV4rmrPE_6hnjPRImernp5M6FhHhCZWktL9xQqZs9N9m2az1Jk-mi0yZLaNIA25pHWcqgdiF1xCbt5STWqFG2nmt1eq7x-FXnoryEqo1HvfOg74crBcubFORpTZ5AhNRpSdqemcpDd_6t0UliPuAg3VlwIedew9RBRvytr2j9GbBC_jgCh7YJ5oQqFjVItolhSMzuKHLRRHZib8Ikz6fA
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=1Hey2Yash*
```

**✅ All credentials are already filled in!**

### **Step 5: Run the test!**
```bash
# Run with visible browser (see what happens)
./run_ai_agent_test.sh --headed

# Or run in headless mode
pytest ui_tests/test_ai_agent_workflow.py -v
```

### **✅ Done! That's it for dev.dagknows.com!**

**Expected result:**
- Browser opens (if --headed)
- Logs in automatically
- Navigates to AI Agent
- Sends a test message
- Takes screenshots
- Test passes ✅

---

## 🏠 **Option 2: Test Against Localhost** (Your Local Docker)

### **Step 1: Start your local application**
```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/app_docker_compose_build_deploy

# Start all services
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d

# Wait for services to be ready (~30 seconds)
sleep 30

# Verify services are running
docker-compose -f local-docker-c-backup-bfr-reorder.yml ps
```

**Expected output:** All services should be "Up"

### **Step 2: Get JWT token from localhost**

1. **Open browser** and go to: http://localhost
2. **Login** with:
   - Email: `yash+user@dagknows.com`
   - Password: `1Hey2Yash*`
3. **Open Dev Tools** (Press F12)
4. Go to **Application** tab → **Local Storage** → `http://localhost`
5. Find `authToken` key
6. **Copy the token value** (long string starting with `eyJ...`)

### **Step 3: Navigate to tests folder**
```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests/e2e_tests
```

### **Step 4: Install dependencies** (if not already done)
```bash
pip install -r requirements.txt
playwright install chromium
```

### **Step 5: Create .env file for local**
```bash
# Copy template
cp env.template .env

# Edit .env file
nano .env  # or use your editor
```

**Update these values in .env:**
```bash
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=yashlocal
DAGKNOWS_TOKEN=<PASTE-TOKEN-FROM-STEP-2-HERE>  # Important!
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=1Hey2Yash*
```

**Save and exit** (Ctrl+X, then Y, then Enter if using nano)

### **Step 6: Run the test!**
```bash
# Run with visible browser
./run_ai_agent_test.sh --local --headed

# Or run specific test
pytest ui_tests/test_ai_agent_workflow.py -v
```

### **✅ Done! That's it for localhost!**

**Expected result:**
- Browser opens to http://localhost
- Logs in automatically
- Navigates to AI Agent
- Sends a test message
- Takes screenshots
- Test passes ✅

---

## 🎯 **Quick Reference**

### **Test User Credentials:**
- **Email:** `yash+user@dagknows.com`
- **Password:** `1Hey2Yash*`
- **First Name:** Yash
- **Last Name:** User
- **Org:** dagknows
- **Role:** Admin

### **Dev Token** (expires 2026-06-21):
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJ5YXNoQGRhZ2tub3dzLmNvbSIsIm5iZiI6MTc2MTE0NjUxMSwiZXhwIjoxNzkyNjgyNjkxLCJqdGkiOiJZMENWR055N01CQzlKYjNQIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoiYWRtaW4iLCJ1c2VyX2NsYWltcyI6eyJ1aWQiOiIzOSIsInVuYW1lIjoieWFzaEBkYWdrbm93cy5jb20iLCJvcmciOiJkYWdrbm93cyIsImZpcnN0X25hbWUiOiJZYXNoIiwibGFzdF9uYW1lIjoiWWFkYXYiLCJyb2xlIjoiQWRtaW4iLCJhZXNfa2V5IjoiY1Q0RTU2aWxDOTlVXG4tcTZ1dlRBcU15VTBwMEFcbnFJWSIsIm9mc3QiOlszNzIsMTUwLDM0Miw0MzEsMTg3LDM5MSwzOTAsMTc0LDIzMywyNzksMjQ2LDQzNiw5MSw0MjYsMjU3LDIxNiwxNzEsMzMzLDExOCwzNjMsMjc0LDE1MiwzNzEsNDM2LDEzNiwyMjAsMTI3LDY3LDQyNSwzNzMsNDM5LDMyMF19fQ.IvHXxMMm4th-jm7IyektCTW3SXxlq4olv6gByzAliuFk1y2zbr91QBY_zdifz5_KnYNk4ruVr9xLrlahC3h7rGJaFU98OiiiLAQ49CFxgUO2iqyr6XcT3GgO5ptobTtOZNV4rmrPE_6hnjPRImernp5M6FhHhCZWktL9xQqZs9N9m2az1Jk-mi0yZLaNIA25pHWcqgdiF1xCbt5STWqFG2nmt1eq7x-FXnoryEqo1HvfOg74crBcubFORpTZ5AhNRpSdqemcpDd_6t0UliPuAg3VlwIedew9RBRvytr2j9GbBC_jgCh7YJ5oQqFjVItolhSMzuKHLRRHZib8Ikz6fA
```

---

## 🎬 **Running Tests - All Options**

### **AI Agent Workflow Test:**
```bash
# Complete workflow with visible browser
./run_ai_agent_test.sh --headed

# For localhost
./run_ai_agent_test.sh --local --headed

# Fast variant (skip navigation)
./run_ai_agent_test.sh --fast --headed

# Slow motion (see each step)
./run_ai_agent_test.sh --slow
```

### **All E2E Tests:**
```bash
# Run all tests
pytest -v

# Run only API tests
pytest api_tests/ -v

# Run only UI tests
pytest ui_tests/ -v

# Generate HTML report
pytest --html=reports/report.html
```

---

## 📸 **View Results**

After test run:

```bash
# View screenshots
ls -la reports/screenshots/

# Open HTML report
open reports/ai_agent_test_report.html  # Mac
# or
xdg-open reports/ai_agent_test_report.html  # Linux
```

---

## 🐛 **Troubleshooting**

### **Problem: "playwright not found"**
```bash
pip install playwright
playwright install chromium
```

### **Problem: "Login failed"**
- Verify password: `1Hey2Yash*`
- Check user exists in the environment
- Run with `--headed` to see what's happening

### **Problem: "Connection refused" (localhost)**
```bash
# Check if services are running
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml ps

# Restart if needed
docker-compose -f local-docker-c-backup-bfr-reorder.yml restart
```

### **Problem: "401 Unauthorized" (localhost)**
- Token is expired or wrong
- Get fresh token from localhost browser
- Make sure you're logged in when copying token

### **Problem: "404 Not Found"**
- Check proxy parameter in .env
- Dev: `?proxy=dev1`
- Local: `?proxy=yashlocal`

---

## 📝 **Configuration Checklist**

### **For dev.dagknows.com:**
- [x] `DAGKNOWS_URL=https://dev.dagknows.com`
- [x] `DAGKNOWS_PROXY=?proxy=dev1`
- [x] JWT token (already in template)
- [x] User credentials (already in template)

### **For localhost:**
- [ ] Local app running
- [ ] `DAGKNOWS_URL=http://localhost`
- [ ] `DAGKNOWS_PROXY=?proxy=yashlocal`
- [ ] JWT token from localhost browser
- [ ] User credentials: `yash+user@dagknows.com` / `1Hey2Yash*`

---

## 🎯 **Next Steps**

1. **Start with dev** - Easiest, everything pre-configured
2. **Try local** - Once dev works, try local
3. **Add more tests** - Use existing as template
4. **Integrate CI/CD** - Run tests automatically

---

## 💡 **Pro Tips**

1. **Dev is fastest to setup** - Everything already configured
2. **Use --headed** - See browser actions during development
3. **Check screenshots** - Debug failures easily
4. **Local token expires** - Get fresh one if 401 errors
5. **Dev token valid until 2026** - No need to update often

---

## ✅ **Summary**

| Environment | Setup Time | Complexity |
|-------------|------------|------------|
| **dev.dagknows.com** | 2 minutes | Easy ⭐ |
| **localhost** | 5 minutes | Medium ⭐⭐ |

**Recommendation:** Start with dev.dagknows.com - it's already fully configured! 🚀

---

**Ready to test? Run this now:**

```bash
cd tests/e2e_tests
cp env.template .env
./run_ai_agent_test.sh --headed
```

**Watch the magic happen!** ✨

