"""
Unit tests for Task Search functionality in TaskService.

Tests task search using the list endpoint with query parameter (GET /api/v1/tasks/?q=...).
This matches how the UI performs searches.
"""

import pytest
from utils.fixtures import TestDataFactory


@pytest.mark.unit
@pytest.mark.task
class TestTaskSearch:
    """Test suite for task search operations (using list endpoint with query parameter)."""
    
    def test_search_tasks_by_title(self, taskservice_client, test_data_factory):
        """Test searching tasks by title."""
        unique_title = f"Unique Search Test Task {pytest.timestamp}"
        task_data = test_data_factory.create_task_data(title=unique_title)
        
        try:
            # Create task
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            # Search for it
            search_results = taskservice_client.search_tasks(unique_title)
            
            assert "tasks" in search_results or "hits" in search_results
            # Verify our task is in results
            tasks = search_results.get("tasks", search_results.get("hits", []))
            found = any(t.get("id") == task_id for t in tasks)
            assert found, f"Task {task_id} not found in search results"
            
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_search_tasks_by_tag(self, taskservice_client, test_data_factory):
        """Test searching tasks by tag."""
        unique_tag = f"test-tag-{pytest.timestamp}"
        task_data = test_data_factory.create_task_data(tags=[unique_tag, "test"])
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            # Search by tag
            search_results = taskservice_client.search_tasks(unique_tag)
            
            tasks = search_results.get("tasks", search_results.get("hits", []))
            found = any(t.get("id") == task_id for t in tasks)
            assert found, f"Task {task_id} not found when searching by tag"
            
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_search_tasks_by_description(self, taskservice_client, test_data_factory):
        """Test searching tasks by description content."""
        unique_desc = f"Unique description content for search {pytest.timestamp}"
        task_data = test_data_factory.create_task_data(description=unique_desc)
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            # Search by description
            search_results = taskservice_client.search_tasks(unique_desc)
            
            tasks = search_results.get("tasks", search_results.get("hits", []))
            found = any(t.get("id") == task_id for t in tasks)
            assert found, "Task not found when searching by description"
            
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_search_nonexistent_task(self, taskservice_client):
        """Test searching for tasks that don't exist."""
        search_results = taskservice_client.search_tasks(
            "nonexistent-unique-search-term-12345"
        )
        
        tasks = search_results.get("tasks", search_results.get("hits", []))
        assert len(tasks) == 0 or all(
            "nonexistent-unique-search-term-12345" not in str(t) 
            for t in tasks
        )
    
    def test_search_with_knn_parameters(self, taskservice_client, test_data_factory):
        """Test UI search with KNN vector similarity parameters."""
        import logging
        unique_title = f"KNN Search Task {pytest.timestamp}"
        task_data = test_data_factory.create_task_data(
            title=unique_title,
            description="This tests the KNN vector similarity search"
        )
        task_id = None
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            # Search with KNN parameters (as UI does)
            search_params = {
                'knn.k': 3,
                'knn.nc': 10,
                'order_by': 'elastic'
            }
            search_results = taskservice_client.search_tasks(
                unique_title, 
                params=search_params
            )
            
            tasks = search_results.get("tasks", search_results.get("hits", []))
            # Should find the task using vector similarity
            found = any(t.get("id") == task_id for t in tasks)
            assert found, "Task not found with KNN search parameters"
            
        finally:
            # DELETE endpoint is broken (returns 500), ignore cleanup errors
            if task_id:
                try:
                    taskservice_client.delete_task(task_id)
                except Exception as e:
                    logging.warning(f"Failed to cleanup task {task_id}: {e}")


@pytest.mark.unit
@pytest.mark.task
class TestTaskList:
    """Test suite for listing tasks."""
    
    def test_list_tasks(self, taskservice_client, test_tasks):
        """Test listing all tasks."""
        response = taskservice_client.list_tasks()
        
        assert "tasks" in response or "hits" in response
        tasks = response.get("tasks", response.get("hits", []))
        
        # Verify our test tasks are in the list
        task_ids = [t["id"] for t in test_tasks]
        found_ids = [t.get("id") for t in tasks if t.get("id") in task_ids]
        
        assert len(found_ids) > 0, "No test tasks found in list"
    
    def test_list_tasks_with_pagination(self, taskservice_client):
        """Test listing tasks with pagination."""
        # Backend uses 'page_size' and 'page_key' for pagination
        response = taskservice_client.list_tasks(params={"page_size": 5, "page_key": "0"})
        
        tasks = response.get("tasks", response.get("hits", []))
        assert len(tasks) <= 5, f"Expected at most 5 tasks, got {len(tasks)}"
        
        # Verify pagination response exists
        pagination = response.get("pagination", {})
        assert "next_page_key" in pagination
        assert "has_more_results" in pagination
    
    def test_list_tasks_with_filters(self, taskservice_client, test_data_factory):
        """Test listing tasks with filters."""
        import logging
        unique_tag = f"filter-test-{pytest.timestamp}"
        task_data = test_data_factory.create_task_data(tags=[unique_tag])
        task_id = None
        
        try:
            response = taskservice_client.create_task(task_data)
            task_id = response["task"]["id"]
            
            # List with tag filter
            filtered = taskservice_client.list_tasks(
                params={"tags": unique_tag}
            )
            
            tasks = filtered.get("tasks", filtered.get("hits", []))
            found = any(t.get("id") == task_id for t in tasks)
            assert found, "Task not found with tag filter"
            
        finally:
            # DELETE endpoint is broken (returns 500), ignore cleanup errors
            if task_id:
                try:
                    taskservice_client.delete_task(task_id)
                except Exception as e:
                    logging.warning(f"Failed to cleanup task {task_id}: {e}")


# Add timestamp to pytest for unique identifiers in tests
@pytest.fixture(scope="session", autouse=True)
def add_pytest_timestamp():
    """Add a timestamp attribute to pytest for generating unique values."""
    import time
    pytest.timestamp = int(time.time())

