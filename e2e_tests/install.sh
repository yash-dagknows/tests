#!/bin/bash
# Complete installation script for E2E tests
# Handles both Python and system dependencies

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  E2E Test Suite Installation${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Check if running with sudo
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}✗ Do not run this script with sudo${NC}"
    echo "Run it normally: ./install.sh"
    exit 1
fi

# Step 1: Check Python version
echo -e "${YELLOW}Step 1: Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python version: ${PYTHON_VERSION}"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${RED}✗ Python 3.8+ required${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python version OK${NC}"
echo

# Step 2: Install system dependencies
echo -e "${YELLOW}Step 2: Installing system dependencies...${NC}"
echo "  This requires sudo and may ask for your password"
echo

if [ -f system_requirements.txt ]; then
    echo "  Installing packages from system_requirements.txt..."
    sudo apt-get update -qq
    
    # Read packages and install (ignore errors for packages that don't exist)
    PACKAGES=$(cat system_requirements.txt | grep -v '^#' | grep -v '^$' | tr '\n' ' ')
    
    # Try to install, but don't fail if some packages are unavailable
    for pkg in $PACKAGES; do
        sudo apt-get install -y "$pkg" 2>/dev/null || echo "  Note: $pkg not found, trying alternatives..."
    done
    
    # Fallback: Try old package names for older Ubuntu versions
    echo "  Installing fallback packages for compatibility..."
    sudo apt-get install -y \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libatspi2.0-0 \
        libasound2 \
        libglib2.0-0 \
        2>/dev/null || true
    
    echo -e "${GREEN}✓ System dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ system_requirements.txt not found${NC}"
    echo "  Trying to install via playwright..."
    
    # Try to use playwright install-deps
    if [ -f venv/bin/playwright ]; then
        sudo venv/bin/playwright install-deps chromium || {
            echo -e "${YELLOW}⚠ playwright install-deps failed, trying manual install${NC}"
            sudo apt-get update
            sudo apt-get install -y libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 \
                libatspi2.0-0t64 libasound2t64 libglib2.0-0t64 libxcomposite1 libxdamage1 \
                libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libxshmfence1 \
                libglu1-mesa fonts-liberation libnss3 libnspr4 2>/dev/null || true
        }
        echo -e "${GREEN}✓ System dependencies installed${NC}"
    else
        echo -e "${RED}✗ Cannot install system dependencies${NC}"
        echo "  Please install manually or create venv first"
        exit 1
    fi
fi
echo

# Step 3: Create/activate virtual environment
echo -e "${YELLOW}Step 3: Setting up Python virtual environment...${NC}"

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate venv
source venv/bin/activate
echo

# Step 4: Install Python dependencies
echo -e "${YELLOW}Step 4: Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python packages installed${NC}"
echo

# Step 5: Install Playwright browsers
echo -e "${YELLOW}Step 5: Installing Playwright browsers...${NC}"
playwright install chromium
echo -e "${GREEN}✓ Playwright browsers installed${NC}"
echo

# Step 6: Create required files
echo -e "${YELLOW}Step 6: Creating required files and directories...${NC}"
touch __init__.py
touch config/__init__.py
touch fixtures/__init__.py
touch pages/__init__.py
touch api_tests/__init__.py
touch ui_tests/__init__.py
touch utils/__init__.py
mkdir -p reports/screenshots
echo -e "${GREEN}✓ Project structure ready${NC}"
echo

# Step 7: Setup configuration
echo -e "${YELLOW}Step 7: Setting up configuration...${NC}"
if [ ! -f .env ]; then
    echo "  Copying env template..."
    cp env.template .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}  ⚠ Review .env file and update if needed${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi
echo

# Summary
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ Installation Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo "What was installed:"
echo "  ✓ System dependencies for Playwright"
echo "  ✓ Python virtual environment"
echo "  ✓ Python packages (pytest, playwright, etc.)"
echo "  ✓ Playwright Chromium browser"
echo "  ✓ Project structure (__init__.py files)"
echo "  ✓ Configuration (.env file)"
echo
echo "Next steps:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Review .env file (already configured for dev.dagknows.com)"
echo "  3. Run tests: ./run_ai_agent_test.sh"
echo
echo "Quick test:"
echo "  source venv/bin/activate"
echo "  pytest ui_tests/test_ai_agent_workflow.py -v"
echo

