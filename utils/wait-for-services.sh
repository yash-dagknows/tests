#!/bin/bash
# Wait for services to be ready before running tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Service endpoints to check
ELASTICSEARCH_URL="${DAGKNOWS_ELASTIC_URL:-http://localhost:9200}"
TASKSERVICE_URL="${DAGKNOWS_TASKSERVICE_URL:-http://localhost:2235}"
REQ_ROUTER_URL="${DAGKNOWS_REQ_ROUTER_URL:-http://localhost:8888}"

# Timeout settings
MAX_RETRIES=30
RETRY_DELAY=2

echo -e "${YELLOW}Waiting for services to be ready...${NC}"

# Function to wait for a service
wait_for_service() {
    local service_name=$1
    local url=$2
    local retries=0

    echo -n "Waiting for $service_name at $url... "

    while [ $retries -lt $MAX_RETRIES ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC}"
            return 0
        fi
        retries=$((retries + 1))
        sleep $RETRY_DELAY
    done

    echo -e "${RED}✗${NC}"
    echo -e "${RED}ERROR: $service_name did not become ready after $MAX_RETRIES attempts${NC}"
    return 1
}

# Wait for Elasticsearch
wait_for_service "Elasticsearch" "$ELASTICSEARCH_URL/_cluster/health" || exit 1

# Wait for TaskService
wait_for_service "TaskService" "$TASKSERVICE_URL/api/v1/tasks/status" || exit 1

# Wait for ReqRouter
wait_for_service "ReqRouter" "$REQ_ROUTER_URL/health" || exit 1

echo -e "${GREEN}All services are ready!${NC}"
exit 0

