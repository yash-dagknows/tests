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
    GENERAL_TAB = 'button:has-text("General"), [role="tab"]:has-text("General")'
    AI_TAB = 'button:has-text("AI"), [role="tab"]:has-text("AI")'
    USERS_TAB = 'button:has-text("Users"), [role="tab"]:has-text("Users")'
    WORKSPACES_TAB = 'button:has-text("Workspaces"), [role="tab"]:has-text("Workspaces")'
    PROXIES_TAB = 'button:has-text("Proxies"), [role="tab"]:has-text("Proxies")'
    AUTH_TOOLS_TAB = 'button:has-text("Authentication Tools"), [role="tab"]:has-text("Authentication Tools")'
    
    # Workspace management selectors
    WORKSPACE_NAME_INPUT = 'input[placeholder="Workspace name"], input[name*="workspace"]'
    ADD_WORKSPACE_BUTTON = 'button:has-text("Add")'
    CURRENT_WORKSPACES_HEADING = 'text=Current workspaces'
    WORKSPACE_TABLE = 'table'
    WORKSPACE_ROW = 'tr:has-text("{workspace_name}")'
    
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
    
    def get_current_alert_mode(self) -> str:
        """
        Get the currently selected alert handling mode.
        
        Returns:
            "deterministic", "ai_selected", "autonomous", or "unknown"
        """
        logger.info("Detecting current alert handling mode...")
        
        # Look for the radio button or option that appears selected/active
        # Check for "Active" badge or checked state
        modes = [
            ("deterministic", ['text=Deterministic >> .. >> text=Always Active', 
                              'text=Deterministic >> .. >> [class*="active"]']),
            ("ai_selected", ['text=AI-Selected >> .. >> text=Active',
                            'text=AI-Selected >> .. >> [class*="active"]']),
            ("autonomous", ['text=Autonomous >> .. >> text=Active',
                           'text=Autonomous >> .. >> [class*="active"]'])
        ]
        
        for mode_name, selectors in modes:
            for selector in selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        logger.info(f"✓ Current mode: {mode_name}")
                        return mode_name
                except Exception:
                    pass
        
        # Fallback: check for visual indicators in screenshot
        self.screenshot("current-mode-check")
        logger.warning("Could not detect current mode from DOM")
        return "unknown"
    
    def click_workspaces_tab(self) -> None:
        """Click the Workspaces tab in the horizontal tab strip."""
        logger.info("Clicking Workspaces tab")
        self.screenshot("before-workspaces-tab-click")
        
        # Try multiple selectors for Workspaces tab
        workspaces_tab_selectors = [
            '[role="tab"]:has-text("Workspaces")',
            'button:has-text("Workspaces")',
            'a:has-text("Workspaces")',
        ]
        
        clicked = False
        for selector in workspaces_tab_selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                if count > 0:
                    # Find the tab in the horizontal strip (not nav link)
                    for i in range(count):
                        element = locator.nth(i)
                        text = element.text_content() or ""
                        if "Workspaces" in text and len(text.strip()) < 20:
                            logger.info(f"Found Workspaces tab with selector: {selector}")
                            element.wait_for(state="visible", timeout=5000)
                            element.click()
                            clicked = True
                            logger.info("✓ Clicked Workspaces tab")
                            break
                    if clicked:
                        break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not clicked:
            self.screenshot("workspaces-tab-not-found")
            raise Exception("Could not find Workspaces tab")
        
        # Wait for workspace settings to load
        self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.screenshot("after-workspaces-tab-click")
        logger.info("✓ Workspaces settings loaded")
    
    def create_workspace(self, workspace_name: str) -> None:
        """
        Create a new workspace.
        
        Args:
            workspace_name: Name of the workspace to create
        """
        logger.info(f"Creating workspace: {workspace_name}")
        self.screenshot(f"before-create-workspace-{workspace_name}")
        
        # Find workspace name input
        input_selectors = [
            'input[placeholder="Workspace name"]',
            'input[name*="workspace"]',
            'input[type="text"]',
        ]
        
        workspace_input = None
        for selector in input_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    first_input = locator.first
                    if first_input.is_visible():
                        workspace_input = first_input
                        logger.info(f"Found workspace input with: {selector}")
                        break
            except Exception:
                pass
        
        if not workspace_input:
            self.screenshot("workspace-input-not-found")
            raise Exception("Could not find workspace name input field")
        
        # Clear and type workspace name
        workspace_input.click()
        workspace_input.fill("")
        workspace_input.fill(workspace_name)
        logger.info(f"✓ Typed workspace name: {workspace_name}")
        
        # Wait a moment for UI to update (button might become enabled after input)
        self.page.wait_for_timeout(1000)
        
        self.screenshot(f"after-typing-workspace-{workspace_name}")
        
        # Click Add button (it's next to the input field)
        add_button_selectors = [
            'button:has-text("Add")',
            'button.btn:has-text("Add")',
            'button[class*="btn"]:has-text("Add")',
            'input[type="button"][value="Add"]',
            'input[type="submit"][value="Add"]',
            'button[type="submit"]',
            # Try finding near the workspace input
            'input[placeholder="Workspace name"] ~ button',
            'input[placeholder="Workspace name"] + button',
            # Look in the Create new workspace section
            'text=Create new workspace >> .. >> button:has-text("Add")',
            'text=Create new workspace >> .. >> button',
            # XPath fallbacks
            '//button[contains(text(), "Add")]',
            '//input[@type="button" and @value="Add"]',
        ]
        
        add_clicked = False
        for selector in add_button_selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                logger.debug(f"Selector '{selector}' found {count} elements")
                
                if count > 0:
                    # Try to find the Add button specifically in Create workspace section
                    element = locator.first
                    if element.is_visible(timeout=2000):
                        element.click()
                        add_clicked = True
                        logger.info(f"✓ Clicked Add button with selector: {selector}")
                        break
            except Exception as e:
                logger.debug(f"Add button selector '{selector}' failed: {e}")
        
        if not add_clicked:
            # Final attempt: Look for any visible button near the input
            try:
                logger.warning("Trying fallback: clicking first visible button near input")
                # Find all buttons on the page
                all_buttons = self.page.locator('button').all()
                logger.info(f"Found {len(all_buttons)} total buttons on page")
                
                # Try to find a button that's close to the input and has "Add" text
                for btn in all_buttons:
                    try:
                        text = btn.text_content() or ""
                        if "Add" in text and btn.is_visible():
                            logger.info(f"Found button with text: '{text}'")
                            btn.click()
                            add_clicked = True
                            logger.info("✓ Clicked Add button (fallback method)")
                            break
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Fallback also failed: {e}")
        
        if not add_clicked:
            self.screenshot("add-button-not-found")
            # Log page content for debugging
            try:
                logger.error("Page HTML snippet:")
                logger.error(self.page.content()[:2000])
            except Exception:
                pass
            raise Exception("Could not find or click Add button")
        
        # Wait for workspace to be created
        self.page.wait_for_timeout(3000)
        self.screenshot(f"after-create-workspace-{workspace_name}")
        logger.info(f"✓ Workspace '{workspace_name}' creation requested")
    
    def verify_workspace_in_list(self, workspace_name: str, timeout: int = 10000) -> bool:
        """
        Verify that a workspace appears in the Current workspaces list.
        
        Args:
            workspace_name: Workspace name to verify
            timeout: Wait timeout in ms
            
        Returns:
            True if workspace found, False otherwise
        """
        logger.info(f"Verifying workspace '{workspace_name}' in list")
        self.screenshot(f"checking-workspace-{workspace_name}")
        
        # Wait for Current workspaces section to load
        try:
            self.page.locator('text=Current workspaces').wait_for(
                state="visible",
                timeout=5000
            )
        except Exception:
            logger.warning("Could not find 'Current workspaces' heading")
        
        # Look for workspace in the table
        workspace_selectors = [
            f'text={workspace_name}',
            f'tr:has-text("{workspace_name}")',
            f'td:has-text("{workspace_name}")',
        ]
        
        for selector in workspace_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    locator.first.wait_for(state="visible", timeout=timeout)
                    logger.info(f"✓ Workspace '{workspace_name}' found in list")
                    return True
            except Exception as e:
                logger.debug(f"Selector '{selector}' not found: {e}")
        
        logger.warning(f"✗ Workspace '{workspace_name}' not found in list")
        self.screenshot(f"workspace-{workspace_name}-not-found")
        return False

    # ==================== RBAC Role Management Methods ====================
    
    # RBAC Tab selector
    RBAC_TAB = 'button:has-text("Workspaces"), [role="tab"]:has-text("Workspaces")'  # Workspaces tab shows RBAC content
    
    # Create Custom Role selectors
    CREATE_CUSTOM_ROLE_HEADING = 'text=Create new custom role'
    ROLE_NAME_INPUT = 'input[placeholder="Role name"]'
    ADD_ROLE_BUTTON = 'button:has-text("Add")'  # Same button used for workspace, but in RBAC context
    
    # Privileges table selectors
    PRIVILEGES_TABLE_HEADING = 'text=Privileges'
    # The privileges table is the table that comes after "Create new custom role" section
    # It has "Privileges" as the first column header and role names as other column headers
    # It contains privilege rows like "task.view_code", "task.list", etc.
    PRIVILEGES_TABLE = 'table:has-text("task.view_code"), table:has-text("task.list"), table:has-text("task.view_io"), text=Privileges >> xpath=following::table[1], text=Create new custom role >> xpath=following::table[1]'
    PRIVILEGE_ROW = 'tr:has-text("{privilege_name}")'  # Row for a specific privilege
    ROLE_COLUMN_HEADER = 'th:has-text("{role_name}")'  # Column header for a role
    PRIVILEGE_CHECKBOX = 'tr:has-text("{privilege_name}") >> td >> input[type="checkbox"]'  # Checkbox in privilege row
    
    def navigate_to_settings_page(self) -> None:
        """
        Navigate to the main settings page (without any tab parameter).
        """
        logger.info("Navigating to settings page")
        self.goto(self.settings_url)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(2000)  # Give time for content to load
        self.screenshot("settings-page-loaded")
        logger.info("✓ Settings page loaded")
        
        # Verify we're on settings page
        current_url = self.page.url
        if "/vsettings" not in current_url:
            logger.warning(f"URL does not contain '/vsettings'. Current URL: {current_url}")
    
    def click_workspaces_tab(self) -> None:
        """
        Click the "Workspaces" tab on the settings page.
        This tab shows the RBAC content including "Create new custom role" section.
        """
        logger.info("Clicking Workspaces tab on settings page")
        self.screenshot("before-workspaces-tab-click")
        
        # Try multiple selectors for the Workspaces tab
        workspaces_tab_selectors = [
            self.WORKSPACES_TAB,
            'button:has-text("Workspaces")',
            '[role="tab"]:has-text("Workspaces")',
            'div[role="tablist"] >> text=Workspaces',
            '//button[contains(text(), "Workspaces")]',
        ]
        
        clicked = False
        for selector in workspaces_tab_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    element = locator.first
                    element.scroll_into_view_if_needed()
                    element.wait_for(state="visible", timeout=5000)
                    element.click()
                    clicked = True
                    logger.info(f"✓ Clicked Workspaces tab with selector: {selector}")
                    break
            except Exception as e:
                logger.debug(f"Could not click Workspaces tab with {selector}: {e}")
        
        if not clicked:
            self.screenshot("workspaces-tab-not-found")
            raise Exception("Could not find or click Workspaces tab")
        
        # Wait for tab content to load
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(2000)  # Give time for content to load
        self.screenshot("after-workspaces-tab-click")
        logger.info("✓ Workspaces tab clicked and content loaded")
        
        # Verify URL contains tab=rbac (Workspaces tab sets this)
        current_url = self.page.url
        if "tab=rbac" not in current_url:
            logger.info(f"URL after clicking Workspaces tab: {current_url}")
            # URL might not have tab=rbac, but content should be loaded
    
    def navigate_to_rbac_tab(self) -> None:
        """
        Navigate to RBAC tab by going to settings and clicking Workspaces tab.
        Alternative: Navigate directly to RBAC tab via URL.
        """
        logger.info("Navigating to RBAC tab via Workspaces tab")
        self.navigate_to_settings_page()
        self.click_workspaces_tab()
        logger.info("✓ RBAC tab loaded (via Workspaces tab)")
    
    def scroll_to_create_custom_role_section(self) -> None:
        """Scroll down to the 'Create new custom role' section."""
        logger.info("Scrolling to 'Create new custom role' section")
        self.screenshot("before-scroll-to-create-role")
        
        try:
            # Find the heading and scroll to it
            heading = self.page.locator(self.CREATE_CUSTOM_ROLE_HEADING)
            heading.first.wait_for(state="visible", timeout=10000)
            heading.first.scroll_into_view_if_needed()
            self.page.wait_for_timeout(1000)
            logger.info("✓ Scrolled to 'Create new custom role' section")
            self.screenshot("after-scroll-to-create-role")
        except Exception as e:
            logger.error(f"Could not find 'Create new custom role' heading: {e}")
            self.screenshot("create-role-heading-not-found")
            # Fallback: scroll down a bit
            self.page.evaluate("window.scrollBy(0, 800)")
            self.page.wait_for_timeout(1000)
            raise Exception("Could not scroll to 'Create new custom role' section")
    
    def create_custom_role(self, role_name: str) -> None:
        """
        Create a new custom role.
        This method mimics the exact pattern used in create_workspace().
        
        IMPORTANT: Must be on RBAC tab (tab=rbac) which shows Workspaces content.
        
        Args:
            role_name: Name of the role to create (e.g., "read1")
        """
        logger.info(f"Creating custom role: {role_name}")
        self.screenshot(f"before-create-role-{role_name}")
        
        # Verify we're on settings page with Workspaces tab
        current_url = self.page.url
        if "/vsettings" not in current_url:
            logger.warning(f"Not on settings page! Current URL: {current_url}")
            logger.info("Navigating to settings page...")
            self.navigate_to_settings_page()
        
        # If not on Workspaces tab, click it
        # Check if Workspaces tab is active by looking for "Create new custom role" section
        create_role_section = self.page.locator(self.CREATE_CUSTOM_ROLE_HEADING)
        if create_role_section.count() == 0 or not create_role_section.first.is_visible(timeout=3000):
            logger.info("Workspaces tab not active, clicking it...")
            self.click_workspaces_tab()
        else:
            logger.info("Workspaces tab appears to be active (Create new custom role section visible)")
        
        # Scroll to the section first
        self.scroll_to_create_custom_role_section()
        
        # Find role name input (exactly like workspace creation)
        input_selectors = [
            'input[placeholder="Role name"]',
            'input[name*="role"]',
            'input[type="text"]',
        ]
        
        role_input = None
        for selector in input_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    first_input = locator.first
                    if first_input.is_visible():
                        role_input = first_input
                        logger.info(f"Found role input with: {selector}")
                        break
            except Exception:
                pass
        
        if not role_input:
            self.screenshot("role-name-input-not-found")
            raise Exception("Could not find role name input field")
        
        # Clear and type role name (exactly like workspace creation)
        role_input.click()
        role_input.fill("")
        role_input.fill(role_name)
        logger.info(f"✓ Typed role name: {role_name}")
        
        # Wait a moment for UI to update (button might become enabled after input)
        self.page.wait_for_timeout(1000)
        
        self.screenshot(f"after-typing-role-name-{role_name}")
        
        # Click Add button - MUST be within "Create new custom role" section (RBAC tab)
        # Prioritize selectors that are scoped to the "Create new custom role" section
        # to avoid finding buttons from other tabs (like General settings)
        add_button_selectors = [
            # Most specific: Within "Create new custom role" section
            'text=Create new custom role >> .. >> button:has-text("Add")',
            'text=Create new custom role >> .. >> button',
            '//div[contains(., "Create new custom role")]//button[contains(text(), "Add")]',
            # Near the role input (should be in the same section)
            'input[placeholder="Role name"] ~ button:has-text("Add")',
            'input[placeholder="Role name"] + button:has-text("Add")',
            'input[placeholder="Role name"] ~ button',
            'input[placeholder="Role name"] + button',
            # More generic (but still try to verify it's in the right section)
            'button:has-text("Add")',
            'button.btn:has-text("Add")',
            'input[type="button"][value="Add"]',
        ]
        
        add_clicked = False
        for selector in add_button_selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                logger.debug(f"Selector '{selector}' found {count} elements")
                
                if count > 0:
                    # Check all matching elements to find the one in "Create new custom role" section
                    for idx in range(count):
                        element = locator.nth(idx)
                        if element.is_visible(timeout=2000):
                            # Verify it's in the "Create new custom role" section by checking position
                            try:
                                element_box = element.bounding_box()
                                input_box = role_input.bounding_box()
                                
                                if element_box and input_box:
                                    # Check if button is near the role input (same section)
                                    y_diff = abs(element_box['y'] - input_box['y'])
                                    x_diff = element_box['x'] - input_box['x']
                                    
                                    # Button should be on same row (within 30px vertically) and to the right
                                    if y_diff < 30 and x_diff > 0:
                                        element.click()
                                        add_clicked = True
                                        logger.info(f"✓ Clicked Add button with selector: {selector} (element {idx}, verified in section)")
                                        break
                            except Exception:
                                # If position check fails, still try clicking if it's one of the specific selectors
                                if 'Create new custom role' in selector or 'Role name' in selector:
                                    element.click()
                                    add_clicked = True
                                    logger.info(f"✓ Clicked Add button with selector: {selector} (element {idx}, section-specific)")
                                    break
                    
                    if add_clicked:
                        break
            except Exception as e:
                logger.debug(f"Add button selector '{selector}' failed: {e}")
        
        if not add_clicked:
            # Final attempt: Look for Add buttons near the role input by position only
            try:
                logger.warning("Trying fallback: finding Add button by position near role input")
                # Find all Add buttons
                all_add_buttons = self.page.locator('button:has-text("Add")').all()
                logger.info(f"Found {len(all_add_buttons)} Add buttons on page")
                
                input_box = role_input.bounding_box()
                if input_box:
                    for btn in all_add_buttons:
                        if btn.is_visible():
                            try:
                                btn_box = btn.bounding_box()
                                if btn_box:
                                    y_diff = abs(btn_box['y'] - input_box['y'])
                                    x_diff = btn_box['x'] - input_box['x']
                                    # Button should be on same row (within 30px) and to the right
                                    if y_diff < 30 and x_diff > 0:
                                        btn.click()
                                        add_clicked = True
                                        logger.info(f"✓ Clicked Add button by position fallback (y_diff={y_diff:.0f}, x_diff={x_diff:.0f})")
                                        break
                            except Exception:
                                pass
            except Exception as e:
                logger.debug(f"Fallback button search failed: {e}")
        
        if not add_clicked:
            self.screenshot("add-role-button-not-found")
            raise Exception("Could not find or click Add button for role")
        
        # Wait for network requests to complete
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for role to appear in privileges table (user reported ~1 second, using 5 seconds for safety)
        logger.info("Waiting for role to appear in privileges table...")
        role_appeared = False
        for wait_attempt in range(10):  # Check every 500ms for up to 5 seconds
            self.page.wait_for_timeout(500)
            # Check if role name appears in privileges table text
            try:
                privileges_table = self._find_privileges_table()
                table_text = privileges_table.text_content()
                if role_name in table_text:
                    logger.info(f"✓ Role '{role_name}' detected in privileges table (attempt {wait_attempt + 1})")
                    role_appeared = True
                    break
            except Exception:
                pass
        
        if not role_appeared:
            logger.warning(f"Role '{role_name}' not detected in table text after 5 seconds, continuing anyway...")
            self.page.wait_for_timeout(2000)  # Additional wait
        
        self.screenshot(f"after-create-role-{role_name}")
        logger.info(f"✓ Custom role '{role_name}' creation requested")
    
    def verify_role_in_privileges_table(self, role_name: str, timeout: int = 20000) -> None:
        """
        Verify that a newly created role appears in the privileges table.
        This method waits for the role to appear and handles horizontal scrolling.
        
        IMPORTANT: After role creation, the role column may be off-screen and requires
        horizontal scrolling in the privileges table to find it.
        
        Args:
            role_name: Name of the role to verify
            timeout: Wait timeout in ms (increased default to 20 seconds)
        """
        logger.info(f"Verifying role '{role_name}' in privileges table")
        logger.info("Note: Role column may require horizontal scrolling to be visible")
        self.screenshot(f"checking-role-{role_name}")
        
        # Wait for privileges table to be visible
        try:
            self.page.locator(self.PRIVILEGES_TABLE_HEADING).wait_for(state="visible", timeout=10000)
            logger.info("✓ Privileges table heading is visible")
        except Exception:
            logger.warning("Could not find 'Privileges' heading, but continuing...")
        
        # Scroll to privileges table first
        self.scroll_to_privileges_table()
        
        # Wait a bit more for the table to update with the new role
        self.page.wait_for_timeout(2000)
        
        # IMPORTANT: After role creation, we MUST scroll horizontally to find the role column
        # The role is added as a new column, which may be off-screen to the right
        logger.info("Scrolling horizontally to find newly created role column...")
        try:
            self.scroll_horizontally_to_role_column(role_name)
            logger.info("✓ Scrolled horizontally to find role column")
        except Exception as e:
            logger.warning(f"Initial horizontal scroll attempt: {e}")
            # Continue with other strategies
        
        # Try multiple strategies to find the role
        role_found = False
        
        # Strategy 1: Look for exact role name in table headers (try without scrolling first)
        role_header_selectors = [
            f'th:has-text("{role_name}")',  # Exact match
            f'th:contains("{role_name}")',  # Contains match (if supported)
            f'//th[contains(text(), "{role_name}")]',  # XPath contains
        ]
        
        for selector in role_header_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    # Check if it's visible (might need horizontal scroll)
                    header = locator.first
                    if header.is_visible(timeout=2000):
                        logger.info(f"✓ Role '{role_name}' found in privileges table (visible) with selector: {selector}")
                        role_found = True
                        break
                    else:
                        logger.info(f"Role '{role_name}' found but not visible (needs horizontal scroll)")
                        # Try scrolling horizontally to find it
                        self.scroll_horizontally_to_role_column(role_name)
                        if header.is_visible(timeout=2000):
                            logger.info(f"✓ Role '{role_name}' found after horizontal scroll")
                            role_found = True
                            break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
                continue
        
        # Strategy 2: If not found, try scrolling horizontally and searching again
        if not role_found:
            logger.info("Role not found in initial search, trying horizontal scroll...")
            try:
                self.scroll_horizontally_to_role_column(role_name)
                # Try finding again after scroll
                for selector in role_header_selectors:
                    locator = self.page.locator(selector)
                    if locator.count() > 0 and locator.first.is_visible(timeout=3000):
                        logger.info(f"✓ Role '{role_name}' found after horizontal scroll with selector: {selector}")
                        role_found = True
                        break
            except Exception as e:
                logger.warning(f"Horizontal scroll attempt failed: {e}")
        
        # Strategy 3: Check if role name appears anywhere in the privileges table (even if not visible)
        if not role_found:
            logger.info("Checking if role name appears anywhere in the privileges table...")
            try:
                privileges_table = self._find_privileges_table()
                table_text = privileges_table.text_content()
                if role_name in table_text:
                    logger.info(f"✓ Role '{role_name}' text found in privileges table content (may need scrolling)")
                    # Try scrolling to find it
                    try:
                        self.scroll_horizontally_to_role_column(role_name)
                        # Verify it's now visible
                        role_header_selector = f'th:has-text("{role_name}")'
                        if self.page.locator(role_header_selector).first.is_visible(timeout=3000):
                            role_found = True
                            logger.info(f"✓ Role '{role_name}' is now visible after scroll")
                    except Exception:
                        pass
            except Exception as e:
                logger.warning(f"Could not check privileges table text: {e}")
        
        if not role_found:
            self.screenshot(f"role-{role_name}-not-found-in-table")
            # Log table headers for debugging
            try:
                privileges_table = self._find_privileges_table()
                all_headers = privileges_table.locator('thead >> th').all()
                header_texts = [h.text_content().strip() for h in all_headers if h.text_content().strip()]
                logger.error(f"Available role headers in privileges table: {header_texts}")
            except Exception as e:
                logger.error(f"Could not get table headers: {e}")
            raise Exception(f"Role '{role_name}' not found in privileges table after {timeout}ms timeout")
        
        logger.info(f"✓ Role '{role_name}' verified in privileges table")
        self.screenshot(f"role-{role_name}-verified-in-table")
    
    def _find_privileges_table(self):
        """
        Find the correct privileges table by looking for specific indicators.
        Returns the table locator that contains privilege rows and role columns.
        """
        logger.info("Finding the correct privileges table...")
        
        # Strategy 1: Find table that contains specific privilege names
        privilege_indicators = ["task.view_code", "task.list", "task.view_io", "task.execute"]
        for indicator in privilege_indicators:
            try:
                # Find table that contains this privilege text
                table = self.page.locator(f'table:has-text("{indicator}")').first
                if table.count() > 0 and table.is_visible():
                    # Verify it has role columns (check for "Admin" or "Editor" in headers)
                    table_text = table.text_content()
                    if "Admin" in table_text or "Editor" in table_text or "Privileges" in table_text:
                        logger.info(f"✓ Found privileges table using indicator: {indicator}")
                        return table
            except Exception:
                continue
        
        # Strategy 2: Find table that comes after "Create new custom role" section
        try:
            create_role_section = self.page.locator(self.CREATE_CUSTOM_ROLE_HEADING).first
            if create_role_section.count() > 0:
                # Find the next table after this section
                following_table = create_role_section.locator('xpath=following::table[1]').first
                if following_table.count() > 0:
                    table_text = following_table.text_content()
                    # Verify it's the privileges table (has privilege names)
                    if any(indicator in table_text for indicator in privilege_indicators):
                        logger.info("✓ Found privileges table after 'Create new custom role' section")
                        return following_table
        except Exception as e:
            logger.debug(f"Strategy 2 failed: {e}")
        
        # Strategy 3: Find table with "Privileges" heading nearby
        try:
            privileges_heading = self.page.locator(self.PRIVILEGES_TABLE_HEADING).first
            if privileges_heading.count() > 0:
                # Find table near the heading
                table = privileges_heading.locator('xpath=following::table[1]').first
                if table.count() > 0:
                    logger.info("✓ Found privileges table near 'Privileges' heading")
                    return table
        except Exception as e:
            logger.debug(f"Strategy 3 failed: {e}")
        
        # Fallback: Return first table (but log warning)
        logger.warning("Could not find privileges table using specific indicators, using first table as fallback")
        return self.page.locator('table').first
    
    def scroll_to_privileges_table(self) -> None:
        """Scroll to the privileges table section."""
        logger.info("Scrolling to privileges table")
        self.screenshot("before-scroll-to-privileges")
        
        try:
            # Find the correct privileges table
            privileges_table = self._find_privileges_table()
            privileges_table.scroll_into_view_if_needed()
            self.page.wait_for_timeout(1000)
            logger.info("✓ Scrolled to privileges table")
            self.screenshot("after-scroll-to-privileges")
        except Exception as e:
            logger.error(f"Could not scroll to privileges table: {e}")
            # Fallback: scroll down more
            self.page.evaluate("window.scrollBy(0, 1200)")
            self.page.wait_for_timeout(1000)
    
    def scroll_horizontally_to_role_column(self, role_name: str) -> None:
        """
        Scroll horizontally in the privileges table to find the role column.
        
        Args:
            role_name: Name of the role column to scroll to
        """
        logger.info(f"Scrolling horizontally to find role column: {role_name}")
        self.screenshot(f"before-horizontal-scroll-{role_name}")
        
        # Find the correct privileges table
        table = self._find_privileges_table()
        if not table.is_visible():
            raise Exception("Privileges table not visible")
        
        # Get the table's scroll container (might be the table itself or a parent)
        table_box = table.bounding_box()
        if not table_box:
            raise Exception("Could not get table bounding box")
        
        # Try multiple selectors for the role header
        role_header_selectors = [
            f'th:has-text("{role_name}")',
            f'//th[contains(text(), "{role_name}")]',  # XPath
        ]
        
        role_header = None
        for selector in role_header_selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                role_header = locator.first
                logger.info(f"Found role header with selector: {selector}")
                break
        
        if not role_header:
            logger.warning(f"Role header '{role_name}' not found in DOM, will search while scrolling")
        
        # Check if role column is already visible
        if role_header and role_header.is_visible():
            logger.info(f"✓ Role column '{role_name}' is already visible")
            return
        
        # Find the scrollable container (table wrapper or table itself)
        # Try to find a parent div with overflow-x
        scrollable_container = None
        try:
            # Try to find scrollable container relative to the table
            container_selectors = [
                'xpath=ancestor::div[contains(@style, "overflow")]',
                'xpath=ancestor::div[@class*="scroll"]',
                'xpath=ancestor::div[@id*="table"]',
            ]
            
            for selector in container_selectors:
                try:
                    container_locator = table.locator(selector)
                    if container_locator.count() > 0:
                        scrollable_container = container_locator.first
                        logger.info(f"Found scrollable container with: {selector}")
                        break
                except Exception:
                    continue
        except Exception:
            pass
        
        # If no specific container found, use the table itself
        if not scrollable_container:
            scrollable_container = table
        
        # Scroll horizontally to find the role column
        max_scroll_attempts = 20  # Increased attempts
        scroll_amount = 300  # Increased scroll amount
        
        for attempt in range(max_scroll_attempts):
            # Try scrolling the container
            try:
                scrollable_container.evaluate(f"element => {{ element.scrollLeft += {scroll_amount}; }}")
            except Exception:
                # Fallback: try scrolling the table directly
                try:
                    table.evaluate(f"element => {{ element.scrollLeft += {scroll_amount}; }}")
                except Exception:
                    # Final fallback: scroll window
                    self.page.evaluate(f"window.scrollBy({scroll_amount}, 0)")
            
            self.page.wait_for_timeout(300)  # Wait for scroll to complete
            
            # Check if role column is now visible
            for selector in role_header_selectors:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    header = locator.first
                    try:
                        if header.is_visible(timeout=1000):
                            header_box = header.bounding_box()
                            if header_box:
                                logger.info(f"✓ Role column '{role_name}' is now visible (attempt {attempt + 1})")
                                self.screenshot(f"after-horizontal-scroll-{role_name}")
                                return
                    except Exception:
                        continue
        
        # If still not found, try scrolling in reverse direction
        logger.warning("Could not find role column scrolling right, trying left...")
        for attempt in range(max_scroll_attempts):
            try:
                scrollable_container.evaluate(f"element => {{ element.scrollLeft -= {scroll_amount}; }}")
            except Exception:
                try:
                    table.evaluate(f"element => {{ element.scrollLeft -= {scroll_amount}; }}")
                except Exception:
                    self.page.evaluate(f"window.scrollBy(-{scroll_amount}, 0)")
            
            self.page.wait_for_timeout(300)
            
            for selector in role_header_selectors:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    header = locator.first
                    try:
                        if header.is_visible(timeout=1000):
                            logger.info(f"✓ Role column '{role_name}' found scrolling left (attempt {attempt + 1})")
                            self.screenshot(f"after-horizontal-scroll-{role_name}")
                            return
                    except Exception:
                        continue
        
        self.screenshot(f"role-column-{role_name}-not-found-after-scroll")
        # Don't raise exception here - let the caller handle it
        logger.warning(f"Could not find role column '{role_name}' after extensive horizontal scrolling")
    
    def assign_privilege_to_role(self, privilege_name: str, role_name: str) -> None:
        """
        Assign a privilege to a role by checking the checkbox.
        
        Args:
            privilege_name: Name of the privilege (e.g., "task.view_code")
            role_name: Name of the role (e.g., "read1")
        """
        logger.info(f"Assigning privilege '{privilege_name}' to role '{role_name}'")
        self.screenshot(f"before-assign-{privilege_name}-to-{role_name}")
        
        # First, ensure the role column is visible
        self.scroll_horizontally_to_role_column(role_name)
        
        # Find the privilege row
        privilege_row_selector = self.PRIVILEGE_ROW.format(privilege_name=privilege_name)
        privilege_row = self.page.locator(privilege_row_selector)
        
        if privilege_row.count() == 0:
            self.screenshot(f"privilege-row-{privilege_name}-not-found")
            raise Exception(f"Could not find privilege row for '{privilege_name}'")
        
        privilege_row.first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        
        # Find the role column header to get its index
        role_header_selector = self.ROLE_COLUMN_HEADER.format(role_name=role_name)
        role_header = self.page.locator(role_header_selector)
        
        if role_header.count() == 0:
            raise Exception(f"Could not find role column header for '{role_name}'")
        
        # Get all table headers to find the column index (use correct privileges table)
        privileges_table = self._find_privileges_table()
        all_headers = privileges_table.locator('thead >> th').all()
        role_column_index = None
        
        for idx, header in enumerate(all_headers):
            header_text = header.text_content()
            if role_name in header_text:
                role_column_index = idx
                logger.info(f"Found role '{role_name}' at column index {idx}")
                break
        
        if role_column_index is None:
            raise Exception(f"Could not determine column index for role '{role_name}'")
        
        # Find the checkbox in the privilege row for this role column
        # The checkbox should be in the td at the same column index
        privilege_row_tds = privilege_row.first.locator('td').all()
        
        if len(privilege_row_tds) <= role_column_index:
            raise Exception(f"Privilege row does not have enough columns (expected at least {role_column_index + 1})")
        
        # Get the td for this role column
        role_column_td = privilege_row_tds[role_column_index]
        
        # Find the checkbox in this td
        checkbox = role_column_td.locator('input[type="checkbox"]')
        
        if checkbox.count() == 0:
            self.screenshot(f"checkbox-not-found-{privilege_name}-{role_name}")
            raise Exception(f"Could not find checkbox for privilege '{privilege_name}' in role '{role_name}' column")
        
        checkbox = checkbox.first
        
        # Check if already checked
        if checkbox.is_checked():
            logger.info(f"✓ Privilege '{privilege_name}' is already assigned to role '{role_name}'")
            return
        
        # Scroll checkbox into view and check it
        checkbox.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        checkbox.check()
        self.page.wait_for_timeout(1000)  # Give time for the change to register
        
        logger.info(f"✓ Assigned privilege '{privilege_name}' to role '{role_name}'")
        self.screenshot(f"after-assign-{privilege_name}-to-{role_name}")
    
    def assign_multiple_privileges_to_role(self, privilege_names: list, role_name: str) -> None:
        """
        Assign multiple privileges to a role.
        
        Args:
            privilege_names: List of privilege names (e.g., ["task.view_code", "task.view_io"])
            role_name: Name of the role
        """
        logger.info(f"Assigning {len(privilege_names)} privileges to role '{role_name}'")
        
        for privilege_name in privilege_names:
            try:
                self.assign_privilege_to_role(privilege_name, role_name)
            except Exception as e:
                logger.error(f"Failed to assign '{privilege_name}' to '{role_name}': {e}")
                raise
        
        logger.info(f"✓ All {len(privilege_names)} privileges assigned to role '{role_name}'")

    # ==================== User Management Methods ====================
    
    # User management selectors
    USERS_TABLE = 'table, [role="table"]'  # Users table
    USER_ROW = 'tr:has-text("{user_email}")'  # Row for a specific user
    USER_DROPDOWN_ARROW = 'tr:has-text("{user_email}") >> button[aria-label*="expand"], tr:has-text("{user_email}") >> [aria-label*="Expand"], tr:has-text("{user_email}") >> button:has([class*="chevron"])'
    MODIFY_SETTINGS_BUTTON = 'button:has-text("Modify settings"), button:has-text("Modify Settings")'
    
    # Modify User Settings form selectors
    MODIFY_USER_SETTINGS_HEADING = 'text=Modify User Settings'
    WORKSPACE_ROLES_TABLE = 'text=Workspace Roles >> .. >> table, text=Workspace Roles >> xpath=following::table[1]'
    WORKSPACE_ROW = 'tr:has-text("{workspace_name}")'  # Row for a workspace in the roles table
    WORKSPACE_ROLE_DROPDOWN = 'tr:has-text("{workspace_name}") >> select, tr:has-text("{workspace_name}") >> [role="combobox"]'
    WORKSPACE_ROLE_OPTION = 'option:has-text("{role_name}"), [role="option"]:has-text("{role_name}")'
    SAVE_CHANGES_BUTTON = 'button:has-text("Save Changes"), button:has-text("Save")'
    SAVE_USER_SETTINGS_BUTTON = 'button:has-text("Save Changes"), button:has-text("Save"), button[type="submit"]:has-text("Save")'
    CANCEL_USER_SETTINGS_BUTTON = 'button:has-text("Cancel")'
    SUCCESS_MESSAGE = 'text=Changes Saved Successfully, text=Changes saved successfully'
    
    def navigate_to_users_tab(self) -> None:
        """
        Navigate to Users tab on settings page.
        """
        logger.info("Navigating to Users tab")
        self.navigate_to_settings_page()
        self.click_users_tab()
        logger.info("✓ Users tab loaded")
    
    def click_users_tab(self) -> None:
        """
        Click the "Users" tab on the settings page.
        """
        logger.info("Clicking Users tab on settings page")
        self.screenshot("before-users-tab-click")
        
        # Try multiple selectors for the Users tab
        users_tab_selectors = [
            self.USERS_TAB,
            'button:has-text("Users")',
            '[role="tab"]:has-text("Users")',
            'div[role="tablist"] >> text=Users',
            '//button[contains(text(), "Users")]',
        ]
        
        clicked = False
        for selector in users_tab_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    element = locator.first
                    element.scroll_into_view_if_needed()
                    element.wait_for(state="visible", timeout=5000)
                    element.click()
                    clicked = True
                    logger.info(f"✓ Clicked Users tab with selector: {selector}")
                    break
            except Exception as e:
                logger.debug(f"Could not click Users tab with {selector}: {e}")
        
        if not clicked:
            self.screenshot("users-tab-not-found")
            raise Exception("Could not find or click Users tab")
        
        # Wait for tab content to load
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(2000)  # Give time for content to load
        self.screenshot("after-users-tab-click")
        logger.info("✓ Users tab clicked and content loaded")
    
    def find_user_in_table(self, user_email: str) -> None:
        """
        Find a user in the users table and scroll to them.
        
        Args:
            user_email: Email of the user to find
        """
        logger.info(f"Finding user '{user_email}' in users table")
        self.screenshot(f"before-find-user-{user_email}")
        
        # Find the user row
        user_row_selector = self.USER_ROW.format(user_email=user_email)
        user_row = self.page.locator(user_row_selector)
        
        if user_row.count() == 0:
            self.screenshot(f"user-{user_email}-not-found")
            raise Exception(f"Could not find user '{user_email}' in users table")
        
        # Scroll to the user row
        user_row.first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(1000)
        logger.info(f"✓ Found user '{user_email}' in table")
        self.screenshot(f"user-{user_email}-found")
    
    def expand_user_row(self, user_email: str) -> None:
        """
        Click the dropdown arrow next to a user to expand their row and show "Modify Settings" button.
        The dropdown arrow is in the 4th column (rightmost) of the All Users table.
        
        Args:
            user_email: Email of the user
        """
        logger.info(f"Expanding user row for '{user_email}'")
        self.screenshot(f"before-expand-user-{user_email}")
        
        # Find the user row first
        self.find_user_in_table(user_email)
        
        # Find the user row
        user_row_selector = self.USER_ROW.format(user_email=user_email)
        user_row = self.page.locator(user_row_selector).first
        
        if user_row.count() == 0:
            raise Exception(f"Could not find user row for '{user_email}'")
        
        # The dropdown arrow is in the 4th column (rightmost column) of the table
        # Strategy 1: Find button/icon in the last column (4th column) of the row
        logger.info("Looking for dropdown arrow in 4th column (rightmost) of user row")
        
        # Get all cells in the user row
        row_cells = user_row.locator('td').all()
        logger.info(f"Found {len(row_cells)} columns in user row")
        
        dropdown_clicked = False
        
        # Try clicking the last cell (4th column) or button in the last cell
        if len(row_cells) >= 4:
            last_cell = row_cells[3]  # 4th column (0-indexed: 0, 1, 2, 3)
            logger.info("Trying to click button/icon in 4th column")
            
            # Look for button or clickable element in the last cell
            cell_button_selectors = [
                'button',
                '[role="button"]',
                'button[aria-label*="expand"]',
                'button[aria-label*="Expand"]',
                'button:has([class*="chevron"])',
                'button:has([class*="arrow"])',
                'button:has(svg)',
                '[class*="chevron"]',
                '[class*="arrow"]',
            ]
            
            for selector in cell_button_selectors:
                try:
                    button = last_cell.locator(selector).first
                    if button.count() > 0 and button.is_visible(timeout=2000):
                        button.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(300)
                        button.click()
                        dropdown_clicked = True
                        logger.info(f"✓ Clicked dropdown arrow in 4th column with selector: {selector}")
                        break
                except Exception as e:
                    logger.debug(f"Selector '{selector}' in 4th column failed: {e}")
                    continue
            
            # If no button found, try clicking the cell itself
            if not dropdown_clicked:
                try:
                    last_cell.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(300)
                    last_cell.click()
                    dropdown_clicked = True
                    logger.info("✓ Clicked 4th column cell directly")
                except Exception as e:
                    logger.debug(f"Could not click 4th column cell: {e}")
        
        # Strategy 2: Find dropdown arrow using various selectors (fallback)
        if not dropdown_clicked:
            logger.info("Trying fallback selectors for dropdown arrow")
            dropdown_selectors = [
                f'{user_row_selector} >> td:last-child >> button',
                f'{user_row_selector} >> td:nth-child(4) >> button',
                f'{user_row_selector} >> button:has([class*="chevron"])',
                f'{user_row_selector} >> button[aria-label*="expand"]',
                f'{user_row_selector} >> button[aria-label*="Expand"]',
                f'{user_row_selector} >> [aria-label*="expand"]',
                f'//tr[contains(., "{user_email}")]//td[last()]//button',
                f'//tr[contains(., "{user_email}")]//button[contains(@aria-label, "expand") or contains(@class, "chevron")]',
            ]
            
            for selector in dropdown_selectors:
                try:
                    locator = self.page.locator(selector)
                    if locator.count() > 0:
                        element = locator.first
                        if element.is_visible(timeout=2000):
                            element.scroll_into_view_if_needed()
                            self.page.wait_for_timeout(300)
                            element.click()
                            dropdown_clicked = True
                            logger.info(f"✓ Clicked dropdown arrow with selector: {selector}")
                            break
                except Exception as e:
                    logger.debug(f"Dropdown selector '{selector}' failed: {e}")
                    continue
        
        if not dropdown_clicked:
            self.screenshot(f"user-dropdown-{user_email}-not-found")
            # Log row structure for debugging
            try:
                row_text = user_row.text_content()
                logger.error(f"User row content: {row_text}")
                logger.error(f"Number of columns: {len(row_cells)}")
            except Exception:
                pass
            raise Exception(f"Could not find or click dropdown arrow for user '{user_email}'")
        
        # Wait for the row to expand and "Modify Settings" button to appear
        self.page.wait_for_timeout(1000)
        self.screenshot(f"after-expand-user-{user_email}")
        logger.info(f"✓ User row expanded for '{user_email}'")
    
    def click_modify_settings_for_user(self, user_email: str) -> None:
        """
        Click "Modify Settings" button for a user.
        This should be called after expanding the user row.
        
        Args:
            user_email: Email of the user
        """
        logger.info(f"Clicking 'Modify Settings' for user '{user_email}'")
        self.screenshot(f"before-modify-settings-{user_email}")
        
        # Find the Modify Settings button
        modify_button_selectors = [
            self.MODIFY_SETTINGS_BUTTON,
            'button:has-text("Modify settings")',
            'button:has-text("Modify Settings")',
            f'//tr[contains(., "{user_email}")]//button[contains(text(), "Modify")]',
        ]
        
        modify_clicked = False
        for selector in modify_button_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    element = locator.first
                    if element.is_visible(timeout=2000):
                        element.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(300)
                        element.click()
                        modify_clicked = True
                        logger.info(f"✓ Clicked Modify Settings with selector: {selector}")
                        break
            except Exception as e:
                logger.debug(f"Modify Settings selector '{selector}' failed: {e}")
                continue
        
        if not modify_clicked:
            self.screenshot(f"modify-settings-button-{user_email}-not-found")
            raise Exception(f"Could not find or click 'Modify Settings' button for user '{user_email}'")
        
        # Wait for the Modify User Settings form to load
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(2000)
        
        # Verify we're on the Modify User Settings page
        try:
            self.page.locator(self.MODIFY_USER_SETTINGS_HEADING).wait_for(state="visible", timeout=10000)
            logger.info("✓ Modify User Settings form loaded")
        except Exception:
            logger.warning("Modify User Settings heading not found, but continuing...")
        
        self.screenshot(f"after-modify-settings-{user_email}")
        logger.info(f"✓ Modify Settings clicked for user '{user_email}'")
    
    def assign_role_to_user_for_workspace(self, workspace_name: str, role_name: str, user_email: str = None) -> None:
        """
        Assign a role to a user for a specific workspace in the Modify User Settings form.
        
        Args:
            workspace_name: Name of the workspace (e.g., "DEV")
            role_name: Name of the role to assign (e.g., "read1")
            user_email: Email of the user (optional, for logging)
        """
        logger.info(f"Assigning role '{role_name}' to workspace '{workspace_name}'")
        if user_email:
            logger.info(f"User: {user_email}")
        self.screenshot(f"before-assign-role-{workspace_name}-{role_name}")
        
        # Find the workspace row in the Workspace Roles table
        workspace_row_selector = self.WORKSPACE_ROW.format(workspace_name=workspace_name)
        workspace_row = self.page.locator(workspace_row_selector)
        
        if workspace_row.count() == 0:
            self.screenshot(f"workspace-row-{workspace_name}-not-found")
            raise Exception(f"Could not find workspace '{workspace_name}' in Workspace Roles table")
        
        # Scroll to the workspace row
        workspace_row.first.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        logger.info(f"✓ Found workspace '{workspace_name}' row")
        
        # Find the role dropdown for this workspace
        dropdown_selectors = [
            f'{workspace_row_selector} >> select',
            f'{workspace_row_selector} >> [role="combobox"]',
            f'{workspace_row_selector} >> input[type="text"]',
            f'{workspace_row_selector} >> button',
        ]
        
        role_dropdown = None
        for selector in dropdown_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    element = locator.first
                    if element.is_visible(timeout=2000):
                        role_dropdown = element
                        logger.info(f"Found role dropdown with selector: {selector}")
                        break
            except Exception as e:
                logger.debug(f"Dropdown selector '{selector}' failed: {e}")
                continue
        
        if not role_dropdown:
            self.screenshot(f"role-dropdown-{workspace_name}-not-found")
            raise Exception(f"Could not find role dropdown for workspace '{workspace_name}'")
        
        # Click the dropdown to open it
        role_dropdown.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300)
        role_dropdown.click()
        self.page.wait_for_timeout(500)  # Wait for dropdown menu to appear
        logger.info("✓ Clicked role dropdown")
        self.screenshot(f"role-dropdown-opened-{workspace_name}")
        
        # Select the role from the dropdown
        role_option_selectors = [
            f'option:has-text("{role_name}")',
            f'[role="option"]:has-text("{role_name}")',
            f'//option[contains(text(), "{role_name}")]',
            f'//div[@role="option" and contains(text(), "{role_name}")]',
            f'text={role_name}',
        ]
        
        role_selected = False
        for selector in role_option_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    element = locator.first
                    if element.is_visible(timeout=2000):
                        element.click()
                        role_selected = True
                        logger.info(f"✓ Selected role '{role_name}' with selector: {selector}")
                        break
            except Exception as e:
                logger.debug(f"Role option selector '{selector}' failed: {e}")
                continue
        
        if not role_selected:
            # Fallback: try typing the role name if it's an input
            try:
                if role_dropdown.get_attribute('tagName') == 'INPUT' or role_dropdown.get_attribute('type') == 'text':
                    role_dropdown.fill(role_name)
                    self.page.wait_for_timeout(500)
                    # Press Enter to confirm
                    role_dropdown.press("Enter")
                    role_selected = True
                    logger.info(f"✓ Typed and selected role '{role_name}'")
            except Exception:
                pass
        
        if not role_selected:
            self.screenshot(f"role-option-{role_name}-not-found")
            raise Exception(f"Could not select role '{role_name}' from dropdown")
        
        # Wait for selection to register
        self.page.wait_for_timeout(1000)
        self.screenshot(f"after-assign-role-{workspace_name}-{role_name}")
        logger.info(f"✓ Assigned role '{role_name}' to workspace '{workspace_name}'")
    
    def save_user_settings(self) -> None:
        """
        Scroll down to find and click the "Save Changes" button in the Modify User Settings form.
        Then wait for the success message and page to load.
        """
        logger.info("Saving user settings")
        self.screenshot("before-save-user-settings")
        
        # Scroll down to find the Save Changes button (it's at the bottom of the form)
        logger.info("Scrolling down to find Save Changes button")
        for _ in range(5):  # Scroll multiple times to ensure we reach the bottom
            self.page.evaluate("window.scrollBy(0, 500)")
            self.page.wait_for_timeout(300)
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to very bottom
        self.page.wait_for_timeout(1000)
        self.screenshot("after-scroll-to-bottom")
        logger.info("✓ Scrolled to bottom of form")
        
        # Find and click the Save Changes button
        save_button_selectors = [
            self.SAVE_CHANGES_BUTTON,
            'button:has-text("Save Changes")',
            'button:has-text("Save")',
            'button[type="submit"]:has-text("Save")',
            'button.btn-primary:has-text("Save Changes")',
            'button:has([class*="check"]):has-text("Save")',  # Button with checkmark icon
        ]
        
        save_clicked = False
        for selector in save_button_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    # Try all matching elements to find the one at the bottom
                    for idx in range(locator.count()):
                        element = locator.nth(idx)
                        if element.is_visible(timeout=2000):
                            # Check if it's near the bottom of the page
                            element_box = element.bounding_box()
                            if element_box:
                                # Button should be in the lower part of the page
                                page_height = self.page.evaluate("document.body.scrollHeight")
                                if element_box['y'] > page_height * 0.6:  # Lower 40% of page
                                    element.scroll_into_view_if_needed()
                                    self.page.wait_for_timeout(300)
                                    element.click()
                                    save_clicked = True
                                    logger.info(f"✓ Clicked Save Changes button with selector: {selector} (element {idx})")
                                    break
            except Exception as e:
                logger.debug(f"Save button selector '{selector}' failed: {e}")
                continue
            
            if save_clicked:
                break
        
        if not save_clicked:
            self.screenshot("save-changes-button-not-found")
            raise Exception("Could not find or click Save Changes button")
        
        # Wait for success message to appear
        logger.info("Waiting for success message...")
        try:
            self.page.locator(self.SUCCESS_MESSAGE).wait_for(state="visible", timeout=10000)
            logger.info("✓ Success message appeared: 'Changes Saved Successfully'")
            self.screenshot("success-message-visible")
        except Exception as e:
            logger.warning(f"Success message not found: {e}")
            # Continue anyway, the save might have worked
        
        # Wait for success message to disappear (modal might auto-close)
        try:
            self.page.locator(self.SUCCESS_MESSAGE).wait_for(state="hidden", timeout=10000)
            logger.info("✓ Success message disappeared")
        except Exception:
            logger.info("Success message did not disappear (may stay visible)")
        
        # Wait for page to load after save
        logger.info("Waiting for page to load after save...")
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(2000)  # Additional wait for UI to stabilize
        self.screenshot("after-save-user-settings")
        logger.info("✓ User settings saved and page loaded")


