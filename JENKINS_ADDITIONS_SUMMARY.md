# Jenkins Integration - Additions Summary

## What Was Added for Your Jenkins/AWS Infrastructure

### Problem Addressed

Your original concerns:
1. ✅ **Docker Network**: Services use `saaslocalnetwork`, not localhost
2. ✅ **Encryption**: Services communicate with `APP_SECRET_KEY` and AES
3. ✅ **Service Discovery**: Services reference each other by name (e.g., `taskservice:2235`)
4. ✅ **AWS ECS Agents**: Tests run on Terraform-managed Jenkins agents
5. ✅ **TLS/Certificates**: Services use mounted certificates

### Solution Implemented

Created **3 deployment strategies** with files for each:

## New Files Created

### 1. Core Jenkins Files

```
tests/
├── docker-compose-jenkins.yml           # Connects to existing saaslocalnetwork
├── Jenkinsfile.production               # Production-ready pipeline
├── ci/
│   └── wait-for-services-jenkins.sh    # Service health checks (Docker names)
│
├── JENKINS_INTEGRATION.md               # Detailed options (3 strategies)
└── JENKINS_SETUP_GUIDE.md              # Quick start guide
```

### 2. Key Differences from Original Test Suite

| Feature | Original (Localhost) | Jenkins Version |
|---------|---------------------|-----------------|
| Network | Test network | `saaslocalnetwork` (external) |
| Service URLs | `localhost:port` | `servicename:port` |
| Authentication | Test mode bypass | Uses `APP_SECRET_KEY` |
| Docker Compose | `docker-compose-test.yml` | `docker-compose-jenkins.yml` |
| Health Checks | `localhost` endpoints | Service name endpoints |

## How It Works

### Option 1: In-Network Testing (Recommended)

**File**: `docker-compose-jenkins.yml`

```yaml
networks:
  saaslocalnetwork:
    external: true  # Uses YOUR existing network

services:
  test-runner:
    networks:
      - saaslocalnetwork  # Same network as your services
    environment:
      # Uses Docker service names
      - DAGKNOWS_TASKSERVICE_URL=http://taskservice:2235
      - DAGKNOWS_REQ_ROUTER_URL=http://req-router:8888
      - APP_SECRET_KEY=${APP_SECRET_KEY}  # Inherits encryption
```

**When to use**: 
- Integration tests against running dev/staging environment
- Fastest option (services already running)
- No service startup time

**Jenkins Pipeline**: `Jenkinsfile.production`

```groovy
pipeline {
    agent { label 'docker-agent' }
    
    environment {
        APP_SECRET_KEY = credentials('dagknows-app-secret-key')
    }
    
    stages {
        stage('Run Tests') {
            steps {
                sh '''
                    cd tests
                    docker-compose -f docker-compose-jenkins.yml run --rm test-runner
                '''
            }
        }
    }
}
```

### Option 2: Isolated Test Stack

**File**: See `JENKINS_INTEGRATION.md` for `docker-compose-jenkins-isolated.yml`

Spins up complete isolated environment:
- Own Postgres
- Own Elasticsearch
- Own TaskService
- Own ReqRouter
- Test Runner

**When to use**:
- Release testing
- Don't want to affect dev/staging
- Need reproducible environment

### Option 3: Hybrid Strategy

**Fast unit tests** (no services) + **Integration tests** (with services)

**When to use**:
- PR validation: Unit tests only (~5 min)
- Main branch: Full suite (~20 min)
- Nightly: All tests with coverage (~30 min)

## Implementation Steps

### Step 1: Configure Jenkins Credentials (5 minutes)

In Jenkins → Credentials → Add:
```
ID: dagknows-app-secret-key
Type: Secret text
Secret: <your APP_SECRET_KEY from dkapp/>
```

Repeat for:
- `dagknows-postgres-password`
- `dagknows-api-key`

### Step 2: Create Jenkins Pipeline (2 minutes)

Jenkins → New Item → Pipeline
- Name: `dagknows-tests`
- Pipeline from SCM
- Script path: `tests/Jenkinsfile.production`

### Step 3: Test Locally (Optional, 10 minutes)

```bash
# Navigate to tests
cd tests

# Export credentials
export APP_SECRET_KEY="..."
export POSTGRESQL_DB_PASSWORD="..."
export api_key="..."

# Test unit tests (no services)
docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
    pytest unit/ -v

# Test integration (requires running services in dkapp/)
docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
    pytest integration/ -v -k "test_task_workflow"
```

### Step 4: Run in Jenkins (1 minute)

1. Go to your pipeline
2. Click "Build with Parameters"
3. Select:
   - TEST_SUITE: `unit`
   - RUN_COVERAGE: `true`
4. Click "Build"

Expected: Tests run in ~5 minutes and pass ✓

## Testing the Setup

### Quick Verification Commands

```bash
# 1. Check network exists
docker network ls | grep saaslocalnetwork

# 2. Check services are running
docker ps --filter "network=saaslocalnetwork"

# 3. Test service connectivity FROM test container
docker run --rm --network=saaslocalnetwork curlimages/curl:latest \
    curl -f http://taskservice:2235/health

# 4. Test locally
cd tests
export APP_SECRET_KEY="your-key"
docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
    pytest unit/ -v --tb=short -x
```

