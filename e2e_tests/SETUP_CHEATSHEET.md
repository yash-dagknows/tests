# 🚀 E2E Tests - Setup Cheatsheet

---

## 📦 **Dev.dagknows.com** (2 minutes)

```bash
cd tests/e2e_tests
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
./setup.sh
cp env.template .env
./run_ai_agent_test.sh --headed
```

**✅ All credentials pre-configured!**

---

## 🏠 **Localhost** (5 minutes)

```bash
# 1. Start local app
cd app_docker_compose_build_deploy
docker-compose -f local-docker-c-backup-bfr-reorder.yml up -d

# 2. Get JWT token
# - Open http://localhost in browser
# - Login: yash+user@dagknows.com / 1Hey2Yash*
# - F12 → Application → Local Storage → Copy 'authToken'

# 3. Setup tests
cd ../tests/e2e_tests
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp env.template .env

# 4. Edit .env:
# DAGKNOWS_URL=http://localhost
# DAGKNOWS_PROXY=?proxy=yashlocal
# DAGKNOWS_TOKEN=<paste-token-here>

# 5. Run
./run_ai_agent_test.sh --local --headed
```

---

## 🎯 **Test Credentials**

```
Email:    yash+user@dagknows.com
Password: 1Hey2Yash*
Org:      dagknows
```

---

## 📊 **Configuration**

| Setting | Dev | Local |
|---------|-----|-------|
| URL | `https://dev.dagknows.com` | `http://localhost` |
| Proxy | `?proxy=dev1` | `?proxy=yashlocal` |
| Token | Pre-configured ✅ | Get from browser |

---

## 🎬 **Common Commands**

```bash
# Run with browser visible
./run_ai_agent_test.sh --headed

# Run against local
./run_ai_agent_test.sh --local --headed

# Run all tests
pytest -v

# Run specific test
pytest ui_tests/test_ai_agent_workflow.py -v
```

---

## 📸 **Results**

```bash
# Screenshots
ls reports/screenshots/

# HTML report
open reports/ai_agent_test_report.html
```

---

**That's it!** 🎉

