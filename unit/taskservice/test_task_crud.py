"""
Unit tests for Task CRUD operations in TaskService.

This test suite covers:
1. Python script tasks (script_type: "python")
2. Shell script tasks (script_type: "shell" or "bash")
3. Command-type tasks (script_type: "command" with commands array)
"""

import pytest
from utils.fixtures import (
    TestDataFactory, 
    create_basic_task, 
    create_python_task, 
    create_bash_task,
    create_command_task
)
from utils.assertions import assert_task_equals, assert_has_required_fields, assert_response_success


@pytest.mark.unit
@pytest.mark.task
class TestPythonTaskCRUD:
    """Test suite for Python script task CRUD operations."""
    
    def test_create_python_task(self, taskservice_client, test_data_factory):
        """Test creating a Python script task."""
        task_data = test_data_factory.create_python_task_data()
        
        response = taskservice_client.create_task(task_data)
        
        assert "task" in response
        created_task = response["task"]
        
        # Verify required fields exist
        assert_has_required_fields(created_task, [
            "id", "title", "description", "script", 
            "script_type", "created_at"
        ])
        
        # Verify it's a Python task
        assert created_task["script_type"] == "python"
        assert created_task["title"] == task_data["title"]
        assert created_task["description"] == task_data["description"]
        
        # Script may be returned as string or as {"lang": "...", "code": "..."}
        if isinstance(created_task["script"], dict):
            assert created_task["script"]["code"] == task_data["script"]
        else:
            assert created_task["script"] == task_data["script"]
        
        # Cleanup
        taskservice_client.delete_task(created_task["id"])
    
    def test_create_python_task_with_custom_id(self, taskservice_client):
        """Test creating a Python task with a custom ID."""
        import time
        custom_id = f"python-task-{int(time.time())}"
        task_data = create_python_task()
        task_data["id"] = custom_id
        
        try:
            # Delete if exists from previous run
            try:
                taskservice_client.delete_task(custom_id)
            except:
                pass
            
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert created_task["id"] == custom_id
            assert created_task["script_type"] == "python"
        finally:
            taskservice_client.delete_task(custom_id)
    
    def test_get_python_task(self, taskservice_client, test_data_factory):
        """Test retrieving a Python task by ID."""
        task_data = test_data_factory.create_python_task_data()
        
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        try:
            fetched = taskservice_client.get_task(task_id)
            
            assert fetched["task"]["id"] == task_id
            assert fetched["task"]["script_type"] == "python"
            assert fetched["task"]["title"] == task_data["title"]
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_update_python_task(self, taskservice_client, test_data_factory):
        """Test updating a Python task's script."""
        task_data = test_data_factory.create_python_task_data()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        try:
            new_script = "print('Updated Python script')\nprint('Line 2')"
            updates = {"script": new_script}
            
            taskservice_client.update_task(
                task_id,
                updates,
                ["script"]
            )
            
            fetched = taskservice_client.get_task(task_id)
            fetched_script = fetched["task"]["script"]
            
            # Script may be returned as string or dict
            if isinstance(fetched_script, dict):
                assert fetched_script["code"] == new_script
            else:
                assert fetched_script == new_script
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_update_python_task_metadata(self, taskservice_client, test_data_factory):
        """Test updating a Python task's title and description."""
        task_data = test_data_factory.create_python_task_data()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        try:
            updates = {
                "title": "Updated Python Task",
                "description": "Updated description for Python task",
                "tags": ["python", "updated", "test"],
            }
            update_fields = list(updates.keys())
            
            taskservice_client.update_task(task_id, updates, update_fields)
            
            fetched = taskservice_client.get_task(task_id)
            updated_task = fetched["task"]
            
            assert updated_task["title"] == updates["title"]
            assert updated_task["description"] == updates["description"]
            assert set(updated_task["tags"]) == set(updates["tags"])
            assert updated_task["script_type"] == "python"  # Should remain Python
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_delete_python_task(self, taskservice_client, test_data_factory):
        """Test deleting a Python task."""
        task_data = test_data_factory.create_python_task_data()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        # Delete it
        delete_response = taskservice_client.delete_task(task_id)
        
        # Verify delete succeeded
        assert delete_response is not None or delete_response == {}


