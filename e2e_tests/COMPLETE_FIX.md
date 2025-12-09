# 🔧 Complete Fix for Module Import Error

## ✅ **Copy-Paste This Entire Block**

Run this on your Ubuntu server to fix the import error:

```bash
cd /home/ubuntu/tests/e2e_tests

# Make sure venv is activated
source venv/bin/activate

# Create ALL required __init__.py files
echo "Creating __init__.py files..."
touch __init__.py
touch config/__init__.py
touch fixtures/__init__.py
touch pages/__init__.py
touch api_tests/__init__.py
touch ui_tests/__init__.py
touch utils/__init__.py

# Verify they were created
echo "Verifying files..."
ls -la config/__init__.py fixtures/__init__.py pages/__init__.py

# Create reports directory
mkdir -p reports/screenshots

# Set PYTHONPATH to current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "✓ Setup complete!"
echo ""
echo "Now run tests:"
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 🔍 **Verify Files Exist**

After running the commands above, verify:

```bash
cd /home/ubuntu/tests/e2e_tests

# Check all __init__.py files
ls -la */__init__.py

# Should show:
# api_tests/__init__.py
# config/__init__.py
# fixtures/__init__.py
# pages/__init__.py
# ui_tests/__init__.py
# utils/__init__.py
```

---

## 🚀 **Then Run Tests**

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

**OR use the test runner script:**
```bash
./run_ai_agent_test.sh --headed
```

(The script automatically sets PYTHONPATH)

---

## 💡 **Why This Happens**

Git might not track empty `__init__.py` files, or they weren't synced properly. Python needs these files in each directory to treat them as packages.

---

**Try the commands above and let me know if it works!** 🎯

