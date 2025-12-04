# Jenkins Setup Guide - Quick Start

## Problem Solved

Your existing `dkapp/docker-compose.yml` setup uses:
- ✅ External network `saaslocalnetwork` (not localhost)
- ✅ Service-to-service communication via Docker names
- ✅ Encryption with `APP_SECRET_KEY`
- ✅ TLS certificates
- ✅ Complex service dependencies

The test suite has been **adapted to work with this infrastructure**.

## Files Created for Jenkins

1. **`docker-compose-jenkins.yml`** - Connects to your existing network
2. **`Jenkinsfile.production`** - Full Jenkins pipeline
3. **`ci/wait-for-services-jenkins.sh`** - Health checks using service names
4. **`JENKINS_INTEGRATION.md`** - Detailed options and strategies

## Quick Setup (5 Steps)

### Step 1: Configure Jenkins Credentials

In Jenkins, add these credentials:

```
1. dagknows-app-secret-key     → Type: Secret text → Value: <your APP_SECRET_KEY>
2. dagknows-postgres-password  → Type: Secret text → Value: <your DB password>
3. dagknows-api-key           → Type: Secret text → Value: <your api_key>
```

### Step 2: Ensure Services Are Running

Your services should already be running via `dkapp/docker-compose.yml`:

```bash
# Check services are running
cd dkapp
docker-compose ps

# Verify network exists
docker network ls | grep saaslocalnetwork
```

### Step 3: Create Jenkins Pipeline

In Jenkins:
1. New Item → Pipeline
2. Name: `dagknows-tests`
3. Pipeline script from SCM
4. Repository: `<your-repo>`
5. Script Path: `tests/Jenkinsfile.production`

### Step 4: Test Locally First (Optional)

Before running in Jenkins, test locally:

```bash
cd tests

# Export your credentials
export APP_SECRET_KEY="your-secret"
export POSTGRESQL_DB_PASSWORD="your-password"
export api_key="your-api-key"

# Run unit tests (fast, no services)
docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
    pytest unit/ -v

# Run integration tests (requires services)
docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
    pytest integration/ -v

# Cleanup
docker-compose -f docker-compose-jenkins.yml down
```

### Step 5: Run in Jenkins

Trigger the pipeline with parameters:
- **TEST_SUITE**: `unit` (start with this)
- **RUN_COVERAGE**: `true`
- **STOP_ON_FAILURE**: `false`

## How It Works

### Architecture

```
┌─────────────────────────────────────────┐
│         Jenkins Agent (ECS)             │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │     Test Container                │ │
│  │  (on saaslocalnetwork)            │ │
│  │                                   │ │
│  │  ┌─────────┐                     │ │
│  │  │ pytest  │────────┐            │ │
│  │  └─────────┘        │            │ │
│  └──────────────────────┼────────────┘ │
│                         │              │
└─────────────────────────┼──────────────┘
                          │
          ┌───────────────┼───────────────┐
          │  saaslocalnetwork             │
          │                               │
          │  ┌──────────────┐            │
          │  │ taskservice  │◄───────────┼─── Tests use
          │  │  :2235       │            │    service names
          │  └──────────────┘            │    NOT localhost!
          │                               │
          │  ┌──────────────┐            │
          │  │ req-router   │◄───────────┤
          │  │  :8888       │            │
          │  └──────────────┘            │
          │                               │
          │  ┌──────────────┐            │
          │  │ postgres     │◄───────────┤
          │  │  :5432       │            │
          │  └──────────────┘            │
          │                               │
          │  ┌──────────────┐            │
          │  │elasticsearch │◄───────────┤
          │  │  :9200       │            │
          │  └──────────────┘            │
          └───────────────────────────────┘
```

### Key Differences from Localhost Setup

| Aspect | Localhost | Jenkins/Docker |
|--------|-----------|----------------|
| Service URL | `http://localhost:2235` | `http://taskservice:2235` |
| Network | Host network | `saaslocalnetwork` |
| Elasticsearch | `localhost:9200` | `elasticsearch:9200` |
| Database | `localhost:5432` | `postgres:5432` |
| Authentication | Optional | Uses `APP_SECRET_KEY` |

## Testing Strategies

### Strategy 1: Fast Feedback (Recommended for PRs)

```groovy
// Only run unit tests on feature branches
when {
    not { branch 'main' }
}
stages {
    stage('Unit Tests') {
        steps {
            sh 'cd tests && pytest unit/ -v'
        }
    }
}
```

