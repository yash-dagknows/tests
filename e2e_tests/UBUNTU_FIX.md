# ✅ Ubuntu Server - Quick Fix

## 🎯 **Copy-Paste This Single Command**

### For Ubuntu 24.04 (Noble)
```bash
sudo apt-get update && sudo apt-get install -y libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libatspi2.0-0t64 libasound2t64 libglib2.0-0t64 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libxshmfence1 libglu1-mesa fonts-liberation libnss3 libnspr4 libdbus-1-3 libxcb1 libxkbcommon0 libx11-6 libx11-xcb1 && cd /home/ubuntu/tests/e2e_tests && source venv/bin/activate && export PYTHONPATH="${PYTHONPATH}:$(pwd)" && pytest ui_tests/test_ai_agent_workflow.py -v
```

### For Ubuntu 22.04 or older
```bash
sudo apt-get update && sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libatspi2.0-0 libasound2 libglib2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libxshmfence1 libglu1-mesa fonts-liberation libnss3 libnspr4 libdbus-1-3 libxcb1 libxkbcommon0 libx11-6 libx11-xcb1 && cd /home/ubuntu/tests/e2e_tests && source venv/bin/activate && export PYTHONPATH="${PYTHONPATH}:$(pwd)" && pytest ui_tests/test_ai_agent_workflow.py -v
```

> **Note**: Ubuntu 24.04 uses `t64` suffix for some packages. See [UBUNTU_24_FIX.md](UBUNTU_24_FIX.md) for details.

This installs dependencies AND runs the test! ✅

---

## 📝 **Or Step-by-Step**

### **Step 1: Install system libraries**
```bash
sudo apt-get update
sudo apt-get install -y \
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

### **Step 2: Run tests**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 💡 **Why sudo playwright Didn't Work**

When you run `sudo`, it uses the system Python, not your venv:

```bash
# ❌ WRONG - sudo doesn't see venv
sudo playwright install-deps

# ✅ RIGHT - Use full path
sudo /home/ubuntu/tests/e2e_tests/venv/bin/playwright install-deps chromium

# ✅ OR EASIER - Install packages directly
sudo apt-get install libatk1.0-0 libatk-bridge2.0-0 ...
```

---

## 🖥️ **Headless Server Notes**

Since you're on a server without display:

1. **Don't use --headed flag**
   ```bash
   # ❌ Won't work on server
   ./run_ai_agent_test.sh --headed
   
   # ✅ Use headless mode
   ./run_ai_agent_test.sh
   ```

2. **Screenshots still work!**
   - Screenshots are captured even in headless mode
   - Find them in: `reports/screenshots/`

3. **View results remotely**
   ```bash
   # From your local machine
   scp -r ubuntu@your-server:/home/ubuntu/tests/e2e_tests/reports/ ./
   ```

---

## ✅ **After Installing Dependencies**

Your tests should now run successfully:

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v
```

**Expected output:**
```
test_complete_ai_agent_workflow[chromium] PASSED
test_ai_agent_direct_navigation[chromium] PASSED
test_ai_agent_workflow_with_complete_flow[chromium] PASSED

3 passed in 45.23s
```

---

**Run the apt-get command and then your tests!** 🚀

