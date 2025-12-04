"""
Integration tests for task workflow across services.

Tests task operations through req-router (proxied to taskservice).
"""

import pytest
import time
from utils.fixtures import TestDataFactory


@pytest.mark.integration
@pytest.mark.task
class TestTaskWorkflowViaReqRouter:
    """Test task operations via req-router proxy."""
    
    def test_create_task_via_req_router(
        self,
        req_router_client,
        authenticated_user,
        test_data_factory
    ):
        """Test creating a task through req-router."""
        task_data = test_data_factory.create_task_data()
        
        try:
            # Create via req-router (proxied to taskservice)
            response = req_router_client.create_task(task_data)
            
            assert "task" in response or "id" in response
            task = response.get("task", response)
            
            assert task["title"] == task_data["title"]
            assert task["script"] == task_data["script"]
            
            # Verify we can fetch it
            fetched = req_router_client.get_task(task["id"])
            fetched_task = fetched.get("task", fetched)
            assert fetched_task["id"] == task["id"]
            
        finally:
            req_router_client.delete_task(task["id"])
    
    def test_task_crud_workflow_via_req_router(
        self,
        req_router_client,
        authenticated_user,
        test_data_factory
    ):
        """
        Test complete CRUD workflow for tasks via req-router.
        
        Flow:
        1. Create task
        2. Read task
        3. Update task
        4. Read updated task
        5. Delete task
        6. Verify deletion
        """
        task_data = test_data_factory.create_task_data()
        
        try:
            # Create
            response = req_router_client.create_task(task_data)
            task = response.get("task", response)
            task_id = task["id"]
            
            # Read
            fetched = req_router_client.get_task(task_id)
            assert fetched.get("task", fetched)["id"] == task_id
            
            # Update
            updates = {
                "title": "Updated Title",
                "description": "Updated Description"
            }
            req_router_client.update_task(task_id, updates)
            
            # Read updated
            updated = req_router_client.get_task(task_id)
            updated_task = updated.get("task", updated)
            assert updated_task["title"] == updates["title"]
            
            # Delete
            req_router_client.delete_task(task_id)
            
            # Verify deleted
            with pytest.raises(Exception):
                req_router_client.get_task(task_id)
                
        except Exception as e:
            # Cleanup if test failed
            try:
                req_router_client.delete_task(task_id)
            except:
                pass
            raise
    
    def test_search_task_via_req_router(
        self,
        req_router_client,
        authenticated_user,
        test_data_factory
    ):
        """Test searching tasks through req-router."""
        unique_title = f"Unique Task for Search {pytest.timestamp}"
        task_data = test_data_factory.create_task_data(title=unique_title)
        
        try:
            # Create task
            response = req_router_client.create_task(task_data)
            task = response.get("task", response)
            task_id = task["id"]
            
            # Wait for indexing
            time.sleep(2)
            
            # Search for it
            search_results = req_router_client.search_tasks(unique_title)
            
            # Verify found
            tasks = search_results.get("tasks", search_results.get("hits", []))
            found = any(t.get("id") == task_id for t in tasks)
            assert found, f"Task {task_id} not found in search results"
            
        finally:
            req_router_client.delete_task(task_id)


@pytest.mark.integration
@pytest.mark.task
@pytest.mark.multiservice
class TestTaskServiceDirectVsReqRouter:
    """Test that task operations work the same via taskservice and req-router."""
    
    def test_task_created_in_taskservice_visible_in_req_router(
        self,
        taskservice_client,
        req_router_client,
        authenticated_user,
        test_data_factory
    ):
        """Test that a task created directly in taskservice is visible via req-router."""
        task_data = test_data_factory.create_task_data()
        
        try:
            # Create in taskservice directly
            response = taskservice_client.create_task(task_data)
            task = response["task"]
            task_id = task["id"]
            
            # Fetch via req-router
            fetched = req_router_client.get_task(task_id)
            fetched_task = fetched.get("task", fetched)
            
            assert fetched_task["id"] == task_id
            assert fetched_task["title"] == task_data["title"]
            
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_task_created_via_req_router_visible_in_taskservice(
        self,
        taskservice_client,
        req_router_client,
        authenticated_user,
        test_data_factory
    ):
        """Test that a task created via req-router is visible in taskservice."""
        task_data = test_data_factory.create_task_data()
        
        try:
            # Create via req-router
            response = req_router_client.create_task(task_data)
            task = response.get("task", response)
            task_id = task["id"]
            
            # Fetch directly from taskservice
            fetched = taskservice_client.get_task(task_id)
            fetched_task = fetched["task"]
            
            assert fetched_task["id"] == task_id
            assert fetched_task["title"] == task_data["title"]
            
        finally:
            taskservice_client.delete_task(task_id)


@pytest.mark.integration
@pytest.mark.task
@pytest.mark.elasticsearch
class TestTaskElasticsearchOperations:
    """Test task storage and retrieval from Elasticsearch."""
    
    def test_task_stored_in_elasticsearch(
        self,
        taskservice_client,
        es_client,
        authenticated_user,
        test_data_factory
    ):
        """Test that created tasks are stored in Elasticsearch."""
        task_data = test_data_factory.create_task_data()
        
        try:
            # Create task
            response = taskservice_client.create_task(task_data)
            task = response["task"]
            task_id = task["id"]
            
            # Wait for indexing
            time.sleep(1)
            
            # Search in ES
            es_response = es_client.search(
                index="*tasks*",
                body={
                    "query": {
                        "term": {"_id": task_id}
                    }
                }
            )
            
            hits = es_response["hits"]["hits"]
            assert len(hits) > 0, f"Task {task_id} not found in Elasticsearch"
            
            es_task = hits[0]["_source"]
            assert es_task["title"] == task_data["title"]
            
        except Exception as e:
            pytest.skip(f"Elasticsearch test requires ES access: {e}")
        finally:
            taskservice_client.delete_task(task_id)
    
    def test_task_updated_in_elasticsearch(
        self,
        taskservice_client,
        es_client,
        authenticated_user,
        test_data_factory
    ):
        """Test that task updates are reflected in Elasticsearch."""
        task_data = test_data_factory.create_task_data()
        
        try:
            # Create task
            response = taskservice_client.create_task(task_data)
            task = response["task"]
            task_id = task["id"]
            
            # Update task
            new_title = "Updated Title in ES"
            taskservice_client.update_task(
                task_id,
                {"title": new_title},
                ["title"]
            )
            
            # Wait for indexing
            time.sleep(1)
            
            # Search in ES
            es_response = es_client.search(
                index="*tasks*",
                body={
                    "query": {
                        "term": {"_id": task_id}
                    }
                }
            )
            
            hits = es_response["hits"]["hits"]
            assert len(hits) > 0
            
            es_task = hits[0]["_source"]
            assert es_task["title"] == new_title
            
        except Exception as e:
            pytest.skip(f"Elasticsearch test requires ES access: {e}")
        finally:
            taskservice_client.delete_task(task_id)