@pytest.mark.unit
@pytest.mark.task
class TestShellTaskCRUD:
    """Test suite for Shell/Bash script task CRUD operations."""
    
    def test_create_shell_task(self, taskservice_client, test_data_factory):
        """Test creating a shell script task."""
        task_data = test_data_factory.create_shell_task_data()
        
        response = taskservice_client.create_task(task_data)
        created_task = response["task"]
        
        assert created_task["script_type"] == "shell"
        assert "script" in created_task
        
        # Cleanup
        taskservice_client.delete_task(created_task["id"])
    
    def test_create_bash_task(self, taskservice_client, test_data_factory):
        """Test creating a bash script task."""
        task_data = test_data_factory.create_bash_task_data()
        
        response = taskservice_client.create_task(task_data)
        created_task = response["task"]
        
        assert created_task["script_type"] == "bash"
        assert "script" in created_task
        
        # Cleanup
        taskservice_client.delete_task(created_task["id"])
    
    def test_update_shell_task_script(self, taskservice_client, test_data_factory):
        """Test updating a shell task's script."""
        task_data = test_data_factory.create_shell_task_data()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        try:
            new_script = "#!/bin/sh\necho 'Updated shell script'\nls -la"
            updates = {"script": new_script}
            
            taskservice_client.update_task(task_id, updates, ["script"])
            
            fetched = taskservice_client.get_task(task_id)
            fetched_script = fetched["task"]["script"]
            
            if isinstance(fetched_script, dict):
                assert fetched_script["code"] == new_script
            else:
                assert fetched_script == new_script
        finally:
            taskservice_client.delete_task(task_id)


@pytest.mark.unit
@pytest.mark.task
class TestCommandTaskCRUD:
    """Test suite for command-type task CRUD operations."""
    
    def test_create_command_task(self, taskservice_client, test_data_factory):
        """Test creating a command-type task."""
        task_data = test_data_factory.create_task_with_commands(
            commands=["ls -la", "pwd", "date"]
        )
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            # Verify it's a command-type task
            assert created_task["script_type"] == "command"
            assert "commands" in created_task
            assert len(created_task["commands"]) == 3
            assert "ls -la" in created_task["commands"]
            assert "pwd" in created_task["commands"]
            assert "date" in created_task["commands"]
        finally:
            taskservice_client.delete_task(created_task["id"])
    
    def test_create_command_task_with_custom_id(self, taskservice_client):
        """Test creating a command-type task with custom ID."""
        import time
        custom_id = f"command-task-{int(time.time())}"
        task_data = create_command_task()
        task_data["id"] = custom_id
        
        try:
            # Delete if exists from previous run
            try:
                taskservice_client.delete_task(custom_id)
            except:
                pass
            
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert created_task["id"] == custom_id
            assert created_task["script_type"] == "command"
            assert "commands" in created_task
        finally:
            taskservice_client.delete_task(custom_id)
    
    def test_get_command_task(self, taskservice_client, test_data_factory):
        """Test retrieving a command-type task by ID."""
        task_data = test_data_factory.create_task_with_commands()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        try:
            fetched = taskservice_client.get_task(task_id)
            
            assert fetched["task"]["id"] == task_id
            assert fetched["task"]["script_type"] == "command"
            assert "commands" in fetched["task"]
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_update_command_task_commands(self, taskservice_client, test_data_factory):
        """Test updating task commands (includes script_type in update_mask per current backend requirement)."""
        task_data = test_data_factory.create_task_with_commands()
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            # Update commands (include script_type in update_mask as backend expects)
            new_commands = ["echo 'updated'", "whoami"]
            taskservice_client.update_task(
                task_id,
                {"commands": new_commands, "script_type": "command"},
                ["commands", "script_type"]  # Backend requires script_type in mask
            )
            
            fetched = taskservice_client.get_task(task_id)
            
            # Verify commands were updated
            assert len(fetched["task"]["commands"]) == 2
            assert "echo 'updated'" in fetched["task"]["commands"]
            assert "whoami" in fetched["task"]["commands"]
            assert fetched["task"]["script_type"] == "command"
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_update_command_task_add_commands(self, taskservice_client, test_data_factory):
        """Test updating command task to add more commands."""
        task_data = test_data_factory.create_task_with_commands(
            commands=["echo 'initial'"]
        )
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            # Add more commands (include script_type per backend requirement)
            new_commands = ["echo 'first'", "echo 'second'", "echo 'third'", "ls"]
            taskservice_client.update_task(
                task_id,
                {"commands": new_commands, "script_type": "command"},
                ["commands", "script_type"]
            )
            
            fetched = taskservice_client.get_task(task_id)
            assert len(fetched["task"]["commands"]) == 4
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_update_command_task_metadata(self, taskservice_client, test_data_factory):
        """Test updating command task's title and tags without changing commands."""
        task_data = test_data_factory.create_task_with_commands()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        original_commands = response["task"]["commands"]
        
        try:
            updates = {
                "title": "Updated Command Task",
                "tags": ["command", "updated"],
            }
            
            taskservice_client.update_task(
                task_id,
                updates,
                ["title", "tags"]
            )
            
            fetched = taskservice_client.get_task(task_id)
            
            # Verify metadata updated but commands unchanged
            assert fetched["task"]["title"] == updates["title"]
            assert set(fetched["task"]["tags"]) == set(updates["tags"])
            assert fetched["task"]["commands"] == original_commands
            assert fetched["task"]["script_type"] == "command"
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_delete_command_task(self, taskservice_client, test_data_factory):
        """Test deleting a command-type task."""
        task_data = test_data_factory.create_task_with_commands()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        delete_response = taskservice_client.delete_task(task_id)
        assert delete_response is not None or delete_response == {}


