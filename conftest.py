"""
Pytest configuration and shared fixtures for DagKnows test suite.

This module provides:
- Test fixtures for common test setup/teardown
- API clients for testing services
- Test data factories
- Database cleanup utilities
"""

import pytest
import os
import sys
import json
import time
from typing import Dict, Any, List
from datetime import datetime
import logging

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'taskservice', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'req_router', 'src'))

# Import test utilities
from utils.api_client import APIClient, TaskServiceClient, ReqRouterClient
from utils.fixtures import TestDataFactory
from utils.cleanup import TestCleanup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def test_config():
    """Load test configuration from environment."""
    config = {
        "req_router_url": os.getenv("DAGKNOWS_REQ_ROUTER_URL", "http://localhost:8888"),
        "taskservice_url": os.getenv("DAGKNOWS_TASKSERVICE_URL", "http://localhost:2235"),
        "settings_url": os.getenv("DAGKNOWS_SETTINGS_URL", "http://localhost:2225"),
        "elastic_url": os.getenv("DAGKNOWS_ELASTIC_URL", "http://localhost:9200"),
        "postgres_host": os.getenv("POSTGRESQL_DB_HOST", "localhost"),
        "postgres_port": int(os.getenv("POSTGRESQL_DB_PORT", "5432")),
        "postgres_db": os.getenv("POSTGRESQL_DB_NAME", "dagknows_test"),
        "postgres_user": os.getenv("POSTGRESQL_DB_USER", "postgres"),
        "postgres_password": os.getenv("POSTGRESQL_DB_PASSWORD", "testpassword123"),
        "test_org": os.getenv("DEFAULT_ORG", "test-org"),
        "test_user_email": os.getenv("TEST_USER_EMAIL", "test@dagknows.com"),
        "test_user_password": os.getenv("TEST_USER_PASSWORD", "testpass123"),
        "test_admin_email": os.getenv("TEST_ADMIN_EMAIL", "admin@dagknows.com"),
        "test_admin_password": os.getenv("TEST_ADMIN_PASSWORD", "adminpass123"),
        "auto_cleanup": os.getenv("AUTO_CLEANUP_TEST_DATA", "true").lower() == "true",
    }
    logger.info(f"Test configuration loaded: {config['req_router_url']}")
    return config

@pytest.fixture(scope="session")
def wait_for_services(test_config):
    """Wait for all services to be ready before running tests."""
    import requests
    from time import sleep
    
    services = {
        "Elasticsearch": f"{test_config['elastic_url']}/_cluster/health",
        "TaskService": f"{test_config['taskservice_url']}/api/v1/tasks/status",
        "ReqRouter": f"{test_config['req_router_url']}/health",
    }
    
    max_retries = 30
    retry_delay = 2
    
    for service_name, url in services.items():
        logger.info(f"Waiting for {service_name} at {url}...")
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code < 500:
                    logger.info(f"{service_name} is ready!")
                    break
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"{service_name} not ready after {max_retries} attempts: {e}")
                    pytest.fail(f"Service {service_name} did not become ready")
                logger.warning(f"Attempt {attempt + 1}/{max_retries}: {service_name} not ready, retrying...")
                sleep(retry_delay)
    
    logger.info("All services are ready!")
    return True

# ============================================================================
# API Client Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def api_client(test_config, wait_for_services):
    """Provides a general-purpose API client for testing."""
    client = APIClient(
        base_url=test_config["req_router_url"],
        test_mode=True
    )
    return client

@pytest.fixture(scope="function")
def taskservice_client(test_config, wait_for_services):
    """Provides a TaskService-specific API client with test user authentication."""
    client = TaskServiceClient(
        base_url=test_config["taskservice_url"],
        test_mode=True
    )
    
    # Automatically set test user info for all tests
    actual_org = os.getenv("DEFAULT_ORG") or test_config.get("test_org", "dagknows")
    
    user_info = {
        "uid": "1",
        "uname": "test@dagknows.com",
        "first_name": "Test",
        "last_name": "User",
        "org": actual_org.lower(),
        "role": "Admin"
    }
    
    client.set_user_info(user_info)
    logger.debug(f"TaskService client configured with org: {actual_org}")
    
    return client

