# 🚀 One-Command Installation

## ⚡ **Copy-Paste This Single Command**

```bash
cd /home/ubuntu/tests/e2e_tests && chmod +x install.sh && ./install.sh
```

That's it! This will:
- ✅ Install all system dependencies (requires sudo password once)
- ✅ Create Python virtual environment
- ✅ Install Python packages
- ✅ Install Playwright browsers
- ✅ Set up project structure
- ✅ Create .env configuration

---

## 📋 **What Gets Installed**

### System Packages (via apt-get)
```
libatk1.0-0, libatk-bridge2.0-0, libcups2, libatspi2.0-0,
libxcomposite1, libxdamage1, libxfixes3, libxrandr2,
libgbm1, libpango-1.0-0, libcairo2, libasound2,
libxshmfence1, libglu1-mesa, fonts-liberation, libnss3, libnspr4
```

### Python Packages (via pip)
```
pytest, playwright, python-dotenv, requests, faker
```

### Playwright Browsers
```
Chromium (headless-capable)
```

---

## 🏃 **After Installation**

### For dev.dagknows.com (Default)
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
./run_ai_agent_test.sh
```

### For Local Docker
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
./run_ai_agent_test.sh --local
```

### Single Test File
```bash
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 🔧 **Manual Installation (If Automatic Fails)**

### Step 1: System Dependencies
```bash
cd /home/ubuntu/tests/e2e_tests
sudo apt-get update
sudo apt-get install -y $(cat system_requirements.txt | grep -v '^#')
```

### Step 2: Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Playwright
```bash
playwright install chromium
```

### Step 4: Project Structure
```bash
./setup.sh
```

---

## ❓ **Troubleshooting**

### Permission Denied
```bash
chmod +x install.sh
./install.sh
```

### Already Installed
If you've already set up parts of the environment, the script will skip those steps.

### Check Installation
```bash
source venv/bin/activate
python3 -c "import playwright; print('✓ Playwright installed')"
playwright --version
pytest --version
```

---

## 📂 **File Structure After Installation**

```
e2e_tests/
├── venv/                    # Virtual environment (auto-created)
├── .env                     # Config (auto-created from template)
├── reports/                 # Test results
│   └── screenshots/         # Auto-captured screenshots
├── __init__.py             # Package markers (all auto-created)
├── config/__init__.py
├── fixtures/__init__.py
├── pages/__init__.py
├── api_tests/__init__.py
├── ui_tests/__init__.py
└── utils/__init__.py
```

---

## ✅ **Verify Installation**

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py::test_ai_agent_direct_navigation -v
```

Expected output:
```
test_ai_agent_direct_navigation[chromium] PASSED

1 passed in 15.23s
```

---

**Ready to test? Run the installation command!** 🎉

