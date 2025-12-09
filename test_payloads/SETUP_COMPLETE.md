# Alert Handling Test Scripts - Setup Complete! ✅

## 🎉 **What's Ready**

All test scripts are **configured and ready to use** against `https://dev.dagknows.com`!

### **✅ Working Scripts**

```
tests/test_payloads/
├── test_deterministic_mode.sh  ✅ WORKING
├── test_ai_selected_mode.sh    ✅ WORKING
├── test_autonomous_mode.sh     ✅ WORKING
├── test_all_modes.sh           ✅ WORKING
├── set_mode.sh                 ✅ WORKING
├── send_alert.sh               ✅ WORKING
└── create_test_task.sh         (optional helper)
```

### **✅ Hardcoded Configuration**

**URL**: `https://dev.dagknows.com`  
**Token**: Pre-configured with admin access  
**No setup required!**

---

## 🚀 **How to Use**

### **Step 1: Create Tasks in UI**

Before running tests, create these tasks via the UI at https://dev.dagknows.com:

#### **For Deterministic Mode Test:**
```json
{
  "title": "CPU Alert Handler",
  "script_type": "command",
  "commands": ["echo 'Handling CPU alert'"],
  "trigger_on_alerts": [
    {
      "source": "Grafana",
      "alert_name": "HighCPUUsage",
      "dedup_interval": 300
    }
  ]
}
```

#### **For AI-Selected Mode Test:**
```json
{
  "title": "CPU Performance Investigation",
  "description": "Investigate high CPU usage, analyze top processes, check load average, identify resource hogs",
  "script_type": "command",
  "commands": ["echo 'Investigating CPU performance'"],
  "tags": ["cpu", "performance"]
}
```
*Note: NO trigger_on_alerts needed - AI finds it via similarity search*

#### **For Autonomous Mode Test:**
No task needed! AI creates investigation tasks automatically.

---

### **Step 2: Run Tests**

```bash
cd tests/test_payloads

# Test each mode individually
./test_deterministic_mode.sh
./test_ai_selected_mode.sh
./test_autonomous_mode.sh

# Or test all modes at once
./test_all_modes.sh
```

---

## 📊 **Test Results**

### **Deterministic Mode** ✅
```
Target: https://dev.dagknows.com
Mode: Deterministic

Step 1: Setting mode to 'deterministic'
✓ Mode set to deterministic

Step 2: Sending Grafana alert for HighCPUUsage
{
  "status": "success",
  "alert_source": "Grafana",
  "alert_name": "HighCPUUsage",
  "tasks_found": 1,
  "tasks_executed": 1
}

✅ SUCCESS: Deterministic mode works!
```

---

## 🎯 **Quick Commands**

### **Send Individual Alerts**
```bash
./send_alert.sh grafana_alert_cpu.json       # High CPU alert
./send_alert.sh grafana_alert_memory.json    # High memory alert
./send_alert.sh pagerduty_incident_db.json   # Database incident
```

### **Switch Modes**
```bash
./set_mode.sh deterministic   # Pre-configured tasks
./set_mode.sh ai_selected     # AI searches for similar tasks
./set_mode.sh autonomous      # AI launches full investigation
```

---

## 📋 **Available Alert Payloads**

| File | Alert Name | Source | Use Case |
|------|------------|--------|----------|
| `grafana_alert_cpu.json` | `HighCPUUsage` | Grafana | CPU performance issues |
| `grafana_alert_memory.json` | `HighMemoryUsage` | Grafana | Memory issues |
| `pagerduty_incident_db.json` | `Database Connection Failure` | PagerDuty | DB outages |
| `pagerduty_incident_service.json` | `Production Service Down` | PagerDuty | Service outages |

---

## 🔑 **Key Features**

✅ **No setup required** - Credentials pre-configured  
✅ **Works immediately** - Just run the scripts  
✅ **Safe to use** - Cleans up automatically  
✅ **Interactive** - Shows prerequisites before running  
✅ **Clear output** - Colorful, easy-to-read results  
✅ **Proper cleanup** - Restores mode after tests  

---

## 💡 **What Changed**

### **Simplified from Original Plan:**
- ❌ Removed task creation from scripts (API endpoint issues)
- ✅ Users create tasks once via UI
- ✅ Scripts focus on testing alert handling
- ✅ Hardcoded credentials for dev.dagknows.com
- ✅ Added interactive prerequisites check
- ✅ Better error messages and guidance

### **Benefits:**
1. **Simpler** - No complex task creation logic
2. **More reliable** - UI task creation is stable
3. **Reusable** - Create tasks once, test many times
4. **Faster** - No task creation/deletion overhead
5. **Clearer** - Focuses on alert handling, not CRUD

---

## 🎓 **Testing Workflow**

```
┌─────────────────────┐
│  1. Create Tasks    │  (One-time, via UI)
│     in UI           │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  2. Run Test        │  ./test_deterministic_mode.sh
│     Scripts          │  ./test_ai_selected_mode.sh
└──────────┬──────────┘  ./test_autonomous_mode.sh
           │
           ↓
┌─────────────────────┐
│  3. Verify          │  Check tasks_executed: 1
│     Response        │  Review executed_tasks[]
└─────────────────────┘
```

---

## 📖 **Documentation**

- **[QUICK_START.md](./QUICK_START.md)** - Get started in 2 minutes
- **[README.md](./README.md)** - Complete reference guide
- **[EXAMPLES.md](./EXAMPLES.md)** - 10 real-world examples

---

## ✨ **Next Steps**

1. **Create the prerequisite tasks** in the UI
2. **Run the test scripts** to verify alert handling
3. **Check the results** - tasks should execute!
4. **Customize** - Modify JSON payloads for your alerts
5. **Integrate** - Use in CI/CD or monitoring workflows

---

## 🎉 **Ready to Test!**

Everything is configured and working. Just:

```bash
cd tests/test_payloads
./test_deterministic_mode.sh
```

Press Enter when prompted, and watch your alert handling in action! 🚀

---

**Status**: ✅ **READY TO USE**  
**Target**: `https://dev.dagknows.com`  
**Authentication**: ✅ **Pre-configured**  
**Last Updated**: December 8, 2025

