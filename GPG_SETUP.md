# GPG-Encrypted .env Support

## Overview

The test suite now supports GPG-encrypted `.env.gpg` files from your `dkapp` setup. This maintains security while allowing automated testing.

## How It Works

### Setup Script (`setup-local.sh`)

The setup script automatically handles both encrypted and unencrypted `.env` files:

1. **Checks for `.env`** first (unencrypted)
2. **Falls back to `.env.gpg`** if `.env` not found
3. **Decrypts temporarily** to read credentials
4. **Creates `.env.local`** with extracted values
5. **Cleans up** decrypted `.env` (keeps `.env.gpg` secure)

### Makefile (`Makefile.local`)

The Makefile includes GPG decryption helpers for automated workflows.

## Usage

### Option 1: Interactive Decryption (Default)

```bash
cd tests
./setup-local.sh
# Will prompt for GPG passphrase if .env.gpg is found
```

### Option 2: Non-Interactive with Environment Variable

```bash
cd tests
export GPG_PASSPHRASE="your-passphrase"
./setup-local.sh
# Decrypts automatically without prompting
```

### Option 3: Using Makefile

```bash
cd tests

# With passphrase in environment
export GPG_PASSPHRASE="your-passphrase"
make -f Makefile.local setup

# Or interactive (will prompt)
make -f Makefile.local setup
```

## Security Features

### ✅ Temporary Decryption Only

```bash
# Before setup:
dkapp/.env.gpg  ← Encrypted (secure)
dkapp/.env      ← Does not exist

# During setup:
dkapp/.env.gpg  ← Still encrypted
dkapp/.env      ← Temporarily decrypted (to read values)

# After setup:
dkapp/.env.gpg  ← Still encrypted (secure)
dkapp/.env      ← Removed (cleaned up)
tests/.env.local ← Created with values (for testing)
```

### ✅ No Permanent Decryption

The original `.env.gpg` is **never modified**. The decrypted `.env` is **automatically removed** after extracting values.

### ✅ Test-Specific Configuration

Credentials are copied to `tests/.env.local` which:
- Is used only for testing
- Can be added to `.gitignore`
- Doesn't affect your production `.env.gpg`

## GPG Passphrase Management

### For Local Development

```bash
# Interactive (most secure)
./setup-local.sh
# Enter passphrase when prompted

# Or set temporarily
export GPG_PASSPHRASE="your-passphrase"
./setup-local.sh
unset GPG_PASSPHRASE  # Clear after use
```

### For CI/CD (Jenkins)

```groovy
// In Jenkinsfile
environment {
    GPG_PASSPHRASE = credentials('gpg-passphrase-id')
}

stages {
    stage('Setup') {
        steps {
            sh './tests/setup-local.sh'
        }
    }
}
```

**Configure in Jenkins:**
1. Jenkins → Credentials → Add
2. Kind: Secret text
3. ID: `gpg-passphrase-id`
4. Secret: Your GPG passphrase

## Workflow Examples

### First-Time Setup

```bash
cd /Users/yashyaadav/dag_workspace/dagknows_src/tests

# If dkapp has .env.gpg
./setup-local.sh
# Enter passphrase when prompted
# ✓ .env.local created
# ✓ Temporary .env cleaned up

# Run tests
make -f Makefile.local quick
```

### Automated Testing

```bash
# Set passphrase once
export GPG_PASSPHRASE="your-passphrase"

# Run setup and tests
./setup-local.sh
make -f Makefile.local unit

# Clear passphrase
unset GPG_PASSPHRASE
```

### CI/CD Pipeline

```bash
# In Jenkins or CI system
export GPG_PASSPHRASE="${SECRET_FROM_VAULT}"
cd tests
./setup-local.sh
make -f Makefile.local test-all
```

## Troubleshooting

### Issue: "GPG command not found"

```bash
# Install GPG
# macOS
brew install gnupg

# Ubuntu/Debian
sudo apt-get install gnupg

# Verify
gpg --version
```

