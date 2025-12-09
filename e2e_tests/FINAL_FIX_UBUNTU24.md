# ✅ Final Fix for Ubuntu 24.04

## 🎯 **Your Issue**

You're seeing:
```
E: Package 'libasound2' has no installation candidate
Failed to install browser dependencies
```

**Root Cause**: Ubuntu 24.04 (Noble) renamed packages with `t64` suffix.

---

## 🚀 **Quick Fix - Copy & Paste**

### **Option 1: Use Updated Install Script** (Recommended)

```bash
cd /home/ubuntu/tests/e2e_tests
./install.sh
```

This will install everything automatically!

---

### **Option 2: Manual Package Install**

```bash
cd /home/ubuntu/tests/e2e_tests

# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    libatk1.0-0t64 \
    libatk-bridge2.0-0t64 \
    libcups2t64 \
    libatspi2.0-0t64 \
    libasound2t64 \
    libglib2.0-0t64 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libxshmfence1 \
    libglu1-mesa \
    fonts-liberation \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libx11-xcb1

# Activate venv and run tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 📋 **What Changed**

We've updated the following files to support Ubuntu 24.04:

1. ✅ **`system_requirements.txt`** - Now uses `t64` package names
2. ✅ **`install.sh`** - Handles both Ubuntu 24.04 and older versions
3. ✅ **Documentation** - Added Ubuntu 24.04 specific guides

---

## 🧪 **Run Tests**

After installing packages:

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

Expected output:
```
test_complete_ai_agent_workflow[chromium] PASSED       [33%]
test_ai_agent_direct_navigation[chromium] PASSED       [66%]
test_ai_agent_workflow_with_complete_flow[chromium] PASSED [100%]

========================= 3 passed in 45.23s =========================
```

---

## 🔍 **Verify Packages Are Installed**

```bash
dpkg -l | grep -E "libasound2|libatk|libcups"
```

You should see:
```
ii  libasound2t64:amd64           1.2.11-1ubuntu0.1
ii  libatk1.0-0t64:amd64          2.52.0-1build1
ii  libatk-bridge2.0-0t64:amd64   2.52.0-1build1
ii  libcups2t64:amd64             2.4.7-1.2ubuntu6
```

Notice the `t64` suffix - that's correct for Ubuntu 24.04!

---

## 📚 **Additional Documentation**

- 📖 [UBUNTU_24_FIX.md](UBUNTU_24_FIX.md) - Detailed Ubuntu 24.04 guide
- 📖 [ONE_COMMAND_INSTALL.md](ONE_COMMAND_INSTALL.md) - Full installation guide
- 📖 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- 📖 [INSTALLATION_SUMMARY.md](INSTALLATION_SUMMARY.md) - What gets installed

---

## ⚡ **TL;DR - Just Run This**

```bash
cd /home/ubuntu/tests/e2e_tests
sudo apt-get install -y libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libatspi2.0-0t64 libasound2t64 libglib2.0-0t64 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libxshmfence1 libglu1-mesa fonts-liberation libnss3 libnspr4 libdbus-1-3 libxcb1 libxkbcommon0 libx11-6 libx11-xcb1
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

**That's it! Your tests should now run successfully.** 🎉

---

## 🆘 **Still Having Issues?**

If you encounter any other errors, check:

1. **Virtual environment**: `source venv/bin/activate` ✓
2. **PYTHONPATH**: `export PYTHONPATH="${PYTHONPATH}:$(pwd)"` ✓
3. **Packages installed**: `dpkg -l | grep libatk` ✓
4. **Playwright installed**: `playwright --version` ✓

Or open [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more help.

---

**Your tests are ready to run!** 🚀

