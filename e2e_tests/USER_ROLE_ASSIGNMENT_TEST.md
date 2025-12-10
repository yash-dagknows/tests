# 👤 User Role Assignment E2E Test

## Overview

This test suite covers the **User Role Assignment** workflow for assigning a role to a user for a specific workspace.

## Test Flow

### `test_assign_role_to_user_for_workspace`

**Complete workflow:**
1. **Logout** - Clean state
2. **Login** - Authenticate as admin user
3. **Wait for pages to load** - Ensure UI is ready
4. **Navigate to Settings -> Users tab** - Go to `https://dev.dagknows.com/vsettings?tab=users`
5. **Wait for page to load** - Ensure Users page is fully loaded
6. **Find user in table** - Locate `sarang+user@dagknows.com` in the users table
7. **Expand user row** - Click dropdown arrow next to user to expand row
8. **Click "Modify Settings"** - Click the "Modify Settings" button that appears
9. **Assign role to workspace** - In the Modify User Settings form:
   - Find workspace "DEV" in Workspace Roles table
   - Click dropdown next to "DEV" workspace
   - Select role "read1" from dropdown
10. **Save user settings** - Click Save button
11. **Verify navigation** - Verify we're back on Users page

---

## Files Created/Updated

### **New Files:**
- ✅ `ui_tests/test_user_role_assignment.py` - Main test file
- ✅ `run_user_role_assignment_test.sh` - Run script
- ✅ `USER_ROLE_ASSIGNMENT_TEST.md` - This documentation

### **Updated Files:**
- ✅ `pages/settings_page.py` - Added user management methods:
  - `navigate_to_users_tab()` - Navigate to Users tab
  - `click_users_tab()` - Click Users tab
  - `find_user_in_table(user_email)` - Find user in table
  - `expand_user_row(user_email)` - Click dropdown to expand user row
  - `click_modify_settings_for_user(user_email)` - Click Modify Settings button
  - `assign_role_to_user_for_workspace(workspace_name, role_name, user_email)` - Assign role
  - `save_user_settings()` - Save user settings
- ✅ `pytest.ini` - Added `user_management` marker

---

## Running the Test

### **Quick Start:**
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
./run_user_role_assignment_test.sh
```

### **With Options:**
```bash
# Run with visible browser
./run_user_role_assignment_test.sh --headed

# Run in slow motion (for debugging)
./run_user_role_assignment_test.sh --slow

# Run against local Docker
./run_user_role_assignment_test.sh --local

# Combine options
./run_user_role_assignment_test.sh --headed --slow
```

### **Direct pytest:**
```bash
source venv/bin/activate
source setup_env.sh
pytest ui_tests/test_user_role_assignment.py -v
```

---

## Test Details

### **Test Class:**
- `TestUserRoleAssignmentE2E`

### **Test Method:**
- `test_assign_role_to_user_for_workspace`

### **Markers:**
- `@pytest.mark.ui`
- `@pytest.mark.e2e`
- `@pytest.mark.user_management`

### **Test Data:**
- **User:** `sarang+user@dagknows.com`
- **Workspace:** `DEV`
- **Role:** `read1`

**Note:** The role `read1` must exist before running this test. If it doesn't exist, create it first using the role management test.

---

## Key Features

### **1. User Table Navigation**
- Finds user by email in the users table
- Scrolls to user row
- Handles table pagination if needed

### **2. User Row Expansion**
- Clicks dropdown arrow next to user
- Waits for row to expand
- Verifies "Modify Settings" button appears

### **3. Modify User Settings Form**
- Navigates to Modify User Settings form
- Finds workspace in Workspace Roles table
- Handles dropdown selection for role assignment

### **4. Role Assignment**
- Opens role dropdown for workspace
- Selects role from dropdown menu
- Handles both `<select>` and custom dropdown components

### **5. Save and Verify**
- Clicks Save button
- Waits for form submission
- Verifies navigation back to Users page

---

## Screenshots

The test captures screenshots at each step:
- `01-user-role-after-logout`
- `02-user-role-after-login`
- `03-user-role-pages-loaded`
- `04-user-role-users-tab`
- `05-user-role-users-page-loaded`
- `06-user-role-user-found`
- `07-user-role-row-expanded`
- `08-user-role-modify-settings-opened`
- `09-user-role-assigned`
- `10-user-role-settings-saved`
- `11-user-role-after-save`

All screenshots are saved to `reports/screenshots/`.

---

## Prerequisites

1. **Role must exist:** The role `read1` must be created before running this test
2. **User must exist:** The user `sarang+user@dagknows.com` must exist
3. **Workspace must exist:** The workspace `DEV` must exist
4. **Admin access:** Test user must have admin permissions

---

## Troubleshooting

### **User not found in table:**
- Verify user email is correct
- Check if user exists in the system
- Ensure Users tab is loaded completely

### **Dropdown arrow not found:**
- Verify user row is visible
- Check if row is already expanded
- Try scrolling to user row again

### **Modify Settings button not found:**
- Ensure user row is expanded
- Wait longer for button to appear
- Check if user has permission to modify settings

### **Workspace not found in form:**
- Verify workspace name matches exactly (case-sensitive)
- Check if workspace exists
- Ensure Modify User Settings form is fully loaded

### **Role not found in dropdown:**
- Verify role name matches exactly (case-sensitive)
- Check if role exists in the system
- Ensure role is available for assignment

---

## Future Enhancements

Potential improvements:
- [ ] Test assigning multiple roles to same user
- [ ] Test assigning role to multiple workspaces
- [ ] Test removing role from user
- [ ] Test with different user types
- [ ] Test role assignment validation

---

## Summary

This test provides comprehensive coverage of the user role assignment workflow, ensuring that:
- ✅ Users can be found in the users table
- ✅ User rows can be expanded
- ✅ Modify Settings form can be opened
- ✅ Roles can be assigned to users for workspaces
- ✅ Changes can be saved successfully

**The test is ready to use!** 🎉

