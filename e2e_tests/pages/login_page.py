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
        logger.info(f"Checking if org field is visible...")
        try:
            # Wait a bit for the field to appear
            org_locator = self.page.locator(self.ORG_INPUT)
            if org_locator.count() > 0:
                # Field exists, check if visible
                if org_locator.is_visible():
                    logger.info(f"Filling org field: {org}")
                    org_locator.fill(org)
                else:
                    logger.info("Org field exists but is not visible")
            else:
                logger.info("Org field does not exist on page")
        except Exception as e:
            logger.warning(f"Could not fill org field: {e}")
    
    def click_sign_in(self) -> None:
        """Click sign in button (the button inside the login form, NOT the top-right nav button)."""
        logger.info("Clicking sign in button in login form")
        # There are TWO "Sign in" buttons on the page:
        # 1. Top-right navigation: "Sign in" link/button (WRONG - doesn't submit form)
        # 2. Login form middle: "Sign in" button (CORRECT - submits the form)
        # 
        # We need to target the button that's INSIDE the login form, not the nav button
        
        try:
            # Strategy 1: Target the input type="button" which is the form submit button
            # This is more specific than the generic button
            form_button = self.page.locator('input[type="button"][value="Sign in"]')
            if form_button.count() > 0 and form_button.is_visible():
                form_button.click()
                logger.info("✓ Clicked login form Sign in button (input type)")
                return
        except Exception as e:
            logger.debug(f"Could not click input button: {e}")
        
        try:
            # Strategy 2: Find button within a form or login container
            # Look for button inside a form element
            form_signin = self.page.locator('form button:has-text("Sign in")')
            if form_signin.count() > 0:
                form_signin.first.click()
                logger.info("✓ Clicked Sign in button inside form")
                return
        except Exception as e:
            logger.debug(f"Could not click form button: {e}")
        
        try:
            # Strategy 3: Use the btn-primary class but be more specific
            # Avoid the nav button by looking for one that's not in header
            primary_btn = self.page.locator('button.btn-primary:has-text("Sign in")').last
            primary_btn.click()
            logger.info("✓ Clicked btn-primary Sign in button (last match)")
        except Exception as e:
            logger.warning(f"All strategies failed: {e}")
            raise Exception("Could not find the login form Sign in button")
    
    def wait_for_login_success(self, timeout: int = 10000) -> None:
        """
        Wait for login to complete successfully.
        
        Args:
            timeout: Wait timeout in ms
        """
        logger.info("Waiting for login success")
        
        # Take screenshot after clicking sign in
        self.screenshot("after-signin-click")
        logger.info("Screenshot taken after sign-in click")
        
        # Wait a moment for any navigation
        self.page.wait_for_timeout(2000)
        
        # Log current URL
        current_url = self.page.url
        logger.info(f"Current URL after sign-in: {current_url}")
        
        # Check for error messages
        error_msg = self.get_error_message()
        if error_msg:
            logger.error(f"Login error message: {error_msg}")
            self.screenshot("login-error")
        
        # Try multiple indicators of successful login
        success_indicators = [
            self.SIGNED_IN_USER_ICON,
            '#signed_in_user_icon',
            '[data-testid="user-menu"]',
            'text=Logout',
            'text=Sign out',
        ]
        
        login_successful = False
        for indicator in success_indicators:
            try:
                self.page.locator(indicator).wait_for(
                    state="visible",
                    timeout=timeout // len(success_indicators)
                )
                logger.info(f"✓ Login successful - found indicator: {indicator}")
                login_successful = True
                break
            except Exception as e:
                logger.debug(f"Indicator '{indicator}' not found: {e}")
        
        if not login_successful:
            # Last resort: check if URL changed from login page
            if "/vlogin" not in self.page.url and "/login" not in self.page.url.lower():
                logger.info("✓ Login appears successful - URL changed from login page")
                login_successful = True
        
        if not login_successful:
            self.screenshot("login-timeout")
            logger.error(f"Login failed - timeout waiting for success indicators")
            logger.error(f"Final URL: {self.page.url}")
            raise TimeoutError("Login did not complete successfully")
    
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
        logger.info(f"Org: {org}")
        
        # Step 1: Logout first (clean state)
        self.logout_first()
        
        # Step 2: Navigate to login page
        self.navigate()
        
        # Step 3: Wait for login form to load
        self.page.wait_for_load_state("networkidle")
        self.screenshot("login-page-loaded")
        
        # Step 4: Fill form
        self.fill_email(email)
        self.fill_password(password)
        
        # Always try to fill org if provided
        if org:
            self.fill_org(org)
        else:
            logger.warning("No org provided - this might cause login to fail")
        
        # Take screenshot before clicking sign in
        self.screenshot("before-signin-click")
        
        # Step 5: Submit
        self.click_sign_in()
        
        # Step 6: Wait for success
        self.wait_for_login_success()
        
        # Step 7: Take screenshot
        self.screenshot("after-login")
        
        logger.info(f"=== Login completed for {email} ===")
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.
        
        Returns:
            True if logged in, False otherwise
        """
        logger.info("Checking if user is logged in...")
        
        # Wait for any redirects to complete
        # After login, URL goes to /vLoginRedirect then to final destination
        try:
            # Wait for redirect to complete (URL should not be vlogin or vLoginRedirect)
            for _ in range(10):  # Max 10 seconds
                current_url = self.page.url.lower()
                if "vlogin" not in current_url and "loginredirect" not in current_url:
                    break
                self.page.wait_for_timeout(1000)
            
            logger.info(f"Current URL after redirect: {self.page.url}")
        except Exception as e:
            logger.warning(f"Error waiting for redirect: {e}")
        
        # Check multiple indicators of being logged in
        logged_in_indicators = [
            self.SIGNED_IN_USER_ICON,
            '#signed_in_user_icon',
            '[data-testid="user-menu"]',
            'button:has-text("Logout")',
            'a:has-text("Logout")',
            'text=Sign out',
        ]
        
        for indicator in logged_in_indicators:
            if self.is_visible(indicator, timeout=3000):
                logger.info(f"✓ User is logged in (found: {indicator})")
                return True
        
        # Fallback: Check if URL is NOT login page
        current_url = self.page.url.lower()
        if "/vlogin" not in current_url and "/login" not in current_url:
            logger.info("✓ User appears logged in (not on login page)")
            return True
        
        logger.warning("✗ User does not appear to be logged in")
        logger.warning(f"Current URL: {self.page.url}")
        return False

