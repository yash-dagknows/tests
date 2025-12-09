"""
Pytest fixtures for E2E tests.

Provides reusable fixtures for both API and UI tests.
"""

import pytest
import logging
from typing import Generator
from playwright.sync_api import Page, Browser, BrowserContext
from fixtures.api_client import DagKnowsAPIClient, create_api_client
from fixtures.auth import AuthHelper, get_auth_helper
from config.env import config
from config.test_users import ADMIN_USER, get_test_user

logger = logging.getLogger(__name__)


# ==================== SESSION FIXTURES ====================

@pytest.fixture(scope="session")
def test_config():
    """Load test configuration."""
    logger.info(f"Test configuration loaded:")
    logger.info(f"  Base URL: {config.BASE_URL}")
    logger.info(f"  Proxy: {config.PROXY_PARAM}")
    logger.info(f"  Test User: {ADMIN_USER.email}")
    return config


@pytest.fixture(scope="session")
def session_auth_helper(test_config):
    """Get session-level auth helper."""
    auth = get_auth_helper()
    
    # Verify token is valid
    if not auth.verify_token():
        logger.warning("JWT token verification failed - tests may fail")
    else:
        logger.info("✓ JWT token verified")
    
    return auth


# ==================== FUNCTION FIXTURES ====================

@pytest.fixture(scope="function")
def api_client(session_auth_helper) -> Generator[DagKnowsAPIClient, None, None]:
    """
    Get API client for tests.
    
    Yields:
        DagKnowsAPIClient instance
    """
    client = create_api_client()
    yield client
    # No cleanup needed - client is stateless


@pytest.fixture(scope="function")
def auth_helper(session_auth_helper) -> AuthHelper:
    """Get auth helper for tests."""
    return session_auth_helper


# ==================== UI FIXTURES (PLAYWRIGHT) ====================

@pytest.fixture(scope="function")
def browser_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Create browser context for UI tests.
    
    Yields:
        BrowserContext with configured options
    """
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,  # For dev/test environments
        accept_downloads=True,
    )
    
    yield context
    
    context.close()


@pytest.fixture(scope="function")
def authenticated_page(browser_context: BrowserContext, test_config) -> Generator[Page, None, None]:
    """
    Get authenticated page for UI tests.
    
    This fixture:
    1. Creates a new page
    2. Sets authentication cookie/localStorage
    3. Navigates to the app
    
    Yields:
        Authenticated Page instance
    """
    page = browser_context.new_page()
    
    # Set authentication in localStorage (like the app does)
    page.goto(test_config.BASE_URL)
    
    # Set auth token in localStorage
    page.evaluate(f"""() => {{
        localStorage.setItem('isAuthenticated', '1');
        localStorage.setItem('authToken', '{test_config.JWT_TOKEN}');
    }}""")
    
    # Set auth cookie
    browser_context.add_cookies([{
        "name": "MY_V_AUTH",
        "value": "1",
        "domain": page.url.split('/')[2],
        "path": "/",
    }])
    
    logger.info("✓ Page authenticated")
    
    yield page
    
    # Screenshot on failure (handled by Playwright config)
    page.close()


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext) -> Generator[Page, None, None]:
    """
    Get unauthenticated page for UI tests.
    
    Use this for testing login flow.
    
    Yields:
        Page instance
    """
    page = browser_context.new_page()
    yield page
    page.close()


# ==================== TEST DATA FIXTURES ====================

@pytest.fixture
def test_task_data():
    """Generate test task data."""
    import time
    timestamp = int(time.time())
    
    return {
        "title": f"E2E Test Task {timestamp}",
        "description": "Test task created by E2E test suite",
        "script_type": "command",
        "commands": [
            "echo 'E2E test task executed'",
            f"echo 'Timestamp: {timestamp}'"
        ],
        "tags": ["e2e-test", "automated"]
    }


@pytest.fixture
def test_alert_data():
    """Generate test alert data (Grafana format)."""
    import time
    timestamp = int(time.time())
    
    return {
        "receiver": "E2E_Test_Endpoint",
        "status": "firing",
        "alerts": [{
            "status": "firing",
            "labels": {
                "alertname": f"E2ETestAlert_{timestamp}",
                "severity": "critical",
                "instance": "test-server"
            },
            "annotations": {
                "description": "E2E test alert",
                "summary": "Test alert from E2E suite"
            },
            "startsAt": str(timestamp),
            "fingerprint": f"e2e_{timestamp}"
        }],
        "commonLabels": {
            "alertname": f"E2ETestAlert_{timestamp}"
        }
    }


# ==================== CLEANUP HELPERS ====================

@pytest.fixture
def cleanup_tasks(api_client):
    """
    Track and cleanup tasks created during tests.
    
    Usage in test:
        task = api_client.create_task(...)
        cleanup_tasks.append(task['task']['id'])
    """
    task_ids = []
    
    yield task_ids
    
    # Cleanup
    for task_id in task_ids:
        try:
            api_client.delete_task(task_id)
            logger.info(f"✓ Cleaned up task: {task_id}")
        except Exception as e:
            logger.warning(f"Failed to cleanup task {task_id}: {e}")


# ==================== PYTEST HOOKS ====================

def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "e2e: End-to-end tests"
    )
    config.addinivalue_line(
        "markers", "api: API-based E2E tests"
    )
    config.addinivalue_line(
        "markers", "ui: UI-based E2E tests"
    )


def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on file location."""
    for item in items:
        if "api_tests" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        elif "ui_tests" in str(item.fspath):
            item.add_marker(pytest.mark.ui)

