# E2E Tests CI/CD Integration - Quick Start

## 📋 Summary of Options

| Option | Best For | Effort | Timeline |
|--------|----------|--------|----------|
| **Option 1: Dedicated Pipeline** | Comprehensive testing, scheduled runs | Low | 1-2 days |
| **Option 2: Post-Deployment** | Immediate feedback after deploy | Medium | 2-3 days |
| **Option 3: Pre-Merge** | Prevent broken code in main | Medium | 2-3 days |
| **Option 4: CodeBuild** | Scalable, AWS-native | Medium | 3-4 days |
| **Option 5: Hybrid** | Production-grade setup | High | 5-7 days |

## 🚀 Recommended: Start with Option 1

### Step 1: Create Jenkins Job

1. **Jenkins UI:**
   - New Item → Pipeline
   - Name: `e2e-tests-pipeline`
   - Pipeline script from SCM: Git
   - Repository: `https://github.com/dagknows/tests.git`
   - Script Path: `e2e_tests/ci/e2e-tests-pipeline.groovy`

2. **Configure Credentials:**
   - Add JWT token as Jenkins credential:
     - ID: `dagknows-jwt-token`
     - Type: Secret text
     - Value: Your JWT token from dev.dagknows.com

3. **Set Parameters:**
   - TEST_ENV: `dev`
   - DAGKNOWS_URL: `https://dev.dagknows.com`
   - DAGKNOWS_PROXY: `?proxy=dev1`

### Step 2: Test Execution

**Manual Run:**
```bash
# In Jenkins UI, click "Build with Parameters"
# Select options and click "Build"
```

**Scheduled Run:**
- In Jenkins job configuration → Build Triggers
- Check "Build periodically"
- Schedule: `H 2 * * *` (runs daily at 2 AM)

### Step 3: View Results

- **HTML Reports:** Available in Jenkins build artifacts
- **JUnit XML:** Integrated with Jenkins test results
- **Screenshots:** Archived for UI test failures

---

## 🔧 Option 2: Add to Service Pipeline

### Example: Add to taskservice pipeline

Edit `taskservice/ci/taskservice-image-push-cb.groovy`:

```groovy
stage('E2E Tests') {
    steps {
        script {
            def e2eTestScript = load 'tests/e2e_tests/ci/e2e-tests-post-deployment.groovy'
            e2eTestScript.runE2ETests([
                serviceName: 'taskservice',
                testEnv: 'dev',
                testTypes: ['api'],  // Fast API tests only
                failOnError: false   // Don't block deployment
            ])
        }
    }
}
```

**Placement:** Add after `stage('Build')` and before `post` block.

---

## 📊 Test Execution Times

| Test Suite | Duration | When to Run |
|------------|----------|-------------|
| API Tests (all) | ~5-10 min | Post-deployment, scheduled |
| UI Tests (all) | ~20-30 min | Scheduled, on-demand |
| API Tests (fast) | ~2-3 min | Post-deployment, pre-merge |
| UI Tests (smoke) | ~5-10 min | Post-deployment |

---

## 🎯 Test Markers

Use pytest markers to filter tests:

```bash
# Run only fast API tests
pytest api_tests/ -m "api and not slow"

# Run only critical UI tests
pytest ui_tests/ -m "ui and smoke"

# Run all API tests
pytest api_tests/ -m "api"

# Run all UI tests
pytest ui_tests/ -m "ui"
```

---

## 🔐 Security Considerations

1. **JWT Token Storage:**
   - ✅ Use Jenkins credentials (encrypted)
   - ✅ Or AWS Secrets Manager
   - ❌ Never hardcode in pipeline

2. **Test User Credentials:**
   - Use dedicated test users
   - Rotate credentials regularly
   - Store in Jenkins credentials

3. **Environment Access:**
   - Limit test environment access
   - Use read-only test users where possible
   - Clean up test data after runs

---

## 📈 Monitoring & Alerts

### Jenkins Notifications

Add to pipeline `post` block:

```groovy
post {
    failure {
        emailext (
            subject: "E2E Tests Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: "E2E tests failed. Check: ${env.BUILD_URL}",
            to: "team@dagknows.com"
        )
    }
}
```

### Slack Integration

```groovy
post {
    failure {
        slackSend(
            channel: '#ci-cd',
            color: 'danger',
            message: "E2E Tests Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues

1. **Playwright browsers not found:**
   ```bash
   playwright install chromium
   playwright install-deps chromium
   ```

2. **JWT token expired:**
   - Update token in Jenkins credentials
   - Tokens typically expire after 24 hours

3. **Tests timeout:**
   - Increase timeout in `pytest.ini`
   - Check network connectivity to test environment

4. **UI tests fail in headless mode:**
   - Ensure Xvfb is running
   - Check DISPLAY environment variable

---

## 📝 Next Steps

1. ✅ Review `CI_CD_INTEGRATION_OPTIONS.md` for detailed options
2. ✅ Choose integration approach
3. ✅ Set up Jenkins job using `e2e-tests-pipeline.groovy`
4. ✅ Configure credentials and environment
5. ✅ Run first test execution
6. ✅ Review results and adjust as needed
7. ✅ Add to service pipelines (if using Option 2)
8. ✅ Set up notifications and monitoring

---

## 📞 Support

For questions or issues:
- Check `README.md` for test setup
- Review `QUICK_START.md` for test execution
- See `TROUBLESHOOTING.md` for common issues

