# Testing Against Remote Deployment

## 📋 Overview

This guide explains how to run the test suite against a **remote DagKnows deployment** (e.g., `https://44.224.1.45`) instead of local Docker services.

---

## 🔑 Prerequisites

### 1. Remote Deployment URL
```
https://44.224.1.45
```

### 2. Bearer Token
You need a valid JWT Bearer token for authentication:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJpcm9ubWFuQGF2ZW5nZXJzLmNvbSIsIm5iZiI6MTc2NDg0NDc5NywiZXhwIjoxNzk2MzgwOTc3LCJqdGkiOiJRQmhCRkxIc3RTZTl1aEMwIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoic3VwcmVtbyIsInVzZXJfY2xhaW1zIjp7InVpZCI6IjEiLCJ1bmFtZSI6Imlyb25tYW5AYXZlbmdlcnMuY29tIiwib3JnIjoiYXZlbmdlcnMiLCJmaXJzdF9uYW1lIjoiVG9ueSIsImxhc3RfbmFtZSI6IlN0YXJrIiwicm9sZSI6IlN1cHJlbW8iLCJhZXNfa2V5IjoiWm5OWkpEVlNJTzNDZFVcbnB6amVCdlBNd1VtXG50SVJJYSIsIm9mc3QiOlsxODEsMzY0LDQzMiwxODEsOTMsMjYxLDEzNSwxNTIsMjczLDMzNCw0MDQsMzI0LDg1LDQzNiw0MTYsMzM5LDE5MiwyMjQsMzQwLDI0Miw5NCw0MzUsMTM3LDg2LDE1MywzMDIsMjIxLDI0OSwyNzMsMzI3LDQzOSwyMzZdfX0.HVKUxWnhp6ob1qktGZe4eJCsb5tX9dONXKNsEFJZ1FGiEPDrWbuc-lhP2SWNn_tHcBGTf-TudSEjyG3moe4d2XnJsMBneMDuO8S3XHvbgkxiEnRqQlT_uRGBCGfzOtlk13FiJY85wAXnBY_1gSNWoqtK7GPg2OdQcVTd4Owq7Xi97tRzlQkyHLfhPMxynzwVogd3ygXPmLQt5PvrJKYCYUqba4qij9l9THUs40JPxyYqhwD6VGm6VBAw9vpqH_eX7MV9HcU96I9lD-fsT8y5k7Yz9mfX6v7x_pw_y5FPcDFDt3WoKc8ZP46uQwu1dOk3iE9LOwtN5OtdfTE7ox_TbQ
```

**Token Info**:
- User: `ironman@avengers.com` (Tony Stark)
- Organization: `avengers`
- Role: `Supremo` (Admin)
- Expires: 2026+ (long-lived token)

---

## 🚀 Running Tests Against Remote Deployment

### Method 1: Using .env.local (Recommended)

Create a `.env.local` file in the tests directory:

```bash
# Navigate to tests directory
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Create .env.local file
cat > .env.local << 'EOF'
DAGKNOWS_URL=https://44.224.1.45
DAGKNOWS_TOKEN=your-token-here
EOF

# Run tests using the convenience script
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v
```

The script automatically loads `.env.local` if it exists!

### Method 2: Environment Variables

Set environment variables before running tests:

```bash
# Navigate to tests directory
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Set deployment URL and token
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-token-here"

# Run tests (from your host machine, NOT in Docker)
python -m pytest unit/taskservice/test_alert_handling_modes.py -v

# Or use the convenience script
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v
```

### Method 3: Inline Environment Variables

Run with environment variables inline:

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

DAGKNOWS_URL="https://44.224.1.45" \
DAGKNOWS_TOKEN="your-token-here" \
python -m pytest unit/taskservice/test_alert_handling_modes.py -v
```

---

## 📝 Test Examples

### Run All Alert Handling Tests

```bash
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-token-here"

python -m pytest unit/taskservice/test_alert_handling_modes.py -v

# Or use the convenience script (loads from .env.local)
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v
```

### Run Specific Mode Tests

**Deterministic Mode Only**:
```bash
python -m pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingDeterministic -v
```

**AI-Selected Mode**:
```bash
python -m pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAISelected -v -m ai_required
```

**Autonomous Mode**:
```bash
python -m pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAutonomous -v -m "ai_required and slow"
```

### Run CRUD Tests

```bash
python -m pytest unit/taskservice/test_task_crud.py -v
```

### Run Search Tests

```bash
python -m pytest unit/taskservice/test_task_search.py -v
```

---

## 🔄 Local vs Remote Mode Comparison

### Local Docker Mode (Default)

```bash
# No environment variables needed
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Uses Docker service names (taskservice, req-router, elasticsearch)
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py -v
```

**Characteristics**:
- Uses Docker service names (`http://taskservice:2235`, `http://req-router:8888`)
- Uses `dk-user-info` header for test authentication
- Waits for all services to be ready (Elasticsearch, TaskService, ReqRouter)
- Test mode enabled (`X-Test-Mode: true`)

### Remote Deployment Mode

```bash
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-token-here"

# Run directly on host (not in Docker)
python -m pytest unit/taskservice/test_alert_handling_modes.py -v

# Or use convenience script
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v
```

