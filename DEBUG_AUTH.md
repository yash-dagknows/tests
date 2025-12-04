# Authentication Debugging Guide

## The Problem

All tests are getting **401 UNAUTHORIZED** errors. This means:
- Tests can reach the services ✓
- But authentication is not working ✗

## Root Cause

TaskService requires authentication, but test mode auth is not enabled in your running dkapp services.

## Quick Fix: Enable Test Mode in dkapp

### Step 1: Check Current Settings

```bash
# Check if ALLOW_DK_USER_INFO_HEADER is enabled in your running taskservice
docker exec dkapp-taskservice-1 printenv ALLOW_DK_USER_INFO_HEADER
docker exec dkapp-taskservice-1 printenv ENFORCE_LOGIN
```

**Expected:**
```
ALLOW_DK_USER_INFO_HEADER=true
ENFORCE_LOGIN=false
```

### Step 2: Update dkapp Environment

```bash
cd ~/dkapp

# Edit your .env file (or .env.gpg and re-encrypt)
nano .env

# Add or update these lines:
ALLOW_DK_USER_INFO_HEADER=true
ENFORCE_LOGIN=false
```

### Step 3: Restart Services

```bash
cd ~/dkapp

# Restart taskservice and req-router with new settings
docker-compose restart taskservice req-router

# Wait for services to restart
sleep 30

# Verify settings are applied
docker exec dkapp-taskservice-1 printenv ALLOW_DK_USER_INFO_HEADER
# Should show: true
```

### Step 4: Run Tests Again

```bash
cd ~/tests

# Rebuild test container with fixes
docker-compose -f docker-compose-local.yml build test-runner

# Run smoke tests
make -f Makefile.local quick

# Run single test
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_smoke.py::test_services_are_reachable -v
```

## Alternative: Create Test-Specific docker-compose Override

Instead of modifying your production dkapp setup, create an override for testing:

```bash
cd ~/dkapp

# Create override file
cat > docker-compose.test-override.yml << 'EOF'
version: '3.8'

services:
  taskservice:
    environment:
      - ALLOW_DK_USER_INFO_HEADER=true
      - ENFORCE_LOGIN=false
      
  req-router:
    environment:
      - ALLOW_DK_USER_INFO_HEADER=true
      - ENFORCE_LOGIN=false
EOF

# Restart with override
docker-compose -f docker-compose.yml -f docker-compose.test-override.yml up -d taskservice req-router

# Wait for restart
sleep 30
```

## Commands to Run Individual Tests

### 1. Smoke Tests (No Auth Needed)

```bash
cd ~/tests

# All smoke tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/ -v

# Single smoke test
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_smoke.py::test_services_are_reachable -v
```

### 2. Single Unit Test

```bash
cd ~/tests

# Specific test file
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -v

# Specific test class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD -v

# First test only (stop on first error)
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py -v -x
```

### 3. Debug Single Test

```bash
cd ~/tests

# Run with verbose output and print statements
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -vv -s

# Run with PDB debugger
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -v --pdb
```

## Verify Authentication is Working

```bash
cd ~/tests

# Test authentication manually
docker-compose -f docker-compose-local.yml run --rm test-runner bash -c '
python3 << EOF
import requests
import json
import urllib.parse

# Create user_info
user_info = {
    "uid": 1,
    "uname": "test@dagknows.com",
    "first_name": "Test",
    "last_name": "User",
    "org": "dagknows",
    "role": "Admin"
}

# Test with dk-user-info header
headers = {
    "dk-user-info": urllib.parse.quote(json.dumps(user_info)),
    "Content-Type": "application/json"
}

# Try to list tasks
response = requests.get("http://taskservice:2235/api/v1/tasks/", headers=headers)
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")

if response.status_code == 200:
    print("\n✓ Authentication working!")
else:
    print("\n✗ Authentication failed!")
    print("Check ALLOW_DK_USER_INFO_HEADER in taskservice")
EOF
'
```

## Quick Diagnostic

```bash
cd ~/dkapp

# Check current environment variables
docker exec dkapp-taskservice-1 env | grep -E "(ALLOW_DK_USER_INFO_HEADER|ENFORCE_LOGIN)"

# If not set or wrong:
# 1. Edit .env file
# 2. Add: ALLOW_DK_USER_INFO_HEADER=true
# 3. Add: ENFORCE_LOGIN=false
# 4. Restart: docker-compose restart taskservice req-router
```

## Summary

**Before running more tests:**

1. ✅ Enable test mode auth in dkapp
2. ✅ Restart services
3. ✅ Rebuild test container
4. ✅ Then run tests

**Commands:**
```bash
# 1. Check settings
docker exec dkapp-taskservice-1 printenv ALLOW_DK_USER_INFO_HEADER

# 2. If not "true", update dkapp/.env and restart
cd ~/dkapp
# Edit .env, add: ALLOW_DK_USER_INFO_HEADER=true
docker-compose restart taskservice req-router
sleep 30

# 3. Rebuild test container
cd ~/tests
docker-compose -f docker-compose-local.yml build test-runner

# 4. Test auth manually (see above)

# 5. Run smoke tests
make -f Makefile.local quick
```

Let me know what `docker exec dkapp-taskservice-1 printenv ALLOW_DK_USER_INFO_HEADER` shows!
