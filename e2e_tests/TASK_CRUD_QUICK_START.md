# 🚀 Task CRUD Test - Quick Start

## ✅ What This Test Does

Creates a task using the form-based interface (not AI):
1. Login
2. Go to Default workspace
3. Click "New Task" → "Create from Form"
4. Fill: Title, Description, Code
5. Save
6. Verify creation

---

## 🏃 Run the Test

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
./run_task_crud_test.sh
```

### **With Visible Browser:**
```bash
./run_task_crud_test.sh --headed --slow
```

---

## 📊 What Gets Created

**Task Title:** `TestTask_<timestamp>`  
**Task Description:** Test description  
**Task Code:** Sample Python script  
**Duration:** 60-80 seconds  
**Screenshots:** 10-12 captured  

---

## 📸 Key Screenshots

1. `01-task-after-login.png` - Logged in
2. `04-task-new-task-dropdown.png` - Dropdown open
3. `05-task-creation-form.png` - Form loaded
4. `06c-task-code-filled.png` - All fields filled
5. `07b-task-after-save.png` - After save
6. `08-task-creation-verified.png` - Verified

**Location:** `reports/screenshots/`

---

## ✅ Expected Result

**URL contains:** `taskId=` or `/task/` or `/tasks/`  
**Task appears** in task list  
**Test passes** ✅

---

## 🎯 Run Options

```bash
# Default (all tests)
./run_task_crud_test.sh

# Just form creation test
./run_task_crud_test.sh --create-from-form

# Minimal test (title + code only)
./run_task_crud_test.sh --minimal

# With browser visible + slow motion
./run_task_crud_test.sh --headed --slow

# Local Docker
./run_task_crud_test.sh --local
```

---

## 📚 Files Created

1. ✅ `pages/task_page.py` - Task Page Object
2. ✅ `ui_tests/test_task_crud.py` - Test file
3. ✅ `run_task_crud_test.sh` - Run script

---

## 🐛 Quick Troubleshooting

**Issue:** New Task button not found  
**Fix:** Check you're in workspace view (`?space=` in URL)

**Issue:** Code editor not found  
**Fix:** Try clicking "Code" tab first

**Issue:** Save button not found  
**Fix:** Scroll to bottom of page

---

## 📄 More Info

- Full documentation: `TASK_CRUD_TEST_SUMMARY.md`
- All tests guide: `ALL_TESTS_GUIDE.md`
- Complete summary: `FINAL_SUMMARY.md`

---

**Ready to run!** 🚀

```bash
./run_task_crud_test.sh --headed --slow
```

The test will create a task with all fields filled and verify creation!

