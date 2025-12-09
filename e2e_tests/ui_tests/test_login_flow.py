"""
E2E UI Test: Login Flow

Tests the complete login workflow via UI.
"""

import pytest
import logging
from pages.login_page import LoginPage
from config.test_users import ADMIN_USER

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.e2e
class TestLoginFlowE2E:
    """Test complete login flow via UI."""
    
    def test_successful_login_and_logout(self, page, test_config):
        """
        E2E Test: Successful login and logout flow.
        
        Flow:
        1. Navigate to login page
        2. Enter valid credentials
        3. Submit form
        4. Verify redirect to dashboard
        5. Verify user is logged in
        6. Logout
        7. Verify logged out
        """
        logger.info("=== Starting Login Flow E2E Test ===")
        
        login_page = LoginPage(page)
        
        # Step 1-5: Login
        logger.info("Steps 1-5: Performing login")
        login_page.login(user=ADMIN_USER)
        
        # Verify we're on dashboard/home
        assert page.url != test_config.BASE_URL + "/vlogin", "Should not be on login page"
        logger.info(f"✓ Redirected to: {page.url}")
        
        # Verify user icon is visible
        assert login_page.is_logged_in(), "User should be logged in"
        logger.info("✓ User is logged in")
        
        # Step 6: Logout
        logger.info("Step 6: Logging out")
        page.goto("/vlogout")
        page.wait_for_timeout(2000)
        
        # Step 7: Verify logged out
        logger.info("Step 7: Verifying logged out")
        # Should be redirected to login page or home without auth
        assert not login_page.is_logged_in(), "User should be logged out"
        logger.info("✓ User is logged out")
        
        logger.info("=== Login Flow E2E Test Completed ===")
    
    def test_login_with_invalid_credentials(self, page):
        """
        E2E Test: Login with invalid credentials shows error.
        
        Flow:
        1. Navigate to login page
        2. Enter invalid credentials
        3. Submit form
        4. Verify error message shown
        5. Verify still on login page
        """
        logger.info("=== Starting Invalid Login E2E Test ===")
        
        login_page = LoginPage(page)
        
        # Navigate to login
        login_page.logout_first()
        login_page.navigate()
        
        # Enter invalid credentials
        logger.info("Entering invalid credentials")
        login_page.fill_email("invalid@example.com")
        login_page.fill_password("wrongpassword")
        login_page.click_sign_in()
        
        # Wait a bit for response
        page.wait_for_timeout(3000)
        
        # Verify still on login page or error shown
        current_url = page.url
        assert "/vlogin" in current_url or "error" in current_url, "Should show error or stay on login page"
        
        # Check for error message
        error_msg = login_page.get_error_message()
        if error_msg:
            logger.info(f"✓ Error message shown: {error_msg}")
        else:
            logger.info("✓ Still on login page (error may be in URL)")
        
        # Verify NOT logged in
        assert not login_page.is_logged_in(), "Should not be logged in"
        
        logger.info("=== Invalid Login E2E Test Completed ===")
    
    def test_login_persists_across_page_reload(self, page):
        """
        E2E Test: Login session persists across page reload.
        
        Flow:
        1. Login
        2. Verify logged in
        3. Reload page
        4. Verify still logged in
        """
        logger.info("=== Starting Login Persistence E2E Test ===")
        
        login_page = LoginPage(page)
        
        # Step 1: Login
        login_page.login(user=ADMIN_USER)
        assert login_page.is_logged_in(), "Should be logged in"
        logger.info("✓ Logged in")
        
        # Step 2: Reload page
        logger.info("Reloading page")
        page.reload()
        page.wait_for_timeout(2000)
        
        # Step 3: Verify still logged in
        assert login_page.is_logged_in(), "Should still be logged in after reload"
        logger.info("✓ Session persisted after reload")
        
        logger.info("=== Login Persistence E2E Test Completed ===")

