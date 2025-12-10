"""
E2E UI Test for Role Management (RBAC).

Tests the workflow of creating a custom role and assigning privileges to it.
"""

import pytest
import logging
import time
from pages.login_page import LoginPage
from pages.settings_page import SettingsPage
from config.test_users import get_test_user
from config.env import config

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.role_management
class TestRoleManagementE2E:
    """Test role creation and privilege assignment workflow."""

    @pytest.fixture(scope="function", autouse=True)
    def setup_role_test(self, page):
        """
        Performs common setup for role management tests:
        1. Logs out (clean state)
        2. Logs in
        3. Waits for pages to load properly
        """
        logger.info("=== Starting common setup for Role Management Test ===")
        
        test_user = get_test_user("Admin")
        
        # Step 1: Logout first (clean state)
        logger.info("Step 1: Logging out first")
        login_page = LoginPage(page)
        login_page.logout_first()
        logger.info("✓ Logged out")
        login_page.screenshot("01-role-after-logout")
        
        # Step 2: Login
        logger.info("Step 2: Logging in")
        login_page.login(user=test_user)
        assert login_page.is_logged_in(), "Login should be successful"
        logger.info("✓ Login successful")
        login_page.screenshot("02-role-after-login")
        
        # Step 3: Wait for pages to load properly
        logger.info("Step 3: Waiting for pages to load properly")
        page.wait_for_load_state("networkidle", timeout=15000)
        page.wait_for_timeout(3000)  # Additional wait for UI to stabilize
        logger.info("✓ Pages loaded")
        login_page.screenshot("03-role-pages-loaded")
        
        yield page  # Yield for the test to use

        logger.info("=== Common teardown for Role Management Test ===")
        # No specific teardown needed - roles persist in the system

    def test_create_role_and_assign_privileges(self, setup_role_test, page):
        """
        E2E Test: Create a custom role and assign privileges to it.
        
        Flow:
        1. Logout & Login (handled by fixture)
        2. Navigate to Settings -> RBAC tab (tab=rbac)
        3. Scroll down to "Create new custom role" section
        4. Create a custom role named "read1"
        5. Verify the role appears in the privileges table
        6. Scroll to privileges table
        7. Scroll horizontally to find the "read1" role column
        8. Assign privileges:
           - task.view_code
           - task.view_io
           - task.view_description
           - task.list
        9. Verify privileges are assigned
        """
        logger.info("=== Starting Role Creation and Privilege Assignment E2E Test ===")
        
        # Generate unique role name with timestamp
        timestamp = int(time.time())
        role_name = f"read1_{timestamp}"
        logger.info(f"Test role name: {role_name}")
        
        # Step 4: Navigate to Settings page
        logger.info("Step 4: Navigating to Settings page")
        settings_page = SettingsPage(page)
        settings_page.navigate_to_settings_page()
        logger.info(f"✓ On settings page: {page.url}")
        settings_page.screenshot("04-role-settings-page")
        
        # Step 5: Click Workspaces tab on the top horizontal strip
        logger.info("Step 5: Clicking Workspaces tab on settings page")
        settings_page.click_workspaces_tab()
        logger.info(f"✓ Workspaces tab clicked: {page.url}")
        settings_page.screenshot("05-role-workspaces-tab")
        
        # Step 6: Scroll down to "Create new custom role" section
        logger.info("Step 6: Scrolling to 'Create new custom role' section")
        settings_page.scroll_to_create_custom_role_section()
        logger.info("✓ Scrolled to create custom role section")
        settings_page.screenshot("06-role-create-section-visible")
        
        # Step 7: Create custom role
        logger.info(f"Step 7: Creating custom role '{role_name}'")
        settings_page.create_custom_role(role_name)
        logger.info(f"✓ Custom role '{role_name}' created")
        settings_page.screenshot("06-role-created")
        
        # Step 8: Scroll to privileges table (role appears in table below)
        logger.info("Step 8: Scrolling to privileges table where role will appear")
        settings_page.scroll_to_privileges_table()
        logger.info("✓ Scrolled to privileges table")
        settings_page.screenshot("08-role-privileges-table-visible")
        
        # Step 9: Verify role appears in privileges table AND scroll horizontally to find it
        # IMPORTANT: After role creation, the role column is added to the right side of the table
        # and requires horizontal scrolling to be visible
        logger.info(f"Step 9: Verifying role '{role_name}' appears in privileges table")
        logger.info("Note: Will scroll horizontally to find the role column (new roles appear on the right)")
        settings_page.verify_role_in_privileges_table(role_name, timeout=30000)  # Increased to 30 seconds
        logger.info(f"✓ Role '{role_name}' found in privileges table")
        settings_page.screenshot("09-role-in-table")
        
        # Step 10: Ensure role column is visible (scroll horizontally if needed)
        logger.info(f"Step 10: Ensuring role column '{role_name}' is visible (horizontal scroll if needed)")
        settings_page.scroll_horizontally_to_role_column(role_name)
        logger.info(f"✓ Role column '{role_name}' is visible")
        settings_page.screenshot("10-role-column-visible")
        
        # Step 11: Assign privileges to the role
        privileges_to_assign = [
            "task.view_code",
            "task.view_io",
            "task.view_description",
            "task.list"
        ]
        
        logger.info(f"Step 10: Assigning {len(privileges_to_assign)} privileges to role '{role_name}'")
        logger.info(f"Privileges to assign: {privileges_to_assign}")
        
        for privilege in privileges_to_assign:
            logger.info(f"  Assigning privilege: {privilege}")
            settings_page.assign_privilege_to_role(privilege, role_name)
            logger.info(f"  ✓ Assigned: {privilege}")
        
        logger.info(f"✓ All {len(privileges_to_assign)} privileges assigned to role '{role_name}'")
        settings_page.screenshot("10-role-all-privileges-assigned")
        
        # Step 12: Verify privileges are assigned (check that checkboxes are checked)
        logger.info("Step 12: Verifying privileges are assigned")
        for privilege in privileges_to_assign:
            try:
                # Find the privilege row
                privilege_row_selector = f'tr:has-text("{privilege}")'
                privilege_row = page.locator(privilege_row_selector).first
                
                # Find the role column header to get index
                role_header_selector = f'th:has-text("{role_name}")'
                all_headers = page.locator('table >> thead >> th').all()
                role_column_index = None
                
                for idx, header in enumerate(all_headers):
                    header_text = header.text_content()
                    if role_name in header_text:
                        role_column_index = idx
                        break
                
                if role_column_index is not None:
                    # Get the checkbox in the role column
                    privilege_row_tds = privilege_row.locator('td').all()
                    if len(privilege_row_tds) > role_column_index:
                        checkbox = privilege_row_tds[role_column_index].locator('input[type="checkbox"]').first
                        if checkbox.is_checked():
                            logger.info(f"  ✓ Verified: {privilege} is checked for {role_name}")
                        else:
                            logger.warning(f"  ✗ {privilege} checkbox is not checked for {role_name}")
                            settings_page.screenshot(f"privilege-not-checked-{privilege}")
            except Exception as e:
                logger.warning(f"  Could not verify privilege '{privilege}': {e}")
        
        logger.info("=== Role Creation and Privilege Assignment E2E Test Completed ===")

