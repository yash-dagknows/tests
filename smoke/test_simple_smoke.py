"""
Simple smoke tests that don't require authentication.
"""

import pytest
import requests
import os


@pytest.mark.smoke
def test_elasticsearch_is_up():
    """Test Elasticsearch is responding."""
    url = os.getenv("DAGKNOWS_ELASTIC_URL", "http://elasticsearch:9200")
    response = requests.get(f"{url}/_cluster/health", timeout=5)
    assert response.status_code == 200
    health = response.json()
    assert health["status"] in ["green", "yellow"]
    print(f"✓ Elasticsearch: {health['status']}")


@pytest.mark.smoke
def test_taskservice_status_unauthenticated():
    """Test TaskService status endpoint (no auth required)."""
    url = os.getenv("DAGKNOWS_TASKSERVICE_URL", "http://taskservice:2235")
    response = requests.get(f"{url}/api/v1/tasks/status", timeout=5)
    # Status endpoint should work without auth
    assert response.status_code == 200
    print(f"✓ TaskService status: {response.text}")


@pytest.mark.smoke
def test_reqrouter_readiness():
    """Test ReqRouter readiness endpoint."""
    url = os.getenv("DAGKNOWS_REQ_ROUTER_URL", "http://req-router:8888")
    response = requests.get(f"{url}/readiness_check", timeout=5)
    assert response.status_code == 200
    print(f"✓ ReqRouter ready")


@pytest.mark.smoke
def test_check_taskservice_auth_mode():
    """Check if taskservice has test mode enabled."""
    url = os.getenv("DAGKNOWS_TASKSERVICE_URL", "http://taskservice:2235")
    
    # Try to create a task with dk-user-info header
    import json
    import urllib.parse
    
    user_info = {
        "uid": 1,
        "uname": "test@dagknows.com",
        "first_name": "Test",
        "last_name": "User",
        "org": "dagknows",
        "role": "Admin"
    }
    
    headers = {
        "dk-user-info": urllib.parse.quote(json.dumps(user_info)),
        "Content-Type": "application/json"
    }
    
    # Try to list tasks with auth header
    response = requests.get(f"{url}/api/v1/tasks/", headers=headers, timeout=5)
    
    print(f"\nAuth test response: {response.status_code}")
    print(f"Response body: {response.text}")
    
    if response.status_code == 401:
        pytest.fail(
            "❌ ALLOW_DK_USER_INFO_HEADER is NOT enabled in taskservice!\n"
            "\n"
            "Fix this by running:\n"
            "  cd ~/dkapp\n"
            "  # Add to .env:\n"
            "  echo 'ALLOW_DK_USER_INFO_HEADER=true' >> .env\n"
            "  echo 'ENFORCE_LOGIN=false' >> .env\n"
            "  docker-compose restart taskservice req-router\n"
            "  sleep 30\n"
        )
    elif response.status_code == 200:
        print("✓ Test mode authentication is working!")
        tasks = response.json()
        print(f"✓ Got tasks response: {type(tasks)}")
    else:
        print(f"⚠ Unexpected status: {response.status_code}")

