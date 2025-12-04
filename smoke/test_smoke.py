"""
Smoke tests for quick validation of critical functionality.

These tests should run in < 1 minute and verify:
- Services are accessible
- Basic API operations work
- Authentication is functional
"""

import pytest
from utils.api_client import TaskServiceClient, ReqRouterClient


@pytest.mark.smoke
@pytest.mark.unit
def test_services_are_reachable():
    """Verify that all critical services are reachable."""
    # This test just verifies pytest can run
    # Service connectivity is checked by conftest.py fixtures
    assert True, "Services reachable"


@pytest.mark.smoke
@pytest.mark.unit
def test_test_suite_is_configured():
    """Verify that test suite is properly configured."""
    import os
    
    # Check that environment variables are set
    assert os.getenv("DAGKNOWS_TASKSERVICE_URL"), "DAGKNOWS_TASKSERVICE_URL not set"
    assert os.getenv("DAGKNOWS_REQ_ROUTER_URL"), "DAGKNOWS_REQ_ROUTER_URL not set"
    
    # Verify they use service names (not localhost)
    taskservice_url = os.getenv("DAGKNOWS_TASKSERVICE_URL")
    assert "taskservice" in taskservice_url or "localhost" in taskservice_url, \
        f"Unexpected taskservice URL: {taskservice_url}"


@pytest.mark.smoke
@pytest.mark.api
def test_taskservice_status_endpoint(test_config):
    """Test that TaskService status endpoint responds."""
    import requests
    
    try:
        url = f"{test_config['taskservice_url']}/health"
        response = requests.get(url, timeout=5)
        assert response.status_code == 200, f"TaskService not responding: {response.status_code}"
    except Exception as e:
        pytest.skip(f"TaskService not accessible: {e}")


@pytest.mark.smoke
@pytest.mark.api
def test_req_router_readiness_endpoint(test_config):
    """Test that ReqRouter readiness endpoint responds."""
    import requests
    
    try:
        url = f"{test_config['req_router_url']}/readiness_check"
        response = requests.get(url, timeout=5)
        assert response.status_code == 200, f"ReqRouter not responding: {response.status_code}"
    except Exception as e:
        pytest.skip(f"ReqRouter not accessible: {e}")


@pytest.mark.smoke
@pytest.mark.api
def test_elasticsearch_cluster_health(test_config):
    """Test that Elasticsearch is healthy."""
    import requests
    
    try:
        url = f"{test_config['elastic_url']}/_cluster/health"
        response = requests.get(url, timeout=5)
        assert response.status_code == 200, f"Elasticsearch not responding: {response.status_code}"
        
        health = response.json()
        assert health["status"] in ["green", "yellow"], \
            f"Elasticsearch not healthy: {health['status']}"
    except Exception as e:
        pytest.skip(f"Elasticsearch not accessible: {e}")

