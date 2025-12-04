"""
End-to-end tests for complete task lifecycle.

Tests task creation, editing, saving, execution, and management.
"""

import pytest
import time
from utils.fixtures import TestDataFactory


@pytest.mark.e2e
@pytest.mark.task
@pytest.mark.slow
class TestCompleteTaskLifecycle:
    """End-to-end test for complete task lifecycle."""
    
    def test_complete_task_lifecycle(
        self,
        req_router_client,
        taskservice_client,
        authenticated_user,
        test_data_factory
    ):
        """
        Test complete task lifecycle from creation to deletion.
        
        Flow:
        1. User creates a new task
        2. User views the task
        3. User edits the task (multiple times)
        4. User saves the task
        5. User adds tags to categorize
        6. User searches for the task
        7. User duplicates the task
        8. User deletes tasks
        """
        try:
            # Step 1: Create task
            print("\n[E2E] Step 1: Creating task...")
            task_data = test_data_factory.create_task_data(
                title="Database Backup Script",
                description="Script to backup production database",
                script="#!/bin/bash\n# Backup script\necho 'Starting backup...'",
                tags=["database", "backup"]
            )
            response = req_router_client.create_task(task_data)
            task = response.get("task", response)
            task_id = task["id"]
            print(f"[E2E] Task created: {task_id}")
            
            # Step 2: View task
            print("\n[E2E] Step 2: Viewing task...")
            fetched = req_router_client.get_task(task_id)
            fetched_task = fetched.get("task", fetched)
            assert fetched_task["id"] == task_id
            assert fetched_task["title"] == task_data["title"]
            print("[E2E] Task viewed successfully")
            
            # Step 3: Edit task (first edit)
            print("\n[E2E] Step 3: Editing task (iteration 1)...")
            req_router_client.update_task(task_id, {
                "script": "#!/bin/bash\n# Backup script v2\necho 'Starting backup...'\npg_dump mydb > backup.sql"
            })
            print("[E2E] Task edited (added pg_dump command)")
            
            # Edit task (second edit)
            print("\n[E2E] Editing task (iteration 2)...")
            req_router_client.update_task(task_id, {
                "script": "#!/bin/bash\n# Backup script v3\necho 'Starting backup...'\npg_dump mydb > backup.sql\necho 'Backup complete!'"
            })
            print("[E2E] Task edited (added completion message)")
            
            # Step 4: Save task (verify updates persisted)
            print("\n[E2E] Step 4: Verifying task saved...")
            updated = req_router_client.get_task(task_id)
            updated_task = updated.get("task", updated)
            assert "Backup complete" in updated_task["script"]
            print("[E2E] Task changes saved successfully")
            
            # Step 5: Add more tags
            print("\n[E2E] Step 5: Adding tags...")
            req_router_client.update_task(task_id, {
                "tags": ["database", "backup", "production", "postgresql"]
            })
            
            tagged = req_router_client.get_task(task_id)
            tagged_task = tagged.get("task", tagged)
            assert len(tagged_task["tags"]) == 4
            print(f"[E2E] Tags updated: {tagged_task['tags']}")
            
            # Step 6: Search for task
            print("\n[E2E] Step 6: Searching for task...")
            time.sleep(2)  # Wait for indexing
            search_results = req_router_client.search_tasks("Database Backup")
            tasks = search_results.get("tasks", search_results.get("hits", []))
            found = any(t.get("id") == task_id for t in tasks)
            assert found, "Task not found in search"
            print("[E2E] Task found via search")
            
            # Step 7: Duplicate task
            print("\n[E2E] Step 7: Duplicating task...")
            duplicate_data = test_data_factory.create_task_data(
                title=f"{task_data['title']} (Copy)",
                description=tagged_task["description"],
                script=tagged_task["script"],
                tags=tagged_task["tags"]
            )
            dup_response = req_router_client.create_task(duplicate_data)
            dup_task = dup_response.get("task", dup_response)
            dup_id = dup_task["id"]
            print(f"[E2E] Task duplicated: {dup_id}")
            
            # Verify duplicate has same content
            assert dup_task["script"] == tagged_task["script"]
            assert set(dup_task["tags"]) == set(tagged_task["tags"])
            
            # Step 8: Delete tasks
            print("\n[E2E] Step 8: Deleting tasks...")
            req_router_client.delete_task(task_id)
            req_router_client.delete_task(dup_id)
            print("[E2E] Tasks deleted")
            
            # Verify deletion
            with pytest.raises(Exception):
                req_router_client.get_task(task_id)
            with pytest.raises(Exception):
                req_router_client.get_task(dup_id)
            print("[E2E] Task lifecycle completed successfully!")
            
        except Exception as e:
            # Cleanup on failure
            try:
                req_router_client.delete_task(task_id)
            except:
                pass
            try:
                req_router_client.delete_task(dup_id)
            except:
                pass
            raise


@pytest.mark.e2e
@pytest.mark.task
class TestTaskCollaboration:
    """Test collaborative task management scenarios."""
    
    def test_multiple_users_working_on_tasks(
        self,
        req_router_client,
        taskservice_client,
        test_data_factory
    ):
        """
        Test multiple users collaborating on tasks.
        
        Flow:
        1. User A creates a task
        2. User B views and edits the task
        3. User A sees User B's changes
        4. Both users can search and find the task
        """
        # This test would require multiple user fixtures
        # Marking as placeholder for now
        pytest.skip("Multi-user collaboration test requires multiple user setup")


@pytest.mark.e2e
@pytest.mark.task
@pytest.mark.slow
class TestTaskWithParameters:
    """Test tasks with input/output parameters."""
    
    def test_parametrized_task_workflow(
        self,
        req_router_client,
        test_data_factory
    ):
        """
        Test workflow for tasks with parameters.
        
        Flow:
        1. Create task with input parameters
        2. Define output parameters
        3. Update parameter definitions
        4. Verify parameters are saved correctly
        """
        try:
            print("\n[E2E] Creating parametrized task...")
            
            task_data = test_data_factory.create_task_with_params(
                title="Parametrized Deployment Task",
                input_params=[
                    {"name": "environment", "type": "string", "required": True},
                    {"name": "version", "type": "string", "required": True},
                    {"name": "dry_run", "type": "boolean", "required": False}
                ],
                output_params=[
                    {"name": "deployment_id", "type": "string"},
                    {"name": "status", "type": "string"}
                ]
            )
            
            response = req_router_client.create_task(task_data)
            task = response.get("task", response)
            task_id = task["id"]
            print(f"[E2E] Parametrized task created: {task_id}")
            
            # Verify parameters
            assert len(task["input_params"]) == 3
            assert len(task["output_params"]) == 2
            
            # Update parameters
            print("\n[E2E] Updating parameters...")
            req_router_client.update_task(task_id, {
                "input_params": task_data["input_params"] + [
                    {"name": "timeout", "type": "integer", "required": False}
                ]
            })
            
            # Verify update
            updated = req_router_client.get_task(task_id)
            updated_task = updated.get("task", updated)
            assert len(updated_task["input_params"]) == 4
            print("[E2E] Parameters updated successfully")
            
            # Cleanup
            req_router_client.delete_task(task_id)
            print("\n[E2E] Parametrized task workflow completed!")
            
        except Exception as e:
            try:
                req_router_client.delete_task(task_id)
            except:
                pass
            raise

