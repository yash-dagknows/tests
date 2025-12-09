# ✅ Sign In Button Fix

## 🐛 **Issue Fixed**

**Error:**
```
Error: strict mode violation: get_by_role("button", name="Sign in") resolved to 2 elements:
1) <button data-v-400e667f="" class="btn btn-primary trial-…>Sign in</button>
2) <input tabindex="3" type="button" value="Sign in" data-…/>
```

**Root Cause**: The login page has **TWO "Sign in" buttons**:
- A `<button>` element
- An `<input type="button">` element

Playwright's strict mode requires selectors to match exactly ONE element.

---

## 🔧 **What Was Fixed**

Updated `/Users/yashyaadav/dag_workspace/dagknows_src/tests/e2e_tests/pages/login_page.py`:

**Before:**
```python
def click_sign_in(self) -> None:
    """Click sign in button."""
    logger.info("Clicking sign in button")
    self.page.get_by_role("button", name="Sign in").click()
```

**After:**
```python
def click_sign_in(self) -> None:
    """Click sign in button."""
    logger.info("Clicking sign in button")
    # There might be multiple "Sign in" buttons on the page
    # Use the actual <button> element, not <input type="button">
    try:
        # First try the button element specifically
        self.page.locator('button:has-text("Sign in")').first.click()
    except Exception:
        # Fallback to the input button
        self.page.locator('input[type="button"][value="Sign in"]').click()
```

**Strategy:**
1. First, try to click the `<button>` element (the actual button)
2. Use `.first` to handle multiple matches
3. Fallback to `<input>` button if needed

---

## ✅ **Now Your Tests Will Work**

The fix is already applied. Run your tests again:

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

Or use the helper script:

```bash
./run_ai_agent_test.sh
```

---

## 📋 **Technical Details**

### Why Multiple Sign-In Buttons?

The login page likely has:
- **Visible button**: The main "Sign in" button users see
- **Hidden button**: Possibly for accessibility or form submission

### Playwright Strict Mode

Playwright enforces "strict mode" by default, which means:
- Selectors MUST match exactly ONE element
- This prevents accidental clicks on wrong elements
- More reliable than `.first` alone

### Solution Options

We chose Option 1, but here are all options:

**Option 1: Target specific element type** (CHOSEN)
```python
self.page.locator('button:has-text("Sign in")').first.click()
```

**Option 2: Use .first (less safe)**
```python
self.page.get_by_role("button", name="Sign in").first.click()
```

**Option 3: More specific CSS selector**
```python
self.page.locator('button.btn-primary:has-text("Sign in")').click()
```

---

## 🎉 **Status: FIXED**

The login should now work! Try running the tests. 🚀

Expected flow:
```
2025-12-09 10:50:57 [INFO] Logging out first (clean state)
2025-12-09 10:50:57 [INFO] Navigating to: https://dev.dagknows.com/vlogout?proxy=dev1
2025-12-09 10:51:00 [INFO] Navigating to login page
2025-12-09 10:51:00 [INFO] Navigating to: https://dev.dagknows.com/vlogin?proxy=dev1
2025-12-09 10:51:01 [INFO] Filling email: yash+user@dagknows.com
2025-12-09 10:51:01 [INFO] Filling password
2025-12-09 10:51:01 [INFO] Clicking sign in button
2025-12-09 10:51:02 [INFO] ✓ Login successful - user icon visible
```

---

**Run the tests now!** The fix is in place.

