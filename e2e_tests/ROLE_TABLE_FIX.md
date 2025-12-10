# 🔧 Role Management Test - Table and Button Fixes

## Issues Fixed

### **Problem 1: Wrong Table Selected**
- **Issue**: `PRIVILEGES_TABLE = 'table'` was too generic and matched the first table on the page
- **Error**: Getting headers from wrong sections like "Admin settings", "Access tokens", etc.
- **Fix**: Created `_find_privileges_table()` method that specifically finds the correct table by:
  1. Looking for tables containing privilege names (`task.view_code`, `task.list`, etc.)
  2. Finding table after "Create new custom role" section
  3. Finding table near "Privileges" heading
  4. Verifying it has role columns (Admin, Editor, etc.)

### **Problem 2: Add Button Not Clicked Properly**
- **Issue**: Add button selector was not specific enough to the "Create new custom role" section
- **Fix**: Improved Add button detection:
  1. Find button within "Create new custom role" section
  2. Verify it's horizontally next to the role name input (same row)
  3. Check position relative to input field (50-300px to the right)
  4. Verify input value before clicking
  5. Wait for input field to clear after click (indicates success)

### **Problem 3: Privileges Table Not Found for Horizontal Scrolling**
- **Issue**: Horizontal scroll was trying to use wrong table
- **Fix**: All methods now use `_find_privileges_table()` to get the correct table

---

## Changes Made

### **1. New Method: `_find_privileges_table()`**
```python
def _find_privileges_table(self):
    """
    Find the correct privileges table by looking for specific indicators.
    Returns the table locator that contains privilege rows and role columns.
    """
    # Strategy 1: Find table with privilege names (task.view_code, task.list, etc.)
    # Strategy 2: Find table after "Create new custom role" section
    # Strategy 3: Find table near "Privileges" heading
    # Fallback: First table (with warning)
```

### **2. Updated `create_custom_role()` Method:**
- ✅ Better Add button detection (position-based)
- ✅ Verify input value before clicking
- ✅ Wait for input field to clear after click
- ✅ Use `_find_privileges_table()` to check for role

### **3. Updated `verify_role_in_privileges_table()` Method:**
- ✅ Uses `_find_privileges_table()` instead of generic `PRIVILEGES_TABLE`
- ✅ Better error messages with actual table headers

### **4. Updated `scroll_horizontally_to_role_column()` Method:**
- ✅ Uses `_find_privileges_table()` to get correct table
- ✅ Better scrollable container detection

### **5. Updated `assign_privilege_to_role()` Method:**
- ✅ Uses `_find_privileges_table()` to get correct table headers

### **6. Updated `scroll_to_privileges_table()` Method:**
- ✅ Uses `_find_privileges_table()` to scroll to correct table

---

## How It Works Now

### **Finding the Correct Privileges Table:**
1. **Look for specific privilege names**: Searches for tables containing `task.view_code`, `task.list`, `task.view_io`, etc.
2. **Verify it's the right table**: Checks for role columns (Admin, Editor, etc.)
3. **Fallback strategies**: If not found, tries other methods

### **Finding the Add Button:**
1. **Within section**: Looks for Add button within "Create new custom role" section
2. **Position check**: Verifies button is on same row as input (y-coordinate similar)
3. **Horizontal position**: Button should be 50-300px to the right of input
4. **Verification**: Checks input value before clicking

### **Role Creation Verification:**
1. **Input field clears**: After clicking Add, input should become empty
2. **Role in table**: Checks if role name appears in privileges table text
3. **Polls every 500ms**: Up to 5 seconds to detect role

---

## Testing

Run the test:
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
./run_role_management_test.sh --slow
```

**Expected behavior:**
- ✅ Add button is found and clicked correctly
- ✅ Role is created (input field clears)
- ✅ Correct privileges table is found
- ✅ Role appears in table
- ✅ Horizontal scrolling works on correct table
- ✅ Privileges can be assigned

---

## Debugging

If the test still fails:

1. **Check Add button**: Look at screenshot `after-filling-role-name-{role_name}.png`
   - Is the Add button visible?
   - Is it next to the input field?

2. **Check table selection**: Look at logs for:
   - "Found privileges table using indicator: ..."
   - "Available role headers in privileges table: ..."
   - Should show: `['Privileges', 'Admin', 'Editor', 'Everything', ...]`

3. **Check role creation**: Look at screenshot `after-create-role-{role_name}.png`
   - Is input field cleared?
   - Does role appear in table?

---

## Summary

✅ **Fixed**: Correct privileges table is now found  
✅ **Fixed**: Add button is clicked properly  
✅ **Fixed**: Role creation is verified  
✅ **Fixed**: All methods use correct table  

**The test should now work correctly!** 🎉

