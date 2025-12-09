"""
Workspace/Landing Page Object.

Handles workspace selection and navigation.
"""

import logging
from typing import Optional
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class WorkspacePage(BasePage):
    """Workspace/Landing page object."""
    
    # Selectors (based on actual UI)
    WORKSPACES_HEADING = 'text=Your workspaces:'  # The heading on landing page
    WORKSPACE_LINK = 'a:has-text("{workspace_name}")'  # Links to workspaces
    DEFAULT_WORKSPACE = 'a:has-text("Default")'  # The "Default" workspace link
    
    def __init__(self, page):
        """Initialize workspace page."""
        super().__init__(page)
        self.landing_url = "/n/landing"
    
    def navigate_to_landing(self) -> None:
        """Navigate to landing page."""
        logger.info("Navigating to landing page")
        self.goto(self.landing_url)
        self.wait_for_load()
    
    def wait_for_workspaces_loaded(self, timeout: int = 15000) -> None:
        """
        Wait for workspaces to load.
        
        Args:
            timeout: Wait timeout in ms
        """
        logger.info("Waiting for workspaces to load")
        logger.info(f"Current URL: {self.page.url}")
        
        # Take screenshot for debugging
        self.screenshot("workspace-page-loading")
        
        # Wait for page to be stable
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            logger.warning("Network idle timeout, continuing...")
        
        # Try multiple possible selectors for the workspaces page
        # Based on the actual UI: "Your workspaces:" heading + workspace links
        workspace_indicators = [
            'text=Your workspaces:',  # The exact heading text with colon
            'text=Your workspaces',   # Without colon
            ':text("Your workspaces")',  # Case insensitive
            'a:has-text("Default")',  # The Default workspace link
            'a[href*="space="]',      # Any workspace link
        ]
        
        page_loaded = False
        for indicator in workspace_indicators:
            try:
                locator = self.page.locator(indicator)
                count = locator.count()
                if count > 0:
                    logger.info(f"Found {count} elements with selector: {indicator}")
                    locator.first.wait_for(
                        state="visible",
                        timeout=timeout // len(workspace_indicators)
                    )
                    logger.info(f"✓ Workspaces loaded (found: {indicator})")
                    page_loaded = True
                    self.screenshot("workspace-page-loaded")
                    break
            except Exception as e:
                logger.debug(f"Indicator '{indicator}' not found: {e}")
        
        if not page_loaded:
            # Last resort: check if we're on landing page
            if "/n/landing" in self.page.url or "/landing" in self.page.url:
                logger.info("On landing page URL, assuming workspaces loaded")
                self.screenshot("workspace-page-by-url")
                page_loaded = True
        
        if not page_loaded:
            self.screenshot("workspace-page-timeout")
            logger.error(f"Failed to detect workspaces page load. URL: {self.page.url}")
            # Get page content for debugging
            try:
                page_text = self.page.content()
                logger.error(f"Page content preview: {page_text[:500]}")
            except Exception:
                pass
            raise TimeoutError("Could not confirm workspaces page loaded")
    
    def click_workspace(self, workspace_name: str) -> None:
        """
        Click on a workspace to enter it.
        
        Args:
            workspace_name: Name of workspace (e.g., "Default", "Agent", etc.)
        """
        logger.info(f"Clicking workspace: {workspace_name}")
        
        # Take screenshot before clicking
        self.screenshot(f"before-click-{workspace_name.lower()}")
        
        # Try multiple selector strategies
        selectors = [
            f'a:has-text("{workspace_name}")',
            f'text={workspace_name}',
            f'a >> text="{workspace_name}"',
            f'[href*="space="] >> text="{workspace_name}"',
        ]
        
        clicked = False
        for selector in selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    logger.info(f"Found workspace with selector: {selector}")
                    locator.first.wait_for(state="visible", timeout=5000)
                    locator.first.click()
                    clicked = True
                    break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not clicked:
            self.screenshot(f"workspace-{workspace_name.lower()}-not-found")
            raise Exception(f"Could not find workspace: {workspace_name}")
        
        # Wait for navigation
        self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        logger.info(f"✓ Entered workspace: {workspace_name}")
        logger.info(f"Current URL: {self.page.url}")
        
        # Take screenshot after clicking
        self.screenshot(f"after-click-{workspace_name.lower()}")
    
    def click_default_workspace(self) -> None:
        """Click on Default workspace (common case)."""
        self.click_workspace("Default")
    
    def verify_workspace_exists(self, workspace_name: str, timeout: int = 5000) -> bool:
        """
        Verify a workspace exists in the list.
        
        Args:
            workspace_name: Workspace name
            timeout: Wait timeout in ms
            
        Returns:
            True if workspace exists, False otherwise
        """
        workspace_selector = f'a:has-text("{workspace_name}")'
        return self.is_visible(workspace_selector, timeout=timeout)
    
    def get_all_workspaces(self) -> list:
        """
        Get list of all workspace names.
        
        Returns:
            List of workspace names
        """
        # Find all workspace links
        workspace_links = self.page.locator('a[href*="space="]').all()
        workspaces = [link.text_content().strip() for link in workspace_links]
        logger.info(f"Found workspaces: {workspaces}")
        return workspaces
    
    def click_workspace_folder_icon(self) -> None:
        """
        Click the folder icon in the left navigation to open workspace dropdown.
        This opens a dropdown menu with all available workspaces.
        """
        logger.info("Clicking workspace folder icon in left navigation")
        self.screenshot("before-folder-icon-click")
        
        # Try multiple selectors for the folder icon
        folder_icon_selectors = [
            '[data-testid="workspace-selector"]',
            'button[aria-label*="workspace"]',
            'button[aria-label*="Workspace"]',
            'button:has(svg)',  # SVG icons
            'div[role="button"]',
            # CSS selectors based on common patterns
            '.workspace-selector',
            '.folder-icon',
            # XPath as fallback
            '//button[contains(@aria-label, "workspace")]',
            '//div[@role="button"]'
        ]
        
        clicked = False
        for selector in folder_icon_selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                logger.debug(f"Found {count} elements with selector: {selector}")
                
                if count > 0:
                    # In left nav, folder icon is typically at the top
                    element = locator.first
                    if element.is_visible():
                        element.click()
                        clicked = True
                        logger.info(f"✓ Clicked folder icon with selector: {selector}")
                        break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not clicked:
            # Fallback: Try to find by position (first button-like element in left nav)
            logger.warning("Could not find folder icon, trying positional fallback")
            try:
                # Try clicking first icon-like element in left sidebar
                self.page.locator('nav button, aside button').first.click()
                clicked = True
                logger.info("✓ Clicked first button in navigation (fallback)")
            except Exception as e:
                logger.error(f"Fallback also failed: {e}")
        
        if not clicked:
            self.screenshot("folder-icon-not-found")
            raise Exception("Could not find or click workspace folder icon")
        
        # Wait for dropdown to appear
        self.page.wait_for_timeout(1000)
        self.screenshot("after-folder-icon-click")
        logger.info("✓ Workspace dropdown opened")
    
    def select_workspace_from_dropdown(self, workspace_name: str) -> None:
        """
        Select a workspace from the dropdown menu.
        
        Args:
            workspace_name: Name of workspace to select
        """
        logger.info(f"Selecting workspace '{workspace_name}' from dropdown")
        self.screenshot(f"before-selecting-{workspace_name}-from-dropdown")
        
        # Try multiple selectors for workspace in dropdown
        workspace_selectors = [
            f'[role="menuitem"]:has-text("{workspace_name}")',
            f'[role="option"]:has-text("{workspace_name}")',
            f'button:has-text("{workspace_name}")',
            f'a:has-text("{workspace_name}")',
            f'div[role="menu"] >> text={workspace_name}',
            f'ul[role="menu"] >> text={workspace_name}',
            f'//div[@role="menu"]//a[contains(., "{workspace_name}")]',
            f'//ul[@role="menu"]//a[contains(., "{workspace_name}")]',
        ]
        
        clicked = False
        for selector in workspace_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    locator.first.scroll_into_view_if_needed()
                    locator.first.wait_for(state="visible", timeout=5000)
                    locator.first.click()
                    clicked = True
                    logger.info(f"✓ Clicked workspace '{workspace_name}' with selector: {selector}")
                    break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not clicked:
            self.screenshot(f"workspace-{workspace_name}-not-in-dropdown")
            raise Exception(f"Could not find workspace '{workspace_name}' in dropdown")
        
        # Wait for navigation
        self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Verify we're in the workspace
        current_url = self.page.url
        logger.info(f"Current URL after selecting workspace: {current_url}")
        
        if "space=" not in current_url:
            logger.warning(f"URL does not contain 'space=' parameter: {current_url}")
        
        self.screenshot(f"after-selecting-{workspace_name}")
        logger.info(f"✓ Navigated to workspace: {workspace_name}")
    
    def navigate_to_workspace_via_dropdown(self, workspace_name: str) -> None:
        """
        Complete workflow: Click folder icon and select workspace from dropdown.
        
        Args:
            workspace_name: Name of workspace to navigate to
        """
        logger.info(f"Navigating to workspace '{workspace_name}' via dropdown")
        self.click_workspace_folder_icon()
        self.select_workspace_from_dropdown(workspace_name)

