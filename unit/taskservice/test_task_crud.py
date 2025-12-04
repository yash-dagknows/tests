"""
Unit tests for Task CRUD operations in TaskService.
"""

import pytest
from utils.fixtures import TestDataFactory, create_basic_task
from utils.assertions import assert_task_equals, assert_has_required_fields, assert_response_success


@pytest.mark.unit
@pytest.mark.task
class TestTaskCRUD:
    """Test suite for task CRUD operations."""
    
    def test_create_basic_task(self, taskservice_client, test_data_factory):
        """Test creating a basic task."""
        task_data = test_data_factory.create_task_data()
        
        response = taskservice_client.create_task(task_data)
        
        assert "task" in response
        created_task = response["task"]
        
        # Verify required fields exist
        assert_has_required_fields(created_task, [
            "id", "title", "description", "script", 
            "script_type", "created_at"
        ])
        
        # Verify data matches
        assert created_task["title"] == task_data["title"]
        assert created_task["description"] == task_data["description"]
        assert created_task["script"] == task_data["script"]
        
        # Cleanup
        taskservice_client.delete_task(created_task["id"])
    
    def test_create_task_with_custom_id(self, taskservice_client):
        """Test creating a task with a custom ID."""
        custom_id = "custom-test-task-123"
        task_data = create_basic_task()
        task_data["id"] = custom_id
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert created_task["id"] == custom_id
        finally:
            taskservice_client.delete_task(custom_id)
    
    def test_create_task_duplicate_id_fails(self, taskservice_client):
        """Test that creating a task with duplicate ID fails."""
        custom_id = "duplicate-id-test"
        task_data = create_basic_task()
        task_data["id"] = custom_id
        
        try:
            # Create first task
            taskservice_client.create_task(task_data)
            
            # Try to create duplicate
            with pytest.raises(Exception) as exc_info:
                taskservice_client.create_task(task_data)
            
            assert "already exists" in str(exc_info.value).lower()
        finally:
            taskservice_client.delete_task(custom_id)
    
    def test_get_task(self, taskservice_client, test_task):
        """Test retrieving a task by ID."""
        fetched_task = taskservice_client.get_task(test_task["id"])
        
        assert fetched_task["task"]["id"] == test_task["id"]
        assert fetched_task["task"]["title"] == test_task["title"]
    
    def test_get_nonexistent_task_fails(self, taskservice_client):
        """Test that getting a non-existent task fails."""
        fake_id = "nonexistent-task-id-12345"
        
        with pytest.raises(Exception) as exc_info:
            taskservice_client.get_task(fake_id)
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_update_task(self, taskservice_client, test_task):
        """Test updating a task."""
        updates = {
            "title": "Updated Title",
            "description": "Updated Description",
            "tags": ["updated", "test"],
        }
        update_fields = list(updates.keys())
        
        taskservice_client.update_task(
            test_task["id"], 
            updates, 
            update_fields
        )
        
        # Fetch and verify
        fetched = taskservice_client.get_task(test_task["id"])
        updated_task = fetched["task"]
        
        assert updated_task["title"] == updates["title"]
        assert updated_task["description"] == updates["description"]
        assert set(updated_task["tags"]) == set(updates["tags"])
    
    def test_update_task_script(self, taskservice_client, test_task):
        """Test updating a task's script."""
        new_script = "echo 'This is updated script'"
        updates = {"script": new_script}
        
        taskservice_client.update_task(
            test_task["id"],
            updates,
            ["script"]
        )
        
        fetched = taskservice_client.get_task(test_task["id"])
        assert fetched["task"]["script"] == new_script
    
    def test_delete_task(self, taskservice_client):
        """Test deleting a task."""
        # Create a task
        task_data = create_basic_task()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        # Delete it
        taskservice_client.delete_task(task_id)
        
        # Verify it's gone
        with pytest.raises(Exception) as exc_info:
            taskservice_client.get_task(task_id)
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_delete_nonexistent_task_fails(self, taskservice_client):
        """Test that deleting a non-existent task fails."""
        fake_id = "nonexistent-task-to-delete"
        
        with pytest.raises(Exception) as exc_info:
            taskservice_client.delete_task(fake_id)
        
        assert "not found" in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.task
class TestTaskWithCommands:
    """Test suite for tasks with command lists."""
    
    def test_create_task_with_commands(self, taskservice_client, test_data_factory):
        """Test creating a task with command list."""
        task_data = test_data_factory.create_task_with_commands(
            commands=["ls -la", "pwd", "date"]
        )
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert created_task["script_type"] == "command"
            assert len(created_task["commands"]) == 3
            assert "ls -la" in created_task["commands"]
        finally:
            taskservice_client.delete_task(created_task["id"])
    
    def test_update_task_commands(self, taskservice_client, test_data_factory):
        """Test updating task commands."""
        task_data = test_data_factory.create_task_with_commands()
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            new_commands = ["echo 'updated'", "whoami"]
            taskservice_client.update_task(
                task_id,
                {"commands": new_commands},
                ["commands"]
            )
            
            fetched = taskservice_client.get_task(task_id)
            assert len(fetched["task"]["commands"]) == 2
        finally:
            taskservice_client.delete_task(task_id)


@pytest.mark.unit
@pytest.mark.task
class TestTaskWithParameters:
    """Test suite for tasks with input/output parameters."""
    
    def test_create_task_with_params(self, taskservice_client, test_data_factory):
        """Test creating a task with parameters."""
        task_data = test_data_factory.create_task_with_params()
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert "input_params" in created_task
            assert "output_params" in created_task
            assert len(created_task["input_params"]) > 0
        finally:
            taskservice_client.delete_task(created_task["id"])
    
    def test_task_param_validation(self, taskservice_client, test_data_factory):
        """Test that task parameter validation works."""
        task_data = test_data_factory.create_task_with_params(
            input_params=[
                {"name": "required_param", "type": "string", "required": True},
            ]
        )
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            fetched = taskservice_client.get_task(task_id)
            params = fetched["task"]["input_params"]
            
            required_param = next(p for p in params if p["name"] == "required_param")
            assert required_param["required"] is True
        finally:
            taskservice_client.delete_task(response["task"]["id"])


@pytest.mark.unit
@pytest.mark.task
class TestTaskTags:
    """Test suite for task tagging functionality."""
    
    def test_create_task_with_tags(self, taskservice_client):
        """Test creating a task with tags."""
        task_data = create_basic_task()
        task_data["tags"] = ["test", "unit", "automation"]
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert set(created_task["tags"]) == set(task_data["tags"])
        finally:
            taskservice_client.delete_task(created_task["id"])
    
    def test_update_task_tags(self, taskservice_client, test_task):
        """Test updating task tags."""
        new_tags = ["updated", "tags", "test"]
        
        taskservice_client.update_task(
            test_task["id"],
            {"tags": new_tags},
            ["tags"]
        )
        
        fetched = taskservice_client.get_task(test_task["id"])
        assert set(fetched["task"]["tags"]) == set(new_tags)
    
    def test_clear_task_tags(self, taskservice_client, test_task):
        """Test clearing task tags."""
        taskservice_client.update_task(
            test_task["id"],
            {"tags": []},
            ["tags"]
        )
        
        fetched = taskservice_client.get_task(test_task["id"])
        assert fetched["task"]["tags"] == []

