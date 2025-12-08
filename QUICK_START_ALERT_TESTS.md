# Quick Start: Alert Handling Tests

## 🎯 Two Ways to Run Tests

### Option 1: Against Remote Deployment (Production-like) 🌐

Test against the actual deployment at `https://44.224.1.45`:

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Create .env.local with credentials (one-time setup)
cat > .env.local << 'EOF'
DAGKNOWS_URL=https://44.224.1.45
DAGKNOWS_TOKEN=your-token-here
EOF

# Use the convenient script (loads from .env.local)
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v

# Or set env vars manually
export DAGKNOWS_URL="https://44.224.1.45"
export DAGKNOWS_TOKEN="your-token-here"
python -m pytest unit/taskservice/test_alert_handling_modes.py -v
```

### Option 2: Against Local Docker 🐳

Test against local Docker services:

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# Start services
docker-compose -f docker-compose-local.yml up -d

# Run tests in Docker
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py -v
```

---

## 🚀 Quick Test Commands

### All Alert Tests
```bash
# Remote
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v

# Local
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py -v
```

### Deterministic Mode Only
```bash
# Remote
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingDeterministic -v

# Local  
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingDeterministic -v
```

### AI-Selected Mode
```bash
# Remote
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAISelected -v -m ai_required

# Local
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAISelected -v -m ai_required
```

### Autonomous Mode
```bash
# Remote
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAutonomous -v -m "ai_required and slow"

# Local
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_alert_handling_modes.py::TestAlertHandlingAutonomous -v -m "ai_required and slow"
```

---

## 📚 Documentation

- **`REMOTE_TESTING_GUIDE.md`** - Complete guide for remote testing
- **`ALERT_HANDLING_TESTS.md`** - Detailed alert test documentation
- **`LOCAL_TESTING_GUIDE.md`** - Local Docker setup guide

---

## 🔑 Remote Deployment Details

**URL**: `https://44.224.1.45`  
**Token**: Already configured in `run_remote_tests.sh`  
**User**: `ironman@avengers.com` (Supremo role)  
**Org**: `avengers`

---

## ✅ What's Included

### Test Files
- ✅ `test_alert_handling_modes.py` - 8 tests for 3 alert modes
- ✅ Deterministic mode tests (2)
- ✅ AI-selected mode tests (2)
- ✅ Autonomous mode tests (1)
- ✅ Alert search/stats tests (3)

### Test Infrastructure
- ✅ Bearer token authentication for remote testing
- ✅ Automatic mode detection (local vs remote)
- ✅ Alert payload generators (Grafana, PagerDuty)
- ✅ API client methods for alerts
- ✅ Proper cleanup handling

### Scripts & Documentation
- ✅ `run_remote_tests.sh` - Convenient remote test runner
- ✅ `REMOTE_TESTING_GUIDE.md` - Complete remote testing guide
- ✅ `ALERT_HANDLING_TESTS.md` - Test suite documentation
- ✅ `QUICK_START_ALERT_TESTS.md` - This quick start guide

---

## 🎉 You're Ready!

Just run:
```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests
./run_remote_tests.sh unit/taskservice/test_alert_handling_modes.py -v
```

That's it! The tests will run against your remote deployment with proper authentication. 🚀