## Troubleshooting Guide

### Problem: Tests can't connect to services

**Symptom**: `Connection refused` or `Could not resolve host`

**Solution**:
```bash
# 1. Verify test container is on correct network
docker-compose -f docker-compose-jenkins.yml config | grep saaslocalnetwork

# 2. Check services are accessible
docker run --rm --network=saaslocalnetwork alpine:latest \
    ping -c 3 taskservice

# 3. Ensure services are running
docker ps --filter "network=saaslocalnetwork" --format "{{.Names}}: {{.Status}}"
```

### Problem: Authentication errors

**Symptom**: `401 Unauthorized` or `Invalid token`

**Solution**:
```bash
# 1. Check APP_SECRET_KEY is set
docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
    sh -c 'echo $APP_SECRET_KEY | wc -c'  # Should be > 10

# 2. Verify ALLOW_DK_USER_INFO_HEADER is true
docker-compose -f docker-compose-jenkins.yml config | grep ALLOW_DK_USER_INFO_HEADER

# 3. Check service logs for auth errors
docker logs req-router --tail 50 | grep -i auth
```

### Problem: Slow or hanging tests

**Symptom**: Tests timeout after 30s

**Solution**:
```bash
# 1. Check service health manually
curl -v http://taskservice:2235/health  # Run FROM test container
curl -v http://req-router:8888/health

# 2. Increase timeout in pytest
export PYTEST_ARGS="--timeout=120 unit/"

# 3. Check for resource constraints
docker stats --no-stream
```

## Migration from Original Test Suite

### What Stays the Same

✅ Test code (unit/, integration/, e2e/)
✅ Test utilities (utils/)
✅ Fixtures (conftest.py)
✅ Test data factories
✅ Assertions

### What Changes for Jenkins

✅ Docker Compose file (uses external network)
✅ Environment variables (service names not localhost)
✅ Jenkinsfile (production-ready)
✅ Health checks (service-name aware)

### No Code Changes Needed

Your tests work **as-is** because:
- API clients use environment variables for URLs
- Tests are parameterized via fixtures
- Service discovery is configuration-based

## Recommended Rollout

### Phase 1: Validation (Week 1)
```bash
# Local validation
cd tests
./ci/wait-for-services-jenkins.sh  # Should pass
docker-compose -f docker-compose-jenkins.yml run --rm test-runner pytest unit/ -v
```

### Phase 2: Jenkins Setup (Week 1)
- Configure credentials
- Create pipeline
- Run unit tests

### Phase 3: Integration Tests (Week 2)
- Enable integration tests
- Monitor stability
- Tune timeouts if needed

### Phase 4: Automation (Week 3)
- Add to PR workflow
- Setup nightly full suite
- Configure notifications

## Performance Expectations

| Test Suite | Time | Services Required |
|------------|------|-------------------|
| Unit only | 2-5 min | None (mocked) |
| Integration | 10-15 min | All running |
| E2E | 20-30 min | All running |
| Full + Coverage | 30-45 min | All running |

## Comparison: Before vs After

### Before (Original Test Suite)
```yaml
# docker-compose-test.yml
networks:
  test_network:  # New isolated network
    driver: bridge

services:
  taskservice:
    image: taskservice:test
    build: ../taskservice  # Builds from scratch
    ports:
      - "2235:2235"  # Exposed to host
```

### After (Jenkins-Ready)
```yaml
# docker-compose-jenkins.yml
networks:
  saaslocalnetwork:
    external: true  # Uses YOUR network

services:
  test-runner:  # Only test runner, uses existing services
    networks:
      - saaslocalnetwork
    environment:
      - DAGKNOWS_TASKSERVICE_URL=http://taskservice:2235  # Service name
```

**Benefits:**
- ✅ No service building
- ✅ No port conflicts
- ✅ Uses production configuration
- ✅ Tests real service communication
- ✅ Respects encryption

## Summary

### You Now Have

1. ✅ **Jenkins-ready test suite** that works with your infrastructure
2. ✅ **3 deployment strategies** (in-network, isolated, hybrid)
3. ✅ **Production Jenkinsfile** with parameters and reporting
4. ✅ **Service-aware health checks** using Docker names
5. ✅ **Comprehensive documentation** for setup and troubleshooting

### No Breaking Changes

- ✅ Original test suite still works for local development
- ✅ Tests themselves unchanged
- ✅ Can use both setups in parallel

### Next Action

**Start with this:**
```bash
cd tests
# Configure credentials as environment variables
export APP_SECRET_KEY="..."
export POSTGRESQL_DB_PASSWORD="..."

# Test unit tests
docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
    pytest unit/ -v -x

# If pass, setup in Jenkins!
```

## Documentation Files

- **`JENKINS_INTEGRATION.md`**: Detailed options and strategies (3 approaches)
- **`JENKINS_SETUP_GUIDE.md`**: Quick start guide (5 steps)
- **`JENKINS_ADDITIONS_SUMMARY.md`**: This file (overview)

**You're ready to integrate tests with your Jenkins/AWS infrastructure! 🚀**

