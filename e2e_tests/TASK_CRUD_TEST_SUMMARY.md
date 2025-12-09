# 📝 Task CRUD E2E Test - Summary

## ✅ What Was Created

### **New Task CRUD Test Suite** ✅
Complete E2E test for creating tasks using the form-based interface.

**Files Created:**
1. ✅ `pages/task_page.py` - Task management Page Object
2. ✅ `ui_tests/test_task_crud.py` - Task CRUD E2E tests
3. ✅ `run_task_crud_test.sh` - Test runner script
4. ✅ `TASK_CRUD_TEST_SUMMARY.md` - This documentation

**Files Modified:**
1. ✅ `pytest.ini` - Added `task_crud` marker

---

## 🧪 Task Creation Test

### **Test Flow:**

```
1. Login with admin user
   ↓
2. Navigate to landing page
   ↓
3. Select "Default" workspace
   ↓
4. Click "New Task" button (top right)
   ↓
5. Select "Create from Form" from dropdown
   ↓
6. Fill task details:
   - Title: TestTask_<timestamp>
   - Description: Test description
   - Code: Python script
   ↓
7. Scroll to bottom
   ↓
8. Click "Save" button
   ↓
9. Verify task created (check URL)
```

### **Expected Result:**
✅ Task is created successfully  
✅ URL contains `taskId=` or `/task/` or `/tasks/`  
✅ Task title visible on page (if available)  

---

## 🚀 How to Run

### **Quick Run (dev.dagknows.com):**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
./run_task_crud_test.sh
```

### **Run Specific Test:**
```bash
# Create from form test
./run_task_crud_test.sh --create-from-form

# Minimal task creation (title + code only)
./run_task_crud_test.sh --minimal
```

### **With Visible Browser:**
```bash
./run_task_crud_test.sh --headed
```

### **Slow Motion (for debugging):**
```bash
./run_task_crud_test.sh --headed --slow
```

### **Local Docker:**
```bash
./run_task_crud_test.sh --local
```

---

## 📋 Test Details

### **Test Class:** `TestTaskCRUDE2E`
### **Test Methods:**
1. **`test_create_task_from_form`** - Complete task creation with all fields
2. **`test_create_task_with_minimal_data`** - Create with title + code only

### **Markers:** `@pytest.mark.ui`, `@pytest.mark.e2e`, `@pytest.mark.task_crud`

### **Test Data:**
- **Title:** `TestTask_<timestamp>` (unique each time)
- **Description:** Automated test description
- **Code:** Sample Python script with timestamp
- **User:** `yash+user@dagknows.com` (Admin)

---

## 📸 Screenshots Captured

The test captures ~10-12 screenshots:

1. `01-task-after-login.png` - After login
2. `02-task-landing-page.png` - Landing page
3. `03-task-workspace-view.png` - Workspace view
4. `04-task-new-task-dropdown.png` - New Task dropdown
5. `05-task-creation-form.png` - Task creation form
6. `06a-task-title-filled.png` - Title filled
7. `06b-task-description-filled.png` - Description filled
8. `06c-task-code-filled.png` - Code filled
9. `07a-task-scrolled-to-save.png` - Scrolled to Save button
10. `07b-task-after-save.png` - After clicking Save
11. `08-task-creation-verified.png` - Verification

All screenshots are in: `reports/screenshots/`

---

## 🔍 Page Object: TaskPage

### **Key Methods:**

#### **Navigation:**
- `click_new_task_button()` - Opens New Task dropdown
- `click_create_from_form()` - Selects "Create from Form"

#### **Form Filling:**
- `fill_task_title(title)` - Fills task title
- `fill_task_description(description)` - Fills description
- `fill_task_code(code)` - Fills code editor

#### **Actions:**
- `scroll_to_bottom()` - Scrolls to Save button
- `click_save_button()` - Clicks Save

#### **Verification:**
- `verify_task_created(title)` - Verifies task creation

#### **Workflow:**
- `complete_task_creation_workflow(title, desc, code)` - All-in-one method

---

## 📊 Test Markers

Run specific test categories:

```bash
# Run only task CRUD tests
pytest -m task_crud

# Run all UI tests
pytest -m ui

# Run all E2E tests
pytest -m e2e

# Combine markers
pytest -m "ui and task_crud"
```

---

## ⚠️ Important Notes

### **Task Cleanup:**
- **Tasks are NOT deleted** after the test
- Each test run creates a new task: `TestTask_<timestamp>`
- You can manually delete test tasks via the UI

### **Code Editor:**
- Uses Monaco editor detection
- Handles both textarea and contenteditable
- Clears existing content before filling

### **Save Button:**
- Scrolls to bottom automatically
- Tries multiple selectors for robustness
- Waits for navigation after save

---

## 🆚 Comparison: Task Creation Methods

| Method | Test | Form Fields | Duration |
|--------|------|-------------|----------|
| **AI Agent** | `test_ai_agent_workflow.py` | Prompt only | 90-120s (AI generation) |
| **Form-based** | `test_task_crud.py` | Title, Desc, Code | 60-80s |

**Task CRUD test is faster** because it doesn't wait for AI generation!

---

## 🐛 Troubleshooting

### **Issue: New Task button not found**
**Solution:**
1. Check screenshot: `new-task-button-not-found.png`
2. Verify you're in workspace view (URL contains `?space=`)
3. Button might be in top-right header

### **Issue: Create from Form not found**
**Solution:**
1. Check dropdown opened (screenshot #4)
2. Verify dropdown items are visible
3. Try clicking New Task again

### **Issue: Code editor not found**
**Solution:**
1. Check if on Code tab (click it if exists)
2. Monaco editor uses `.monaco-editor textarea.inputarea`
3. Try scrolling to code section

### **Issue: Save button not found**
**Solution:**
1. Scroll to bottom of page
2. Button might be `"Create Task"` instead of `"Save"`
3. Check screenshot: `save-button-not-found.png`

---

## 📄 Related Documentation

- `README.md` - Main E2E test suite documentation
- `AI_AGENT_WORKFLOW_TEST.md` - AI-based task creation
- `WORKSPACE_TEST_SUMMARY.md` - Workspace management
- `ALERT_HANDLING_TESTS.md` - Alert handling tests
- `ALL_TESTS_GUIDE.md` - Complete test suite reference

---

## ✅ Summary

### **Task CRUD Test Features:**
✅ Form-based task creation  
✅ Title, description, and code fields  
✅ Automatic scrolling  
✅ Robust selector strategies  
✅ Screenshot debugging  
✅ URL verification  
✅ Minimal data test (optional fields)  

### **Total Tests:** 2
1. Complete task creation (all fields)
2. Minimal task creation (title + code)

### **Total Duration:** ~60-80 seconds per test

### **Ready to Run:**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
./run_task_crud_test.sh --headed --slow
```

---

**Task CRUD test is ready!** 🚀

The test will:
- ✅ Create a task with unique name
- ✅ Fill all form fields
- ✅ Scroll and click Save
- ✅ Verify task creation via URL

**Expected Duration:** 60-80 seconds  
**Screenshots:** 10-12 captured at each step  
**Tasks Created:** `TestTask_<timestamp>` (not auto-deleted)

