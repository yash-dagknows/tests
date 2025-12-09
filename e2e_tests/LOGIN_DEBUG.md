# 🔍 Login Debugging - Enhanced

## 🎯 **What Was Added**

I've added extensive debugging to the login flow to understand why it's timing out:

### **Screenshots at Every Step**
1. `login-page-loaded.png` - After navigating to login page
2. `before-signin-click.png` - After filling credentials, before clicking
3. `after-signin-click.png` - Immediately after clicking sign-in button
4. `login-error.png` - If an error message appears
5. `login-timeout.png` - If login times out
6. `after-login.png` - If login succeeds

### **Enhanced Logging**
- Current URL after sign-in click
- Error messages (if any)
- Org field status (visible/hidden/exists)
- Multiple login success indicators checked

### **Multiple Success Indicators**
The test now checks for:
1. `#signed_in_user_icon`
2. `[data-testid="user-menu"]`
3. Text "Logout"
4. Text "Sign out"
5. URL change from `/vlogin`

---

## 🚀 **Run Tests Again**

```bash
cd /home/ubuntu/tests/e2e_tests
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 📸 **Check Screenshots**

After the test runs, check the screenshots:

```bash
ls -lah reports/screenshots/
```

Look at these key screenshots:
```bash
# View or download these:
reports/screenshots/before-signin-click.png
reports/screenshots/after-signin-click.png
```

You can download them from the server:
```bash
# From your local machine
scp -r ubuntu@your-server:/home/ubuntu/tests/e2e_tests/reports/screenshots/ ./
```

---

## 📋 **Look for These in Logs**

After running, check the logs for:

1. **"Org field" messages** - Is the org field being filled?
   ```
   [INFO] Checking if org field is visible...
   [INFO] Filling org field: dagknows
   ```

2. **"Current URL after sign-in"** - Where did it navigate?
   ```
   [INFO] Current URL after sign-in: https://dev.dagknows.com/...
   ```

3. **"Login error message"** - Any error?
   ```
   [ERROR] Login error message: Invalid credentials
   ```

4. **Success indicators** - Which ones were found?
   ```
   [INFO] ✓ Login successful - found indicator: ...
   ```

---

## 🤔 **What to Look For**

### If credentials are wrong:
- Screenshot will show error message
- URL will stay at `/vlogin`

### If form submission didn't work:
- Screenshot will still show login form
- URL will stay at `/vlogin`

### If login succeeded but indicator is wrong:
- Screenshot will show logged-in page
- URL will have changed (e.g., `/n/landing`)
- But test timeout because indicator selector is wrong

---

## 📞 **Next Steps**

After running the test:

1. **Share the log output** - especially the lines with:
   - "Current URL after sign-in"
   - "Org field" status
   - Any error messages

2. **Share screenshot names** - What files were created in `reports/screenshots/`?

3. **If possible, download and share**:
   - `before-signin-click.png`
   - `after-signin-click.png`

This will help us understand exactly what's happening! 🕵️

