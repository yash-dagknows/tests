# Setup: Remote Deployment Testing

## Quick Setup (3 Steps)

### 1. Create `.env.local` file

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Copy the template
cp env.local.template .env.local

# Edit with your credentials
nano .env.local  # or vim, code, etc.
```

### 2. Add Your Credentials

Edit `.env.local`:

```bash
DAGKNOWS_URL=https://44.224.1.45
DAGKNOWS_TOKEN=your-actual-token-here
```

**Get your token from**:
- Remote machine: Check `.env.local` on the deployment server
- Your admin: Request a test token
- Auth service: Generate a new token

### 3. Run Tests

```bash
# That's it! The script automatically loads .env.local
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v
```

---

## Verify Setup

```bash
# Check your config is loaded
./run_remote_tests.sh --help

# Should show:
# 🌐 Testing against: https://44.224.1.45
# 👤 User: ironman@avengers.com (Supremo)
# 🔑 Token: eyJhbGci...
```

---

## Security Notes

✅ `.env.local` is **git-ignored** (safe to use)  
✅ Keep your token private  
✅ Don't commit `.env.local` to version control  
✅ Token is only visible to you

---

## Troubleshooting

**Issue**: "DAGKNOWS_TOKEN is not set"

```bash
# Check .env.local exists
ls -la .env.local

# Check contents
cat .env.local

# Ensure no spaces around = sign
# ✅ CORRECT:   DAGKNOWS_TOKEN=abc123
# ❌ WRONG:     DAGKNOWS_TOKEN = abc123
```

**Issue**: Token seems wrong

```bash
# Test manually
curl -H "Authorization: Bearer $DAGKNOWS_TOKEN" \
     https://44.224.1.45/api/v1/tasks/status
```

---

## Alternative: Environment Variables

If you don't want to use `.env.local`, export directly:

```bash
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-token"

./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v
```

---

## Next Steps

Once setup is complete, see:
- **`QUICK_START_ALERT_TESTS.md`** - Test commands
- **`REMOTE_TESTING_GUIDE.md`** - Complete guide
- **`ALERT_HANDLING_TESTS.md`** - Test details

---

**Ready? Run your first test:**

```bash
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingDeterministic::test_deterministic_alert_triggers_configured_task -v
```

