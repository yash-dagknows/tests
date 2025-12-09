"""
Base Page class for Page Object Model.

All page objects inherit from this base class.
"""

import logging
from typing import Optional
from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, page: Page):
        """
        Initialize base page.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
    
    def goto(self, path: str = "/") -> None:
        """
        Navigate to a path.
        
        Args:
            path: Relative path from base URL
        """
        logger.info(f"Navigating to: {path}")
        self.page.goto(path)
    
    def wait_for_load(self, timeout: int = 30000) -> None:
        """Wait for page to load."""
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
    
    def wait_for_network_idle(self, timeout: int = 30000) -> None:
        """Wait for network to be idle."""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def screenshot(self, name: str) -> None:
        """
        Take screenshot.
        
        Args:
            name: Screenshot filename
        """
        path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=path)
        logger.info(f"Screenshot saved: {path}")
    
    def click(self, selector: str, timeout: int = 10000) -> None:
        """
        Click element by selector.
        
        Args:
            selector: CSS selector or text
            timeout: Wait timeout in ms
        """
        self.page.locator(selector).click(timeout=timeout)
    
    def fill(self, selector: str, value: str, timeout: int = 10000) -> None:
        """
        Fill input field.
        
        Args:
            selector: CSS selector
            value: Value to fill
            timeout: Wait timeout in ms
        """
        self.page.locator(selector).fill(value, timeout=timeout)
    
    def get_text(self, selector: str) -> str:
        """
        Get text content of element.
        
        Args:
            selector: CSS selector
            
        Returns:
            Text content
        """
        return self.page.locator(selector).text_content()
    
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if element is visible.
        
        Args:
            selector: CSS selector
            timeout: Wait timeout in ms
            
        Returns:
            True if visible, False otherwise
        """
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: int = 30000
    ) -> Locator:
        """
        Wait for selector to reach state.
        
        Args:
            selector: CSS selector
            state: State to wait for (visible, hidden, attached)
            timeout: Wait timeout in ms
            
        Returns:
            Locator for the element
        """
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        return locator
    
    def wait_for_url(self, url_pattern: str, timeout: int = 30000) -> None:
        """
        Wait for URL to match pattern.
        
        Args:
            url_pattern: URL pattern (regex or substring)
            timeout: Wait timeout in ms
        """
        self.page.wait_for_url(url_pattern, timeout=timeout)
    
    def reload(self) -> None:
        """Reload current page."""
        self.page.reload()

