"""
E2E UI Test: Task Creation and Management

Tests complete task creation and management workflow via UI.
"""

import pytest
import logging
import time
from pages.login_page import LoginPage
from pages.task_page import TaskPage
from config.test_users import ADMIN_USER

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.e2e
class TestTaskCreationE2E:
    """Test task creation and management via UI."""
    
    def test_create_and_delete_simple_task(self, page):
        """
        E2E Test: Create and delete a simple task via UI.
        
        Flow:
        1. Login
        2. Navigate to home
        3. Click "Create Runbook"
        4. Fill task details
        5. Save task
        6. Verify task appears
        7. Delete task
        8. Verify task removed
        """
        logger.info("=== Starting Task Creation E2E Test ===")
        
        # Step 1: Login
        login_page = LoginPage(page)
        login_page.login(user=ADMIN_USER)
        
        # Step 2: Navigate to home
        task_page = TaskPage(page)
        task_page.navigate_to_home()
        
        # Step 3-6: Create task
        timestamp = int(time.time())
        task_title = f"E2E UI Test Task {timestamp}"
        
        logger.info(f"Creating task: {task_title}")
        task_page.create_top_level_task(
            title=task_title,
            script_type="command",
            commands="echo 'E2E UI test task'"
        )
        
        # Verify task exists
        assert task_page.verify_task_exists(task_title), "Task should exist"
        logger.info("✓ Task created successfully")
        
        # Take screenshot
        task_page.screenshot(f"task-created-{timestamp}")
        
        # Step 7-8: Delete task
        logger.info("Deleting task")
        task_page.delete_task(task_title)
        
        # Verify task deleted
        assert not task_page.verify_task_exists(task_title, timeout=2000), "Task should be deleted"
        logger.info("✓ Task deleted successfully")
        
        logger.info("=== Task Creation E2E Test Completed ===")
    
    def test_create_parent_child_task_hierarchy(self, page):
        """
        E2E Test: Create parent task with child tasks via UI.
        
        Flow:
        1. Login
        2. Create parent task
        3. Add first child task
        4. Add second child task
        5. Verify hierarchy
        6. Cleanup
        """
        logger.info("=== Starting Task Hierarchy E2E Test ===")
        
        # Login
        login_page = LoginPage(page)
        login_page.login(user=ADMIN_USER)
        
        task_page = TaskPage(page)
        task_page.navigate_to_home()
        
        timestamp = int(time.time())
        parent_title = f"E2E Parent Task {timestamp}"
        child1_title = f"E2E Child 1 {timestamp}"
        child2_title = f"E2E Child 2 {timestamp}"
        
        try:
            # Create parent
            logger.info("Creating parent task")
            task_page.create_top_level_task(
                title=parent_title,
                commands="echo 'Parent task'"
            )
            
            # Create child 1
            logger.info("Creating child task 1")
            task_page.create_child_task(
                parent_title=parent_title,
                child_title=child1_title,
                script_type="command",
                commands="echo 'Child 1'"
            )
            
            # Create child 2
            logger.info("Creating child task 2")
            task_page.create_child_task(
                parent_title=parent_title,
                child_title=child2_title,
                script_type="python",
                commands="print('Child 2')"
            )
            
            # Verify all tasks exist
            assert task_page.verify_task_exists(parent_title), "Parent should exist"
            assert task_page.verify_task_exists(child1_title), "Child 1 should exist"
            assert task_page.verify_task_exists(child2_title), "Child 2 should exist"
            
            logger.info("✓ Task hierarchy created successfully")
            
            # Screenshot
            task_page.screenshot(f"task-hierarchy-{timestamp}")
            
        finally:
            # Cleanup (delete in reverse order)
            logger.info("Cleaning up tasks")
            for title in [child2_title, child1_title, parent_title]:
                try:
                    if task_page.verify_task_exists(title, timeout=2000):
                        task_page.delete_task(title)
                        logger.info(f"✓ Deleted: {title}")
                except Exception as e:
                    logger.warning(f"Failed to delete {title}: {e}")
        
        logger.info("=== Task Hierarchy E2E Test Completed ===")
    
    def test_edit_existing_task(self, page):
        """
        E2E Test: Edit an existing task via UI.
        
        Flow:
        1. Login
        2. Create a task
        3. Open task for editing
        4. Modify task details
        5. Save changes
        6. Verify changes persisted
        7. Cleanup
        """
        logger.info("=== Starting Task Editing E2E Test ===")
        
        # Login
        login_page = LoginPage(page)
        login_page.login(user=ADMIN_USER)
        
        task_page = TaskPage(page)
        task_page.navigate_to_home()
        
        timestamp = int(time.time())
        original_title = f"E2E Edit Test {timestamp}"
        updated_title = f"E2E Edit Test {timestamp} - UPDATED"
        
        try:
            # Create task
            logger.info("Creating task")
            task_page.create_top_level_task(
                title=original_title,
                commands="echo 'Original'"
            )
            
            # TODO: Implement task editing in TaskPage
            # For now, we'll just verify the task exists
            assert task_page.verify_task_exists(original_title), "Task should exist"
            logger.info("✓ Task created and verified")
            
            # Note: Full edit flow would require:
            # - Click on task to open
            # - Click edit button
            # - Modify fields
            # - Save
            # - Verify changes
            
            logger.info("⚠ Full edit flow not yet implemented in page object")
            
        finally:
            # Cleanup
            try:
                task_page.delete_task(original_title)
                logger.info("✓ Cleaned up test task")
            except Exception as e:
                logger.warning(f"Cleanup failed: {e}")
        
        logger.info("=== Task Editing E2E Test Completed ===")

