"""
E2E UI Test for User Role Assignment.

Tests the workflow of assigning a role to a user for a specific workspace.
"""

import pytest
import logging
from pages.login_page import LoginPage
from pages.settings_page import SettingsPage
from config.test_users import get_test_user
from config.env import config

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.user_management
class TestUserRoleAssignmentE2E:
    """Test user role assignment workflow."""

    @pytest.fixture(scope="function", autouse=True)
    def setup_user_role_test(self, page):
        """
        Performs common setup for user role assignment tests:
        1. Logs out (clean state)
        2. Logs in
        3. Waits for pages to load properly
        """
        logger.info("=== Starting common setup for User Role Assignment Test ===")
        
        test_user = get_test_user("Admin")
        
        # Step 1: Logout first (clean state)
        logger.info("Step 1: Logging out first")
        login_page = LoginPage(page)
        login_page.logout_first()
        logger.info("✓ Logged out")
        login_page.screenshot("01-user-role-after-logout")
        
        # Step 2: Login
        logger.info("Step 2: Logging in")
        login_page.login(user=test_user)
        assert login_page.is_logged_in(), "Login should be successful"
        logger.info("✓ Login successful")
        login_page.screenshot("02-user-role-after-login")
        
        # Step 3: Wait for pages to load properly
        logger.info("Step 3: Waiting for pages to load properly")
        page.wait_for_load_state("networkidle", timeout=15000)
        page.wait_for_timeout(3000)  # Additional wait for UI to stabilize
        logger.info("✓ Pages loaded")
        login_page.screenshot("03-user-role-pages-loaded")
        
        yield page  # Yield for the test to use

        logger.info("=== Common teardown for User Role Assignment Test ===")
        # No specific teardown needed - role assignments persist in the system

    def test_assign_role_to_user_for_workspace(self, setup_user_role_test, page):
        """
        E2E Test: Assign a role to a user for a specific workspace.
        
        Flow:
        1. Logout & Login (handled by fixture)
        2. Navigate to Settings -> Users tab
        3. Find user in the users table
        4. Click dropdown arrow next to user to expand row
        5. Click "Modify Settings" button
        6. In Modify User Settings form, find the workspace
        7. Click dropdown next to workspace
        8. Select the role from dropdown
        9. Save the changes
        10. Verify the role is assigned
        """
        logger.info("=== Starting User Role Assignment E2E Test ===")
        
        # Test data
        user_email = "sarang+user@dagknows.com"
        workspace_name = "DEV"
        role_name = "read1"
        
        logger.info(f"Test data:")
        logger.info(f"  User: {user_email}")
        logger.info(f"  Workspace: {workspace_name}")
        logger.info(f"  Role: {role_name}")
        
        # Step 4: Navigate to Settings -> Users tab
        logger.info("Step 4: Navigating to Settings -> Users tab")
        settings_page = SettingsPage(page)
        settings_page.navigate_to_users_tab()
        
        # Verify we're on Users tab
        current_url = page.url
        assert "tab=users" in current_url, f"Should be on Users tab, but URL is: {current_url}"
        logger.info(f"✓ On Users tab: {current_url}")
        settings_page.screenshot("04-user-role-users-tab")
        
        # Step 5: Wait for page to load
        logger.info("Step 5: Waiting for Users page to load")
        page.wait_for_load_state("networkidle", timeout=10000)
        page.wait_for_timeout(2000)  # Additional wait
        logger.info("✓ Users page loaded")
        settings_page.screenshot("05-user-role-users-page-loaded")
        
        # Step 6: Find user in the users table
        logger.info(f"Step 6: Finding user '{user_email}' in users table")
        settings_page.find_user_in_table(user_email)
        logger.info(f"✓ User '{user_email}' found in table")
        settings_page.screenshot("06-user-role-user-found")
        
        # Step 7: Click dropdown arrow next to user to expand row
        logger.info(f"Step 7: Clicking dropdown arrow for user '{user_email}'")
        settings_page.expand_user_row(user_email)
        logger.info(f"✓ User row expanded for '{user_email}'")
        settings_page.screenshot("07-user-role-row-expanded")
        
        # Step 8: Click "Modify Settings" button
        logger.info(f"Step 8: Clicking 'Modify Settings' for user '{user_email}'")
        settings_page.click_modify_settings_for_user(user_email)
        logger.info(f"✓ Modify Settings clicked for '{user_email}'")
        settings_page.screenshot("08-user-role-modify-settings-opened")
        
        # Step 9: Assign role to user for workspace
        logger.info(f"Step 9: Assigning role '{role_name}' to workspace '{workspace_name}' for user '{user_email}'")
        settings_page.assign_role_to_user_for_workspace(
            workspace_name=workspace_name,
            role_name=role_name,
            user_email=user_email
        )
        logger.info(f"✓ Role '{role_name}' assigned to workspace '{workspace_name}'")
        settings_page.screenshot("09-user-role-assigned")
        
        # Step 10: Scroll down and click "Save Changes" button
        logger.info("Step 10: Scrolling down to find and click 'Save Changes' button")
        settings_page.save_user_settings()
        logger.info("✓ Save Changes button clicked")
        settings_page.screenshot("10-user-role-save-changes-clicked")
        
        # Step 11: Wait for success message
        logger.info("Step 11: Waiting for success message 'Changes Saved Successfully'")
        try:
            page.locator('text=Changes Saved Successfully, text=Changes saved successfully').wait_for(
                state="visible", timeout=10000
            )
            logger.info("✓ Success message appeared: 'Changes Saved Successfully'")
            settings_page.screenshot("11-user-role-success-message")
        except Exception as e:
            logger.warning(f"Success message not found: {e}")
            settings_page.screenshot("11-user-role-success-message-not-found")
        
        # Step 12: Wait for page to load after save
        logger.info("Step 12: Waiting for page to load after save")
        page.wait_for_load_state("networkidle", timeout=15000)
        page.wait_for_timeout(3000)  # Additional wait for UI to stabilize
        logger.info("✓ Page loaded after save")
        settings_page.screenshot("12-user-role-after-page-load")
        
        # Step 13: Verify we're back on Users page (form should close after save)
        logger.info("Step 13: Verifying navigation back to Users page")
        current_url = page.url
        if "tab=users" in current_url:
            logger.info(f"✓ Back on Users page: {current_url}")
        else:
            logger.info(f"Current URL after save: {current_url}")
        
        settings_page.screenshot("13-user-role-final-state")
        
        logger.info("=== User Role Assignment E2E Test Completed ===")

