# Local Testing Guide - Test with Your dkapp Setup

## Overview

This guide shows you how to test locally with your existing `dkapp` and `dkproxy` setup **before** integrating with Jenkins.

## Prerequisites

You need:
1. ✅ `dkapp` services running (your existing setup)
2. ✅ `dkproxy` (if testing proxy functionality)
3. ✅ Docker and Docker Compose installed
4. ✅ Python 3.10+ (for local pytest execution)

## Quick Start (10 minutes)

### Step 1: Start Your dkapp Services (2 min)

```bash
# Navigate to dkapp directory
cd ../dkapp

# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps

# Check network exists
docker network ls | grep saaslocalnetwork
```

**Expected output**: All services should show "Up" status

### Step 2: Setup Test Environment (3 min)

```bash
# Navigate to tests directory
cd ../tests

# Run setup (creates .env.local and installs dependencies)
make -f Makefile.local setup
```

This will:
- Create `.env.local` from example
- Install Python dependencies
- Create results and logs directories

### Step 3: Configure Environment (2 min)

```bash
# Edit .env.local with your actual values
nano .env.local  # or vi, code, etc.
```

**IMPORTANT**: Copy these values from your `dkapp/.env`:

```bash
# From dkapp/.env, copy these values:
POSTGRESQL_DB_PASSWORD=<your value>
APP_SECRET_KEY=<your value>
api_key=<your value>
```

### Step 4: Verify Services (1 min)

```bash
# Check dkapp services are accessible
make -f Makefile.local check-dkapp

# Verify connectivity
make -f Makefile.local verify-services
```

**Expected**: All checks should pass with ✓

### Step 5: Run Your First Test (2 min)

```bash
# Run fast unit tests
make -f Makefile.local test-unit-docker
```

**Expected**: Tests run and pass in < 5 minutes

🎉 **Success!** You're now running tests locally!

## Available Commands

### Quick Reference

```bash
# Setup
make -f Makefile.local setup              # Initial setup
make -f Makefile.local check-dkapp        # Check if services running

# Run Tests
make -f Makefile.local test-unit-docker   # Unit tests (fast, 2-5 min)
make -f Makefile.local test-integration   # Integration tests (10-15 min)
make -f Makefile.local test-e2e          # E2E tests (20-30 min)
make -f Makefile.local test-quick        # Smoke tests (1-2 min)
make -f Makefile.local test-all          # All tests (30-45 min)

# With Coverage
make -f Makefile.local test-coverage     # Tests + coverage report

# Specific Tests
make -f Makefile.local test-specific TEST=unit/taskservice/test_task_crud.py

# Debugging
make -f Makefile.local shell             # Open shell in test container
make -f Makefile.local verify-services   # Test service connectivity
make -f Makefile.local status            # Show dkapp service status

# Cleanup
make -f Makefile.local clean             # Clean test artifacts
```

### Aliases (Shorter Commands)

```bash
make -f Makefile.local unit              # Same as test-unit-docker
make -f Makefile.local integration       # Same as test-integration
make -f Makefile.local e2e               # Same as test-e2e
make -f Makefile.local quick             # Same as test-quick
make -f Makefile.local smoke             # Same as test-quick
make -f Makefile.local coverage          # Same as test-coverage
```

## Detailed Testing Workflow

### 1. Unit Tests (Start Here)

```bash
# Run unit tests (no service dependencies)
make -f Makefile.local unit

# These test:
# - Task CRUD operations
# - Search functionality
# - Workspace management
# - Authentication logic
# - Tenant management
```

**Time**: 2-5 minutes  
**Services needed**: None (tests use mocks)  
**Best for**: Quick validation during development

### 2. Integration Tests

```bash
# Run integration tests (requires dkapp services)
make -f Makefile.local integration

# These test:
# - req-router → taskservice communication
# - Task → Elasticsearch indexing
# - Tenant creation flow
# - Database operations
# - Service-to-service authentication
```

**Time**: 10-15 minutes  
**Services needed**: All dkapp services  
**Best for**: Verifying service interactions

### 3. End-to-End Tests

```bash
# Run E2E tests (complete workflows)
make -f Makefile.local e2e

# These test:
# - Complete tenant onboarding
# - Task lifecycle (create → edit → delete)
# - Multi-user collaboration
# - Workspace management workflows
```

**Time**: 20-30 minutes  
**Services needed**: All dkapp services  
**Best for**: Release validation

### 4. Quick Smoke Tests

```bash
# Run only critical smoke tests
make -f Makefile.local quick

# These test:
# - Can services be reached?
# - Can create a basic task?
# - Can authenticate?
```

**Time**: 1-2 minutes  
**Services needed**: All dkapp services  
**Best for**: Quick sanity check

## Testing Specific Scenarios

### Test Tenant Creation

```bash
# Test tenant creation workflow
make -f Makefile.local test-specific TEST=integration/test_tenant_creation.py -v
```

### Test Task Workflow

```bash
# Test task operations
make -f Makefile.local test-specific TEST=integration/test_task_workflow.py -v
```

### Test a Single Test Function

```bash
# Run one specific test
make -f Makefile.local test-specific \
    TEST="unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task"
```

## Debugging Tests

### Open a Shell in Test Container

```bash
# Get an interactive shell
make -f Makefile.local shell

# Now you're inside the container, run commands:
pytest unit/taskservice/test_task_crud.py -v
pytest integration/ -v -k "tenant"
curl http://taskservice:2235/health
exit
```

### Run Tests with Debugger

```bash
# Tests will drop into debugger on failure
make -f Makefile.local debug
```

### Check Service Connectivity

```bash
# Verify all services are reachable
make -f Makefile.local verify-services

# Should show:
# ✓ Elasticsearch OK
# ✓ TaskService OK
# ✓ ReqRouter OK
```

