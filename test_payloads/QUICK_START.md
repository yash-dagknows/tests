# Quick Start Guide - Alert Handling Mode Tests

Get started testing alert handling modes in **under 2 minutes**! ⚡

## 🚀 **Setup**

### **Quick Setup** (scripts have hardcoded credentials for dev.dagknows.com)

The scripts are **pre-configured** with:
- URL: `https://dev.dagknows.com`
- Bearer token: Already hardcoded

**Just run them!** No configuration needed for dev.dagknows.com.

### **Custom Setup** (for other deployments)

To test against a different deployment, set environment variables:

```bash
export DAGKNOWS_URL="https://your-deployment.com"
export DAGKNOWS_TOKEN="your-bearer-token"
```

Or create a `.env` file:
```bash
cd tests/test_payloads
cp env.template .env
# Edit .env with your URL and token
```

---

## 📋 **Prerequisites**

### **Create Tasks in UI First**

Before running tests, create these tasks through the UI:

#### **1. For Deterministic Mode Test**
Create a task with:
- **Title**: "CPU Alert Handler" (or any name)
- **Script**: Any command or Python script
- **Trigger Configuration**:
  ```json
  {
    "source": "Grafana",
    "alert_name": "HighCPUUsage",
    "dedup_interval": 300
  }
  ```

#### **2. For AI-Selected Mode Test**
Create a tooltask with:
- **Title**: "CPU Performance Investigation"
- **Description**: "Investigate high CPU usage, analyze processes, check load average..."
- **Tags**: `cpu`, `performance`
- **NO trigger configuration needed** (AI finds it by similarity)
- **Set mode**: Go to UI → Settings → Alert Handling Mode → `ai_selected`

#### **3. For Autonomous Mode Test**
- No task needed! AI creates investigation tasks automatically
- Requires AI/LLM to be configured
- **Set mode**: Go to UI → Settings → Alert Handling Mode → `autonomous`

---

## ✅ **Run Tests**

### **Test One Mode**

```bash
cd tests/test_payloads

# Test deterministic mode
./test_deterministic_mode.sh

# Test AI-selected mode
./test_ai_selected_mode.sh

# Test autonomous mode
./test_autonomous_mode.sh
```

Each script will:
1. Show prerequisites
2. Wait for you to press Enter
3. Send alert and verify response

### **Test All Modes**

```bash
./test_all_modes.sh
```

**Expected output:**
```
╔════════════════════════════════════════════════════════════════════╗
║         DagKnows Alert Handling Modes - Complete Test Suite       ║
╚════════════════════════════════════════════════════════════════════╝

Target: https://dev.dagknows.com

═══════════════════════════════════════════════════════════════════
  TEST 1/3: DETERMINISTIC MODE
═══════════════════════════════════════════════════════════════════
✅ SUCCESS: Deterministic mode works!
```

---

## 🎯 **Manual Testing**

### **Send Individual Alerts**

```bash
# Send Grafana CPU alert
./send_alert.sh grafana_alert_cpu.json

# Send Grafana memory alert
./send_alert.sh grafana_alert_memory.json

# Send PagerDuty DB incident
./send_alert.sh pagerduty_incident_db.json
```

The response will show `tasks_executed: 1` if a matching task executed.

---

## 📋 **Available Payloads**

| File | Type | Alert Name | Use Case |
|------|------|------------|----------|
| `grafana_alert_cpu.json` | Grafana | `HighCPUUsage` | CPU performance |
| `grafana_alert_memory.json` | Grafana | `HighMemoryUsage` | Memory issues |
| `pagerduty_incident_db.json` | PagerDuty | `Database Connection Failure` | DB outage |
| `pagerduty_incident_service.json` | PagerDuty | `Production Service Down` | Service outage |

---

## 🛠️ **Helper Scripts**

### **Change Alert Handling Mode**

Set via UI: **Settings → Alert Handling Mode**
- `deterministic` - Pre-configured tasks execute
- `ai_selected` - AI finds similar tasks
- `autonomous` - AI launches full investigation

Or use the helper script:
```bash
./set_mode.sh deterministic
./set_mode.sh ai_selected
./set_mode.sh autonomous
```

### **Send Individual Alerts**

```bash
./send_alert.sh grafana_alert_cpu.json
./send_alert.sh pagerduty_incident_db.json
./send_alert.sh grafana_alert_memory.json
```

---

## 🔍 **Troubleshooting**

### **❌ "Task was not triggered"**

**Check:**
1. **Mode is set correctly** via UI:
   - Settings → Alert Handling Mode → `deterministic` (or appropriate mode)

2. **Alert source matches task config exactly**:
   - Grafana alerts → `source: "Grafana"` (capital G)
   - PagerDuty → `source: "Pagerduty"` (capital P, lowercase d)

3. **Alert name matches exactly** (case-sensitive):
   ```json
   // In task config
   "alert_name": "HighCPUUsage"
   
   // In alert payload
   "labels": {"alertname": "HighCPUUsage"}
   ```

4. **Task exists and has trigger configured**:
   - Check task in UI has `trigger_on_alerts` properly configured

---

## 📊 **Example: Complete Test Flow**

```bash
# 1. Create task in UI with trigger:
#    source: "Grafana"
#    alert_name: "HighCPUUsage"

# 2. Set mode in UI:
#    Settings → Alert Handling Mode → deterministic

# 3. Run deterministic test
cd tests/test_payloads
./test_deterministic_mode.sh
# Press Enter when prompted
# Output: Tasks Executed: 1 ✅

# 4. Test all modes (set mode in UI before each test)
./test_all_modes.sh

# 5. Or send individual alerts
./send_alert.sh grafana_alert_cpu.json
```

---

## 💡 **Tips**

1. **Start with deterministic mode** - most reliable and easiest to test
2. **Use unique alert names** - include timestamps to avoid conflicts
3. **Check logs** - response will show if tasks were executed
4. **Cleanup** - test scripts automatically clean up created tasks
5. **AI modes require configuration** - ensure OpenAI or similar is configured

---

## 🎓 **Next Steps**

- Read full documentation: `README.md`
- Integrate into test suite: see parent directory tests
- Create custom payloads: copy and modify JSON files
- Add to CI/CD: use these scripts in your pipeline

---

**Questions?** Check the main [README.md](./README.md) for detailed documentation.

**Ready to test?** Run: `./test_all_modes.sh` 🚀

