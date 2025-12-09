# ✅ Configuration Updated for Local Testing

## 🎯 **What Changed**

Updated all configuration to properly handle **local testing with `?proxy=yashlocal`**

---

## 📝 **Key Updates**

### **1. Proxy Configuration**

| Environment | Old Value | New Value |
|-------------|-----------|-----------|
| **dev.dagknows.com** | `?proxy=dev1` | `?proxy=dev1` ✅ (no change) |
| **localhost** | ~~Empty string~~ ❌ | `?proxy=yashlocal` ✅ |

---

### **2. JWT Token Handling**

**Important clarification added:**
- ⚠️ JWT tokens are **DIFFERENT** for each environment
- Dev token from `https://dev.dagknows.com`
- Local token from `http://localhost`
- **DO NOT mix them!**

---

## 📦 **Files Updated**

### **1. `env.template`**
- Updated proxy documentation
- Added notes about different JWT tokens
- Clarified local proxy: `?proxy=yashlocal`

### **2. `config/env.py`**
- Updated `get_proxy_param_for_url()` method
- Returns `?proxy=yashlocal` for localhost
- Auto-detects environment

### **3. `run_ai_agent_test.sh`**
- `--local` flag now sets `DAGKNOWS_PROXY=?proxy=yashlocal`
- Script output shows proxy being used

### **4. `AI_AGENT_WORKFLOW_TEST.md`**
- Updated local testing instructions
- Added JWT token differences
- Clarified proxy requirements

### **5. `AI_AGENT_TEST_SUMMARY.md`**
- Updated quick start for local
- Added step to get local JWT token
- Configuration table updated

### **6. `LOCAL_VS_DEV_CONFIG.md`** (NEW)
- Complete guide comparing dev vs local
- How to get JWT tokens for each
- Common mistakes and fixes
- Verification checklist

---

## 🚀 **New Configuration**

### **For dev.dagknows.com:**

```bash
# .env
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_PROXY=?proxy=dev1
DAGKNOWS_TOKEN=your-dev-jwt-token  # Get from dev browser
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-dev-password
```

### **For localhost:**

```bash
# .env
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=yashlocal  # REQUIRED!
DAGKNOWS_TOKEN=your-local-jwt-token  # Get from localhost browser
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-local-password
```

---

## ✅ **How to Use**

### **1. For Local Testing:**

```bash
# Start your local app
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d

# Get JWT token from localhost
# 1. Login to http://localhost in browser
# 2. Dev Tools (F12) → Application → Local Storage
# 3. Copy 'authToken' value

# Configure
cd ../tests/e2e_tests
cp env.template .env
# Edit .env with:
#   DAGKNOWS_URL=http://localhost
#   DAGKNOWS_PROXY=?proxy=yashlocal
#   DAGKNOWS_TOKEN=<token from step above>

# Run test
./run_ai_agent_test.sh --local --headed
```

### **2. For Dev Testing:**

```bash
# Get JWT token from dev.dagknows.com
# 1. Login to https://dev.dagknows.com
# 2. Dev Tools (F12) → Application → Local Storage
# 3. Copy 'authToken' value

# Configure
cd tests/e2e_tests
cp env.template .env
# Edit .env with:
#   DAGKNOWS_URL=https://dev.dagknows.com
#   DAGKNOWS_PROXY=?proxy=dev1
#   DAGKNOWS_TOKEN=<token from step above>

# Run test
./run_ai_agent_test.sh --headed
```

---

## 🎯 **Automatic Detection**

The framework **automatically** detects environment:

```python
# config/env.py
if "localhost" in BASE_URL:
    proxy = "?proxy=yashlocal"  # ✅ Auto for local
elif "dev.dagknows.com" in BASE_URL:
    proxy = "?proxy=dev1"       # ✅ Auto for dev
```

You just need correct URL and token in `.env`!

---

## 📚 **Documentation**

| File | What It Covers |
|------|----------------|
| `env.template` | Configuration template |
| `LOCAL_VS_DEV_CONFIG.md` | Complete comparison guide |
| `AI_AGENT_WORKFLOW_TEST.md` | Full test documentation |
| `AI_AGENT_TEST_SUMMARY.md` | Quick reference |

---

## ⚠️ **Important Reminders**

1. **JWT tokens are different** for dev vs local
2. **Both environments need proxy** parameter
3. **Get fresh tokens** from correct environment
4. **Local app must be running** for local tests
5. **Proxy parameter is critical** - tests will fail without it

---

## ✅ **Verification**

Test your configuration:

```bash
# Check .env
cat tests/e2e_tests/.env | grep -E "URL|PROXY|TOKEN"

# Should show:
# DAGKNOWS_URL=http://localhost (or dev)
# DAGKNOWS_PROXY=?proxy=yashlocal (or dev1)
# DAGKNOWS_TOKEN=eyJhbGci... (valid token)
```

---

## 🎉 **Ready to Test!**

Both environments now properly configured:

```bash
# Local
./run_ai_agent_test.sh --local --headed

# Dev
./run_ai_agent_test.sh --headed
```

**Everything is updated and ready!** 🚀

---

**Questions? Check `LOCAL_VS_DEV_CONFIG.md` for detailed comparison!**

