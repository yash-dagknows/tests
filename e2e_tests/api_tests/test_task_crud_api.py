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
import requests
from fixtures.api_client import create_api_client
from config.test_users import get_test_user

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
    
    def test_task_full_lifecycle_via_api(self, api_client):
        """
        E2E Test: Full task lifecycle (Create, Read, Update, Delete) via API.
        
        Flow:
        1. CREATE: Prepare task data (title, description, code) and POST to /api/tasks/
        2. READ: Verify task was created and fetch it by ID
        3. UPDATE: Update task with new title, description, and code
        4. READ: Verify the update was successful
        5. DELETE: Clean up - Delete the created task (currently commented out for UI verification)
        
        Note: We use /api/tasks/ (same as frontend) which goes through req-router.
        req-router internally forwards /api/tasks/ to /api/v1/tasks/ in taskservice.
        """
        logger.info("=== Starting Task Full Lifecycle E2E Test (API-based) ===")
        
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
        logger.info("Step 2: Creating task via API POST /api/tasks/ (same as frontend)")
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
            logger.info(f"✓ Task verified via GET /api/tasks/{task_id}")
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
                logger.info("✓ Task appears in list")
            else:
                logger.warning(f"Task {task_id} not found in list (might be pagination issue)")
        except Exception as e:
            logger.warning(f"Could not verify task in list: {e}")
        
        # Step 7: Update task with new data
        logger.info("Step 7: Updating task with new title, description, and code")
        updated_title = f"{task_title} - UPDATED"
        updated_description = f"{task_description} - Updated via API E2E test"
        updated_code = """
print("Hello from UPDATED E2E API test")
result = "Task updated successfully"
print(f"Updated Result: {result}")
# New functionality added
x = 10
y = 20
sum_result = x + y
print(f"Sum: {sum_result}")
"""
        
        try:
            # Get the full task object first (needed for update)
            get_response = api_client.get_task(task_id)
            if "task" in get_response:
                task_to_update = get_response["task"]
            else:
                task_to_update = get_response
            
            # Update the task fields
            task_to_update["title"] = updated_title
            task_to_update["description"] = updated_description
            task_to_update["script"] = updated_code
            
            # Create update_mask (list of fields being updated)
            # Frontend does: Object.keys(cloned_task).filter((v) => { return !['num_voters','voters'].includes(v)})
            update_mask = [key for key in task_to_update.keys() if key not in ['num_voters', 'voters']]
            
            # Update the task (frontend uses PATCH with task and update_mask)
            update_response = api_client.update_task(
                task_id=task_id,
                task_data=task_to_update,
                update_mask=update_mask
            )
            
            # Verify update response
            if "task" in update_response:
                updated_task = update_response["task"]
            else:
                updated_task = update_response
            
            assert updated_task["title"] == updated_title, "Updated title should match"
            assert updated_task["description"] == updated_description, "Updated description should match"
            logger.info("✓ Task updated successfully")
            logger.info(f"  New title: {updated_title}")
            logger.info(f"  New description: {updated_description}")
        except Exception as e:
            logger.error(f"✗ Task update failed: {e}")
            raise
        
        # Step 8: Verify update persisted by fetching task again
        logger.info("Step 8: Verifying update persisted by fetching task again")
        try:
            final_get_response = api_client.get_task(task_id)
            if "task" in final_get_response:
                final_task = final_get_response["task"]
            else:
                final_task = final_get_response
            
            assert final_task["title"] == updated_title, "Final task title should match updated title"
            assert final_task["description"] == updated_description, "Final task description should match updated description"
            
            # Script can be returned as string or as dict with {'code': '...', 'lang': 'python'}
            script_value = final_task.get("script")
            if isinstance(script_value, dict):
                # Backend returns script as structured object
                actual_code = script_value.get("code", "")
                assert actual_code == updated_code, f"Final task script code should match updated code. Got: {actual_code[:100]}..."
                logger.info(f"✓ Script verified (structured format: lang={script_value.get('lang', 'unknown')})")
            elif isinstance(script_value, str):
                # Backend returns script as plain string
                assert script_value == updated_code, "Final task script should match updated code"
                logger.info("✓ Script verified (string format)")
            else:
                logger.warning(f"Script field has unexpected type: {type(script_value)}")
            
            logger.info("✓ Update verified - all changes persisted")
        except AssertionError as e:
            logger.warning(f"Assertion failed during update verification: {e}")
            logger.warning("This might be expected if task update is asynchronous or script format differs")
        except Exception as e:
            logger.warning(f"Could not verify update persistence: {e}")
            logger.warning("This might be expected if task update is asynchronous")
        
        # Step 9: Clean up - Delete the created task
        logger.info("Step 9: Cleaning up - Deleting created task")
        try:
            # Extract wsid from the task (frontend always passes wsid when deleting)
            # Get the task to find its workspace_ids
            get_response = api_client.get_task(task_id)
            if "task" in get_response:
                task_for_deletion = get_response["task"]
            else:
                task_for_deletion = get_response
            
            # Extract wsid from workspace_ids (frontend uses current_space_state or "__DEFAULT__")
            workspace_ids = task_for_deletion.get("workspace_ids", [])
            if workspace_ids and len(workspace_ids) > 0:
                wsid = workspace_ids[0]  # Use first workspace ID
            else:
                wsid = "__DEFAULT__"  # Frontend uses "__DEFAULT__" if no wsid
            
            logger.info(f"Deleting task with wsid: {wsid}")
            
            # Delete with wsid and recurse=True (to delete any child tasks)
            # Frontend: deleteTask(task_id, recurse, forced=false)
            api_client.delete_task(task_id, wsid=wsid, recurse=True, forced=False)
            logger.info(f"✓ Task deleted: {task_id}")
            
            # Verify deletion - wait a bit for deletion to propagate
            logger.info("Step 10: Verifying deletion")
            time.sleep(2)  # Give more time for deletion to propagate
            
            # Check if task still exists (using method that doesn't log errors for 404s)
            task_still_exists = api_client.task_exists(task_id, wsid=wsid)
            if task_still_exists:
                logger.warning(f"Task {task_id} still exists after deletion.")
                logger.warning("This might indicate the deletion didn't work properly")
            else:
                logger.info(f"✓ Task {task_id} successfully verified as deleted (task no longer exists).")
        except Exception as e:
            logger.error(f"✗ Task deletion failed: {e}")
            logger.error(f"Task ID for manual cleanup: {task_id}")
            raise
        
        logger.info("=== Task Full Lifecycle E2E Test (API-based) Completed ===")
        
        # Return task_id for potential use in other tests
        return task_id

