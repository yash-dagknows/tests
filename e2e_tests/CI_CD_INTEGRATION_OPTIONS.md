# E2E Tests CI/CD Integration Options

This document outlines different options for integrating the E2E test suite (API and UI tests) into the DagKnows CI/CD pipeline.

## Current CI/CD Architecture

- **Jenkins** as CI/CD orchestrator
- **AWS CodeBuild** for building Docker images
- **ECR Public** for image storage
- **Service-specific pipelines** in `{service}/ci/*.groovy`
- **Terraform-managed Jenkins** in `terraform-jenkins/ecs/`
- **Jenkins agents** with Docker support

---

## Integration Options

### **Option 1: Dedicated E2E Test Pipeline (Recommended)**

**Approach:** Create a standalone Jenkins pipeline that runs E2E tests independently, triggered by:
- Manual execution
- Scheduled runs (nightly, weekly)
- Post-deployment webhooks
- Git webhooks (on merge to main)

**Implementation:**
```
tests/e2e_tests/ci/e2e-tests-pipeline.groovy
```

**Pros:**
- ✅ Clean separation of concerns
- ✅ Can run independently of service deployments
- ✅ Easy to schedule (nightly smoke tests)
- ✅ Can test against multiple environments (dev, staging)
- ✅ Doesn't slow down service build/deploy pipelines
- ✅ Can run in parallel with other pipelines

**Cons:**
- ❌ Requires manual trigger or separate automation
- ❌ May test against stale deployments

**Best For:**
- Comprehensive test coverage
- Scheduled regression testing
- Multi-environment validation

---

### **Option 2: Post-Deployment E2E Tests**

**Approach:** Add E2E test stage to existing service pipelines (e.g., `taskservice-image-push-cb.groovy`) that runs after successful deployment.

**Implementation:**
Add stage to existing pipelines:
```groovy
stage('E2E Tests') {
    steps {
        // Run E2E tests against deployed service
    }
}
```

**Pros:**
- ✅ Tests run automatically after deployment
- ✅ Validates that deployment actually works
- ✅ Immediate feedback on deployment quality
- ✅ Catches integration issues early

**Cons:**
- ❌ Slows down deployment pipeline
- ❌ May fail due to transient issues (not deployment problems)
- ❌ Requires test environment to be stable
- ❌ All services would need this (duplication)

**Best For:**
- Critical service deployments
- Production deployments
- Services with high change frequency

---

### **Option 3: Pre-Merge E2E Tests (PR Validation)**

**Approach:** Run E2E tests as part of PR validation, before code is merged.

**Implementation:**
- GitHub Actions / GitLab CI
- Jenkins Multibranch Pipeline
- Pre-commit hooks (lightweight tests only)

**Pros:**
- ✅ Prevents broken code from being merged
- ✅ Early feedback to developers
- ✅ Reduces main branch failures

**Cons:**
- ❌ Requires PR-based workflow
- ❌ May be too slow for quick iterations
- ❌ Needs test environment for PRs

**Best For:**
- Teams using PR-based workflow
- Preventing regressions
- Code quality gates

---

### **Option 4: AWS CodeBuild Integration**

**Approach:** Use AWS CodeBuild (like image builds) to run E2E tests in a dedicated build project.

**Implementation:**
```
tests/e2e_tests/ci/buildspec_e2e_tests.yaml
```

**Pros:**
- ✅ Consistent with existing build infrastructure
- ✅ Scalable (CodeBuild handles parallelism)
- ✅ Can use same IAM roles/permissions
- ✅ Easy to configure different environments
- ✅ Built-in artifact storage

**Cons:**
- ❌ Requires CodeBuild project setup
- ❌ Additional AWS costs
- ❌ Less flexible than Jenkins for complex workflows

**Best For:**
- Teams already using CodeBuild extensively
- Need for scalable test execution
- Integration with AWS services

---

### **Option 5: Hybrid Approach (Recommended for Production)**

**Approach:** Combine multiple options:
1. **Lightweight API tests** in post-deployment (fast feedback)
2. **Full E2E suite** in dedicated scheduled pipeline (comprehensive)
3. **Critical path tests** in pre-merge (prevent regressions)

**Implementation:**
- Fast API tests: Run after each deployment (5-10 min)
- Full suite: Run nightly or on-demand (30-60 min)
- Critical tests: Run on PR (smoke tests only)

**Pros:**
- ✅ Best of all worlds
- ✅ Fast feedback + comprehensive coverage
- ✅ Flexible and adaptable

