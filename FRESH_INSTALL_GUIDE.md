# Fresh Instance Setup Guide

## Prerequisites Check

Your fresh instance should have:
- ✅ `dkapp` installed in home folder
- ✅ `dkproxy` installed in home folder
- ✅ Docker and Docker Compose installed
- ✅ Python 3.10+ installed

## Complete Setup Steps

### Step 1: Navigate to Your Setup (2 minutes)

```bash
# Assuming your structure is:
# ~/dkapp/
# ~/dkproxy/
# ~/dagknows_src/  (or wherever you cloned the repo)

cd ~/dagknows_src/tests

# Verify you're in the right place
pwd
# Should show: /home/youruser/dagknows_src/tests

ls -la
# Should show: setup-local.sh, Makefile.local, pytest.ini, etc.
```

### Step 2: Start dkapp Services (5 minutes)

```bash
# Go to dkapp directory
cd ~/dkapp

# Start all services
docker-compose up -d

# Wait for services to start (this takes ~60 seconds)
echo "Waiting for services to start..."
sleep 60

# Check services are running
docker-compose ps

# You should see:
# - postgres        (Up)
# - elasticsearch   (Up)
# - taskservice     (Up)
# - req-router      (Up)
# - settings        (Up)
# - conv-mgr        (Up)
# - wsfe            (Up)
# And others...

# Verify network exists
docker network ls | grep saaslocalnetwork
# Should show: saaslocalnetwork
```

**If services fail to start:**
```bash
# Check logs
docker-compose logs | tail -50

# Common issues:
# - Port conflicts: Stop other services using same ports
# - Memory: Ensure Docker has 4GB+ memory
# - Disk space: Check available space
```

### Step 3: Install Prerequisites (3 minutes)

```bash
# Go to tests directory
cd ~/dagknows_src/tests

# Make scripts executable
chmod +x setup-local.sh
chmod +x ci/wait-for-services-jenkins.sh
chmod +x utils/wait-for-services.sh

# Install Python dependencies
pip3 install -r requirements.txt

# If pip3 not found, install Python and pip first:
# Ubuntu/Debian:
# sudo apt update
# sudo apt install python3 python3-pip

# macOS:
# brew install python3
```

### Step 4: Run Setup Script (5 minutes)

```bash
cd ~/dagknows_src/tests

# Run the setup script
./setup-local.sh
```

**What the script will do:**

1. Check if dkapp is configured
2. Look for `~/dkapp/.env` or `~/dkapp/.env.gpg`
3. If `.env.gpg` found, prompt for GPG passphrase
4. Extract credentials and create `.env.local`
5. Install Python dependencies
6. Verify services are accessible

**Expected Output:**
```
========================================
DagKnows Test Suite - Local Setup
========================================

Step 1: Checking dkapp setup...
✓ dkapp directory found
✓ dkapp/.env found (or .env.gpg decrypted)

Step 2: Checking Docker network...
✓ saaslocalnetwork exists

Step 3: Creating .env.local...
✓ .env.local created

Step 4: Creating directories...
✓ Directories created

Step 5: Installing Python dependencies...
✓ Dependencies installed

Step 6: Verifying services...
✓ taskservice running
✓ req-router running
✓ postgres running
✓ elasticsearch running

========================================
Setup Complete!
========================================

Next steps:
  1. Run quick test:    make -f Makefile.local quick
  2. Run unit tests:    make -f Makefile.local unit
  3. Run all tests:     make -f Makefile.local test-all
  4. Get help:          make -f Makefile.local help
```

**If you have `.env.gpg`:**
```
⚠ Found dkapp/.env.gpg (encrypted)
Decrypting .env.gpg...
Please enter GPG passphrase when prompted...
[Enter your passphrase]
✓ Successfully decrypted .env
```

### Step 5: Verify Services (2 minutes)

```bash
# Check services are accessible from test container
make -f Makefile.local verify-services
```