**Result**: Tests run in < 5 minutes, no services needed

### Strategy 2: Full Suite (Recommended for main/master)

```groovy
// Run all tests on main branch
when {
    branch 'main'
}
stages {
    stage('All Tests') {
        steps {
            sh '''
                cd tests
                docker-compose -f docker-compose-jenkins.yml run --rm test-runner
            '''
        }
    }
}
```

**Result**: Complete test coverage in ~20-30 minutes

### Strategy 3: Nightly Full Regression

```groovy
// Schedule full test suite nightly
triggers {
    cron('H 2 * * *')  // 2 AM every day
}
parameters {
    choice(name: 'TEST_SUITE', choices: ['all'])
    booleanParam(name: 'RUN_COVERAGE', defaultValue: true)
}
```

**Result**: Comprehensive testing without blocking development

## Troubleshooting

### Issue: "Connection refused" errors

**Cause**: Tests trying to use localhost instead of service names

**Fix**: Ensure environment variables use service names:
```bash
DAGKNOWS_TASKSERVICE_URL=http://taskservice:2235  # ✓ Correct
DAGKNOWS_TASKSERVICE_URL=http://localhost:2235     # ✗ Wrong
```

### Issue: "Network saaslocalnetwork not found"

**Cause**: Services not running or network not created

**Fix**:
```bash
# Create network if missing
docker network create saaslocalnetwork

# Or start services
cd dkapp && docker-compose up -d
```

### Issue: "Authentication failed"

**Cause**: Missing APP_SECRET_KEY or api_key

**Fix**: 
1. Check Jenkins credentials are configured
2. Verify environment variables in pipeline:
```groovy
environment {
    APP_SECRET_KEY = credentials('dagknows-app-secret-key')
}
```

### Issue: "Service not healthy"

**Cause**: Services not running or not ready

**Fix**:
```bash
# Check service health
docker ps --filter "network=saaslocalnetwork"

# Check specific service
docker logs taskservice --tail 50
docker logs req-router --tail 50

# Restart services if needed
cd dkapp && docker-compose restart
```

### Issue: Tests hang waiting for services

**Cause**: Firewall or network isolation

**Fix**: Ensure test container is on the same network:
```yaml
# In docker-compose-jenkins.yml
networks:
  saaslocalnetwork:
    external: true  # Must be external!
```

## Phased Rollout Plan

### Week 1: Setup & Validation
- [ ] Configure Jenkins credentials
- [ ] Create Jenkins pipeline
- [ ] Run unit tests successfully
- [ ] Verify results are published

### Week 2: Integration Tests
- [ ] Run integration tests against dev environment
- [ ] Monitor for flaky tests
- [ ] Tune timeout settings if needed
- [ ] Add to PR pipeline

### Week 3: Full Automation
- [ ] Add to main branch pipeline
- [ ] Setup nightly full regression
- [ ] Configure notifications (Slack/Email)
- [ ] Document any custom changes

### Week 4: Optimization
- [ ] Analyze test execution time
- [ ] Implement test parallelization if needed
- [ ] Setup coverage trending
- [ ] Train team on test writing

## Example Pipeline Execution

```
✓ Checkout                          (10s)
✓ Environment Check                 (5s)
✓ Service Health Check             (30s)
✓ Run Tests
    ├─ Unit Tests                   (2m)
    ├─ Integration Tests            (5m)
    └─ E2E Tests                    (10m)
✓ Collect Logs                     (10s)
✓ Publish Results                  (20s)

Total Time: ~18 minutes
```

## Next Steps

1. **Start Simple**: Begin with unit tests only
2. **Validate**: Ensure tests pass in Jenkins environment
3. **Expand**: Add integration tests gradually
4. **Automate**: Enable for all PRs once stable
5. **Monitor**: Track test stability and execution time

## Support

If you encounter issues:

1. Check `JENKINS_INTEGRATION.md` for detailed options
2. Review service logs: `docker logs <service-name>`
3. Verify network connectivity: `docker network inspect saaslocalnetwork`
4. Test locally first before running in Jenkins

## Summary

Your test suite is now **Jenkins-ready** with:
- ✅ Network-aware configuration
- ✅ Service discovery via Docker names
- ✅ Encryption support
- ✅ Production-ready Jenkinsfile
- ✅ Multiple execution strategies
- ✅ Comprehensive documentation

Start with **unit tests**, then gradually enable **integration** and **E2E** tests as confidence grows.

