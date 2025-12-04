# Ubuntu 22.04+ Setup Guide

## Issue: "externally-managed-environment" Error

On Ubuntu 22.04+ (with Python 3.11+), you'll see this error when trying to install packages system-wide.

This is a **security feature** to prevent breaking system Python packages.

## Solution: Use Virtual Environment

### Option 1: Quick Manual Fix (Do This Now)

```bash
cd ~/tests

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your prompt now
# Install dependencies
pip install -r requirements.txt

# Run tests
make -f Makefile.local quick
```

### Option 2: Re-run Setup Script (Automatic)

The setup script now automatically creates a venv:

```bash
cd ~/tests

# Pull the updated script
git pull origin main

# Re-run setup (it will create venv automatically)
./setup-local.sh

# Activate venv
source venv/bin/activate

# Run tests
make -f Makefile.local quick
```

## Using Virtual Environment

### Always Activate Before Testing

```bash
cd ~/tests

# Activate venv
source venv/bin/activate

# Now you'll see (venv) in your prompt:
# (venv) ubuntu@server:~/tests$

# Run tests
make -f Makefile.local quick
```

### Or Use Docker (No venv Needed)

```bash
cd ~/tests

# Tests run in Docker container (venv not needed)
make -f Makefile.local unit
make -f Makefile.local integration
```

## Complete Setup After the Error

Since you already ran `./setup-local.sh` and it created `.env.local`, you just need to:

```bash
cd ~/tests

# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify services
make -f Makefile.local verify-services

# Run tests
make -f Makefile.local quick
```

## Daily Workflow

### Method 1: Using venv (for local pytest)

```bash
cd ~/tests
source venv/bin/activate  # Activate venv
make -f Makefile.local test-unit  # Uses local pytest
```

### Method 2: Using Docker (no venv needed)

```bash
cd ~/tests
# No need to activate venv!
make -f Makefile.local unit  # Uses Docker container
make -f Makefile.local integration
```

## Updating the Setup Script

To get the automatic venv creation:

```bash
cd ~/tests

# If you have git
git pull origin main

# Or manually download the updated setup-local.sh
# Then run it again:
./setup-local.sh
```

## Troubleshooting

### Issue: "venv not found"

```bash
cd ~/tests
python3 -m venv venv
```

### Issue: "python3-venv not installed"

```bash
sudo apt update
sudo apt install python3-venv
```

### Issue: Forgot to activate venv

```bash
cd ~/tests
source venv/bin/activate
# Now you should see (venv) in prompt
```

### Issue: Want to deactivate venv

```bash
deactivate
# Removes (venv) from prompt
```

## Summary

For Ubuntu 22.04+ with Python 3.11+:

**Quick Fix:**
```bash
cd ~/tests
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
make -f Makefile.local quick
```

**Daily Use:**
```bash
cd ~/tests
source venv/bin/activate  # Activate first
make -f Makefile.local unit

# Or just use Docker (no venv needed):
make -f Makefile.local unit  # Already uses Docker
```

That's it! Virtual environments keep your system Python safe while allowing you to install test dependencies.

