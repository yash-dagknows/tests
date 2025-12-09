# 🖥️ Running E2E Tests on Ubuntu Server

Special instructions for headless Ubuntu servers.

---

## ⚡ **Quick Fix - Run This Now**

```bash
# Install Playwright system dependencies
sudo playwright install-deps chromium

# Then run tests (headless mode)
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 🎯 **Complete Setup for Ubuntu Server**

### **Step 1: Install system dependencies**

```bash
# Option A: Use Playwright with full path (recommended)
sudo /home/ubuntu/tests/e2e_tests/venv/bin/playwright install-deps chromium

# Option B: Use apt-get directly
sudo apt-get update && sudo apt-get install -y \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libxshmfence1 \
    libglu1-mesa \
    fonts-liberation \
    libnss3 \
    libnspr4
```

**Note:** `sudo playwright` won't work because sudo doesn't see your venv. Use full path or apt-get directly.

### **Step 2: Run tests in HEADLESS mode**

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate

# Run WITHOUT --headed flag (server has no display)
pytest ui_tests/test_ai_agent_workflow.py -v

# Or use test runner
./run_ai_agent_test.sh  # No --headed!
```

---

## 📊 **Headless vs Headed Mode**

### **Headless Mode** (for servers)
```bash
# No visible browser - runs in background
pytest ui_tests/test_ai_agent_workflow.py -v
```
- ✅ Works on servers without display
- ✅ Screenshots still captured
- ✅ Faster execution
- ✅ Recommended for CI/CD

### **Headed Mode** (for local development)
```bash
# Opens visible browser window
pytest ui_tests/test_ai_agent_workflow.py -v --headed
```
- ⚠️ Requires display (X server)
- ⚠️ Won't work on headless servers
- ✅ Good for debugging locally

---

## 🚀 **Complete Setup Commands (Ubuntu Server)**

Copy-paste this entire block:

```bash
# Navigate to folder
cd /home/ubuntu/tests/e2e_tests

# Install system dependencies
sudo playwright install-deps chromium

# Activate venv
source venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run tests in headless mode
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 📸 **Screenshots on Server**

Even in headless mode, screenshots are captured!

```bash
# View screenshots after test
ls -la reports/screenshots/

# Download screenshots to local machine (from your local terminal)
scp -r ubuntu@your-server:/home/ubuntu/tests/e2e_tests/reports/screenshots/ ./
```

---

## 🎯 **For CI/CD / Headless Servers**

### **Recommended pytest.ini config:**

The `pytest.ini` already configures headless mode as default. To force headless:

```bash
# Run in headless mode explicitly
pytest ui_tests/test_ai_agent_workflow.py -v --browser chromium --headed=false
```

---

## 💡 **Best Practice for Server Testing**

1. **Use headless mode** - Server has no display
2. **Capture screenshots** - For debugging (already configured)
3. **Generate HTML reports** - View results easily
4. **Download artifacts** - Copy screenshots/reports to local machine

### **Complete Server Test Run:**

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate

# Run tests (headless)
pytest ui_tests/test_ai_agent_workflow.py -v \
    --html=reports/report.html \
    --self-contained-html

# Download results (run from your local machine)
scp ubuntu@your-server:/home/ubuntu/tests/e2e_tests/reports/report.html ./
scp -r ubuntu@your-server:/home/ubuntu/tests/e2e_tests/reports/screenshots/ ./
```

---

## 🔧 **Verify Setup**

### **Check system dependencies installed:**
```bash
dpkg -l | grep libgbm1
dpkg -l | grep libatk1.0-0
# Should show installed packages
```

### **Check Playwright browsers:**
```bash
source venv/bin/activate
playwright --version
```

### **Test browser can launch:**
```bash
python3 -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(); print('✓ Browser launched!'); browser.close()"
```

---

## ✅ **Summary for Ubuntu Server**

| Step | Command | Why |
|------|---------|-----|
| 1 | `sudo playwright install-deps` | Install system libraries |
| 2 | `source venv/bin/activate` | Activate Python venv |
| 3 | `pytest -v` (no --headed) | Run in headless mode |
| 4 | Download screenshots/reports | View results locally |

---

## 🎯 **Your Next Commands**

Run these **right now** on your Ubuntu server:

```bash
# Install dependencies
sudo playwright install-deps chromium

# Run tests
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v
```

**Should work!** 🚀