@pytest.fixture(scope="function")
def req_router_client(test_config, wait_for_services):
    """Provides a ReqRouter-specific API client with test user authentication."""
    client = ReqRouterClient(
        base_url=test_config["req_router_url"],
        test_mode=True
    )
    
    # Automatically set test user info for all tests
    actual_org = os.getenv("DEFAULT_ORG") or test_config.get("test_org", "dagknows")
    
    user_info = {
        "uid": "1",
        "uname": "test@dagknows.com",
        "first_name": "Test",
        "last_name": "User",
        "org": actual_org.lower(),
        "role": "Admin"
    }
    
    client.set_user_info(user_info)
    logger.debug(f"ReqRouter client configured with org: {actual_org}")
    
    return client

# ============================================================================
# Test User Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def test_user(test_config, req_router_client):
    """Creates a test user for the test and cleans up afterwards."""
    from faker import Faker
    fake = Faker()
    
    user_data = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": "TestPass123!",
        "organization": f"test-org-{int(time.time())}",
    }
    
    logger.info(f"Creating test user: {user_data['email']}")
    
    # In test mode, create a mock user without actual API call
    # since user creation requires authentication
    user = {
        "id": 1,
        "email": user_data["email"],
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
        "organization": user_data["organization"],
        "password": user_data["password"],
    }
    
    yield user

@pytest.fixture(scope="function")
def authenticated_user(test_user, req_router_client, taskservice_client, test_config):
    """Creates and authenticates a test user with user_info header."""
    # In test mode with ALLOW_DK_USER_INFO_HEADER=true,
    # we can bypass authentication by sending user info directly
    
    # Use the actual org from environment (e.g., "avengers")
    actual_org = os.getenv("DEFAULT_ORG") or test_config.get("test_org", "dagknows")
    
    user_info = {
        "uid": str(test_user["id"]),  # Ensure string
        "uname": test_user["email"],
        "first_name": test_user["first_name"],
        "last_name": test_user["last_name"],
        "org": actual_org.lower(),  # Use actual org from environment
        "role": "Admin"
    }
    
    logger.info(f"Using org for tests: {actual_org}")
    
    # Set user info on clients (uses dk-user-info header)
    taskservice_client.set_user_info(user_info)
    req_router_client.set_user_info(user_info)
    
    test_user["user_info"] = user_info
    return test_user

@pytest.fixture(scope="function")
def test_admin(test_config, req_router_client):
    """Provides admin user credentials and authentication."""
    token = req_router_client.login(
        test_config["test_admin_email"],
        test_config["test_admin_password"]
    )
    req_router_client.set_auth_token(token)
    return {
        "email": test_config["test_admin_email"],
        "password": test_config["test_admin_password"],
        "auth_token": token,
    }

# ============================================================================
# Tenant Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def test_tenant(test_config, req_router_client, test_admin):
    """Creates a test tenant and cleans up afterwards."""
    from faker import Faker
    fake = Faker()
    
    tenant_data = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "organization": f"test-tenant-{int(time.time())}",
        "password": "TenantPass123!",
    }
    
    logger.info(f"Creating test tenant: {tenant_data['organization']}")
    
    tenant = None  # Initialize to avoid UnboundLocalError
    try:
        tenant = req_router_client.create_tenant(tenant_data)
        tenant["password"] = tenant_data["password"]
        yield tenant
    finally:
        if test_config["auto_cleanup"] and tenant is not None:
            try:
                logger.info(f"Cleaning up test tenant: {tenant_data['organization']}")
                req_router_client.delete_tenant(tenant["id"])
            except Exception as e:
                logger.warning(f"Failed to cleanup tenant: {e}")

# ============================================================================
# Task Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def test_task(authenticated_user, taskservice_client):
    """Creates a test Python task and cleans up afterwards."""
    task_data = {
        "title": f"Test Task {int(time.time())}",
        "description": "Test task description",
        "script": "print('Hello World')",
        "script_type": "python",
        "tags": ["test"],
    }
    
    logger.info(f"Creating test task: {task_data['title']}")
    
    task = None  # Initialize to avoid UnboundLocalError
    try:
        response = taskservice_client.create_task(task_data)
        task = response.get("task", response)  # Handle wrapped response
        yield task
    finally:
        if task is not None:
            try:
                logger.info(f"Cleaning up test task: {task['id']}")
                taskservice_client.delete_task(task["id"])
            except Exception as e:
                logger.warning(f"Failed to cleanup task: {e}")

