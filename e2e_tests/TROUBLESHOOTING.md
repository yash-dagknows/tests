# 🐛 Troubleshooting E2E Tests

Common issues and solutions.

---

## 🔴 **Issue: "externally-managed-environment" Error**

### **Error Message:**
```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
```

### **✅ Solution: Use Virtual Environment**

This happens on Ubuntu/Debian systems. You need to use a virtual environment:

```bash
cd tests/e2e_tests

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Now install packages
pip install -r requirements.txt
playwright install chromium

# Run tests
./run_ai_agent_test.sh --headed
```

**Important:** Always activate venv before running tests:
```bash
source venv/bin/activate
```

To deactivate:
```bash
deactivate
```

---

## 🔴 **Issue: "ModuleNotFoundError: No module named 'fixtures'"**

### **Error Message:**
```
ModuleNotFoundError: No module named 'fixtures'
ImportError while loading conftest
```

### **✅ Solution: Run setup script**

This happens when `__init__.py` files are missing or Python can't find modules.

```bash
cd tests/e2e_tests

# Run setup script to create all required files
./setup.sh

# Now run tests
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v
```

**OR manually create files:**
```bash
cd tests/e2e_tests

# Create all __init__.py files
touch __init__.py
touch config/__init__.py
touch fixtures/__init__.py
touch pages/__init__.py
touch api_tests/__init__.py
touch ui_tests/__init__.py
touch utils/__init__.py

# Set PYTHONPATH and run
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 🔴 **Issue: "playwright: command not found"**

### **✅ Solution:**
```bash
# Make sure you're in virtual environment
source venv/bin/activate

# Install playwright
pip install playwright
playwright install chromium
```

---

## 🔴 **Issue: "Login failed" or "401 Unauthorized"**

### **For dev.dagknows.com:**
- Token should be already configured in template
- If still fails, token might be expired
- Get new token from dev.dagknows.com browser

### **For localhost:**
- Make sure you got token from localhost browser (not dev!)
- Token is different for each environment
- Steps to get token:
  1. Login to http://localhost
  2. F12 → Application → Local Storage
  3. Copy `authToken` value
  4. Update in `.env`

---

## 🔴 **Issue: "Connection refused" (localhost)**

### **✅ Solution: Start local app**

```bash
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d

# Wait for services to start
sleep 30

# Check status
docker-compose -f local-docker-c-backup-bfr-reorder.yml ps
```

All services should show "Up".

---

## 🔴 **Issue: "404 Not Found"**

### **✅ Solution: Check proxy parameter**

| Environment | Required Proxy |
|-------------|----------------|
| dev.dagknows.com | `?proxy=dev1` |
| localhost | `?proxy=yashlocal` |

Check your `.env`:
```bash
cat .env | grep PROXY
```

---

## 🔴 **Issue: Browser doesn't open with --headed**

### **✅ Solution: Install chromium**

```bash
source venv/bin/activate
playwright install chromium
```

---

## 🔴 **Issue: "Module not found" errors**

### **✅ Solution: Reinstall in venv**

```bash
cd tests/e2e_tests
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔴 **Issue: Test fails at login page**

### **Possible causes:**

1. **Wrong password**
   - Check: `1Hey2Yash*` (note the asterisk!)

2. **User doesn't exist**
   - Verify `yash+user@dagknows.com` exists in your environment

3. **Waiting for page load**
   - Increase timeout in test if slow network

### **Debug:**
```bash
# Run with visible browser to see what happens
./run_ai_agent_test.sh --headed

# Check screenshots
ls -la reports/screenshots/
```

---

## 🔴 **Issue: "New Task button not found"**

### **Possible causes:**

1. **User doesn't have permissions**
   - User must be Admin role

2. **Page not loaded**
   - Test has 10s timeout, should be enough

3. **Wrong workspace**
   - Make sure clicking "Default" workspace

### **Debug:**
```bash
# Check screenshot: 03-workspace-view.png
ls reports/screenshots/03-workspace-view.png
```

---

## 🔴 **Issue: Tests pass but no screenshots**

### **✅ Solution: Create directory**

```bash
mkdir -p reports/screenshots
```

---

## 🔴 **Issue: Import errors in tests**

### **✅ Solution: Make sure in correct directory**

```bash
cd tests/e2e_tests
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 🔴 **Issue: Docker containers won't start (localhost)**

### **✅ Solution: Check logs and ports**

```bash
cd app_docker_compose_build_deploy

# Check logs
docker-compose -f local-docker-c-backup-bfr-reorder.yml logs

# Check ports aren't in use
docker-compose -f local-docker-c-backup-bfr-reorder.yml ps

# Restart everything
docker-compose -f local-docker-c-backup-bfr-reorder.yml down
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d
```

---

## ✅ **Verification Checklist**

Before running tests, verify:

### **For Dev:**
- [ ] Virtual environment activated (`source venv/bin/activate`)
- [ ] Dependencies installed (`pip list | grep playwright`)
- [ ] `.env` file exists and has correct values
- [ ] Token is for dev.dagknows.com
- [ ] Proxy is `?proxy=dev1`

### **For Local:**
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Local app is running (`docker-compose ps`)
- [ ] Token from localhost browser
- [ ] Proxy is `?proxy=yashlocal`
- [ ] Can access http://localhost

---

## 🎯 **Quick Checks**

### **Check venv is activated:**
```bash
which python
# Should show: .../tests/e2e_tests/venv/bin/python
```

### **Check playwright installed:**
```bash
pip list | grep playwright
```

### **Check configuration:**
```bash
cat .env
```

### **Check local app running:**
```bash
curl http://localhost
# Should return HTML
```

---

## 💡 **Best Practices**

1. **Always use virtual environment**
   - Prevents system package conflicts
   - Clean dependency management

2. **Activate venv every time**
   - Before running tests
   - Before installing packages

3. **Get fresh tokens**
   - If 401 errors
   - After restarting local app

4. **Use --headed during debugging**
   - See what's happening
   - Easier to diagnose issues

5. **Check screenshots**
   - Every test saves screenshots
   - Great for debugging failures

---

## 📞 **Still Stuck?**

1. **Check screenshots:** `reports/screenshots/`
2. **Run with output:** `pytest ui_tests/test_ai_agent_workflow.py -v -s`
3. **Check logs:** Look for error messages
4. **Try dev first:** Easier than local setup

---

## 🔍 **Debugging Commands**

```bash
# Verbose output
pytest ui_tests/test_ai_agent_workflow.py -v -s

# Keep browser open on failure
pytest ui_tests/test_ai_agent_workflow.py --headed

# Slow motion (see each action)
./run_ai_agent_test.sh --slow

# Check Python environment
which python
pip list

# Check configuration
cat .env | grep -v TOKEN  # Hide token for security

# Test connectivity
curl -I https://dev.dagknows.com  # For dev
curl -I http://localhost  # For local
```

---

**Most Common Fix:** Use virtual environment! 🎯

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

