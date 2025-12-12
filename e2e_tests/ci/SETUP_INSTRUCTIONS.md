# E2E Tests Pipeline Setup Instructions

## Quick Setup Guide

### Step 1: Verify Docker Agent Available

The pipeline uses the existing **Docker agent** (label: `docker`). No additional agent setup is required.

**Requirements for Docker agent:**
- Python 3.10+ installed
- Git installed
- Network access to GitHub and dev.dagknows.com

The pipeline will automatically:
- Create a Python virtual environment
- Install all dependencies (API + UI test packages)
- Install Playwright browsers
- Run tests

**No agent image build needed!** ✅

### Step 2: Create Jenkins Pipeline Job

1. **Jenkins UI:**
   - New Item → Pipeline
   - **Name:** `e2e-tests-pipeline`
   - **Description:** E2E API Tests for DagKnows

2. **Pipeline Configuration:**
   - **Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** `https://github.com/yash-dagknows/tests.git`
   - **Credentials:** Select `yash-dagknows-github-pat`
   - **Branches to build:** `*/main` (or your branch)
   - **Script Path:** `e2e_tests/ci/e2e-tests-pipeline.groovy`

3. **Configure Pipeline Parameters:**
   
   In the Jenkins job configuration page, check the box **"This project is parameterized"** (under "General" section).
   
   Then click **"Add Parameter"** and add the following parameters in order:

   **Parameter 1: TEST_ENV (Choice Parameter)**
   - Click "Add Parameter" → Select **"Choice Parameter"**
   - **Name:** `TEST_ENV`
   - **Choices:** (one per line)
     ```
     dev
     staging
     prod
     ```
   - **Description:** `Target environment for E2E tests`
   - **Default Value:** `dev`

   **Parameter 2: DAGKNOWS_URL (String Parameter)**
   - Click "Add Parameter" → Select **"String Parameter"**
   - **Name:** `DAGKNOWS_URL`
   - **Default Value:** `https://dev.dagknows.com`
   - **Description:** `Base URL for DagKnows application`

   **Parameter 3: DAGKNOWS_PROXY (String Parameter)**
   - Click "Add Parameter" → Select **"String Parameter"**
   - **Name:** `DAGKNOWS_PROXY`
   - **Default Value:** `?proxy=dev1`
   - **Description:** `Proxy parameter for requests`

   **Parameter 4: TEST_MARKERS (String Parameter)**
   - Click "Add Parameter" → Select **"String Parameter"**
   - **Name:** `TEST_MARKERS`
   - **Default Value:** `api`
   - **Description:** `Pytest markers to filter tests (e.g., "api and not slow")`

   **Parameter 5: BRANCH (String Parameter)**
   - Click "Add Parameter" → Select **"String Parameter"**
   - **Name:** `BRANCH`
   - **Default Value:** `main`
   - **Description:** `Git branch to checkout`

4. **Save the job**

### Step 3: Add GitHub Project (Optional but Recommended)

If you want to link the Jenkins job to the GitHub repository:

1. In the Jenkins job configuration, scroll to **"GitHub project"** section
2. Check the box **"GitHub project"**
3. **Project url:** `https://github.com/yash-dagknows/tests.git`
4. This enables GitHub integration features like viewing commits, pull requests, etc.

### Step 4: Configure Credentials

1. **JWT Token:**
   - Manage Jenkins → Credentials → Add Credentials
   - **Type:** Secret text
   - **ID:** `dagknows-jwt-token`
   - **Secret:** Your JWT token from dev.dagknows.com
   - **Description:** JWT token for DagKnows API authentication

2. **Git Token (if not already configured):**
   - **ID:** `yash-dagknows-github-pat`
   - **Type:** Username with password
   - **Username:** Your GitHub username
   - **Password:** Your GitHub personal access token

### Step 5: Test the Pipeline

1. **Manual Run:**
   - Go to the pipeline job
   - Click "Build with Parameters"
   - Set parameters:
     - TEST_ENV: `dev`
     - DAGKNOWS_URL: `https://dev.dagknows.com`
     - DAGKNOWS_PROXY: `?proxy=dev1`
     - TEST_MARKERS: `api`
     - BRANCH: `main`
   - Click "Build"

2. **Check Build Log:**
   - Monitor the build progress
   - Check for any errors
   - Review test results in the build artifacts

### Step 6: Schedule Regular Runs (Optional)

1. **In Jenkins job configuration:**
   - Build Triggers → Build periodically
   - Schedule: `H 2 * * *` (runs daily at 2 AM)
   - Or: `H */6 * * *` (runs every 6 hours)

## Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| TEST_ENV | `dev` | Target environment (dev/staging/prod) |
| DAGKNOWS_URL | `https://dev.dagknows.com` | Base URL for DagKnows |
| DAGKNOWS_PROXY | `?proxy=dev1` | Proxy parameter |
| TEST_MARKERS | `api` | Pytest markers to filter tests |
| BRANCH | `main` | Git branch to checkout |

## Expected Test Execution Time

- **API Tests (all):** ~5-10 minutes
- **API Tests (fast only):** ~2-3 minutes

## Artifacts Generated

After each run, the following artifacts are available:

- `reports/api-report.html` - HTML test report
- `reports/api-junit.xml` - JUnit XML for Jenkins integration
- Test results visible in Jenkins Test Result Trend

## Troubleshooting

### Issue: Agent not found
**Solution:** Ensure Docker agent with label `docker` exists and is online

### Issue: Git checkout fails
**Solution:** Verify Git credentials are configured correctly

### Issue: JWT token invalid
**Solution:** Update JWT token in Jenkins credentials (tokens expire after 24 hours)

### Issue: Tests fail with connection errors
**Solution:** Verify agent can reach `dev.dagknows.com` from network

### Issue: Python dependencies not found
**Solution:** Pipeline creates venv and installs dependencies - check build logs for pip install errors. Ensure Docker agent has Python 3.10+ and pip installed.

### Issue: Virtual environment creation fails
**Solution:** Ensure Docker agent has `python3-venv` package installed. On Ubuntu/Debian: `apt-get install python3-venv`

## Next Steps

Once API tests are working:
1. ✅ Verify all API tests pass
2. ✅ Set up scheduled runs
3. ✅ Configure notifications (Slack/email)
4. 🔄 Add UI tests later (will require Playwright in agent)

## Support

For issues or questions:
- Check pipeline build logs
- Review `README_AGENT_SETUP.md` for agent configuration
- See `CI_CD_QUICK_START.md` for general CI/CD guidance

