# Local vs Dev Configuration Guide

Quick reference for configuring tests for local vs dev environments.

---

## ⚠️ **Key Differences**

| Setting | dev.dagknows.com | localhost |
|---------|------------------|-----------|
| **URL** | `https://dev.dagknows.com` | `http://localhost` |
| **Proxy** | `?proxy=dev1` | `?proxy=yashlocal` |
| **JWT Token** | Get from dev.dagknows.com | Get from localhost |
| **Token Source** | Dev browser session | Local browser session |

**CRITICAL:** JWT tokens are DIFFERENT! Don't mix them!

---

## 🌐 **For dev.dagknows.com**

### **.env Configuration**

```bash
# Dev Environment
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_PROXY=?proxy=dev1
DAGKNOWS_TOKEN=eyJhbGci...  # Get from dev.dagknows.com
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-dev-password
TEST_ORG=dagknows
```

### **Get JWT Token from Dev:**

1. Login to https://dev.dagknows.com
2. Open browser Dev Tools (F12)
3. Go to **Application** → **Local Storage** → `https://dev.dagknows.com`
4. Find `authToken` key
5. Copy the value
6. Paste into `.env` as `DAGKNOWS_TOKEN`

### **Run Test:**

```bash
cd tests/e2e_tests
./run_ai_agent_test.sh --headed
```

---

## 🏠 **For localhost (Your Docker Setup)**

### **Step 1: Start Local App**

```bash
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d
```

### **Step 2: Get JWT Token from Local**

1. Login to http://localhost in browser
2. Open browser Dev Tools (F12)
3. Go to **Application** → **Local Storage** → `http://localhost`
4. Find `authToken` key
5. Copy the value (will be DIFFERENT from dev!)
6. Paste into `.env` as `DAGKNOWS_TOKEN`

### **Step 3: .env Configuration**

```bash
# Local Environment
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=yashlocal  # REQUIRED! Different from dev!
DAGKNOWS_TOKEN=eyJhbGci...  # Get from localhost (DIFFERENT from dev!)
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-local-password
TEST_ORG=dagknows
```

### **Step 4: Run Test:**

```bash
cd tests/e2e_tests
./run_ai_agent_test.sh --local --headed
```

---

## 🔍 **How to Verify Your Configuration**

### **Check Your .env File:**

```bash
cd tests/e2e_tests
cat .env | grep -E "DAGKNOWS_URL|DAGKNOWS_PROXY"
```

### **Expected Output:**

For **dev**:
```
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_PROXY=?proxy=dev1
```

For **local**:
```
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=yashlocal
```

---

## ⚠️ **Common Mistakes**

### **❌ Mistake 1: Using dev token for localhost**
```bash
# WRONG!
DAGKNOWS_URL=http://localhost
DAGKNOWS_TOKEN=dev-token-here  # This won't work!
```

**✅ Fix:** Get token from localhost browser

---

### **❌ Mistake 2: Wrong proxy for localhost**
```bash
# WRONG!
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=dev1  # Wrong proxy!
```

**✅ Fix:** Use `?proxy=yashlocal` for localhost

---

### **❌ Mistake 3: No proxy for localhost**
```bash
# WRONG!
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=  # Missing proxy!
```

**✅ Fix:** Must set `?proxy=yashlocal`

---

## 🚀 **Quick Setup Commands**

### **For Dev Testing:**

```bash
# Create .env
cat > tests/e2e_tests/.env << 'EOF'
DAGKNOWS_URL=https://dev.dagknows.com
DAGKNOWS_PROXY=?proxy=dev1
DAGKNOWS_TOKEN=your-dev-token-here
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-dev-password
EOF

# Run test
cd tests/e2e_tests
./run_ai_agent_test.sh --headed
```

### **For Local Testing:**

```bash
# Start app
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d

# Create .env
cat > ../tests/e2e_tests/.env << 'EOF'
DAGKNOWS_URL=http://localhost
DAGKNOWS_PROXY=?proxy=yashlocal
DAGKNOWS_TOKEN=your-local-token-here
TEST_USER_EMAIL=yash+user@dagknows.com
TEST_USER_PASSWORD=your-local-password
EOF

# Run test
cd ../tests/e2e_tests
./run_ai_agent_test.sh --local --headed
```

---

## 🔧 **Automatic Configuration**

The test framework automatically detects environment:

```python
# In config/env.py
if "localhost" in BASE_URL:
    proxy = "?proxy=yashlocal"  # Auto-set for local
elif "dev.dagknows.com" in BASE_URL:
    proxy = "?proxy=dev1"  # Auto-set for dev
```

You just need to set:
- Correct `DAGKNOWS_URL`
- Correct `DAGKNOWS_TOKEN` (most important!)
- Correct `DAGKNOWS_PROXY`

---

## 📝 **Token Validity Check**

Test if your token is valid:

### **For Dev:**
```bash
curl -H "Authorization: Bearer YOUR_DEV_TOKEN" \
     "https://dev.dagknows.com/api/v1/tasks/?page_size=1&proxy=dev1"
```

### **For Local:**
```bash
curl -H "Authorization: Bearer YOUR_LOCAL_TOKEN" \
     "http://localhost/api/v1/tasks/?page_size=1&proxy=yashlocal"
```

If you get valid JSON response (not 401), token is good!

---

## 🎯 **Switching Between Environments**

### **Option 1: Multiple .env Files**

```bash
# Create separate configs
.env.dev      # Dev configuration
.env.local    # Local configuration

# Switch by copying
cp .env.dev .env    # Test against dev
cp .env.local .env  # Test against local
```

### **Option 2: Use Script Flag**

```bash
# Script automatically sets proxy for --local
./run_ai_agent_test.sh --local --headed
```

---

## ✅ **Verification Checklist**

Before running tests, verify:

### **For Dev:**
- [ ] `DAGKNOWS_URL=https://dev.dagknows.com`
- [ ] `DAGKNOWS_PROXY=?proxy=dev1`
- [ ] JWT token from dev.dagknows.com
- [ ] Token is not expired
- [ ] Can access dev.dagknows.com

### **For Local:**
- [ ] Local app is running
- [ ] `DAGKNOWS_URL=http://localhost`
- [ ] `DAGKNOWS_PROXY=?proxy=yashlocal`
- [ ] JWT token from localhost
- [ ] Token is not expired
- [ ] Can access http://localhost

---

## 🐛 **Troubleshooting**

### **Problem: 401 Unauthorized**

**Cause:** Wrong token or expired token

**Solution:**
1. Get fresh token from correct environment
2. Verify token in browser works
3. Copy exact token (no spaces/newlines)

---

### **Problem: 404 Not Found**

**Cause:** Wrong proxy parameter

**Solution:**
- For dev: Must be `?proxy=dev1`
- For local: Must be `?proxy=yashlocal`

---

### **Problem: Connection Refused**

**Cause:** Local app not running

**Solution:**
```bash
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d
```

---

## 💡 **Pro Tips**

1. **Keep tokens separate** - Never mix dev and local tokens
2. **Token expiry** - Tokens expire, get fresh ones regularly
3. **Local app state** - Restart local app if issues persist
4. **Browser session** - Stay logged in while getting token
5. **Test both** - Run tests against both environments regularly

---

**Remember:** The most critical difference is the JWT token - they are completely different for each environment!