**Expected Output:**
```
Verifying service connectivity...
Testing Elasticsearch...
✓ Elasticsearch OK
Testing TaskService...
✓ TaskService OK
Testing ReqRouter...
✓ ReqRouter OK

All services accessible!
```

### Step 6: Run Your First Test (2 minutes)

```bash
# Run quick smoke tests
make -f Makefile.local quick
```

**Expected Output:**
```
Running quick smoke tests...
======================= test session starts ========================
collected 3 items

e2e/test_ai_session_workflow.py::TestAIServicePlaceholder::test_ai_service_architecture_documented ✓
e2e/test_ai_session_workflow.py::TestAIServicePlaceholder::test_ai_service_endpoints_defined ✓

======================= 2 passed in 2.34s ==========================
```

### Step 7: Run Full Unit Tests (5 minutes)

```bash
# Run all unit tests
make -f Makefile.local unit
```

**Expected Output:**
```
Running unit tests in Docker...
======================= test session starts ========================
collected 25 items

unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task ✓
unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_task_with_custom_id ✓
unit/taskservice/test_task_crud.py::TestTaskCRUD::test_get_task ✓
[... more tests ...]

======================= 25 passed in 4.12s =========================
```

🎉 **Success!** Your test suite is now working!

## Complete Setup Summary

Here's what you did:

```bash
# 1. Start dkapp
cd ~/dkapp && docker-compose up -d

# 2. Setup tests
cd ~/dagknows_src/tests
chmod +x setup-local.sh
./setup-local.sh

# 3. Verify
make -f Makefile.local verify-services

# 4. Test
make -f Makefile.local quick
make -f Makefile.local unit
```

## Directory Structure

After setup, your structure should be:

```
~/
├── dkapp/
│   ├── docker-compose.yml
│   ├── .env (or .env.gpg)
│   └── ... (running services)
│
├── dkproxy/
│   └── ... (proxy files)
│
└── dagknows_src/
    ├── taskservice/
    ├── req_router/
    └── tests/
        ├── .env.local           ← Created by setup
        ├── results/             ← Test results
        ├── logs/                ← Test logs
        ├── setup-local.sh       ← Setup script
        ├── Makefile.local       ← Commands
        └── ... (test files)
```

## Troubleshooting Common Issues

### Issue 1: "saaslocalnetwork not found"

**Cause:** dkapp services not started

**Fix:**
```bash
cd ~/dkapp
docker-compose up -d
sleep 60  # Wait for startup
cd ~/dagknows_src/tests
./setup-local.sh
```

### Issue 2: "Permission denied" on scripts

**Cause:** Scripts not executable

**Fix:**
```bash
cd ~/dagknows_src/tests
chmod +x setup-local.sh
chmod +x ci/wait-for-services-jenkins.sh
chmod +x utils/wait-for-services.sh
```

### Issue 3: "pip3 not found"

**Cause:** Python not installed

**Fix:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# macOS
brew install python3

# Verify
python3 --version
pip3 --version
```

### Issue 4: "Docker not found"

**Cause:** Docker not installed

**Fix:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
docker-compose --version
```

### Issue 5: "Connection refused" to services

**Cause:** Services not fully started or not healthy

**Fix:**
```bash
# Check service health
cd ~/dkapp
docker-compose ps

# Check logs
docker-compose logs taskservice --tail 50
docker-compose logs req-router --tail 50

# Restart if needed
docker-compose restart

# Wait for healthy state
sleep 30

# Try again
cd ~/dagknows_src/tests
make -f Makefile.local verify-services
```

### Issue 6: "GPG command not found"

**Cause:** GPG not installed (needed if using .env.gpg)

**Fix:**
```bash
# Ubuntu/Debian
sudo apt install gnupg

# macOS
brew install gnupg

# Verify
gpg --version
```

### Issue 7: Docker daemon not running

**Cause:** Docker service not started

**Fix:**
```bash
# Ubuntu/Debian
sudo systemctl start docker
sudo systemctl enable docker

# macOS
# Open Docker Desktop application

# Verify
docker ps
```

## Quick Commands Reference

### Daily Usage