### View Service Logs

```bash
# View dkapp service logs
cd ../dkapp
docker-compose logs -f taskservice
docker-compose logs -f req-router

# Or specific service
docker logs taskservice --tail 50
```

## Common Issues & Solutions

### Issue 1: "saaslocalnetwork not found"

**Symptom**:
```
✗ saaslocalnetwork not found!
```

**Solution**:
```bash
# Start dkapp services first
cd ../dkapp
docker-compose up -d

# Verify
docker network ls | grep saaslocalnetwork
```

### Issue 2: "Services not running"

**Symptom**:
```
✗ taskservice not running!
```

**Solution**:
```bash
# Check dkapp status
cd ../dkapp
docker-compose ps

# Restart if needed
docker-compose restart

# Or fully restart
docker-compose down && docker-compose up -d
```

### Issue 3: "Connection refused"

**Symptom**:
```
requests.exceptions.ConnectionError: Connection refused
```

**Solution**:
```bash
# 1. Check if services are healthy
make -f Makefile.local verify-services

# 2. Check service logs
cd ../dkapp
docker-compose logs taskservice | tail -50

# 3. Wait for services to be fully ready
# Services may take 30-60s to start
sleep 30
make -f Makefile.local verify-services
```

### Issue 4: ".env.local contains placeholder values"

**Symptom**:
```
✗ .env.local contains placeholder values!
```

**Solution**:
```bash
# Edit .env.local and replace all "your_*_here" with actual values
nano .env.local

# Copy from dkapp/.env:
# - POSTGRESQL_DB_PASSWORD
# - APP_SECRET_KEY
# - api_key
```

### Issue 5: "Authentication failed"

**Symptom**:
```
401 Unauthorized
```

**Solution**:
```bash
# 1. Verify APP_SECRET_KEY is set correctly in .env.local
grep APP_SECRET_KEY .env.local

# 2. Ensure it matches dkapp/.env
grep APP_SECRET_KEY ../dkapp/.env

# 3. Verify ALLOW_DK_USER_INFO_HEADER is true
# This should already be set in docker-compose-local.yml
```

### Issue 6: Tests hang or timeout

**Symptom**:
```
Test timeout after 300s
```

**Solution**:
```bash
# 1. Check Elasticsearch is responsive
curl http://localhost:9200/_cluster/health

# 2. Check database connectivity
docker exec postgres pg_isready

# 3. Increase Docker resources
# Docker Desktop → Preferences → Resources
# Memory: 4GB+ recommended
# CPUs: 2+ recommended
```

## File Structure

```
tests/
├── Makefile.local              # Main commands for local testing
├── docker-compose-local.yml    # Docker config for local testing
├── .env.local                  # Your local configuration
│
├── unit/                       # Unit tests
├── integration/                # Integration tests
├── e2e/                       # End-to-end tests
│
└── LOCAL_TESTING_GUIDE.md     # This file
```

## Integration with Jenkins (Later)

The local setup uses the same structure as Jenkins:
- ✅ Same Docker network (`saaslocalnetwork`)
- ✅ Same service names (no localhost)
- ✅ Same authentication (`APP_SECRET_KEY`)
- ✅ Same environment variables

**When ready for Jenkins**:
1. Your tests already work locally ✓
2. Just configure Jenkins credentials
3. Use `Jenkinsfile.production`
4. Everything will work the same way!

## Performance Expectations

| Test Type | Time | Services Required |
|-----------|------|-------------------|
| Unit | 2-5 min | None |
| Integration | 10-15 min | dkapp |
| E2E | 20-30 min | dkapp |
| Full Suite | 30-45 min | dkapp |
| Quick Smoke | 1-2 min | dkapp |

## Tips for Effective Testing

### 1. Start Small
```bash
# Begin with unit tests
make -f Makefile.local unit

# Then try one integration test
make -f Makefile.local test-specific TEST=integration/test_task_workflow.py
```

### 2. Use Smoke Tests for Quick Checks
```bash
# Before committing code
make -f Makefile.local quick
```

### 3. Run Full Suite Before Releases
```bash
# Comprehensive testing
make -f Makefile.local test-all
```

### 4. Check Coverage
```bash
# See what's tested
make -f Makefile.local coverage
open results/htmlcov/index.html
```

### 5. Debug Failed Tests
```bash
# Get a shell for investigation
make -f Makefile.local shell

# Inside container:
pytest unit/taskservice/test_task_crud.py -v -s --pdb
```

## Next Steps

After local testing works:

1. ✅ **Confirm tests pass locally**
2. ✅ **Add tests for your specific features**
3. ✅ **Setup Jenkins credentials** (from dkapp/.env)
4. ✅ **Create Jenkins pipeline** (use Jenkinsfile.production)
5. ✅ **Automate in CI/CD**

## Summary

You can now:
- ✅ Test locally with your existing dkapp setup
- ✅ Run tests with simple make commands
- ✅ Debug tests interactively
- ✅ Verify service connectivity
- ✅ Run specific test scenarios
- ✅ Generate coverage reports

Everything is ready for Jenkins integration when you're ready!

## Quick Command Reference Card

```bash
# Setup
make -f Makefile.local setup
make -f Makefile.local check-dkapp

# Test
make -f Makefile.local unit              # Fast unit tests
make -f Makefile.local integration       # Service tests
make -f Makefile.local e2e              # Full workflows
make -f Makefile.local quick            # Smoke tests

# Debug
make -f Makefile.local shell            # Interactive shell
make -f Makefile.local verify-services  # Check connectivity
make -f Makefile.local status           # Service status

# Help
make -f Makefile.local help             # Show all commands
```

**Start testing now**: `make -f Makefile.local setup` 🚀

