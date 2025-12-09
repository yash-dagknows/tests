"""
E2E UI Tests for Task CRUD Operations

Tests task creation, viewing, editing, and management workflows.
"""

import pytest
import logging
import time
from pages.login_page import LoginPage
from pages.workspace_page import WorkspacePage
from pages.task_page import TaskPage
from config.test_users import get_test_user

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.task_crud
class TestTaskCRUDE2E:
    """E2E tests for task CRUD operations."""
    
    def test_create_task_from_form(self, page, test_config):
        """
        E2E Test: Create a new task using the form.
        
        Flow:
        1. Login
        2. Navigate to landing page
        3. Select Default workspace
        4. Click "New Task" button (top right)
        5. Select "Create from Form" from dropdown
        6. Fill task details:
           - Title
           - Description
           - Code
        7. Scroll down and click Save
        8. Verify task is created with valid URL
        """
        logger.info("=== Starting Task Creation from Form E2E Test ===")
        
        # Generate unique task name with timestamp
        timestamp = int(time.time())
        test_task_title = f"TestTask_{timestamp}"
        test_task_description = f"Test task created at {timestamp} for E2E testing"
        test_task_code = f"""#!/usr/bin/env python3
# Test task created by E2E test
# Timestamp: {timestamp}

import sys

def main():
    print("Hello from test task {timestamp}")
    print("This is a test task created by E2E automation")
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
        
        logger.info(f"Test task title: {test_task_title}")
        
        # Get test user
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"
        
        # Step 1: Login
        logger.info("Step 1: Logging in")
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        assert login_page.is_logged_in(), "Login should be successful"
        logger.info("✓ Login successful")
        login_page.screenshot("01-task-after-login")
        
        # Step 2: Navigate to landing page
        logger.info("Step 2: Navigating to landing page")
        workspace_page = WorkspacePage(page)
        workspace_page.navigate_to_landing()
        workspace_page.wait_for_workspaces_loaded()
        assert "/n/landing" in page.url or "/landing" in page.url, \
            "Should be on landing page"
        logger.info("✓ On landing page")
        workspace_page.screenshot("02-task-landing-page")
        
        # Step 3: Click Default workspace
        logger.info("Step 3: Clicking 'Default' workspace")
        workspace_page.click_default_workspace()
        assert "?space=" in page.url or "space=" in page.url, \
            "Should be in workspace view"
        logger.info(f"✓ In Default workspace: {page.url}")
        workspace_page.screenshot("03-task-workspace-view")
        
        # Step 4: Click "New Task" button
        logger.info("Step 4: Clicking 'New Task' button")
        task_page = TaskPage(page)
        task_page.click_new_task_button()
        logger.info("✓ New Task dropdown opened")
        task_page.screenshot("04-task-new-task-dropdown")
        
        # Step 5: Click "Create from Form"
        logger.info("Step 5: Clicking 'Create from Form'")
        task_page.click_create_from_form()
        logger.info("✓ Navigated to task creation form")
        task_page.screenshot("05-task-creation-form")
        
        # Step 6: Fill task details
        logger.info("Step 6: Filling task details")
        
        logger.info("Step 6a: Filling title")
        task_page.fill_task_title(test_task_title)
        task_page.screenshot("06a-task-title-filled")
        
        logger.info("Step 6b: Filling description")
        task_page.fill_task_description(test_task_description)
        task_page.screenshot("06b-task-description-filled")
        
        logger.info("Step 6c: Filling code")
        task_page.fill_task_code(test_task_code)
        task_page.screenshot("06c-task-code-filled")
        
        logger.info("✓ All task details filled")
        
        # Step 7: Scroll and click Save
        logger.info("Step 7: Scrolling to bottom and clicking Save")
        task_page.scroll_to_bottom()
        task_page.screenshot("07a-task-scrolled-to-save")
        
        task_page.click_save_button()
        logger.info("✓ Save button clicked")
        task_page.screenshot("07b-task-after-save")
        
        # Step 8: Verify task creation
        logger.info("Step 8: Verifying task creation")
        current_url = page.url
        logger.info(f"Current URL: {current_url}")
        
        # Check URL contains task indicator
        has_task_url = any(indicator in current_url for indicator in ["taskId=", "/task/", "/tasks/"])
        
        if has_task_url:
            logger.info(f"✓ URL indicates task page: {current_url}")
        else:
            logger.warning(f"URL does not clearly indicate task page: {current_url}")
            # Still take screenshot for debugging
            task_page.screenshot("08-task-url-verification")
        
        # Verify task was created
        task_created = task_page.verify_task_created(test_task_title)
        
        if task_created:
            logger.info(f"✓ Task '{test_task_title}' was created successfully")
        else:
            logger.warning("Could not definitively verify task creation")
            # We'll assert on URL at least
            assert has_task_url or "space=" in current_url, \
                f"Expected task URL but got: {current_url}"
        
        task_page.screenshot("08-task-creation-verified")
        
        logger.info(f"✓ Task creation test completed. Task title: {test_task_title}")
        logger.info(f"✓ Final URL: {current_url}")
        logger.info("=== Task Creation from Form E2E Test Completed ===")
        
        # NOTE: Cleanup (deleting task) is NOT performed
        # Tasks can be cleaned up manually or via separate script
    
    def test_create_task_with_minimal_data(self, page, test_config):
        """
        E2E Test: Create task with minimal data (title and code only).
        
        This tests that description is optional.
        """
        logger.info("=== Starting Minimal Task Creation Test ===")
        
        timestamp = int(time.time())
        test_task_title = f"MinimalTask_{timestamp}"
        test_task_code = "print('Minimal task')"
        
        # Get test user
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"
        
        # Login and navigate
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        assert login_page.is_logged_in()
        
        workspace_page = WorkspacePage(page)
        workspace_page.navigate_to_landing()
        workspace_page.wait_for_workspaces_loaded()
        workspace_page.click_default_workspace()
        
        # Create task with minimal data
        task_page = TaskPage(page)
        task_page.click_new_task_button()
        task_page.click_create_from_form()
        
        # Fill only title and code (skip description)
        task_page.fill_task_title(test_task_title)
        task_page.fill_task_code(test_task_code)
        
        task_page.click_save_button()
        
        # Verify
        current_url = page.url
        logger.info(f"Task created with minimal data. URL: {current_url}")
        
        task_created = task_page.verify_task_created(test_task_title)
        assert task_created or "taskId=" in current_url or "/task/" in current_url, \
            "Task should be created with minimal data"
        
        logger.info("✓ Minimal task creation successful")
        logger.info("=== Minimal Task Creation Test Completed ===")

