"""
Login Page Object.

Handles login page interactions and authentication flow.
"""

import logging
from typing import Optional
from pages.base_page import BasePage
from config.test_users import TestUser, ADMIN_USER

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page object (matches dagknows_nuxt/components/LoginForm.vue)."""
    
    # Selectors (matching actual UI)
    EMAIL_INPUT = 'input[placeholder="Email or Username"]'
    PASSWORD_INPUT = 'input[placeholder="Password"]'
    ORG_INPUT = 'input#org'
    SIGN_IN_BUTTON = 'button:has-text("Sign in")'
    SIGNED_IN_USER_ICON = '#signed_in_user_icon'
    ERROR_MESSAGE = '.login-error, .error-message'
    
    def __init__(self, page):
        """Initialize login page."""
        super().__init__(page)
        self.url = "/vlogin"
    
    def navigate(self) -> None:
        """Navigate to login page."""
        logger.info("Navigating to login page")
        self.goto(self.url)
        self.wait_for_load()
    
    def logout_first(self) -> None:
        """Logout if already logged in (clean slate)."""
        logger.info("Logging out first (clean state)")
        self.goto("/vlogout")
        self.page.wait_for_timeout(2000)
    
    def fill_email(self, email: str) -> None:
        """Fill email field."""
        logger.info(f"Filling email: {email}")
        self.page.get_by_placeholder("Email or Username").click()
        self.page.get_by_placeholder("Email or Username").fill(email)
    
    def fill_password(self, password: str) -> None:
        """Fill password field."""
        logger.info("Filling password")
        self.page.get_by_placeholder("Password").click()
        self.page.get_by_placeholder("Password").fill(password)
    
    def fill_org(self, org: str) -> None:
        """Fill organization field (if visible)."""
        if self.page.locator(self.ORG_INPUT).is_visible():
            logger.info(f"Filling org: {org}")
            self.page.locator(self.ORG_INPUT).fill(org)
    
    def click_sign_in(self) -> None:
        """Click sign in button."""
        logger.info("Clicking sign in button")
        self.page.get_by_role("button", name="Sign in").click()
    
    def wait_for_login_success(self, timeout: int = 10000) -> None:
        """
        Wait for login to complete successfully.
        
        Args:
            timeout: Wait timeout in ms
        """
        logger.info("Waiting for login success")
        # Wait for user icon to appear (indicates successful login)
        self.page.locator(self.SIGNED_IN_USER_ICON).wait_for(
            state="visible",
            timeout=timeout
        )
        logger.info("✓ Login successful - user icon visible")
    
    def get_error_message(self) -> Optional[str]:
        """
        Get error message if login failed.
        
        Returns:
            Error message text or None
        """
        try:
            return self.page.locator(self.ERROR_MESSAGE).text_content(timeout=2000)
        except Exception:
            return None
    
    def login(
        self,
        user: Optional[TestUser] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        org: Optional[str] = None
    ) -> None:
        """
        Complete login flow (matches dagknows_nuxt login behavior).
        
        Args:
            user: TestUser instance (preferred)
            email: Email (if not using TestUser)
            password: Password (if not using TestUser)
            org: Organization (if not using TestUser)
        """
        # Use TestUser or individual parameters
        if user:
            email = user.email
            password = user.password
            org = user.org
        else:
            email = email or ADMIN_USER.email
            password = password or ADMIN_USER.password
            org = org or ADMIN_USER.org
        
        logger.info(f"=== Starting login flow for {email} ===")
        
        # Step 1: Logout first (clean state)
        self.logout_first()
        
        # Step 2: Navigate to login page
        self.navigate()
        
        # Step 3: Fill form
        self.fill_email(email)
        self.fill_password(password)
        if org:
            self.fill_org(org)
        
        # Step 4: Submit
        self.click_sign_in()
        
        # Step 5: Wait for success
        self.wait_for_login_success()
        
        # Step 6: Take screenshot
        self.screenshot("after-login")
        
        logger.info(f"=== Login completed for {email} ===")
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.
        
        Returns:
            True if logged in, False otherwise
        """
        return self.is_visible(self.SIGNED_IN_USER_ICON, timeout=2000)

