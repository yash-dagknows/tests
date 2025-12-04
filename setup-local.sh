#!/bin/bash
# Quick setup script for local testing

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}DagKnows Test Suite - Local Setup${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if in tests directory
if [ ! -f "pytest.ini" ]; then
    echo -e "${RED}Error: Must run from tests/ directory${NC}"
    exit 1
fi

# Step 1: Check dkapp
echo -e "\n${YELLOW}Step 1: Checking dkapp setup...${NC}"

if [ ! -d "../dkapp" ]; then
    echo -e "${RED}✗ dkapp directory not found${NC}"
    echo "Expected: ../dkapp"
    exit 1
fi

echo -e "${GREEN}✓ dkapp directory found${NC}"

# Check for .env or .env.gpg
DKAPP_ENV_FILE=""
DKAPP_ENV_DECRYPTED=false

if [ -f "../dkapp/.env" ]; then
    echo -e "${GREEN}✓ dkapp/.env found (unencrypted)${NC}"
    DKAPP_ENV_FILE="../dkapp/.env"
elif [ -f "../dkapp/.env.gpg" ]; then
    echo -e "${YELLOW}⚠ Found dkapp/.env.gpg (encrypted)${NC}"
    echo "Decrypting .env.gpg..."
    
    # Decrypt using GPG
    if [ -n "$GPG_PASSPHRASE" ]; then
        # Non-interactive mode with passphrase from env
        echo "Using GPG_PASSPHRASE from environment"
        gpg --batch --yes --pinentry-mode loopback --passphrase "$GPG_PASSPHRASE" \
            -o ../dkapp/.env -d ../dkapp/.env.gpg 2>/dev/null
    else
        # Interactive mode - will prompt user
        echo "Please enter GPG passphrase when prompted..."
        gpg -o ../dkapp/.env -d ../dkapp/.env.gpg
    fi
    
    if [ $? -eq 0 ] && [ -f "../dkapp/.env" ]; then
        echo -e "${GREEN}✓ Successfully decrypted .env${NC}"
        DKAPP_ENV_FILE="../dkapp/.env"
        DKAPP_ENV_DECRYPTED=true
    else
        echo -e "${RED}✗ Failed to decrypt .env.gpg${NC}"
        echo "Please ensure GPG is configured correctly"
        exit 1
    fi
else
    echo -e "${RED}✗ Neither dkapp/.env nor dkapp/.env.gpg found${NC}"
    echo "Please configure dkapp first"
    exit 1
fi

# Step 2: Check network
echo -e "\n${YELLOW}Step 2: Checking Docker network...${NC}"

if ! docker network ls | grep -q saaslocalnetwork; then
    echo -e "${YELLOW}⚠ saaslocalnetwork not found${NC}"
    echo "Starting dkapp services..."
    cd ../dkapp
    docker-compose up -d
    cd ../tests
    echo -e "${GREEN}✓ Services started${NC}"
else
    echo -e "${GREEN}✓ saaslocalnetwork exists${NC}"
fi

# Step 3: Create .env.local
echo -e "\n${YELLOW}Step 3: Creating .env.local...${NC}"

if [ -f ".env.local" ]; then
    echo -e "${YELLOW}⚠ .env.local already exists${NC}"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env.local"
    else
        rm .env.local
    fi
fi

if [ ! -f ".env.local" ]; then
    echo "Creating .env.local from $DKAPP_ENV_FILE..."
    
    # Extract values from dkapp/.env (now decrypted if it was .gpg)
    POSTGRES_PASSWORD=$(grep -E "^POSTGRESQL_DB_PASSWORD=" "$DKAPP_ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    APP_SECRET=$(grep -E "^APP_SECRET_KEY=" "$DKAPP_ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    API_KEY=$(grep -E "^api_key=" "$DKAPP_ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    POSTGRES_DB=$(grep -E "^POSTGRESQL_DB_NAME=" "$DKAPP_ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    POSTGRES_USER=$(grep -E "^POSTGRESQL_DB_USER=" "$DKAPP_ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    DEFAULT_ORG=$(grep -E "^DEFAULT_ORG=" "$DKAPP_ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    SUPER_USER_ORG=$(grep -E "^SUPER_USER_ORG=" "$DKAPP_ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
    
    # Create .env.local
    cat > .env.local << EOF
# Local Testing Environment Configuration
# Auto-generated from dkapp/.env

# Database
POSTGRESQL_DB_HOST=postgres
POSTGRESQL_DB_PORT=5432
POSTGRESQL_DB_NAME=${POSTGRES_DB:-dagknows}
POSTGRESQL_DB_USER=${POSTGRES_USER:-postgres}
POSTGRESQL_DB_PASSWORD=${POSTGRES_PASSWORD}

# Security Keys
APP_SECRET_KEY=${APP_SECRET}
api_key=${API_KEY}

# Organization
DEFAULT_ORG=${DEFAULT_ORG:-dagknows}
SUPER_USER_ORG=${SUPER_USER_ORG:-dagknows}

# Service URLs (using Docker service names)
DAGKNOWS_ELASTIC_URL=http://elasticsearch:9200
DAGKNOWS_TASKSERVICE_URL=http://taskservice:2235
DAGKNOWS_REQ_ROUTER_URL=http://req-router:8888
DAGKNOWS_SETTINGS_URL=http://settings:2225

# Test mode
TESTING=true
TEST_MODE=true
ALLOW_DK_USER_INFO_HEADER=true
ENFORCE_LOGIN=false
EOF
    
    echo -e "${GREEN}✓ .env.local created${NC}"
fi

# Step 4: Create directories
echo -e "\n${YELLOW}Step 4: Creating directories...${NC}"
mkdir -p results logs
echo -e "${GREEN}✓ Directories created${NC}"

# Step 5: Install dependencies
echo -e "\n${YELLOW}Step 5: Installing Python dependencies...${NC}"
if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
    # Check if we're in a virtual environment
    if [ -z "$VIRTUAL_ENV" ]; then
        # Not in venv, check if venv exists
        if [ -d "venv" ]; then
            echo -e "${YELLOW}Virtual environment found, activating...${NC}"
            source venv/bin/activate
            echo -e "${GREEN}✓ Virtual environment activated${NC}"
        else
            # Create virtual environment
            echo -e "${YELLOW}Creating virtual environment (Python 3.11+ requirement)...${NC}"
            python3 -m venv venv
            if [ $? -eq 0 ]; then
                source venv/bin/activate
                echo -e "${GREEN}✓ Virtual environment created and activated${NC}"
            else
                echo -e "${RED}✗ Failed to create virtual environment${NC}"
                echo -e "${YELLOW}Install manually: python3 -m venv venv${NC}"
                echo -e "${YELLOW}Then activate: source venv/bin/activate${NC}"
                echo -e "${YELLOW}Then install: pip install -r requirements.txt${NC}"
            fi
        fi
    else
        echo -e "${GREEN}✓ Already in virtual environment${NC}"
    fi
    
    # Install dependencies
    pip install -r requirements.txt 2>&1 | grep -v "Requirement already satisfied" || true
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    else
        echo -e "${YELLOW}⚠ Some dependencies may have failed to install${NC}"
        echo "Run manually: pip install -r requirements.txt"
    fi
else
    echo -e "${YELLOW}⚠ pip not found, skipping Python dependencies${NC}"
    echo "Install Python: sudo apt install python3 python3-pip python3-venv"
fi

# Step 6: Verify services
echo -e "\n${YELLOW}Step 6: Verifying services...${NC}"

if docker ps --filter "network=saaslocalnetwork" | grep -q taskservice; then
    echo -e "${GREEN}✓ taskservice running${NC}"
else
    echo -e "${RED}✗ taskservice not running${NC}"
    echo "Start dkapp: cd ../dkapp && docker-compose up -d"
fi

if docker ps --filter "network=saaslocalnetwork" | grep -q req-router; then
    echo -e "${GREEN}✓ req-router running${NC}"
else
    echo -e "${RED}✗ req-router not running${NC}"
fi

if docker ps --filter "network=saaslocalnetwork" | grep -q postgres; then
    echo -e "${GREEN}✓ postgres running${NC}"
else
    echo -e "${RED}✗ postgres not running${NC}"
fi

if docker ps --filter "network=saaslocalnetwork" | grep -q elasticsearch; then
    echo -e "${GREEN}✓ elasticsearch running${NC}"
else
    echo -e "${RED}✗ elasticsearch not running${NC}"
fi

# Summary
# Cleanup: Remove decrypted .env if we created it
if [ "$DKAPP_ENV_DECRYPTED" = true ]; then
    echo -e "\n${YELLOW}Cleaning up decrypted .env file...${NC}"
    rm -f ../dkapp/.env
    echo -e "${GREEN}✓ Temporary .env removed (keeping .env.gpg secure)${NC}"
fi

echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}"

echo -e "\n${GREEN}Next steps:${NC}"
echo -e "  1. Run quick test:    ${BLUE}make -f Makefile.local quick${NC}"
echo -e "  2. Run unit tests:    ${BLUE}make -f Makefile.local unit${NC}"
echo -e "  3. Run all tests:     ${BLUE}make -f Makefile.local test-all${NC}"
echo -e "  4. Get help:          ${BLUE}make -f Makefile.local help${NC}"

echo -e "\n${YELLOW}Verify services are accessible:${NC}"
echo -e "  ${BLUE}make -f Makefile.local verify-services${NC}"

echo -e "\n${YELLOW}Note:${NC} If you used .env.gpg, the decrypted .env was cleaned up."
echo -e "Your credentials are safely stored in .env.local for testing."

if [ -d "venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    echo -e "\n${YELLOW}Important:${NC} Virtual environment created but not currently active."
    echo -e "Before running tests, activate it with:"
    echo -e "  ${BLUE}source venv/bin/activate${NC}"
    echo -e "\nOr use the Makefile which handles this automatically:"
    echo -e "  ${BLUE}make -f Makefile.local quick${NC}"
fi

echo ""

