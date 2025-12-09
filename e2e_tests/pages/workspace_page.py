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
    
    # Selectors
    WORKSPACES_HEADING = 'h1:has-text("Your workspaces:"), h2:has-text("Your workspaces:")'
    WORKSPACE_LINK = 'a:has-text("{workspace_name}")'
    DEFAULT_WORKSPACE = 'a:has-text("Default")'
    
    def __init__(self, page):
        """Initialize workspace page."""
        super().__init__(page)
        self.landing_url = "/n/landing"
    
    def navigate_to_landing(self) -> None:
        """Navigate to landing page."""
        logger.info("Navigating to landing page")
        self.goto(self.landing_url)
        self.wait_for_load()
    
    def wait_for_workspaces_loaded(self, timeout: int = 10000) -> None:
        """
        Wait for workspaces to load.
        
        Args:
            timeout: Wait timeout in ms
        """
        logger.info("Waiting for workspaces to load")
        self.page.locator(self.WORKSPACES_HEADING).wait_for(
            state="visible",
            timeout=timeout
        )
        logger.info("✓ Workspaces loaded")
    
    def click_workspace(self, workspace_name: str) -> None:
        """
        Click on a workspace to enter it.
        
        Args:
            workspace_name: Name of workspace (e.g., "Default", "Agent", etc.)
        """
        logger.info(f"Clicking workspace: {workspace_name}")
        
        # Wait for workspace link to be visible
        workspace_selector = f'a:has-text("{workspace_name}")'
        self.page.locator(workspace_selector).wait_for(state="visible")
        
        # Click workspace
        self.page.locator(workspace_selector).click()
        
        # Wait for navigation
        self.page.wait_for_load_state("networkidle")
        logger.info(f"✓ Entered workspace: {workspace_name}")
    
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

