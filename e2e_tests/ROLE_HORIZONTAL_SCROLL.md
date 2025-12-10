# 🔄 Horizontal Scrolling for Role Columns

## Overview

After creating a custom role, the role appears as a **new column** in the Privileges table. This column is typically added to the **right side** of the table, which means it may be **off-screen** and requires **horizontal scrolling** to be visible.

---

## ✅ **Yes, Our Script Handles This!**

The test script **explicitly handles horizontal scrolling** to find the newly created role column. Here's how:

---

## Flow After Role Creation

### **1. Role Creation** (`create_custom_role()`)
- Creates the role
- Waits for role to appear in table text (polls every 500ms)
- Takes screenshot

### **2. Scroll to Privileges Table** (`scroll_to_privileges_table()`)
- Scrolls vertically to the privileges table section
- Ensures table is visible

### **3. Verify Role & Scroll Horizontally** (`verify_role_in_privileges_table()`)
- **Immediately attempts horizontal scroll** to find the role column
- Uses multiple strategies:
  1. **Direct search** - Try to find role header (may not be visible)
  2. **Horizontal scroll then search** - Scroll right/left, then search again
  3. **Text content check** - Check if role name is in table text, then scroll to find it

### **4. Ensure Role Column is Visible** (`scroll_horizontally_to_role_column()`)
- **Explicitly scrolls horizontally** to make the role column visible
- Scrolls right (up to 20 attempts, 300px each)
- If not found, scrolls left (reverse direction)
- Returns when role column is visible

---

## Implementation Details

### **`verify_role_in_privileges_table()` Method:**

```python
# Step 1: Scroll to privileges table
self.scroll_to_privileges_table()

# Step 2: Wait for table to update
self.page.wait_for_timeout(2000)

# Step 3: IMMEDIATELY try horizontal scroll (role is likely off-screen)
logger.info("Scrolling horizontally to find newly created role column...")
self.scroll_horizontally_to_role_column(role_name)

# Step 4: Then try multiple strategies to verify it's there
# Strategy 1: Direct search
# Strategy 2: Scroll and search again
# Strategy 3: Check table text, then scroll
```

### **`scroll_horizontally_to_role_column()` Method:**

```python
# Finds scrollable container (table wrapper, table, or window)
# Scrolls right: up to 20 attempts × 300px = 6000px total
# If not found, scrolls left: up to 20 attempts × 300px
# Checks visibility after each scroll
# Returns when role column is visible
```

---

## Test Flow

```
Step 6: Create custom role
  ↓
Step 7: Scroll to privileges table (vertical scroll)
  ↓
Step 8: Verify role (includes horizontal scroll)
  ├─ Scroll horizontally to find role column
  ├─ Try multiple search strategies
  └─ Verify role is visible
  ↓
Step 9: Ensure role column is visible (explicit horizontal scroll)
  ↓
Step 10: Assign privileges (now that column is visible)
```

---

## Why Horizontal Scrolling is Needed

1. **New columns are added to the right** - The role column appears at the end of the table
2. **Table has horizontal scroll** - The privileges table is wider than the viewport
3. **Role may not be immediately visible** - Even if it exists in the DOM, it's off-screen

---

## How It Works

### **Scroll Detection:**
- Finds the scrollable container (table wrapper div, table element, or window)
- Uses multiple strategies to detect scrollable elements

### **Scroll Strategy:**
1. **Scroll Right** (primary):
   - Scrolls 300px to the right, up to 20 times
   - Checks if role column is visible after each scroll
   - Stops when found

2. **Scroll Left** (fallback):
   - If right scroll doesn't work, scrolls left
   - Useful if we've scrolled past the role column

### **Visibility Check:**
- After each scroll, checks if role header is visible
- Uses multiple selectors:
  - `th:has-text("{role_name}")`
  - XPath: `//th[contains(text(), "{role_name}")]`

---

## Screenshots Captured

The test captures screenshots at key points:
- `06-role-created.png` - After role creation
- `07-role-privileges-table-visible.png` - After scrolling to table
- `08-role-in-table.png` - After finding role in table
- `09-role-column-visible.png` - After horizontal scroll to make column visible
- `after-horizontal-scroll-{role_name}.png` - After successful horizontal scroll

---

## Debugging

If horizontal scrolling fails:

1. **Check screenshots** - See if table is visible and scrollable
2. **Check logs** - Look for:
   - "Scrolling horizontally to find newly created role column..."
   - "Role column '{role_name}' is now visible"
   - "Could not find role column after extensive horizontal scrolling"
3. **Increase scroll attempts** - Modify `max_scroll_attempts` in `scroll_horizontally_to_role_column()`
4. **Increase scroll amount** - Modify `scroll_amount` (currently 300px)

---

## Summary

✅ **Yes, the script handles horizontal scrolling!**

- ✅ Scrolls to privileges table (vertical)
- ✅ Immediately attempts horizontal scroll after role creation
- ✅ Uses multiple strategies to find the role column
- ✅ Explicitly ensures role column is visible before assigning privileges
- ✅ Handles edge cases (reverse scrolling, multiple containers)

**The test is designed to handle the horizontal scrolling requirement!** 🎉

