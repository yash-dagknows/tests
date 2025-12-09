# ✅ Credentials & Configuration Update Complete

## 🎯 **What Was Updated**

All configuration files have been updated with actual credentials and simplified for testing.

---

## 📝 **Files Updated (6 files)**

### **1. `.gitignore` (NEW)**
- **Location:** `tests/.gitignore`
- **Added:** `__pycache__/` and all Python/test artifacts
- **Status:** ✅ Created

### **2. `config/env.py`**
- **Updated:** Default JWT token to dev token
- **Updated:** Default user email to `yash+user@dagknows.com`
- **Updated:** Default password to `1Hey2Yash*`
- **Status:** ✅ Updated

### **3. `config/test_users.py`**
- **Simplified:** Removed VIEWER_USER and CUSTOMER_USER
- **Kept:** Only ADMIN_USER with correct credentials
- **Updated:** First Name to "Yash", Last Name to "User"
- **Status:** ✅ Simplified

### **4. `env.template`**
- **Updated:** JWT token (valid until 2026-06-21)
- **Updated:** User credentials
- **Removed:** Viewer and Customer user sections
- **Status:** ✅ Updated

### **5. `QUICK_SETUP_GUIDE.md` (NEW)**
- **Created:** Complete setup guide for both dev and local
- **Includes:** Step-by-step instructions
- **Status:** ✅ Created

### **6. `SETUP_CHEATSHEET.md` (NEW)**
- **Created:** One-page quick reference
- **Includes:** All commands and credentials
- **Status:** ✅ Created

---

## 🔑 **Updated Credentials**

### **Test User:**
```
Email:      yash+user@dagknows.com
Password:   1Hey2Yash*
First Name: Yash
Last Name:  User
Org:        dagknows
Role:       Admin
```

### **Dev JWT Token (expires 2026-06-21):**
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJ5YXNoQGRhZ2tub3dzLmNvbSIsIm5iZiI6MTc2MTE0NjUxMSwiZXhwIjoxNzkyNjgyNjkxLCJqdGkiOiJZMENWR055N01CQzlKYjNQIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoiYWRtaW4iLCJ1c2VyX2NsYWltcyI6eyJ1aWQiOiIzOSIsInVuYW1lIjoieWFzaEBkYWdrbm93cy5jb20iLCJvcmciOiJkYWdrbm93cyIsImZpcnN0X25hbWUiOiJZYXNoIiwibGFzdF9uYW1lIjoiWWFkYXYiLCJyb2xlIjoiQWRtaW4iLCJhZXNfa2V5IjoiY1Q0RTU2aWxDOTlVXG4tcTZ1dlRBcU15VTBwMEFcbnFJWSIsIm9mc3QiOlszNzIsMTUwLDM0Miw0MzEsMTg3LDM5MSwzOTAsMTc0LDIzMywyNzksMjQ2LDQzNiw5MSw0MjYsMjU3LDIxNiwxNzEsMzMzLDExOCwzNjMsMjc0LDE1MiwzNzEsNDM2LDEzNiwyMjAsMTI3LDY3LDQyNSwzNzMsNDM5LDMyMF19fQ.IvHXxMMm4th-jm7IyektCTW3SXxlq4olv6gByzAliuFk1y2zbr91QBY_zdifz5_KnYNk4ruVr9xLrlahC3h7rGJaFU98OiiiLAQ49CFxgUO2iqyr6XcT3GgO5ptobTtOZNV4rmrPE_6hnjPRImernp5M6FhHhCZWktL9xQqZs9N9m2az1Jk-mi0yZLaNIA25pHWcqgdiF1xCbt5STWqFG2nmt1eq7x-FXnoryEqo1HvfOg74crBcubFORpTZ5AhNRpSdqemcpDd_6t0UliPuAg3VlwIedew9RBRvytr2j9GbBC_jgCh7YJ5oQqFjVItolhSMzuKHLRRHZib8Ikz6fA
```

---

## 🚀 **Quick Start (Dev)**

**It's now SUPER easy to test against dev.dagknows.com:**

```bash
cd tests/e2e_tests
cp env.template .env
pip install -r requirements.txt
playwright install chromium
./run_ai_agent_test.sh --headed
```

**✅ All credentials are pre-configured in the template!**

---

## 🏠 **Quick Start (Local)**

```bash
# 1. Start local app
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d

# 2. Get JWT token from localhost browser
# Login to http://localhost
# F12 → Application → Local Storage → Copy 'authToken'

# 3. Setup tests
cd ../tests/e2e_tests
cp env.template .env

# 4. Edit .env and update:
# DAGKNOWS_URL=http://localhost
# DAGKNOWS_PROXY=?proxy=yashlocal
# DAGKNOWS_TOKEN=<paste-token-here>

# 5. Run
./run_ai_agent_test.sh --local --headed
```

---

## 📊 **Configuration Summary**

| Environment | URL | Proxy | Token Source |
|-------------|-----|-------|--------------|
| **Dev** | `https://dev.dagknows.com` | `?proxy=dev1` | Pre-configured ✅ |
| **Local** | `http://localhost` | `?proxy=yashlocal` | Get from browser |

---

## ✅ **What's Pre-Configured**

For **dev.dagknows.com**, the template now includes:

1. ✅ Complete JWT token (valid until 2026)
2. ✅ Test user email: `yash+user@dagknows.com`
3. ✅ Test user password: `1Hey2Yash*`
4. ✅ Correct proxy: `?proxy=dev1`
5. ✅ Correct URL: `https://dev.dagknows.com`

**Just `cp env.template .env` and run!**

---

## 📚 **Documentation Files**

| File | Purpose |
|------|---------|
| `QUICK_SETUP_GUIDE.md` | Detailed setup for both environments |
| `SETUP_CHEATSHEET.md` | One-page quick reference |
| `LOCAL_VS_DEV_CONFIG.md` | Comparison guide |
| `AI_AGENT_WORKFLOW_TEST.md` | Test documentation |

---

## 🎯 **Key Changes**

### **Simplified:**
- ❌ Removed VIEWER_USER
- ❌ Removed CUSTOMER_USER
- ✅ Only ADMIN_USER needed

### **Updated:**
- ✅ Real JWT token (valid until 2026)
- ✅ Real user credentials
- ✅ Correct first/last names

### **Added:**
- ✅ `.gitignore` for `__pycache__`
- ✅ Quick setup guides
- ✅ Cheatsheet

---

## 🎉 **Ready to Use!**

Everything is now configured and ready:

```bash
cd tests/e2e_tests

# For dev (easiest!)
cp env.template .env
./run_ai_agent_test.sh --headed

# For local
# (Get token first, then update .env, then run)
./run_ai_agent_test.sh --local --headed
```

---

## 📝 **Next Steps**

1. ✅ **Test against dev** - Run `./run_ai_agent_test.sh --headed`
2. ✅ **Test against local** - Follow local setup guide
3. ✅ **Add more tests** - Use existing as template
4. ✅ **Review screenshots** - Check `reports/screenshots/`

---

## 🎓 **Documentation to Read**

**Start here:**
1. `SETUP_CHEATSHEET.md` - 1 minute read
2. `QUICK_SETUP_GUIDE.md` - 5 minute read
3. `AI_AGENT_WORKFLOW_TEST.md` - Full documentation

---

**Everything is ready!** Just run:

```bash
cd tests/e2e_tests
cp env.template .env
./run_ai_agent_test.sh --headed
```

🚀 **Watch your first E2E test run!** 🎬

