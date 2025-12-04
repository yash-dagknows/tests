# Quick Start - Test Locally in 5 Minutes

## Prerequisites

1. Your `dkapp` services should be running
2. Docker Desktop running
3. Terminal access

## Step-by-Step Instructions

### 1. Navigate to tests directory

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests
```

### 2. Run the setup script

```bash
./setup-local.sh
```

This will:
- ✅ Check if dkapp is configured
- ✅ Start dkapp services if needed
- ✅ Create `.env.local` from your `dkapp/.env`
- ✅ Install Python dependencies
- ✅ Verify services are running

### 3. Verify everything works

```bash
make -f Makefile.local verify-services
```

Expected output:
```
Testing Elasticsearch...
✓ Elasticsearch OK
Testing TaskService...
✓ TaskService OK
Testing ReqRouter...
✓ ReqRouter OK
```

### 4. Run your first test

```bash
# Option A: Quick smoke test (1-2 minutes)
make -f Makefile.local quick

# Option B: Unit tests (2-5 minutes)
make -f Makefile.local unit

# Option C: Specific test
make -f Makefile.local test-specific TEST=unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task
```

## If Setup Fails

### Issue: "dkapp services not running"

```bash
# Start dkapp
cd ../dkapp
docker-compose up -d

# Wait 30 seconds for services to start
sleep 30

# Check status
docker-compose ps

# Go back to tests
cd ../tests
```

### Issue: "saaslocalnetwork not found"

```bash
# Create network
docker network create saaslocalnetwork

# Or restart dkapp
cd ../dkapp
docker-compose down
docker-compose up -d
cd ../tests
```

### Issue: "Connection refused"

```bash
# Check services are healthy
cd ../dkapp
docker-compose ps

# Restart problematic service
docker-compose restart taskservice

# Wait for it to be ready
sleep 10

# Try again
cd ../tests
make -f Makefile.local verify-services
```

## What to Test First

### 1. Smoke Test (Fastest - 1-2 min)

```bash
make -f Makefile.local quick
```

Tests basic connectivity and critical paths.

### 2. Unit Tests (Fast - 2-5 min)

```bash
make -f Makefile.local unit
```

Tests individual components without service dependencies.

### 3. Integration Tests (Medium - 10-15 min)

```bash
make -f Makefile.local integration
```

Tests service-to-service communication.

### 4. E2E Tests (Slow - 20-30 min)

```bash
make -f Makefile.local e2e
```

Tests complete workflows.

## Common Commands

```bash
# Show all available commands
make -f Makefile.local help

# Check if dkapp is running
make -f Makefile.local check-dkapp

# Verify services are accessible
make -f Makefile.local verify-services

# Show service status
make -f Makefile.local status

# Run specific test file
make -f Makefile.local test-specific TEST=unit/taskservice/test_task_crud.py

# Open interactive shell
make -f Makefile.local shell

# Clean test artifacts
make -f Makefile.local clean
```

## Test Results

Results are saved in:
- `results/junit.xml` - JUnit XML format
- `results/report.html` - HTML test report
- `results/htmlcov/` - Coverage report (if run with coverage)

View HTML report:
```bash
# macOS
open results/report.html

# Linux
xdg-open results/report.html

# Or just open in browser
```

## Next Steps After Local Testing Works

Once local tests pass:

1. ✅ **Add your own tests** for new features
2. ✅ **Run tests before committing** code
3. ✅ **Setup Jenkins** when ready (see JENKINS_SETUP_GUIDE.md)
4. ✅ **Automate in CI/CD** pipeline

## Troubleshooting

### All services show "not running"

```bash
# Start from scratch
cd ../dkapp
docker-compose down
docker-compose up -d

# Wait for everything to start
sleep 60

# Check status
docker-compose ps

# Try tests again
cd ../tests
make -f Makefile.local unit
```

### Tests timeout

```bash
# Check Docker resources
# Docker Desktop → Preferences → Resources
# Ensure: Memory >= 4GB, CPUs >= 2

# Check service health
cd ../dkapp
docker-compose logs taskservice --tail 50
docker-compose logs req-router --tail 50
```

### "Module not found" errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or in Docker
make -f Makefile.local unit  # Uses Docker, no local pip needed
```

## Complete Example Session

```bash
# 1. Setup
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests
./setup-local.sh

# 2. Verify
make -f Makefile.local verify-services

# 3. Test
make -f Makefile.local quick      # Smoke test (1-2 min)
make -f Makefile.local unit       # Unit tests (2-5 min)

# 4. View results
open results/report.html

# 5. If all pass, try integration
make -f Makefile.local integration  # (10-15 min)
```

## Success Criteria

You know it's working when:

✅ `./setup-local.sh` completes without errors  
✅ `make -f Makefile.local verify-services` shows all ✓  
✅ `make -f Makefile.local quick` passes  
✅ `make -f Makefile.local unit` passes  

## Summary

**Fastest path to first test**:
```bash
cd tests
./setup-local.sh
make -f Makefile.local quick
```

**That's it!** 🚀

For more details, see [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md)

