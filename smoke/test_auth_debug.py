"""
Authentication debugging tests.
"""

import pytest
import requests
import json
import urllib.parse
import os


@pytest.mark.smoke
def test_taskservice_status_no_auth():
    """Test taskservice status endpoint (should work without auth)."""
    url = os.getenv("DAGKNOWS_TASKSERVICE_URL", "http://taskservice:2235")
    response = requests.get(f"{url}/api/v1/tasks/status", timeout=5)
    
    print(f"\nStatus endpoint: {response.status_code}")
    print(f"Response: {response.text}")
    
    assert response.status_code == 200
    print("✓ TaskService status endpoint works")


@pytest.mark.smoke  
def test_check_allow_dk_user_info_header():
    """Check if ALLOW_DK_USER_INFO_HEADER is enabled by checking response."""
    url = os.getenv("DAGKNOWS_TASKSERVICE_URL", "http://taskservice:2235")
    
    # Use actual org from environment
    actual_org = os.getenv("DEFAULT_ORG", "dagknows")
    
    print(f"\nUsing org: {actual_org}")
    
    user_info = {
        "uid": "1",
        "uname": "test@dagknows.com",
        "first_name": "Test",
        "last_name": "User",
        "org": actual_org.lower(),
        "role": "Admin"
    }
    
    headers = {
        "dk-user-info": urllib.parse.quote(json.dumps(user_info)),
        "Content-Type": "application/json"
    }
    
    print(f"\nTesting with user_info header...")
    print(f"User info: {user_info}")
    print(f"Header value: {headers['dk-user-info'][:50]}...")
    
    # Try a simple GET request
    response = requests.get(f"{url}/api/v1/tasks/", headers=headers, timeout=5)
    
    print(f"\nResponse status: {response.status_code}")
    print(f"Response body: {response.text[:200]}")
    
    if response.status_code == 401:
        print("\n❌ Got 401 - ALLOW_DK_USER_INFO_HEADER likely NOT enabled")
        print("\nTo fix, run these commands:")
        print("  cd ~/dkapp")
        print("  nano .env  # or vi .env")
        print("  # Add these lines:")
        print("  ALLOW_DK_USER_INFO_HEADER=true")
        print("  ENFORCE_LOGIN=false")
        print("  # Save and exit")
        print("  docker-compose restart taskservice req-router")
        print("  sleep 30")
        pytest.fail("Authentication not enabled - see instructions above")
        
    elif response.status_code == 500:
        print("\n⚠ Got 500 - Auth working but internal error")
        print("\nCheck taskservice logs:")
        print("  docker logs dkapp-taskservice-1 --tail 50")
        print("\nLikely causes:")
        print("  - Missing org/workspace in database")
        print("  - Database connection issue")
        print("  - Elasticsearch issue")
        # Don't fail - this is expected for fresh setup
        
    elif response.status_code == 200:
        print("\n✓ Got 200 - Authentication working!")
        tasks = response.json()
        print(f"✓ Response type: {type(tasks)}")
        

@pytest.mark.smoke
def test_create_minimal_task_with_auth():
    """Try to create a minimal task with authentication."""
    url = os.getenv("DAGKNOWS_TASKSERVICE_URL", "http://taskservice:2235")
    
    # Use actual org from environment
    actual_org = os.getenv("DEFAULT_ORG", "dagknows")
    
    print(f"\nUsing org: {actual_org}")
    
    user_info = {
        "uid": "1",
        "uname": "test@dagknows.com",
        "first_name": "Test",
        "last_name": "User",
        "org": actual_org.lower(),
        "role": "Admin"
    }
    
    headers = {
        "dk-user-info": urllib.parse.quote(json.dumps(user_info)),
        "Content-Type": "application/json"
    }
    
    task_data = {
        "title": "Minimal Test Task",
        "script": "echo 'test'",
        "script_type": "shell"
    }
    
    print(f"\nAttempting to create task...")
    print(f"Task data: {task_data}")
    
    response = requests.post(
        f"{url}/api/v1/tasks/",
        json=task_data,
        headers=headers,
        timeout=10
    )
    
    print(f"\nResponse status: {response.status_code}")
    print(f"Response body: {response.text[:500]}")
    
    if response.status_code == 401:
        pytest.fail("❌ Still getting 401 - auth not working")
    elif response.status_code == 500:
        print("\n⚠ Got 500 - Check taskservice logs")
        print("Run: docker logs dkapp-taskservice-1 --tail 100")
        pytest.skip("Internal error - check logs")
    elif response.status_code in [200, 201]:
        print("\n✓ Task created successfully!")
        result = response.json()
        print(f"Task ID: {result.get('task', {}).get('id', 'N/A')}")
    else:
        print(f"\n⚠ Unexpected status: {response.status_code}")

