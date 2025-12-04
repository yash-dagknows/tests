# START HERE - Local Testing First, Jenkins Later

## What You Asked For

✅ Test locally with your existing `dkapp` and `dkproxy` setup  
✅ Use simple `make` commands  
✅ Support GPG-encrypted `.env.gpg` files  
✅ Ensure it will integrate easily with Jenkins later  
✅ No Jenkins setup required right now  

## What You Got

### For LOCAL TESTING NOW (Use These)

```
tests/
├── setup-local.sh              ← Run this first! (Handles .env.gpg)
├── Makefile.local              ← Use these make commands
├── docker-compose-local.yml    ← Connects to your dkapp
├── .env.local                  ← Auto-created from dkapp/.env or .env.gpg
│
├── START_HERE.md               ← This file
├── QUICK_START.md              ← 5-minute guide
├── LOCAL_TESTING_GUIDE.md      ← Detailed guide
└── GPG_SETUP.md                ← GPG encryption guide (NEW!)
```

### For JENKINS LATER (Ignore For Now)

```
tests/
├── Jenkinsfile.production      ← For Jenkins (later)
├── docker-compose-jenkins.yml  ← For Jenkins (later)
│
├── JENKINS_SETUP_GUIDE.md      ← Read when ready for Jenkins
└── JENKINS_INTEGRATION.md      ← Detailed Jenkins options
```

## Your Action Plan

### Phase 1: Local Testing (TODAY - 30 minutes)

#### Step 1: Setup (5 minutes)

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests
./setup-local.sh
```

**If you have `.env.gpg` (encrypted):**
- Script will detect it automatically
- You'll be prompted for GPG passphrase
- Credentials extracted and saved to `.env.local`
- Temporary decrypted file cleaned up

**If you have `.env` (unencrypted):**
- Script uses it directly
- No passphrase needed

**What this does:**
- ✅ Checks if `dkapp` is running
- ✅ Handles `.env` or `.env.gpg` automatically
- ✅ Creates `.env.local` with your credentials
- ✅ Installs dependencies
- ✅ Verifies services

#### Step 2: Verify (2 minutes)

```bash
make -f Makefile.local verify-services
```

**Expected output:**
```
Testing Elasticsearch...
✓ Elasticsearch OK
Testing TaskService...
✓ TaskService OK
Testing ReqRouter...
✓ ReqRouter OK

All services accessible!
```

#### Step 3: Run First Test (5 minutes)

```bash
# Quick smoke test
make -f Makefile.local quick
```

**What it tests:**
- Can connect to services?
- Can create a task?
- Can search tasks?
- Basic authentication?

**Expected:** All tests pass ✓

#### Step 4: Run Full Unit Tests (10 minutes)

```bash
make -f Makefile.local unit
```

**What it tests:**
- Task CRUD operations
- Search functionality
- Workspace management
- Tenant operations
- Authentication

**Expected:** ~25 tests pass in 2-5 minutes

#### Step 5: Try Integration Tests (Optional - 15 minutes)

```bash
make -f Makefile.local integration
```

**What it tests:**
- Service-to-service communication
- Tenant creation flow
- Task → Elasticsearch indexing
- Database operations

**Expected:** ~12 tests pass in 10-15 minutes

## GPG Encryption Support (NEW!)

### If Your dkapp Uses `.env.gpg`

#### Option 1: Interactive (Recommended for Local)

```bash
cd tests
./setup-local.sh
# Enter GPG passphrase when prompted
```

#### Option 2: Non-Interactive (For Automation)

```bash
cd tests
export GPG_PASSPHRASE="your-passphrase"
./setup-local.sh
unset GPG_PASSPHRASE  # Clear after use
```

#### What Happens:

1. Script detects `.env.gpg`
2. Decrypts temporarily to read values
3. Extracts credentials to `.env.local`
4. **Cleans up** decrypted `.env` (keeps `.env.gpg` secure)

**Security:** Your `.env.gpg` stays encrypted. Decryption is temporary only.

See [GPG_SETUP.md](GPG_SETUP.md) for detailed GPG documentation.

### Phase 2: Add Your Tests (THIS WEEK)

Now that testing works, add tests for your features:

```bash
# 1. Look at existing tests for examples
cat unit/taskservice/test_task_crud.py

# 2. Create your test file
cp unit/taskservice/test_task_crud.py unit/taskservice/test_my_feature.py

# 3. Edit and add your tests
nano unit/taskservice/test_my_feature.py

# 4. Run your test
make -f Makefile.local test-specific TEST=unit/taskservice/test_my_feature.py
```

### Phase 3: Jenkins Integration (LATER - When Ready)

When local testing is solid and you're ready for CI/CD:

```bash
# Read the Jenkins setup guide
cat JENKINS_SETUP_GUIDE.md

# Key points:
# 1. Tests use SAME configuration (already works)
# 2. Configure Jenkins credentials (including GPG_PASSPHRASE)
# 3. Use Jenkinsfile.production
# 4. Everything will work identically
```

**For Jenkins with GPG:**
```groovy
// In Jenkinsfile
environment {
    GPG_PASSPHRASE = credentials('gpg-passphrase-id')
}
```

## Quick Command Reference

### Essential Commands

```bash
# Setup (run once)
./setup-local.sh                          # Handles .env or .env.gpg

