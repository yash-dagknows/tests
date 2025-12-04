"""
Unit tests for Workspace operations in TaskService.
"""

import pytest
from utils.fixtures import TestDataFactory
from utils.assertions import assert_has_required_fields


@pytest.mark.unit
@pytest.mark.workspace
class TestWorkspaceCRUD:
    """Test suite for workspace CRUD operations."""
    
    def test_create_workspace(self, taskservice_client, test_data_factory):
        """Test creating a workspace."""
        workspace_data = test_data_factory.create_workspace_data()
        
        try:
            response = taskservice_client.create_workspace(workspace_data)
            workspace = response.get("workspace", response)
            
            assert_has_required_fields(workspace, ["id", "name", "description"])
            assert workspace["name"] == workspace_data["name"]
            
        finally:
            taskservice_client.delete_workspace(workspace["id"])
    
    def test_get_workspace(self, taskservice_client, test_workspace):
        """Test retrieving a workspace by ID."""
        response = taskservice_client.get_workspace(test_workspace["id"])
        workspace = response.get("workspace", response)
        
        assert workspace["id"] == test_workspace["id"]
        assert workspace["name"] == test_workspace["name"]
    
    def test_update_workspace(self, taskservice_client, test_workspace):
        """Test updating a workspace."""
        updates = {
            "name": "Updated Workspace Name",
            "description": "Updated description",
        }
        
        taskservice_client.update_workspace(test_workspace["id"], updates)
        
        response = taskservice_client.get_workspace(test_workspace["id"])
        updated = response.get("workspace", response)
        
        assert updated["name"] == updates["name"]
        assert updated["description"] == updates["description"]
    
    def test_delete_workspace(self, taskservice_client, test_data_factory):
        """Test deleting a workspace."""
        workspace_data = test_data_factory.create_workspace_data()
        response = taskservice_client.create_workspace(workspace_data)
        workspace_id = response.get("workspace", response)["id"]
        
        # Delete
        taskservice_client.delete_workspace(workspace_id)
        
        # Verify deleted
        with pytest.raises(Exception):
            taskservice_client.get_workspace(workspace_id)
    
    def test_list_workspaces(self, taskservice_client, test_workspace):
        """Test listing workspaces."""
        response = taskservice_client.list_workspaces()
        
        workspaces = response.get("workspaces", response.get("items", []))
        assert len(workspaces) > 0
        
        # Verify our test workspace is in the list
        found = any(w.get("id") == test_workspace["id"] for w in workspaces)
        assert found, f"Test workspace {test_workspace['id']} not found in list"


@pytest.mark.unit
@pytest.mark.workspace
@pytest.mark.task
class TestWorkspaceTaskAssociation:
    """Test suite for workspace-task associations."""
    
    def test_create_task_in_workspace(self, taskservice_client, test_workspace, test_data_factory):
        """Test creating a task within a workspace."""
        task_data = test_data_factory.create_task_data()
        task_data["workspace_id"] = test_workspace["id"]
        
        try:
            response = taskservice_client.create_task(task_data)
            task = response["task"]
            
            assert task.get("workspace_id") == test_workspace["id"]
            
        finally:
            taskservice_client.delete_task(task["id"])
    
    def test_list_tasks_in_workspace(self, taskservice_client, test_workspace, test_data_factory):
        """Test listing tasks within a specific workspace."""
        # Create a task in the workspace
        task_data = test_data_factory.create_task_data()
        task_data["workspace_id"] = test_workspace["id"]
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            # List tasks in workspace
            tasks = taskservice_client.list_tasks(
                params={"workspace_id": test_workspace["id"]}
            )
            
            task_list = tasks.get("tasks", tasks.get("hits", []))
            found = any(t.get("id") == task_id for t in task_list)
            assert found, "Task not found in workspace task list"
            
        finally:
            taskservice_client.delete_task(task_id)