### Issue: "Decryption failed"

```bash
# Check if .env.gpg is valid
gpg -d ../dkapp/.env.gpg

# If it works, passphrase is correct
# If not, check:
# 1. Correct GPG key installed
# 2. Correct passphrase
# 3. File not corrupted
```

### Issue: "Permission denied"

```bash
# Ensure scripts are executable
chmod +x setup-local.sh
chmod +x ci/wait-for-services-jenkins.sh
```

### Issue: Passphrase not working in non-interactive mode

```bash
# Ensure GPG_PASSPHRASE is set
echo $GPG_PASSPHRASE

# Try interactive mode first
unset GPG_PASSPHRASE
./setup-local.sh
```

## File Structure

```
dkapp/
├── .env.gpg              ← Encrypted (committed to git)
└── .env                  ← Temporary (auto-removed, in .gitignore)

tests/
├── .env.local            ← Test config (created from .env.gpg)
├── setup-local.sh        ← Handles decryption
└── Makefile.local        ← Includes GPG helpers
```

## Best Practices

### ✅ Do This

```bash
# Keep .env.gpg in git
git add dkapp/.env.gpg
git commit -m "Update encrypted config"

# Use setup script
./setup-local.sh

# Clear passphrase after use
unset GPG_PASSPHRASE
```

### ❌ Don't Do This

```bash
# Don't commit decrypted .env
git add dkapp/.env  # ✗ Bad!

# Don't hardcode passphrase
GPG_PASSPHRASE="secret" ./setup-local.sh  # ✗ Bad!

# Don't leave passphrase in environment
export GPG_PASSPHRASE="secret"
# ... do work ...
# (forgot to unset)  # ✗ Bad!
```

## Encryption Workflow (For Reference)

If you need to update `.env.gpg`:

```bash
cd dkapp

# Edit .env
nano .env

# Encrypt
gpg -c .env
# Enter passphrase when prompted
# Creates .env.gpg

# Remove unencrypted
rm -f .env

# Commit encrypted version
git add .env.gpg
git commit -m "Update config"
```

Or using Makefile (if you have one in dkapp):

```bash
cd dkapp
make encrypt  # Encrypts .env to .env.gpg and removes .env
```

## Integration with Existing Workflow

### Your Current dkapp Makefile

```makefile
# In dkapp/Makefile
define decrypt_env
	@if [ -n "$$GPG_PASSPHRASE" ]; then \
		gpg --batch --yes --pinentry-mode loopback --passphrase "$$GPG_PASSPHRASE" \
			-o .env -d .env.gpg; \
	else \
		gpg -o .env -d .env.gpg; \
	fi
endef

encrypt:
	gpg -c .env
	rm -f .env
```

### Tests Now Use Same Pattern

```bash
# In tests/setup-local.sh and Makefile.local
# Same decryption logic as dkapp
# Consistent across your entire setup
```

## Summary

✅ **Automatic**: Setup script detects and handles `.env.gpg`  
✅ **Secure**: Temporary decryption only, auto-cleanup  
✅ **Flexible**: Interactive or non-interactive modes  
✅ **CI-Ready**: Works with Jenkins credentials  
✅ **Consistent**: Uses same GPG pattern as dkapp  

## Quick Reference

```bash
# Setup with encrypted .env
cd tests
./setup-local.sh              # Interactive
# or
export GPG_PASSPHRASE="..."
./setup-local.sh              # Non-interactive

# Run tests
make -f Makefile.local quick

# Cleanup (if needed)
rm -f .env.local
rm -f ../dkapp/.env  # Remove any leftover decrypted file
```

## Next Steps

1. ✅ Ensure `dkapp/.env.gpg` exists
2. ✅ Run `./setup-local.sh`
3. ✅ Enter passphrase when prompted
4. ✅ Run tests: `make -f Makefile.local quick`
5. ✅ For Jenkins: Configure GPG_PASSPHRASE credential

Your tests now work securely with encrypted configuration! 🔒