# Verify (run anytime)
make -f Makefile.local check-dkapp
make -f Makefile.local verify-services

# Test (run often)
make -f Makefile.local quick              # Fastest (1-2 min)
make -f Makefile.local unit               # Fast (2-5 min)
make -f Makefile.local integration        # Medium (10-15 min)
make -f Makefile.local e2e                # Slow (20-30 min)

# Specific tests
make -f Makefile.local test-specific TEST=unit/taskservice/test_task_crud.py

# Debug
make -f Makefile.local shell              # Interactive container
make -f Makefile.local status             # Service status

# Help
make -f Makefile.local help               # Show all commands
```

### If Something Goes Wrong

```bash
# Check dkapp services
cd ../dkapp && docker-compose ps

# Restart dkapp
cd ../dkapp && docker-compose restart

# Start fresh
cd ../dkapp && docker-compose down && docker-compose up -d

# Clean test artifacts
cd ../tests && make -f Makefile.local clean

# Re-run setup (will re-decrypt .env.gpg if needed)
cd ../tests && ./setup-local.sh
```

## File Organization

```
tests/
│
├── FOR LOCAL TESTING (Use Now):
│   ├── setup-local.sh              # Setup script (handles GPG)
│   ├── Makefile.local              # Local commands (with GPG helpers)
│   ├── docker-compose-local.yml    # Local Docker config
│   ├── START_HERE.md               # This file
│   ├── QUICK_START.md              # 5-min guide
│   ├── LOCAL_TESTING_GUIDE.md      # Detailed guide
│   └── GPG_SETUP.md                # GPG encryption guide (NEW!)
│
├── FOR JENKINS (Later):
│   ├── Jenkinsfile.production      # Jenkins pipeline
│   ├── docker-compose-jenkins.yml  # Jenkins Docker config
│   ├── JENKINS_SETUP_GUIDE.md      # Jenkins setup
│   └── JENKINS_INTEGRATION.md      # Jenkins options
│
├── TEST CODE (Add your tests here):
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   └── e2e/                        # E2E tests
│
└── FRAMEWORK (Don't modify):
    ├── conftest.py                 # Test fixtures
    ├── utils/                      # Test utilities
    ├── pytest.ini                  # Pytest config
    └── requirements.txt            # Dependencies
```

## What Makes This Work

### 1. Supports Both .env and .env.gpg

```bash
# Checks for .env first
if [ -f "../dkapp/.env" ]; then
    # Use directly
    
# Falls back to .env.gpg
elif [ -f "../dkapp/.env.gpg" ]; then
    # Decrypt temporarily
    # Extract values
    # Cleanup decrypted file
fi
```

### 2. Uses Your Existing Infrastructure

```yaml
# docker-compose-local.yml
networks:
  saaslocalnetwork:
    external: true  # YOUR network from dkapp
```

### 3. Service Discovery via Docker Names

```python
# Not localhost:2235 ✗
# Uses taskservice:2235 ✓
DAGKNOWS_TASKSERVICE_URL=http://taskservice:2235
```

### 4. Inherits Your Authentication

```bash
# From your dkapp/.env or .env.gpg
APP_SECRET_KEY=<your value>
api_key=<your value>
```

## Success Checklist

- [ ] `./setup-local.sh` completed successfully
- [ ] GPG passphrase entered (if using .env.gpg)
- [ ] `.env.local` created with credentials
- [ ] `make -f Makefile.local verify-services` shows all ✓
- [ ] `make -f Makefile.local quick` passes
- [ ] `make -f Makefile.local unit` passes
- [ ] Can run specific test successfully
- [ ] Understand how to add new tests
- [ ] Know that Jenkins integration is ready when needed

## FAQs

### Q: What if I have .env.gpg instead of .env?

**A:** The setup script handles it automatically! Just run `./setup-local.sh` and enter your GPG passphrase when prompted.

### Q: Is my .env.gpg file modified?

**A:** No! The `.env.gpg` stays encrypted. We only decrypt temporarily to read values, then clean up.

### Q: Can I use GPG_PASSPHRASE environment variable?

**A:** Yes!
```bash
export GPG_PASSPHRASE="your-passphrase"
./setup-local.sh
unset GPG_PASSPHRASE
```

### Q: Will this work in Jenkins?

**A:** Yes! Configure `GPG_PASSPHRASE` as a Jenkins credential and it works identically.

### Q: Do I need to configure anything for Jenkins now?

**A:** No! Focus on local testing. Jenkins files are ready but you don't need them yet.

## Get Started Now

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests
./setup-local.sh
# Enter GPG passphrase if prompted
make -f Makefile.local quick
```

That's it! 🚀

---

**Questions?** See:
- [QUICK_START.md](QUICK_START.md) - 5-minute guide
- [LOCAL_TESTING_GUIDE.md](LOCAL_TESTING_GUIDE.md) - Detailed guide
- [GPG_SETUP.md](GPG_SETUP.md) - GPG encryption guide (NEW!)
- [Makefile.local](Makefile.local) - All available commands

**Ready for Jenkins?** See:
- [JENKINS_SETUP_GUIDE.md](JENKINS_SETUP_GUIDE.md) - Quick setup
- [JENKINS_INTEGRATION.md](JENKINS_INTEGRATION.md) - Detailed options
