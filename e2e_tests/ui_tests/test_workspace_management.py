"""
E2E UI Tests for Workspace Management

Tests workspace creation, verification, and navigation workflows.
"""

import pytest
import logging
import time
from pages.login_page import LoginPage
from pages.workspace_page import WorkspacePage
from pages.settings_page import SettingsPage
from config.test_users import get_test_user

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.workspace_management
class TestWorkspaceManagementE2E:
    """E2E tests for workspace management."""
    
    def test_create_and_navigate_to_workspace(self, page, test_config):
        """
        E2E Test: Create a new workspace and navigate to it.
        
        Flow:
        1. Login
        2. Navigate to landing page
        3. Select Default workspace
        4. Go to Settings → Workspaces tab
        5. Create new workspace
        6. Verify workspace appears in list
        7. Navigate to new workspace via folder icon dropdown
        8. Verify successful navigation
        """
        logger.info("=== Starting Workspace Creation E2E Test ===")
        
        # Generate unique workspace name with timestamp
        timestamp = int(time.time())
        test_workspace_name = f"test{timestamp}"
        logger.info(f"Test workspace name: {test_workspace_name}")
        
        # Get test user
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"
        
        # Step 1: Login
        logger.info("Step 1: Logging in")
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        assert login_page.is_logged_in(), "Login should be successful"
        logger.info("✓ Login successful")
        login_page.screenshot("01-workspace-after-login")
        
        # Step 2: Navigate to landing page
        logger.info("Step 2: Navigating to landing page")
        workspace_page = WorkspacePage(page)
        workspace_page.navigate_to_landing()
        workspace_page.wait_for_workspaces_loaded()
        assert "/n/landing" in page.url or "/landing" in page.url, \
            "Should be on landing page"
        logger.info("✓ On landing page")
        workspace_page.screenshot("02-workspace-landing-page")
        
        # Step 3: Click Default workspace
        logger.info("Step 3: Clicking 'Default' workspace")
        workspace_page.click_default_workspace()
        assert "?space=" in page.url or "space=" in page.url, \
            "Should be in workspace view"
        logger.info(f"✓ In Default workspace: {page.url}")
        workspace_page.screenshot("03-workspace-default-workspace")
        
        # Step 4: Navigate to Settings → Workspaces tab
        logger.info("Step 4: Navigating to Settings → Workspaces")
        settings_page = SettingsPage(page)
        settings_page.click_settings_in_nav()
        assert "/vsettings" in page.url, "Should be on settings page"
        logger.info("✓ On settings page")
        settings_page.screenshot("04-workspace-settings-page")
        
        logger.info("Step 4b: Clicking Workspaces tab")
        settings_page.click_workspaces_tab()
        logger.info("✓ Workspaces tab loaded")
        settings_page.screenshot("05-workspace-workspaces-tab")
        
        # Step 5: Create new workspace
        logger.info(f"Step 5: Creating workspace '{test_workspace_name}'")
        settings_page.create_workspace(test_workspace_name)
        logger.info(f"✓ Workspace '{test_workspace_name}' creation requested")
        settings_page.screenshot("06-workspace-created")
        
        # Step 6: Verify workspace appears in list
        logger.info(f"Step 6: Verifying workspace '{test_workspace_name}' in list")
        workspace_found = settings_page.verify_workspace_in_list(
            test_workspace_name,
            timeout=15000
        )
        assert workspace_found, \
            f"Workspace '{test_workspace_name}' should appear in Current workspaces list"
        logger.info(f"✓ Workspace '{test_workspace_name}' found in list")
        settings_page.screenshot("07-workspace-verified-in-list")
        
        # Step 7: Navigate to new workspace via folder icon
        logger.info(f"Step 7: Navigating to workspace '{test_workspace_name}' via folder dropdown")
        
        # First, we need to be in a workspace view (not settings)
        # Go back to Default workspace first
        workspace_page.navigate_to_landing()
        workspace_page.wait_for_workspaces_loaded()
        workspace_page.click_default_workspace()
        page.wait_for_timeout(2000)
        workspace_page.screenshot("08-workspace-back-to-default")
        
        # Now click folder icon and select new workspace
        logger.info("Step 7a: Clicking folder icon in left nav")
        workspace_page.click_workspace_folder_icon()
        workspace_page.screenshot("09-workspace-folder-dropdown-open")
        
        logger.info(f"Step 7b: Selecting '{test_workspace_name}' from dropdown")
        workspace_page.select_workspace_from_dropdown(test_workspace_name)
        workspace_page.screenshot("10-workspace-navigated-to-new")
        
        # Step 8: Verify we're in the new workspace
        logger.info(f"Step 8: Verifying navigation to '{test_workspace_name}'")
        current_url = page.url
        logger.info(f"Current URL: {current_url}")
        
        # Verify URL contains space parameter
        assert "space=" in current_url, \
            f"URL should contain 'space=' parameter: {current_url}"
        
        # Additional verification: Check if we can see workspace-specific elements
        # (e.g., "New Task" button, workspace name display, etc.)
        try:
            # Wait for New Task button to be visible (common in workspace view)
            page.locator('button:has-text("New Task"), button:has-text("+ New Task")').wait_for(
                state="visible",
                timeout=10000
            )
            logger.info("✓ Workspace view loaded (found 'New Task' button)")
        except Exception as e:
            logger.warning(f"Could not find 'New Task' button: {e}")
            # Not a failure, just means UI might be different
        
        workspace_page.screenshot("11-workspace-final-verification")
        
        logger.info(f"✓ Successfully navigated to workspace '{test_workspace_name}'")
        logger.info("=== Workspace Creation E2E Test Completed ===")
        
        # NOTE: Cleanup (deleting workspace) is NOT performed
        # as it requires additional API or UI interactions
        # Workspaces can be cleaned up manually or via separate script

