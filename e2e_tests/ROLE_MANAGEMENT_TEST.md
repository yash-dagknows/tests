# 🎭 Role Management E2E Test

## Overview

This test suite covers the **Role-Based Access Control (RBAC)** workflow for creating custom roles and assigning privileges to them.

## Test Flow

### `test_create_role_and_assign_privileges`

**Complete workflow:**
1. **Logout** - Clean state
2. **Login** - Authenticate as admin user
3. **Wait for pages to load** - Ensure UI is ready
4. **Navigate to RBAC tab** - Go to `https://dev.dagknows.com/vsettings?tab=rbac`
5. **Scroll to "Create new custom role"** - Scroll down to the role creation section
6. **Create custom role** - Create a role named `read1_<timestamp>`
7. **Verify role in table** - Confirm the role appears in the privileges table
8. **Scroll to privileges table** - Navigate to the privileges section
9. **Scroll horizontally** - Find the newly created role column (table has horizontal scroll)
10. **Assign privileges** - Check checkboxes for:
    - `task.view_code`
    - `task.view_io`
    - `task.view_description`
    - `task.list`
11. **Verify assignments** - Confirm all privileges are checked

---

## Files Created/Updated

### **New Files:**
- ✅ `ui_tests/test_role_management.py` - Main test file
- ✅ `run_role_management_test.sh` - Run script
- ✅ `ROLE_MANAGEMENT_TEST.md` - This documentation

### **Updated Files:**
- ✅ `pages/settings_page.py` - Added RBAC role management methods:
  - `navigate_to_rbac_tab()` - Navigate to RBAC tab
  - `scroll_to_create_custom_role_section()` - Scroll to role creation
  - `create_custom_role(role_name)` - Create a new role
  - `verify_role_in_privileges_table(role_name)` - Verify role exists
  - `scroll_to_privileges_table()` - Scroll to privileges section
  - `scroll_horizontally_to_role_column(role_name)` - Horizontal scroll
  - `assign_privilege_to_role(privilege_name, role_name)` - Assign privilege
  - `assign_multiple_privileges_to_role(privilege_names, role_name)` - Bulk assign
- ✅ `pytest.ini` - Added `role_management` marker

---

## Running the Test

### **Quick Start:**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
./run_role_management_test.sh
```

### **With Options:**
```bash
# Run with visible browser
./run_role_management_test.sh --headed

# Run in slow motion (for debugging)
./run_role_management_test.sh --slow

# Run against local Docker
./run_role_management_test.sh --local

# Combine options
./run_role_management_test.sh --headed --slow
```

### **Direct pytest:**
```bash
source venv/bin/activate
source setup_env.sh
pytest ui_tests/test_role_management.py -v
```

---

## Test Details

### **Test Class:**
- `TestRoleManagementE2E`

### **Test Method:**
- `test_create_role_and_assign_privileges`

### **Markers:**
- `@pytest.mark.ui`
- `@pytest.mark.e2e`
- `@pytest.mark.role_management`

### **Prerequisites:**
- Admin user credentials configured
- Access to `dev.dagknows.com` or local Docker setup
- Virtual environment activated

---

## Key Features

### **1. Role Creation**
- Creates unique role names with timestamp: `read1_<timestamp>`
- Scrolls to the "Create new custom role" section
- Fills role name input
- Clicks "Add" button
- Verifies role appears in privileges table

### **2. Horizontal Scrolling**
- Handles tables with horizontal scroll
- Finds the newly created role column
- Scrolls both table container and window if needed

### **3. Privilege Assignment**
- Assigns multiple privileges to a role
- Finds checkboxes by privilege row and role column
- Verifies checkboxes are checked after assignment

### **4. Robust Selectors**
- Multiple selector strategies for reliability
- Screenshots at each step for debugging
- Comprehensive error handling

---

## Screenshots

The test captures screenshots at each step:
- `01-role-after-logout`
- `02-role-after-login`
- `03-role-pages-loaded`
- `04-role-rbac-tab`
- `05-role-create-section-visible`
- `06-role-created`
- `07-role-in-table`
- `08-role-privileges-table-visible`
- `09-role-column-visible`
- `10-role-all-privileges-assigned`

All screenshots are saved to `reports/screenshots/`.

---

## Troubleshooting

### **Role not appearing in table:**
- Check if role creation was successful
- Verify network requests completed
- Increase timeout in `verify_role_in_privileges_table()`

### **Cannot find role column:**
- The table may need more horizontal scrolling
- Check if the role name matches exactly
- Try increasing `max_scroll_attempts` in `scroll_horizontally_to_role_column()`

### **Checkbox not found:**
- Verify privilege name matches exactly (case-sensitive)
- Check if the role column index is correct
- Ensure the table has loaded completely

---

## Future Enhancements

Potential improvements:
- [ ] Test role deletion
- [ ] Test role editing
- [ ] Test assigning roles to users
- [ ] Test privilege removal
- [ ] Test with multiple roles
- [ ] Test with all privilege types

---

## Summary

This test provides comprehensive coverage of the RBAC role creation and privilege assignment workflow, ensuring that:
- ✅ Roles can be created successfully
- ✅ Roles appear in the privileges table
- ✅ Privileges can be assigned to roles
- ✅ The UI handles horizontal scrolling correctly
- ✅ All assignments are verified

**The test is ready to use!** 🎉

