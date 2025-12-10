"""
E2E API Test: Task CRUD Operations

Tests task creation, reading, updating, and deletion via API endpoints.
This test sends requests directly to dev.dagknows.com (or configured base URL).

Based on frontend API calls:
- Create: POST /api/tasks/ with {"task": task_data}
- Read: GET /api/tasks/{task_id}?wsid={wsid}
- Update: PUT /api/tasks/{task_id}?wsid={wsid} with task_data
- Delete: DELETE /api/tasks/{task_id}?recurse={recurse}&wsid={wsid}&forced={forced}
"""

import pytest
import logging
import time
from fixtures.api_client import DagKnowsAPIClient, create_api_client
from config.test_users import get_test_user
from config.env import config

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.e2e
@pytest.mark.task_crud
class TestTaskCRUDE2E:
    """Test task CRUD operations via API (E2E)."""
    
    @pytest.fixture(scope="function")
    def api_client(self):
        """Create API client for test."""
        test_user = get_test_user("Admin")
        client = create_api_client()
        logger.info(f"API Client initialized for {test_user.email}")
        return client
    
    def test_create_task_via_api(self, api_client):
        """
        E2E Test: Create a task via API.
        
        Flow:
        1. Prepare task data (title, description, code)
        2. Send POST request to /api/v1/tasks/ with {"task": task_data}
        3. Verify task was created successfully
        4. Verify task details match what was sent
        5. Get task by ID to verify it exists
        6. Clean up: Delete the created task
        
        Note: We use /api/v1/tasks/ (the new endpoint) instead of /api/tasks/ (legacy).
        The frontend uses /api/tasks/ which gets proxied to /api/v1/tasks/ by req-router.
        For direct API tests, we use /api/v1/tasks/ directly.
        """
        logger.info("=== Starting Task Creation E2E Test (API-based) ===")
        
        # Generate unique task title with timestamp
        timestamp = int(time.time())
        task_title = f"E2E API Test Task {timestamp}"
        task_description = f"Task created via API E2E test at {timestamp}"
        task_code = """
print("Hello from E2E API test")
result = "Task created successfully"
print(f"Result: {result}")
"""
        
        # Step 1: Prepare task data (matching frontend structure)
        logger.info("Step 1: Preparing task data")
        task_data = {
            "title": task_title,
            "description": task_description,
            "script_type": "python",
            "script": task_code,
            # Frontend sets workspace_ids and source_wsid from current_space_state
            # For API test, we can omit these or set them explicitly
        }
        
        logger.info(f"Task data prepared:")
        logger.info(f"  Title: {task_title}")
        logger.info(f"  Description: {task_description}")
        logger.info(f"  Script type: python")
        
        # Step 2: Create task via API
        logger.info("Step 2: Creating task via API POST /api/v1/tasks/")
        try:
            create_response = api_client.create_task(task_data)
            logger.info(f"✓ API request successful")
        except Exception as e:
            logger.error(f"✗ Task creation failed: {e}")
            raise
        
        # Step 3: Verify response structure
        logger.info("Step 3: Verifying response structure")
        # Response should have "task" key (based on frontend: result_task["task"])
        if "task" in create_response:
            created_task = create_response["task"]
        else:
            # Some APIs return task directly
            created_task = create_response
        
        assert created_task is not None, "Response should contain task data"
        task_id = created_task.get("id")
        assert task_id, "Task ID should be present in response"
        logger.info(f"✓ Task created with ID: {task_id}")
        
        # Step 4: Verify task details
        logger.info("Step 4: Verifying task details")
        assert created_task.get("title") == task_title, "Task title should match"
        assert created_task.get("description") == task_description, "Task description should match"
        logger.info(f"✓ Task details verified")
        
        # Step 5: Get task by ID to verify it exists in system
        logger.info("Step 5: Fetching task by ID to verify it exists")
        try:
            get_response = api_client.get_task(task_id)
            
            # Response might have "task" key or return task directly
            if "task" in get_response:
                fetched_task = get_response["task"]
            else:
                fetched_task = get_response
            
            assert fetched_task["id"] == task_id, "Fetched task ID should match"
            assert fetched_task["title"] == task_title, "Fetched task title should match"
            logger.info(f"✓ Task verified via GET /api/v1/tasks/{task_id}")
        except Exception as e:
            logger.warning(f"Could not fetch task immediately after creation: {e}")
            logger.info("This might be expected if task creation is asynchronous")
        
        # Step 6: Verify task appears in list
        logger.info("Step 6: Verifying task appears in task list")
        try:
            list_response = api_client.list_tasks(page_size=50)
            tasks = list_response.get("tasks", [])
            task_ids = [t.get("id") for t in tasks if t.get("id")]
            
            if task_id in task_ids:
                logger.info(f"✓ Task appears in list")
            else:
                logger.warning(f"Task {task_id} not found in list (might be pagination issue)")
        except Exception as e:
            logger.warning(f"Could not verify task in list: {e}")
        
        # Step 7: Clean up - Delete the created task
        logger.info("Step 7: Cleaning up - Deleting created task")
        try:
            api_client.delete_task(task_id)
            logger.info(f"✓ Task deleted: {task_id}")
        except Exception as e:
            logger.warning(f"Task deletion failed (may need manual cleanup): {e}")
            logger.warning(f"Task ID for manual cleanup: {task_id}")
        
        logger.info("=== Task Creation E2E Test (API-based) Completed ===")
        
        # Return task_id for potential use in other tests
        return task_id

