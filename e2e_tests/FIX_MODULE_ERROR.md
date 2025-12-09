# 🔧 Fix: "ModuleNotFoundError: No module named 'fixtures'"

## ✅ **Quick Fix (Copy-Paste These Commands)**

```bash
cd /home/ubuntu/tests/e2e_tests

# Make sure venv is activated
source venv/bin/activate

# Run setup script to create required files
./setup.sh

# Now run tests - should work!
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 🎯 **What This Does**

The `setup.sh` script:
1. ✅ Creates all required `__init__.py` files
2. ✅ Creates `reports/screenshots/` directory
3. ✅ Ensures Python can find all modules

---

## 🔍 **Why This Happened**

Python needs `__init__.py` files in each directory to recognize them as packages. When you cloned/synced the repo, these empty files might not have been created on the Ubuntu server.

---

## 📝 **Manual Fix (If setup.sh Doesn't Work)**

```bash
cd /home/ubuntu/tests/e2e_tests

# Create all __init__.py files manually
touch __init__.py
touch config/__init__.py
touch fixtures/__init__.py
touch pages/__init__.py
touch api_tests/__init__.py
touch ui_tests/__init__.py
touch utils/__init__.py

# Create reports directory
mkdir -p reports/screenshots

# Set PYTHONPATH and run
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## ✅ **Verify Setup**

Check all files exist:
```bash
ls -la */__init__.py
```

Should show:
```
api_tests/__init__.py
config/__init__.py
fixtures/__init__.py
pages/__init__.py
ui_tests/__init__.py
utils/__init__.py
```

---

## 🚀 **After Fix - Run Tests**

```bash
# Option 1: Using test script (recommended)
./run_ai_agent_test.sh --headed

# Option 2: Direct pytest
source venv/bin/activate
pytest ui_tests/test_ai_agent_workflow.py -v

# Option 3: Run all tests
pytest -v
```

---

## 💡 **Note**

The `run_ai_agent_test.sh` script now automatically sets `PYTHONPATH`, so using the script is the easiest way!

---

**TL;DR: Just run `./setup.sh` and you're good to go!** ✨