**Cons:**
- ❌ More complex to set up and maintain
- ❌ Requires test categorization (fast vs. slow)

**Best For:**
- Production environments
- Large teams
- Critical applications

---

## Recommended Implementation Plan

### **Phase 1: Dedicated E2E Pipeline (Quick Win)**

1. Create `tests/e2e_tests/ci/e2e-tests-pipeline.groovy`
2. Set up test environment configuration
3. Enable manual and scheduled execution
4. Integrate with Jenkins agents

**Timeline:** 1-2 days

### **Phase 2: Post-Deployment Integration**

1. Add E2E test stage to critical service pipelines
2. Start with API tests only (faster)
3. Add UI tests for critical paths
4. Configure failure handling (warn vs. fail)

**Timeline:** 2-3 days

### **Phase 3: Optimization**

1. Categorize tests (fast vs. slow)
2. Implement parallel test execution
3. Add test result reporting/dashboards
4. Set up notifications (Slack, email)

**Timeline:** 3-5 days

---

## Technical Considerations

### **Test Environment Requirements**

- **Target Environment:** `dev.dagknows.com` or dedicated test environment
- **JWT Token:** Stored in Jenkins credentials or AWS Secrets Manager
- **Test Data:** Isolated test data or cleanup after tests
- **Browser:** Playwright browsers installed on Jenkins agent
- **Network:** Access to test environment from Jenkins

### **Infrastructure Needs**

1. **Jenkins Agent:**
   - Docker support (for containerized tests)
   - Python 3.10+
   - Node.js (for Playwright)
   - Sufficient memory (UI tests need ~2GB)

2. **Test Execution:**
   - Parallel execution for speed
   - Artifact collection (screenshots, reports)
   - Test result reporting (JUnit XML, HTML)

3. **Configuration:**
   - Environment variables (URLs, tokens)
   - Test user credentials
   - Proxy settings

### **Failure Handling**

- **Non-blocking:** E2E tests fail but don't block deployment (warnings)
- **Blocking:** Critical E2E tests must pass (failures block deployment)
- **Retry logic:** Automatic retry for flaky tests
- **Notifications:** Alert on test failures

---

## Example Pipeline Structure

### **Dedicated E2E Pipeline**

```groovy
pipeline {
    agent {
        node {
            label 'docker'  // or 'e2e-tests' dedicated agent
        }
    }
    
    environment {
        TEST_ENV = 'dev'
        DAGKNOWS_URL = 'https://dev.dagknows.com'
        DAGKNOWS_PROXY = '?proxy=dev1'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout dagknows_src repo
            }
        }
        
        stage('Setup') {
            steps {
                dir('tests/e2e_tests') {
                    sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install -r requirements.txt
                        playwright install chromium
                    '''
                }
            }
        }
        
        stage('API Tests') {
            steps {
                dir('tests/e2e_tests') {
                    sh '''
                        source venv/bin/activate
                        pytest api_tests/ -v --html=reports/api-report.html
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'tests/e2e_tests/reports/**/*'
                }
            }
        }
        
        stage('UI Tests') {
            steps {
                dir('tests/e2e_tests') {
                    sh '''
                        source venv/bin/activate
                        pytest ui_tests/ -v --html=reports/ui-report.html
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'tests/e2e_tests/reports/**/*'
                }
            }
        }
    }
    
    post {
        always {
            junit 'tests/e2e_tests/reports/junit.xml'
            publishHTML([
                reportDir: 'tests/e2e_tests/reports',
                reportFiles: 'api-report.html,ui-report.html',
                reportName: 'E2E Test Report'
            ])
        }
    }
}
```

---

## Next Steps

1. **Choose integration approach** based on team needs
2. **Set up test environment** (if not using dev.dagknows.com)
3. **Create Jenkins pipeline** file
4. **Configure Jenkins job** in Jenkins UI
5. **Test pipeline execution**
6. **Add to service pipelines** (if using Option 2)

---

## Questions to Consider

1. **When should tests run?**
   - After deployment? Before merge? Scheduled?

2. **What happens on failure?**
   - Block deployment? Send alerts? Just log?

3. **Which tests to run?**
   - All tests? Critical path only? Fast tests first?

4. **Test environment?**
   - Use dev.dagknows.com? Dedicated test environment?

5. **Resource requirements?**
   - Dedicated Jenkins agent? Shared agent? Container?