**Characteristics**:
- Uses remote URL (`https://44.224.1.45`)
- Uses Bearer token for real authentication
- Skips internal service health checks
- Test mode disabled (uses production authentication)
- Can load credentials from `.env.local`

---

## 🛠️ How It Works

The test framework automatically detects the mode:

```python
# conftest.py detects mode from environment
base_url = os.getenv("DAGKNOWS_URL")
bearer_token = os.getenv("DAGKNOWS_TOKEN")

if base_url and bearer_token:
    # Remote mode
    config["req_router_url"] = base_url
    config["bearer_token"] = bearer_token
    config["use_bearer_auth"] = True
else:
    # Local Docker mode
    config["req_router_url"] = "http://req-router:8888"
    config["use_bearer_auth"] = False
```

API clients automatically switch authentication:

```python
if test_config.get("use_bearer_auth"):
    # Remote mode: Use Bearer token
    client.set_bearer_token(test_config["bearer_token"])
else:
    # Local mode: Use test user info header
    client.set_user_info(user_info)
```

---

## ✅ Verification

Check that remote mode is active:

```bash
# Create .env.local with your credentials
cat > .env.local << 'EOF'
DAGKNOWS_URL=https://44.224.1.45
DAGKNOWS_TOKEN=your-token-here
EOF

# Run with verbose logging
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingDeterministic::test_deterministic_alert_triggers_configured_task -v -s

# Look for these log messages:
# 🌐 Remote deployment mode: https://44.224.1.45
# ✓ Bearer token authentication enabled
# Remote deployment mode - skipping internal service checks
```

---

## ⚠️ Important Notes

### 1. Run Tests Outside Docker

When testing against remote deployment, **run pytest directly on your host machine**, not inside Docker:

```bash
# ✅ CORRECT (host machine)
export DAGKNOWS_BASE_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="eyJhbGci..."
python -m pytest unit/taskservice/test_alert_handling_modes.py -v

# ❌ WRONG (inside Docker - can't reach remote URL)
docker-compose -f docker-compose-local.yml run --rm test-runner pytest ...
```

### 2. Token Expiration

The provided token expires in 2026. If tests fail with 401/403 errors, check token expiration:

```bash
# Decode JWT token (requires jq)
echo "eyJhbGci..." | cut -d. -f2 | base64 -d | jq
```

### 3. Network Access

Ensure your machine can reach the remote deployment:

```bash
# Test connectivity
curl -v https://44.224.1.45/health

# Test with Bearer token
curl -H "Authorization: Bearer eyJhbGci..." \
     https://44.224.1.45/api/v1/tasks/status
```

### 4. Data Cleanup

Tests create tasks and alerts on the remote deployment. Make sure:
- Tests clean up after themselves (they do)
- DELETE operations work (check `BACKEND_DELETE_BUG.md` for known issues)
- Or manually clean up if needed

### 5. Concurrent Testing

Be careful running tests concurrently against production-like environments:
- Tests may interfere with each other
- Use unique identifiers (tests use timestamps)
- Consider test isolation

---

## 🐛 Troubleshooting

### Issue: "Connection refused" or "Network unreachable"

**Problem**: Can't reach remote deployment

**Solution**:
```bash
# Check network
ping 44.224.1.45

# Check HTTPS
curl -v https://44.224.1.45

# Check if firewall/VPN blocking
```

### Issue: "401 Unauthorized" or "403 Forbidden"

**Problem**: Bearer token invalid or expired

**Solution**:
```bash
# Verify token format
echo $DAGKNOWS_TOKEN | wc -c  # Should be long (~800+ chars)

# Test token manually
curl -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
     https://44.224.1.45/api/v1/tasks/status

# Get new token if expired
```

### Issue: Tests skip with "AI mode not configured"

**Problem**: Remote deployment doesn't have AI modes enabled

**Solution**:
- Check deployment configuration
- Tests will skip gracefully if modes not available
- This is expected behavior

### Issue: "ModuleNotFoundError" when running pytest

**Problem**: Python packages not installed

**Solution**:
```bash
# Install test dependencies
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests
pip install -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Related Documentation

- **`ALERT_HANDLING_TESTS.md`** - Alert handling test details
- **`LOCAL_TESTING_GUIDE.md`** - Local Docker testing setup
- **`TEST_COMMANDS_REFERENCE.md`** - All test commands
- **`tests/utils/api_client.py`** - API client implementation

---

## 🔐 Security Notes

**DO NOT**:
- Commit Bearer tokens to Git
- Share tokens publicly
- Use production tokens in automated CI/CD (use separate test tokens)

**DO**:
- Store tokens securely (environment variables, secrets manager)
- Rotate tokens periodically
- Use least-privilege tokens for testing
- Revoke tokens when no longer needed

---

## 📞 Support

For issues with remote testing:
1. Verify network connectivity to deployment
2. Check Bearer token validity and expiration
3. Review test logs for authentication errors
4. Check deployment logs if you have access
5. Contact deployment admin for access issues

---

**Last Updated**: December 8, 2025
**Deployment**: `https://44.224.1.45`
**Organization**: `avengers`
**Test User**: `ironman@avengers.com`

