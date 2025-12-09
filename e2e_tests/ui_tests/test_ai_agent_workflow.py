"""
E2E UI Test: AI Agent Workflow

Tests the complete workflow of creating a task using AI Agent.

Flow:
1. Navigate to login page
2. Login with credentials
3. Navigate to landing page
4. Select workspace (Default)
5. Click "New Task" → "Create with AI Agent"
6. Type message and send
7. Wait for AI response

This test matches the exact user workflow shown in the screenshots.
"""

import pytest
import logging
from pages.login_page import LoginPage
from pages.workspace_page import WorkspacePage
from pages.ai_agent_page import AIAgentPage
from config.test_users import get_test_user

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.ai_required
class TestAIAgentWorkflowE2E:
    """Test AI Agent task creation workflow via UI."""
    
    def test_complete_ai_agent_workflow(self, page, test_config):
        """
        E2E Test: Complete AI Agent workflow from login to AI interaction.
        
        This test follows the exact user journey:
        1. Login at /vlogin
        2. Land on /n/landing
        3. Click "Default" workspace
        4. Navigate to /?space=
        5. Click "New Task" dropdown
        6. Select "Create with AI Agent"
        7. Navigate to /tasks/DAGKNOWS?agent=1&space=
        8. Type prompt in "How can I help?" section
        9. Send message
        10. Wait for AI response
        """
        logger.info("=== Starting Complete AI Agent Workflow E2E Test ===")
        
        # Get test user credentials
        # Use specific user: yash+user@dagknows.com
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"  # Override with specific user
        
        # Step 1-2: Login
        logger.info("Step 1-2: Logging in")
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        
        # Verify login successful
        assert login_page.is_logged_in(), "Login should be successful"
        logger.info("✓ Login successful")
        
        # Take screenshot after login
        login_page.screenshot("01-after-login")
        
        # Step 3: Navigate to landing page (or verify we're there)
        logger.info("Step 3: Navigating to landing page")
        workspace_page = WorkspacePage(page)
        workspace_page.navigate_to_landing()
        
        # Wait for workspaces to load
        workspace_page.wait_for_workspaces_loaded()
        
        # Verify we're on landing page
        assert "/n/landing" in page.url or "/landing" in page.url, \
            "Should be on landing page"
        logger.info("✓ On landing page")
        
        # Take screenshot of landing page
        workspace_page.screenshot("02-landing-page")
        
        # Step 4: Click "Default" workspace
        logger.info("Step 4: Clicking 'Default' workspace")
        workspace_page.click_default_workspace()
        
        # Verify we're in the workspace (URL should have ?space=)
        page.wait_for_timeout(2000)  # Wait for navigation
        assert "?space=" in page.url or "space=" in page.url, \
            "Should be in workspace view"
        logger.info(f"✓ In workspace view: {page.url}")
        
        # Take screenshot of workspace
        workspace_page.screenshot("03-workspace-view")
        
        # Step 5-7: Create with AI Agent
        logger.info("Step 5-7: Opening AI Agent")
        ai_agent_page = AIAgentPage(page)
        
        # Click "New Task" button
        ai_agent_page.click_new_task_button()
        
        # Take screenshot of dropdown
        ai_agent_page.screenshot("04-new-task-dropdown")
        
        # Click "Create with AI Agent"
        ai_agent_page.click_create_with_ai_agent()
        
        # Verify we're on AI agent page
        page.wait_for_timeout(2000)
        assert "agent=1" in page.url, "Should be on AI agent page"
        assert "tasks/DAGKNOWS" in page.url or "/tasks/" in page.url, \
            "Should be on tasks page"
        logger.info(f"✓ On AI agent page: {page.url}")
        
        # Take screenshot of AI agent page
        ai_agent_page.screenshot("05-ai-agent-page")
        
        # Step 8-10: Send message to AI
        logger.info("Step 8-10: Sending message to AI")
        
        # Wait for AI agent page to be fully loaded
        ai_agent_page.wait_for_agent_page_loaded()
        
        # Verify agent mode is active
        assert ai_agent_page.verify_agent_mode_active(), \
            "Agent mode should be active"
        
        # Type and send message
        test_prompt = "Create a task to check server CPU usage and restart the service if needed"
        ai_agent_page.send_message(test_prompt)
        
        logger.info(f"✓ Message sent: {test_prompt}")
        
        # Take screenshot after sending
        ai_agent_page.screenshot("06-message-sent")
        
        # Wait for AI response (this can be slow)
        logger.info("Waiting for AI response...")
        ai_agent_page.wait_for_ai_response(timeout=60000)
        
        # Take final screenshot
        ai_agent_page.screenshot("07-ai-response")
        
        logger.info("✓ AI response received (or timeout reached)")
        logger.info("=== AI Agent Workflow E2E Test Completed ===")
    
    def test_ai_agent_direct_navigation(self, page, test_config):
        """
        E2E Test: Navigate directly to AI agent page (bypass landing/workspace).
        
        This is a faster test that skips the navigation steps.
        """
        logger.info("=== Starting AI Agent Direct Navigation Test ===")
        
        # Get test user
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"
        
        # Login
        logger.info("Logging in")
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        assert login_page.is_logged_in(), "Should be logged in"
        
        # Navigate directly to AI agent page
        logger.info("Navigating directly to AI agent page")
        ai_agent_page = AIAgentPage(page)
        ai_agent_page.navigate_to_ai_agent_directly(workspace="")
        
        # Verify we're on agent page
        page.wait_for_timeout(2000)
        assert "agent=1" in page.url, "Should be on AI agent page"
        logger.info(f"✓ On AI agent page: {page.url}")
        
        # Wait for page to load
        ai_agent_page.wait_for_agent_page_loaded()
        
        # Send a simple message
        test_prompt = "Help me troubleshoot high memory usage"
        ai_agent_page.send_message(test_prompt)
        
        logger.info(f"✓ Message sent: {test_prompt}")
        
        # Wait for response
        ai_agent_page.wait_for_ai_response(timeout=30000)
        
        # Take screenshot
        ai_agent_page.screenshot("ai-agent-direct-response")
        
        logger.info("=== AI Agent Direct Navigation Test Completed ===")
    
    def test_ai_agent_workflow_with_complete_flow(self, page, test_config):
        """
        E2E Test: Complete workflow using helper method.
        
        This demonstrates using the complete_ai_agent_workflow helper.
        """
        logger.info("=== Starting AI Agent Complete Flow Test ===")
        
        # Get test user
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"
        
        # Login
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        
        # Navigate to AI agent (can skip to direct navigation for speed)
        ai_agent_page = AIAgentPage(page)
        ai_agent_page.navigate_to_ai_agent_directly(workspace="")
        
        # Use complete workflow helper
        prompt = "Create a monitoring task for database performance"
        ai_agent_page.complete_ai_agent_workflow(
            prompt=prompt,
            wait_for_response=True
        )
        
        # Verify we're still on agent page
        assert "agent=1" in page.url, "Should still be on agent page"
        
        logger.info("✓ Complete AI agent workflow executed successfully")
        logger.info("=== AI Agent Complete Flow Test Completed ===")

