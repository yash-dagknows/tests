#!/bin/bash
# Wait for services to be ready in Jenkins/Docker environment
# Uses Docker service names instead of localhost

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=====================================${NC}"
echo -e "${YELLOW}Checking Service Health (Jenkins)${NC}"
echo -e "${YELLOW}=====================================${NC}"

# Service endpoints to check (using Docker service names)
declare -A SERVICES=(
    ["Elasticsearch"]="elasticsearch:9200/_cluster/health"
    ["TaskService"]="taskservice:2235/health"
    ["ReqRouter"]="req-router:8888/health"
    ["Settings"]="settings:2225/health"
)

# Timeout settings
MAX_RETRIES=30
RETRY_DELAY=3

# Function to check if we're in Docker
is_in_docker() {
    [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null
}

# Function to wait for a service
wait_for_service() {
    local service_name=$1
    local endpoint=$2
    local retries=0

    echo -e "\n${YELLOW}Checking $service_name...${NC}"
    echo "Endpoint: http://$endpoint"

    while [ $retries -lt $MAX_RETRIES ]; do
        # Try to connect
        if curl -sf "http://$endpoint" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $service_name is ready${NC}"
            return 0
        fi
        
        retries=$((retries + 1))
        
        if [ $retries -eq $MAX_RETRIES ]; then
            echo -e "${RED}✗ $service_name did not become ready after $MAX_RETRIES attempts${NC}"
            echo -e "${RED}Last curl attempt:${NC}"
            curl -v "http://$endpoint" 2>&1 || true
            return 1
        fi
        
        echo -e "Attempt $retries/$MAX_RETRIES: $service_name not ready yet, waiting ${RETRY_DELAY}s..."
        sleep $RETRY_DELAY
    done
}

# Main execution
echo -e "\n${YELLOW}Environment:${NC}"
if is_in_docker; then
    echo "  Running inside Docker container"
else
    echo "  Running on host machine"
fi

echo -e "\n${YELLOW}Docker Network Info:${NC}"
# Check network connectivity
if command -v docker &> /dev/null; then
    echo "Networks:"
    docker network ls | grep saas || echo "  saaslocalnetwork not visible (may need to be in container)"
fi

echo -e "\n${YELLOW}Checking services on saaslocalnetwork...${NC}"

# Check each service
all_healthy=true
for service_name in "${!SERVICES[@]}"; do
    if ! wait_for_service "$service_name" "${SERVICES[$service_name]}"; then
        all_healthy=false
        echo -e "${RED}Failed to connect to $service_name${NC}"
    fi
done

echo -e "\n${YELLOW}=====================================${NC}"
if [ "$all_healthy" = true ]; then
    echo -e "${GREEN}✓ All services are healthy!${NC}"
    echo -e "${YELLOW}=====================================${NC}"
    exit 0
else
    echo -e "${RED}✗ Some services are not healthy${NC}"
    echo -e "${YELLOW}=====================================${NC}"
    
    echo -e "\n${YELLOW}Diagnostic Information:${NC}"
    echo "Services running on saaslocalnetwork:"
    if command -v docker &> /dev/null; then
        docker ps --filter "network=saaslocalnetwork" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || true
    fi
    
    exit 1
fi

