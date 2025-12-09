# 🔧 Ubuntu 24.04 (Noble) Package Fix

## 🎯 **Quick Fix - Copy & Paste**

```bash
cd /home/ubuntu/tests/e2e_tests
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
```

Then continue with your tests:

```bash
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 📝 **What's the Issue?**

Ubuntu 24.04 (Noble Numbat) renamed several packages with `t64` suffix:

| Old Name (Ubuntu 22.04) | New Name (Ubuntu 24.04) |
|-------------------------|-------------------------|
| `libasound2`           | `libasound2t64`         |
| `libatk1.0-0`          | `libatk1.0-0t64`        |
| `libatk-bridge2.0-0`   | `libatk-bridge2.0-0t64` |
| `libatspi2.0-0`        | `libatspi2.0-0t64`      |
| `libcups2`             | `libcups2t64`           |
| `libglib2.0-0`         | `libglib2.0-0t64`       |

The `t64` suffix indicates 64-bit `time_t` support (Y2038 problem fix).

---

## 🚀 **Use Updated Install Script**

The `install.sh` script has been updated to handle both old and new package names:

```bash
cd /home/ubuntu/tests/e2e_tests
./install.sh
```

It will:
1. Try to install `t64` packages first (Ubuntu 24.04)
2. Fall back to old names if needed (Ubuntu 22.04)
3. Continue even if some packages fail

---

## 🐛 **If You See This Error**

```
E: Package 'libasound2' has no installation candidate
Failed to install browser dependencies
```

**Solution**: Run the quick fix command above, or use the updated `install.sh`.

---

## ✅ **Verify Installation**

```bash
# Check if packages are installed
dpkg -l | grep libatk
dpkg -l | grep libasound
dpkg -l | grep libcups

# Should show t64 versions on Ubuntu 24.04
```

---

## 📚 **For Other Ubuntu Versions**

### Ubuntu 22.04 (Jammy) - Use old names
```bash
sudo apt-get install -y \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libasound2 \
    libglib2.0-0 \
    ...other packages...
```

### Ubuntu 24.04+ (Noble+) - Use t64 names
```bash
sudo apt-get install -y \
    libatk1.0-0t64 \
    libatk-bridge2.0-0t64 \
    libcups2t64 \
    libatspi2.0-0t64 \
    libasound2t64 \
    libglib2.0-0t64 \
    ...other packages...
```

---

## 🎉 **After Fix**

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

Expected output:
```
test_complete_ai_agent_workflow[chromium] PASSED
test_ai_agent_direct_navigation[chromium] PASSED
test_ai_agent_workflow_with_complete_flow[chromium] PASSED

3 passed in ~45s
```

---

## 🔍 **Check Ubuntu Version**

```bash
lsb_release -a
# or
cat /etc/os-release
```

Ubuntu 24.04 will show:
```
DISTRIB_CODENAME=noble
```

---

**Run the quick fix command and you're good to go!** 🚀