```bash
# Start dkapp (if not running)
cd ~/dkapp && docker-compose up -d

# Navigate to tests
cd ~/dagknows_src/tests

# Quick tests (1-2 min)
make -f Makefile.local quick

# Unit tests (2-5 min)
make -f Makefile.local unit

# Integration tests (10-15 min)
make -f Makefile.local integration

# All tests (30-45 min)
make -f Makefile.local test-all

# View results
open results/report.html  # macOS
xdg-open results/report.html  # Linux
```

### Maintenance

```bash
# Check service status
cd ~/dkapp && docker-compose ps

# View logs
cd ~/dkapp && docker-compose logs -f taskservice

# Restart services
cd ~/dkapp && docker-compose restart

# Stop services
cd ~/dkapp && docker-compose down

# Clean test artifacts
cd ~/dagknows_src/tests && make -f Makefile.local clean
```

### Debugging

```bash
# Verify services accessible
cd ~/dagknows_src/tests
make -f Makefile.local verify-services

# Check dkapp is running
make -f Makefile.local check-dkapp

# Open shell in test container
make -f Makefile.local shell

# Show service status
make -f Makefile.local status

# Show all commands
make -f Makefile.local help
```

## File Locations

Important files to know about:

```bash
# Your credentials (auto-generated, don't commit)
~/dagknows_src/tests/.env.local

# Test results (after running tests)
~/dagknows_src/tests/results/report.html
~/dagknows_src/tests/results/junit.xml

# Test logs
~/dagknows_src/tests/logs/

# dkapp services
~/dkapp/docker-compose.yml
~/dkapp/.env (or .env.gpg)
```

## Next Steps After Setup

### 1. Verify Everything Works

```bash
cd ~/dagknows_src/tests

# Run quick tests
make -f Makefile.local quick

# Run unit tests
make -f Makefile.local unit

# Check results
ls -la results/
```

### 2. Understand Available Tests

```bash
# List test files
find . -name "test_*.py" -type f

# Unit tests
ls -la unit/

# Integration tests
ls -la integration/

# E2E tests
ls -la e2e/
```

### 3. Run Specific Scenarios

```bash
# Test tenant creation
make -f Makefile.local test-specific TEST=integration/test_tenant_creation.py

# Test task workflow
make -f Makefile.local test-specific TEST=integration/test_task_workflow.py

# Test task CRUD
make -f Makefile.local test-specific TEST=unit/taskservice/test_task_crud.py
```

### 4. Generate Coverage Report

```bash
# Run tests with coverage
make -f Makefile.local coverage

# View coverage report
open results/htmlcov/index.html  # macOS
xdg-open results/htmlcov/index.html  # Linux
```

## Automated Setup Script (Optional)

Save this as `~/setup-dagknows-tests.sh` for future fresh installs:

```bash
#!/bin/bash
set -e

echo "Setting up DagKnows Test Suite..."

# Start dkapp
cd ~/dkapp
docker-compose up -d
sleep 60

# Setup tests
cd ~/dagknows_src/tests
chmod +x setup-local.sh
./setup-local.sh

# Verify
make -f Makefile.local verify-services

# Run quick test
make -f Makefile.local quick

echo "Setup complete! Tests are working."
```

Then just:
```bash
chmod +x ~/setup-dagknows-tests.sh
~/setup-dagknows-tests.sh
```

## Summary

You've successfully set up the test suite! You can now:

✅ Run tests against your local dkapp  
✅ Test locally before committing code  
✅ Debug issues with integrated services  
✅ Develop new features with test coverage  
✅ Prepare for Jenkins CI/CD integration  

## Help & Documentation

- **Quick Start**: `cat QUICK_START.md`
- **Local Testing**: `cat LOCAL_TESTING_GUIDE.md`
- **GPG Setup**: `cat GPG_SETUP.md`
- **All Commands**: `make -f Makefile.local help`
- **This Guide**: `cat FRESH_INSTALL_GUIDE.md`

**Questions?** All documentation is in the `~/dagknows_src/tests/` directory!

