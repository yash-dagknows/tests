# ⚠️ IMPORTANT: ENFORCE_LOGIN Setting

## The Issue You're Seeing

After setting `ENFORCE_LOGIN=false` in dkapp, you see an **empty task page** in the application.

## Why This Happens

`ENFORCE_LOGIN=false` means:
- ✅ API endpoints don't require authentication
- ✅ Requests can come through without login
- ❌ **BUT users are anonymous/not logged in**
- ❌ Tasks are filtered by org/user, so anonymous users see nothing

## 🚨 CRITICAL: DON'T Use ENFORCE_LOGIN=false in Production!

**`ENFORCE_LOGIN=false` is ONLY for testing**, not for your actual application!

### For Production/Normal Use:
```bash
ENFORCE_LOGIN=true  # ← Keep this for production
ALLOW_DK_USER_INFO_HEADER=false  # ← Keep this for production
```

### For Testing ONLY:
```bash
ENFORCE_LOGIN=false  # ← Only for tests
ALLOW_DK_USER_INFO_HEADER=true  # ← Only for tests
```

## ✅ Better Approach: Separate Test Configuration

Instead of modifying your production dkapp, use a separate configuration for testing:

### Option 1: Environment Variable Override (Recommended)

Keep your production `.env` as-is, and override for specific containers:

```yaml
# In dkapp/docker-compose.test-override.yml
version: '3.8'

services:
  taskservice:
    environment:
      - ALLOW_DK_USER_INFO_HEADER=true  # Enable header-based auth
      - ENFORCE_LOGIN=false              # Disable login requirement
      
  req-router:
    environment:
      - ALLOW_DK_USER_INFO_HEADER=true
      - ENFORCE_LOGIN=false
```

**Usage:**
```bash
# Normal production use
cd ~/dkapp
docker-compose up -d

# For testing (with override)
cd ~/dkapp
docker-compose -f docker-compose.yml -f docker-compose.test-override.yml restart taskservice req-router
```

### Option 2: Use Test-Specific Services

Don't modify your production dkapp at all. The tests already handle this via `docker-compose-local.yml`:

```yaml
# tests/docker-compose-local.yml sets these for test-runner only
environment:
  - ALLOW_DK_USER_INFO_HEADER=true
  - ENFORCE_LOGIN=false
```

**Your production services keep their normal settings!**

## 🔧 Fix Your Current Situation

If you changed `ENFORCE_LOGIN=false` in your production dkapp:

```bash
cd ~/dkapp

# 1. Edit .env (or .env.gpg)
nano .env

# 2. Change back to:
ENFORCE_LOGIN=true
ALLOW_DK_USER_INFO_HEADER=false

# 3. Restart services
docker-compose restart taskservice req-router

# 4. Wait
sleep 30

# 5. Refresh your browser - you should see login page
```

## ✅ Recommended Setup

### For Your Production dkapp:
```bash
# ~/dkapp/.env
ENFORCE_LOGIN=true  # Users must login
ALLOW_DK_USER_INFO_HEADER=false  # No header-based auth
```

### For Tests:
The test container already sets test-mode variables internally, so your production dkapp stays secure!

## 🎯 Why You See Empty Task Page

When `ENFORCE_LOGIN=false`:
1. Users can access the app without logging in
2. But they're **anonymous** (no user ID, no org)
3. Task list is filtered by user's org
4. Anonymous user has no org → no tasks shown
5. You see an empty page

**Solution:** Keep `ENFORCE_LOGIN=true` for production, only use `false` in test environment.

## 📋 Testing Without Breaking Production

```bash
# Your production dkapp stays normal
cd ~/dkapp
# Keep ENFORCE_LOGIN=true in .env

# Tests work independently
cd ~/tests
make -f Makefile.local quick  # Works with your production settings!
```

The test runner is on the same network but **doesn't require** changing your production services' authentication settings!

## Summary

✅ **For Production**: `ENFORCE_LOGIN=true` (users must login)  
✅ **For Tests**: Test container handles auth internally  
❌ **Don't use**: `ENFORCE_LOGIN=false` in production  

Your tests can work **without** changing production security settings!