@pytest.mark.unit
@pytest.mark.task
class TestTaskGeneralOperations:
    """Test suite for general task operations (non-type specific)."""
    
    def test_create_task_duplicate_id_fails(self, taskservice_client):
        """Test that creating a task with duplicate ID fails."""
        import time
        custom_id = f"duplicate-id-test-{int(time.time())}"
        task_data = create_basic_task()
        task_data["id"] = custom_id
        
        try:
            # Clean up any existing task with this ID
            try:
                taskservice_client.delete_task(custom_id)
            except:
                pass
            
            # Create first task
            taskservice_client.create_task(task_data)
            
            # Try to create duplicate
            with pytest.raises(Exception) as exc_info:
                taskservice_client.create_task(task_data)
            
            assert "already exists" in str(exc_info.value).lower() or "conflict" in str(exc_info.value).lower()
        finally:
            taskservice_client.delete_task(custom_id)
    
    def test_get_nonexistent_task_fails(self, taskservice_client):
        """Test that getting a non-existent task fails."""
        fake_id = "nonexistent-task-id-12345"
        
        with pytest.raises(Exception) as exc_info:
            taskservice_client.get_task(fake_id)
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_delete_nonexistent_task_idempotent(self, taskservice_client):
        """Test that deleting a non-existent task is idempotent."""
        import time
        fake_id = f"nonexistent-task-to-delete-{int(time.time())}"
        
        # DELETE should be idempotent - doesn't crash on non-existent tasks
        try:
            result = taskservice_client.delete_task(fake_id)
            assert result is not None or result == {}
        except Exception as e:
            # Or if it raises an error, verify it's the right error
            assert "not found" in str(e).lower()


@pytest.mark.unit
@pytest.mark.task
class TestTaskWithParameters:
    """Test suite for tasks with input/output parameters."""
    
    def test_create_python_task_with_params(self, taskservice_client, test_data_factory):
        """Test creating a Python task with parameters."""
        task_data = test_data_factory.create_task_with_params()
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert "input_params" in created_task
            assert "output_params" in created_task
            assert len(created_task["input_params"]) > 0
        finally:
            taskservice_client.delete_task(created_task["id"])
    
    def test_create_command_task_with_params(self, taskservice_client, test_data_factory):
        """Test creating a command task with parameters."""
        task_data = test_data_factory.create_task_with_commands(
            commands=["echo <param1>", "echo <param2>"]
        )
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            # Commands with <param> should auto-generate input_params
            assert created_task["script_type"] == "command"
            # The backend should extract params from commands
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
    
    def test_create_python_task_with_tags(self, taskservice_client):
        """Test creating a Python task with tags."""
        task_data = create_python_task()
        task_data["tags"] = ["python", "test", "unit", "automation"]
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert set(created_task["tags"]) == set(task_data["tags"])
            assert created_task["script_type"] == "python"
        finally:
            taskservice_client.delete_task(created_task["id"])
    
    def test_create_command_task_with_tags(self, taskservice_client):
        """Test creating a command task with tags."""
        task_data = create_command_task()
        task_data["tags"] = ["command", "test", "cli"]
        
        try:
            response = taskservice_client.create_task(task_data)
            created_task = response["task"]
            
            assert set(created_task["tags"]) == set(task_data["tags"])
            assert created_task["script_type"] == "command"
        finally:
            taskservice_client.delete_task(created_task["id"])
    
    def test_update_task_tags(self, taskservice_client, test_data_factory):
        """Test updating task tags."""
        task_data = test_data_factory.create_python_task_data()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        try:
            new_tags = ["updated", "tags", "test"]
            
            taskservice_client.update_task(
                task_id,
                {"tags": new_tags},
                ["tags"]
            )
            
            fetched = taskservice_client.get_task(task_id)
            assert set(fetched["task"]["tags"]) == set(new_tags)
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_clear_task_tags(self, taskservice_client, test_data_factory):
        """Test clearing task tags."""
        task_data = test_data_factory.create_python_task_data()
        response = taskservice_client.create_task(task_data)
        task_id = response["task"]["id"]
        
        try:
            taskservice_client.update_task(
                task_id,
                {"tags": []},
                ["tags"]
            )
            
            fetched = taskservice_client.get_task(task_id)
            assert fetched["task"]["tags"] == []
        finally:
            taskservice_client.delete_task(task_id)