@pytest.fixture(scope="function")
def test_tasks(authenticated_user, taskservice_client):
    """Creates multiple test Python tasks and cleans up afterwards."""
    tasks = []
    task_ids = []
    
    try:
        for i in range(3):
            task_data = {
                "title": f"Test Task {i} - {int(time.time())}",
                "description": f"Test task {i} description",
                "script": f"print('Task {i}')",
                "script_type": "python",
                "tags": ["test", f"task-{i}"],
            }
            response = taskservice_client.create_task(task_data)
            task = response.get("task", response)  # Handle wrapped response
            tasks.append(task)
            task_ids.append(task["id"])
        
        yield tasks
    finally:
        for task_id in task_ids:
            try:
                taskservice_client.delete_task(task_id)
            except Exception as e:
                logger.warning(f"Failed to cleanup task {task_id}: {e}")

# ============================================================================
# Workspace Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def test_workspace(authenticated_user, taskservice_client):
    """Creates a test workspace and cleans up afterwards."""
    workspace_data = {
        "name": f"Test Workspace {int(time.time())}",
        "description": "Test workspace description",
    }
    
    logger.info(f"Creating test workspace: {workspace_data['name']}")
    
    workspace = None  # Initialize to avoid UnboundLocalError
    try:
        response = taskservice_client.create_workspace(workspace_data)
        workspace = response.get("workspace", response)  # Handle wrapped response
        yield workspace
    finally:
        if workspace is not None:
            try:
                logger.info(f"Cleaning up test workspace: {workspace['id']}")
                taskservice_client.delete_workspace(workspace["id"])
            except Exception as e:
                logger.warning(f"Failed to cleanup workspace: {e}")

# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def db_connection(test_config):
    """Provides a database connection for tests that need direct DB access."""
    import psycopg2
    
    conn = psycopg2.connect(
        host=test_config["postgres_host"],
        port=test_config["postgres_port"],
        database=test_config["postgres_db"],
        user=test_config["postgres_user"],
        password=test_config["postgres_password"]
    )
    
    yield conn
    
    conn.close()

@pytest.fixture(scope="function")
def es_client(test_config):
    """Provides an Elasticsearch client for tests that need direct ES access."""
    from elasticsearch import Elasticsearch
    
    client = Elasticsearch([test_config["elastic_url"]])
    
    yield client
    
    # Cleanup test indices if needed
    # client.indices.delete(index='test_*', ignore=[404])

# ============================================================================
# Test Data Factory Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def test_data_factory():
    """Provides a factory for generating test data."""
    return TestDataFactory()

# ============================================================================
# Cleanup Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def cleanup_tracker():
    """Tracks resources created during test for cleanup."""
    tracker = TestCleanup()
    yield tracker
    tracker.cleanup_all()

# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """Pytest configuration hook."""
    # Create results and logs directories
    os.makedirs("results", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    logger.info("=" * 80)
    logger.info("DagKnows Test Suite Starting")
    logger.info("=" * 80)

def pytest_sessionstart(session):
    """Called before test session starts."""
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Pytest version: {pytest.__version__}")

def pytest_sessionfinish(session, exitstatus):
    """Called after test session finishes."""
    logger.info("=" * 80)
    logger.info(f"Test session finished with exit status: {exitstatus}")
    logger.info("=" * 80)

def pytest_runtest_setup(item):
    """Called before each test runs."""
    logger.info(f"Starting test: {item.nodeid}")

def pytest_runtest_teardown(item, nextitem):
    """Called after each test runs."""
    logger.info(f"Finished test: {item.nodeid}")

# ============================================================================
# Custom Markers
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Modify test items after collection."""
    # Auto-add markers based on test location
    for item in items:
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        
        # Add markers based on test name
        if "tenant" in item.nodeid.lower():
            item.add_marker(pytest.mark.tenant)
        if "task" in item.nodeid.lower():
            item.add_marker(pytest.mark.task)
        if "auth" in item.nodeid.lower():
            item.add_marker(pytest.mark.auth)

