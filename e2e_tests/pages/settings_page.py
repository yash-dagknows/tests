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
    
    def navigate_to_rbac_tab(self) -> None:
        """
        Navigate directly to RBAC tab via URL.
        The RBAC content is shown when tab=rbac is in the URL.
        """
        logger.info("Navigating to RBAC tab")
        rbac_url = f"{self.settings_url}?tab=rbac"
        self.goto(rbac_url)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.page.wait_for_timeout(2000)  # Give time for content to load
        self.screenshot("rbac-tab-loaded")
        logger.info("✓ RBAC tab loaded")
        
        # Verify we're on RBAC tab
        current_url = self.page.url
        if "tab=rbac" not in current_url:
            logger.warning(f"URL does not contain 'tab=rbac'. Current URL: {current_url}")
    
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
        
        Args:
            role_name: Name of the role to create (e.g., "read1")
        """
        logger.info(f"Creating custom role: {role_name}")
        self.screenshot(f"before-create-role-{role_name}")
        
        # Scroll to the section first
        self.scroll_to_create_custom_role_section()
        
        # Find and fill the role name input
        role_input = None
        input_selectors = [
            self.ROLE_NAME_INPUT,
            'input[placeholder*="Role name"]',
            'label:has-text("Role name") + input',
            'text=Create new custom role >> .. >> input'
        ]
        
        for selector in input_selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0 and locator.first.is_visible():
                role_input = locator.first
                logger.info(f"Found role name input with: {selector}")
                break
        
        if not role_input:
            self.screenshot("role-name-input-not-found")
            raise Exception("Could not find role name input field")
        
        role_input.fill(role_name)
        logger.info(f"✓ Filled role name: {role_name}")
        self.page.wait_for_timeout(1000)
        self.screenshot(f"after-filling-role-name-{role_name}")
        
        # Find and click the Add button (next to the input field in "Create new custom role" section)
        # The Add button should be horizontally next to the role name input field
        add_button = None
        
        # Strategy 1: Find Add button within the "Create new custom role" section
        # Look for the section container first
        create_role_section = self.page.locator(self.CREATE_CUSTOM_ROLE_HEADING).first
        if create_role_section.count() > 0:
            # Find Add button within the same section (parent or following sibling)
            section_container = create_role_section.locator('xpath=ancestor::div[contains(@class, "section") or contains(@class, "card") or contains(@class, "box")] | ancestor::div[1]')
            
            # Try to find Add button near the role name input
            add_button_selectors = [
                # Direct sibling of input
                f'{self.ROLE_NAME_INPUT} + button:has-text("Add")',
                f'{self.ROLE_NAME_INPUT} ~ button:has-text("Add")',
                # Within the same container as the input
                f'text=Create new custom role >> .. >> button:has-text("Add")',
                # XPath: button with "Add" text that's near the role name input
                f'//div[contains(., "Create new custom role")]//input[@placeholder="Role name"]/following-sibling::button[contains(text(), "Add")]',
                f'//div[contains(., "Create new custom role")]//button[contains(text(), "Add")]',
            ]
            
            for selector in add_button_selectors:
                try:
                    locator = self.page.locator(selector)
                    if locator.count() > 0:
                        btn = locator.first
                        if btn.is_visible():
                            # Verify it's near the role name input (same row)
                            btn_box = btn.bounding_box()
                            input_box = role_input.bounding_box()
                            if btn_box and input_box:
                                # Check if they're on the same row (y-coordinate similar) and button is to the right
                                if abs(btn_box['y'] - input_box['y']) < 30 and btn_box['x'] > input_box['x']:
                                    add_button = btn
                                    logger.info(f"Found Add button for role with: {selector}")
                                    break
                except Exception as e:
                    logger.debug(f"Selector '{selector}' failed: {e}")
                    continue
        
        # Strategy 2: Find Add button by position relative to role name input
        if not add_button:
            logger.info("Trying to find Add button by position...")
            input_box = role_input.bounding_box()
            if input_box:
                # Find all Add buttons and check which one is next to the input
                all_add_buttons = self.page.locator('button:has-text("Add")').all()
                for btn in all_add_buttons:
                    if btn.is_visible():
                        btn_box = btn.bounding_box()
                        if btn_box:
                            # Check if button is on the same row (y similar) and to the right of input
                            y_diff = abs(btn_box['y'] - input_box['y'])
                            x_diff = btn_box['x'] - input_box['x']
                            if y_diff < 30 and 50 < x_diff < 300:  # Button is 50-300px to the right
                                add_button = btn
                                logger.info(f"Found Add button by position (y_diff={y_diff:.0f}, x_diff={x_diff:.0f})")
                                break
        
        if add_button:
            # Verify input field has the role name before clicking
            current_input_value = role_input.input_value()
            if current_input_value != role_name:
                logger.warning(f"Input value mismatch. Expected: '{role_name}', Got: '{current_input_value}'")
                role_input.fill(role_name)  # Re-fill if needed
                self.page.wait_for_timeout(500)
            
            # Click the Add button
            add_button.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)  # Small wait before click
            add_button.click()
            logger.info("✓ Clicked Add button for role")
            
            # Wait for the input field to clear (indicates successful creation)
            # Check if input value becomes empty after a short wait
            self.page.wait_for_timeout(1000)  # Wait for UI to update
            try:
                current_value = role_input.input_value()
                if current_value == "":
                    logger.info("✓ Input field cleared, indicating role creation was submitted")
                else:
                    logger.info(f"Input field still has value: '{current_value}' (may have been cleared and refilled)")
            except Exception:
                logger.warning("Could not check input field value, but continuing...")
            
            self.page.wait_for_load_state("networkidle", timeout=10000)
            
            # Wait for role to appear in privileges table (user reported ~1 second, using 5 seconds for safety)
            # Also try to detect when the role appears in the table
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
        else:
            self.screenshot("add-role-button-not-found")
            raise Exception("Could not find or click Add button for role")
    
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


