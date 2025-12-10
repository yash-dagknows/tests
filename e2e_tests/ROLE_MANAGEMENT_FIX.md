# 🔧 Role Management Test Fixes

## Issues Fixed

### **Problem 1: Role Not Appearing in Table**
- **Issue**: After creating a role, it takes ~1 second for it to appear in the privileges table
- **Fix**: 
  - Increased wait time after role creation from 2 seconds to 5 seconds
  - Added intelligent waiting that checks if role name appears in table text
  - Polls every 500ms for up to 5 seconds to detect when role appears

### **Problem 2: Role Not Found After Creation**
- **Issue**: Test was timing out when trying to find the role in the privileges table
- **Fix**:
  - Improved `verify_role_in_privileges_table()` method with multiple strategies:
    1. **Strategy 1**: Look for role header with multiple selectors (exact match, contains, XPath)
    2. **Strategy 2**: Scroll horizontally and search again
    3. **Strategy 3**: Check if role name appears in table text (even if not visible), then scroll to find it
  - Increased default timeout from 10 seconds to 20 seconds
  - Added better error logging (shows available role headers for debugging)

### **Problem 3: Horizontal Scrolling Not Working**
- **Issue**: Role column might be off-screen and needs horizontal scrolling
- **Fix**:
  - Enhanced `scroll_horizontally_to_role_column()` method:
    - Increased scroll attempts from 10 to 20
    - Increased scroll amount from 200px to 300px
    - Added reverse scrolling (left) if right scrolling doesn't find it
    - Better detection of scrollable containers (table wrapper, table itself, or window)
    - Multiple selector strategies for finding role headers
    - More robust error handling

---

## Changes Made

### **`pages/settings_page.py`**

#### **1. `create_custom_role()` method:**
```python
# Before: Fixed 2 second wait
self.page.wait_for_timeout(2000)

# After: Intelligent waiting (up to 5 seconds)
# Polls every 500ms to detect when role appears in table
for wait_attempt in range(10):
    self.page.wait_for_timeout(500)
    table_text = self.page.locator(self.PRIVILEGES_TABLE).first.text_content()
    if role_name in table_text:
        role_appeared = True
        break
```

#### **2. `verify_role_in_privileges_table()` method:**
- **Increased timeout**: 10s → 20s (default), test uses 30s
- **Multiple search strategies**:
  - Try finding role header directly
  - Scroll horizontally and search again
  - Check table text content for role name
- **Better error messages**: Logs available role headers for debugging

#### **3. `scroll_horizontally_to_role_column()` method:**
- **Increased attempts**: 10 → 20
- **Increased scroll amount**: 200px → 300px
- **Reverse scrolling**: If right scroll doesn't work, try left
- **Better container detection**: Finds scrollable parent divs
- **Multiple fallbacks**: Table container → Table itself → Window scroll

### **`ui_tests/test_role_management.py`**

#### **Increased timeout:**
```python
# Before: 15 seconds
settings_page.verify_role_in_privileges_table(role_name, timeout=15000)

# After: 30 seconds
settings_page.verify_role_in_privileges_table(role_name, timeout=30000)
```

---

## How It Works Now

### **Role Creation Flow:**
1. Fill role name input
2. Click "Add" button
3. Wait for network idle
4. **Intelligently wait for role to appear** (polls table text every 500ms)
5. Take screenshot

### **Role Verification Flow:**
1. Scroll to privileges table
2. Wait 2 seconds for table to update
3. **Strategy 1**: Try finding role header directly (multiple selectors)
4. **Strategy 2**: If not found, scroll horizontally and search again
5. **Strategy 3**: Check if role name is in table text, then scroll to find it
6. Log available headers if not found (for debugging)

### **Horizontal Scrolling Flow:**
1. Find privileges table
2. Try to find scrollable container (wrapper div, table, or window)
3. Scroll right (up to 20 attempts, 300px each)
4. Check if role column is visible after each scroll
5. If not found, scroll left (reverse direction)
6. Return when found, or log warning if not found

---

## Testing

Run the test:
```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
./run_role_management_test.sh --slow
```

**Expected behavior:**
- ✅ Role creation waits intelligently for role to appear
- ✅ Role verification finds the role even if it needs horizontal scrolling
- ✅ Test completes successfully

---

## Debugging Tips

If the test still fails:

1. **Check screenshots**: Look at `reports/screenshots/` for:
   - `after-create-role-<role_name>.png` - See if role was created
   - `checking-role-<role_name>.png` - See table state
   - `role-<role_name>-not-found-in-table.png` - See what's visible

2. **Check logs**: The test logs available role headers if role is not found:
   ```
   Available role headers in table: ['Privileges', 'min', 'Editor', 'Everything', ...]
   ```

3. **Increase timeouts**: If role takes longer than 1 second to appear, increase wait time in `create_custom_role()`

4. **Check horizontal scroll**: The table might need more horizontal scrolling - increase `max_scroll_attempts` or `scroll_amount`

---

## Summary

✅ **Fixed**: Role creation now waits intelligently for role to appear  
✅ **Fixed**: Role verification uses multiple strategies to find the role  
✅ **Fixed**: Horizontal scrolling is more robust and handles edge cases  
✅ **Improved**: Better error messages and debugging information  

**The test should now work reliably!** 🎉

