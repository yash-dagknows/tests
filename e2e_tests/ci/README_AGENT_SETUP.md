# Jenkins E2E Test Agent Setup

This document explains the agent requirements for running E2E tests.

## Agent Approach: Use Existing Docker Agent

The pipeline uses the **existing Docker agent** (label: `docker`). No dedicated agent image is required.

The pipeline automatically:
- Creates a Python virtual environment
- Installs all dependencies from `requirements.txt` (API + UI)
- Installs Playwright browsers
- Runs tests in isolation

## Agent Requirements

### Minimum Requirements
- **Python 3.10+** - Installed on the Docker agent
- **Git** - For repository checkout
- **pip** - For installing Python packages
- **Network access** - To GitHub and dev.dagknows.com

### Optional (for UI tests later)
- **Node.js** - Will be installed via Playwright if needed
- **System libraries** - Playwright install-deps will handle these

### Network Requirements
- Outbound HTTPS access to `dev.dagknows.com` (or configured test environment)
- Access to GitHub for repository checkout
- Access to Jenkins master

## How It Works

1. **Pipeline starts** on Docker agent
2. **Virtual environment created** in `e2e_tests/venv/`
3. **Dependencies installed** from `requirements.txt`:
   - pytest, requests, etc. (API tests)
   - playwright, pytest-playwright (UI tests - ready for later)
4. **Playwright browsers installed** (Chromium)
5. **Tests executed** in the virtual environment

## Verifying Agent Setup

### Test Python Installation

```bash
python3 --version
# Should output: Python 3.10.x or higher
```

### Test Git Installation

```bash
git --version
```

### Test Network Access

```bash
curl -I https://dev.dagknows.com
# Should return HTTP 200 or 302
```

## Troubleshooting

### Issue: Python not found
**Solution:** Ensure Python 3.10+ is installed on the Docker agent

### Issue: pip not found
**Solution:** Install python3-pip on the Docker agent

### Issue: Virtual environment creation fails
**Solution:** Ensure `python3-venv` package is installed on the Docker agent

### Issue: Playwright install fails
**Solution:** The pipeline will continue (Playwright only needed for UI tests). For UI tests, ensure system libraries are available or let Playwright install-deps handle it.

### Issue: Network connectivity
**Solution:** Verify agent can reach:
- GitHub (for checkout)
- dev.dagknows.com (for API tests)
- Jenkins master

## Benefits of This Approach

✅ **No agent image to build/maintain**
✅ **Dependencies isolated in venv** (no conflicts)
✅ **Easy to update** (just update requirements.txt)
✅ **Works with existing infrastructure**
✅ **All dependencies included** (API + UI ready)

## Alternative: Dedicated Agent Image

If you prefer a pre-built agent image for faster execution, see `Dockerfile.e2e-agent` for reference. However, the virtual environment approach is recommended for simplicity and maintainability.
