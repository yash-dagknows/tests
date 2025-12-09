# 🚀 Run E2E Tests RIGHT NOW!

Copy and paste these commands to run your first test in 2 minutes!

---

## ⚡ **Test Against Dev (Fastest - 2 minutes)**

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests/e2e_tests

# Install (first time only)
pip install -r requirements.txt
playwright install chromium

# Setup (already pre-configured!)
cp env.template .env

# Run test with visible browser
./run_ai_agent_test.sh --headed
```

**✅ That's it! Watch the browser automate your workflow!**

---

## 🏠 **Test Against Localhost (5 minutes)**

### **Step 1: Start Local App**
```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d
```

### **Step 2: Get JWT Token**
1. Open browser: http://localhost
2. Login: `yash+user@dagknows.com` / `1Hey2Yash*`
3. Press F12 → Application → Local Storage
4. Copy `authToken` value

### **Step 3: Setup & Run**
```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests/e2e_tests

# Install (first time only)
pip install -r requirements.txt
playwright install chromium

# Setup
cp env.template .env

# Edit .env file:
nano .env
# Change:
#   DAGKNOWS_URL=http://localhost
#   DAGKNOWS_PROXY=?proxy=yashlocal
#   DAGKNOWS_TOKEN=<paste-token-from-step-2>
# Save: Ctrl+X, Y, Enter

# Run test
./run_ai_agent_test.sh --local --headed
```

---

## 📊 **View Results**

```bash
# Screenshots (taken at each step)
ls -la reports/screenshots/

# HTML report
open reports/ai_agent_test_report.html
```

---

## 🎯 **What You'll See**

With `--headed` flag, you'll watch:
1. ✅ Browser opens
2. ✅ Navigates to login
3. ✅ Enters credentials
4. ✅ Logs in
5. ✅ Navigates to landing page
6. ✅ Clicks "Default" workspace
7. ✅ Clicks "New Task"
8. ✅ Selects "Create with AI Agent"
9. ✅ Types test message
10. ✅ Sends message
11. ✅ Waits for AI response
12. ✅ Test passes!

**All automated! No manual clicking!** 🎬

---

## 💡 **Pro Tips**

- Start with **dev** - it's pre-configured
- Use `--headed` to watch the browser
- Screenshots saved on failure for debugging
- Token for dev valid until 2026!

---

## 🐛 **If Something Fails**

```bash
# Check configuration
cat .env

# Run with more output
pytest ui_tests/test_ai_agent_workflow.py -v -s

# Check screenshots for what went wrong
ls reports/screenshots/
```

---

## ✅ **Credentials (Already Configured)**

```
Email:    yash+user@dagknows.com
Password: 1Hey2Yash*
```

---

**Ready? Copy the commands above and run!** 🚀

**Recommended:** Start with dev.dagknows.com (top section) - it's the easiest!

