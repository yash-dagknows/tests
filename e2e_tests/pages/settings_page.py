"""
Settings Page Object.

Handles settings page navigation and configuration.
"""

import logging
from typing import Optional
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class SettingsPage(BasePage):
    """Settings page object for configuring DagKnows."""
    
    # Selectors for settings page
    SETTINGS_HEADING = 'text=Settings'
    
    # Tab selectors (horizontal strip at top)
    GENERAL_TAB = 'button:has-text("General"), a:has-text("General")'
    AI_TAB = 'button:has-text("AI"), a:has-text("AI")'
    USERS_TAB = 'button:has-text("Users"), a:has-text("Users")'
    WORKSPACES_TAB = 'button:has-text("Workspaces"), a:has-text("Workspaces")'
    PROXIES_TAB = 'button:has-text("Proxies"), a:has-text("Proxies")'
    AUTH_TOOLS_TAB = 'button:has-text("Authentication Tools"), a:has-text("Authentication Tools")'
    
    # Incident Response section selectors
    INCIDENT_RESPONSE_HEADING = 'text=Incident Response'
    DETERMINISTIC_RADIO = 'text=Deterministic'
    AI_SELECTED_RADIO = 'text=AI-Selected'
    AUTONOMOUS_RADIO = 'text=Autonomous'
    
    # Save button (if any)
    SAVE_BUTTON = 'button:has-text("Save")'
    
    def __init__(self, page):
        """Initialize settings page."""
        super().__init__(page)
        self.settings_url = "/vsettings"
    
    def navigate_to_settings(self) -> None:
        """Navigate to settings page."""
        logger.info("Navigating to settings page")
        self.goto(self.settings_url)
        self.wait_for_load()
        
        # Wait for settings page to load
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Take screenshot
        self.screenshot("settings-page-loaded")
        logger.info("✓ Settings page loaded")
    
    def click_settings_in_nav(self) -> None:
        """Click Settings link in left navigation bar."""
        logger.info("Clicking Settings in left navigation")
        
        # Take screenshot before clicking
        self.screenshot("before-settings-click")
        
        # Try multiple selector strategies for Settings link
        settings_selectors = [
            'a[href="/vsettings"]',  # Direct link
            'a[href*="settings"]',  # Link containing settings
            'text=Settings',  # Text match
            '[class*="nav"] >> text=Settings',  # In nav with text
        ]
        
        clicked = False
        for selector in settings_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    logger.info(f"Found Settings link with: {selector}")
                    locator.first.wait_for(state="visible", timeout=5000)
                    locator.first.click()
                    clicked = True
                    logger.info("✓ Clicked Settings link")
                    break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not clicked:
            self.screenshot("settings-link-not-found")
            raise Exception("Could not find Settings link in navigation")
        
        # Wait for navigation
        self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Verify we're on settings page
        current_url = self.page.url
        if "/vsettings" not in current_url and "/settings" not in current_url.lower():
            logger.warning(f"URL doesn't contain 'settings': {current_url}")
        
        logger.info(f"Current URL: {current_url}")
        self.screenshot("after-settings-navigation")
    
    def click_ai_tab(self) -> None:
        """Click the AI tab in the horizontal tab strip."""
        logger.info("Clicking AI tab")
        
        # Take screenshot before clicking
        self.screenshot("before-ai-tab-click")
        
        # Try multiple selectors for AI tab
        ai_tab_selectors = [
            'button:has-text("AI")',
            'a:has-text("AI")',
            '[role="tab"]:has-text("AI")',
            'text=AI',
        ]
        
        clicked = False
        for selector in ai_tab_selectors:
            try:
                locator = self.page.locator(selector)
                # Find one that's not within another text (e.g., not part of "AI-Selected")
                count = locator.count()
                if count > 0:
                    # Try to find the exact match (just "AI")
                    for i in range(count):
                        element = locator.nth(i)
                        text = element.text_content() or ""
                        text = text.strip()
                        if text == "AI" or "AI Configuration" in text:
                            logger.info(f"Found AI tab with selector: {selector}, text: {text}")
                            element.wait_for(state="visible", timeout=5000)
                            element.click()
                            clicked = True
                            logger.info("✓ Clicked AI tab")
                            break
                    if clicked:
                        break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not clicked:
            self.screenshot("ai-tab-not-found")
            raise Exception("Could not find AI tab")
        
        # Wait for AI settings to load
        self.page.wait_for_timeout(2000)
        
        # Take screenshot after clicking
        self.screenshot("after-ai-tab-click")
        logger.info("✓ AI settings loaded")
    
    def select_deterministic_mode(self) -> None:
        """Select Deterministic mode in Incident Response section."""
        logger.info("Selecting Deterministic mode")
        
        # Take screenshot before selection
        self.screenshot("before-deterministic-selection")
        
        # First, scroll down to make sure Incident Response section is visible
        # The section might be below the fold
        logger.info("Scrolling down to Incident Response section...")
        try:
            # Try to find "Enable Incident Response" toggle which is above the modes
            enable_toggle = self.page.locator('text=Enable Incident Response')
            if enable_toggle.count() > 0:
                logger.info("Found 'Enable Incident Response' - scrolling to it")
                enable_toggle.first.scroll_into_view_if_needed()
                self.page.wait_for_timeout(1000)
        except Exception as e:
            logger.debug(f"Could not scroll to Enable Incident Response: {e}")
        
        # Take screenshot after scrolling
        self.screenshot("after-scroll-to-incident-response")
        
        # Now look for the Incident Response section heading (use .first to avoid strict mode violation)
        try:
            # There are multiple "Incident Response" texts, use the heading one
            incident_heading = self.page.locator('text=Incident Response').first
            incident_heading.scroll_into_view_if_needed()
            logger.info("✓ Incident Response section visible")
        except Exception as e:
            logger.warning(f"Could not find Incident Response heading: {e}")
        
        # Wait a moment for the section to be fully visible
        self.page.wait_for_timeout(1000)
        
        # Take screenshot showing the Incident Response section
        self.screenshot("incident-response-section-visible")
        
        # Now try to find and click Deterministic mode
        # Look for the Deterministic option with "Always Active" badge
        deterministic_selectors = [
            'text=Deterministic',  # Text match (will find all, we'll use .first)
            ':text("Deterministic")',  # Case insensitive
            '[role="radio"]:has-text("Deterministic")',  # Radio button with text
            'button:has-text("Deterministic")',  # If it's a button
            'div:has-text("Deterministic") >> visible=true',  # Visible div
        ]
        
        selected = False
        for selector in deterministic_selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                if count > 0:
                    logger.info(f"Found Deterministic option with: {selector} (count: {count})")
                    
                    # Scroll to and click the first visible match
                    element = locator.first
                    element.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(500)
                    element.wait_for(state="visible", timeout=5000)
                    
                    # Take screenshot before clicking
                    self.screenshot("before-clicking-deterministic")
                    
                    # Click it
                    element.click()
                    
                    selected = True
                    logger.info("✓ Clicked Deterministic mode")
                    break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not selected:
            logger.error("Could not find Deterministic mode option")
            self.screenshot("deterministic-not-found")
            # Try to log what's visible
            try:
                page_text = self.page.inner_text('body')
                if "Deterministic" in page_text:
                    logger.error("'Deterministic' text IS present on page")
                else:
                    logger.error("'Deterministic' text NOT found on page")
            except Exception:
                pass
            raise Exception("Could not find or click Deterministic mode option")
        
        # Wait for selection to register
        self.page.wait_for_timeout(2000)
        
        # Take screenshot after selection
        self.screenshot("after-deterministic-selection")
        logger.info("✓ Deterministic mode selected")
    
    def select_ai_selected_mode(self) -> None:
        """Select AI-Selected mode in Incident Response section."""
        logger.info("Selecting AI-Selected mode")
        
        self.screenshot("before-ai-selected-selection")
        
        # Scroll to Incident Response section
        try:
            enable_toggle = self.page.locator('text=Enable Incident Response')
            if enable_toggle.count() > 0:
                enable_toggle.first.scroll_into_view_if_needed()
                self.page.wait_for_timeout(1000)
        except Exception:
            pass
        
        ai_selected_selectors = [
            'text=AI-Selected',
            '[value="ai_selected"]',
            'input[type="radio"] + label:has-text("AI-Selected")',
        ]
        
        for selector in ai_selected_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    locator.first.scroll_into_view_if_needed()
                    locator.first.wait_for(state="visible", timeout=5000)
                    locator.first.click()
                    logger.info("✓ AI-Selected mode selected")
                    self.page.wait_for_timeout(2000)
                    self.screenshot("after-ai-selected-selection")
                    return
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        self.screenshot("ai-selected-not-found")
        raise Exception("Could not select AI-Selected mode")
    
    def select_autonomous_mode(self) -> None:
        """Select Autonomous mode in Incident Response section."""
        logger.info("Selecting Autonomous mode")
        
        self.screenshot("before-autonomous-selection")
        
        # Scroll to Incident Response section
        try:
            enable_toggle = self.page.locator('text=Enable Incident Response')
            if enable_toggle.count() > 0:
                enable_toggle.first.scroll_into_view_if_needed()
                self.page.wait_for_timeout(1000)
        except Exception:
            pass
        
        autonomous_selectors = [
            'text=Autonomous',
            '[value="autonomous"]',
            'input[type="radio"] + label:has-text("Autonomous")',
        ]
        
        for selector in autonomous_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    locator.first.scroll_into_view_if_needed()
                    locator.first.wait_for(state="visible", timeout=5000)
                    locator.first.click()
                    logger.info("✓ Autonomous mode selected")
                    self.page.wait_for_timeout(2000)
                    self.screenshot("after-autonomous-selection")
                    return
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        self.screenshot("autonomous-not-found")
        raise Exception("Could not select Autonomous mode")
    
    def verify_mode_selected(self, mode: str) -> bool:
        """
        Verify that a specific mode is selected.
        
        Args:
            mode: "deterministic", "ai_selected", or "autonomous"
        
        Returns:
            True if mode is selected
        """
        logger.info(f"Verifying {mode} mode is selected")
        
        # Check if the radio button is checked
        # This depends on the actual HTML structure
        mode_text = {
            "deterministic": "Deterministic",
            "ai_selected": "AI-Selected",
            "autonomous": "Autonomous"
        }.get(mode, mode)
        
        try:
            # Look for checked radio button or active state
            checked_selectors = [
                f'text={mode_text} >> .. >> input[checked]',
                f'text={mode_text} >> .. >> [class*="active"]',
                f'text={mode_text} >> .. >> [class*="selected"]',
            ]
            
            for selector in checked_selectors:
                if self.page.locator(selector).count() > 0:
                    logger.info(f"✓ {mode_text} mode is selected")
                    return True
            
            logger.warning(f"Could not verify {mode_text} mode selection")
            return False
        except Exception as e:
            logger.warning(f"Error verifying mode: {e}")
            return False
    
    def save_settings(self) -> None:
        """Save settings if there's a save button."""
        logger.info("Checking for Save button")
        
        try:
            save_button = self.page.locator(self.SAVE_BUTTON)
            if save_button.count() > 0 and save_button.is_visible():
                logger.info("Clicking Save button")
                save_button.click()
                self.page.wait_for_timeout(2000)
                logger.info("✓ Settings saved")
            else:
                logger.info("No Save button found (settings auto-save)")
        except Exception as e:
            logger.warning(f"Could not save settings: {e}")


