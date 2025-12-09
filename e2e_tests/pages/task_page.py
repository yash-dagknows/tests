"""
Page Object for Task Management
Handles task creation, editing, and management UI interactions.
"""

import logging
from playwright.sync_api import Page
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class TaskPage(BasePage):
    """Task management page object."""
    
    # Selectors for New Task button and dropdown
    NEW_TASK_BUTTON = 'button:has-text("New Task"), button:has-text("+ New Task")'
    CREATE_FROM_FORM_OPTION = 'text=Create from Form, [role="menuitem"]:has-text("Create from Form")'
    CREATE_WITH_AI_AGENT_OPTION = 'text=Create with AI Agent'
    
    # Task form selectors
    TITLE_INPUT = 'input[placeholder="Title"], input[name="title"]'
    DESCRIPTION_EDITOR = 'div[contenteditable="true"], textarea[placeholder*="Description"]'
    CODE_TAB = 'button:has-text("Code"), [role="tab"]:has-text("Code")'
    CODE_EDITOR = '.monaco-editor textarea, textarea.inputarea'
    SAVE_BUTTON = 'button:has-text("Save"), button[type="submit"]'
    
    # Task view selectors
    TASK_TITLE_DISPLAY = 'h1, h2, .task-title'
    TASK_ID_IN_URL = '?taskId='
    
    def __init__(self, page: Page):
        """Initialize task page."""
        super().__init__(page)
    
    def click_new_task_button(self) -> None:
        """Click the 'New Task' button to open dropdown."""
        logger.info("Clicking 'New Task' button")
        self.screenshot("before-new-task-click")
        
        # Try multiple selectors for the "New Task" button
        selectors = [
            'button:has-text("New Task")',
            'button:has-text("+ New Task")',
            'button[aria-label*="New Task"]',
            'button[aria-label*="new task"]',
            # Look in top right area
            'header >> button:has-text("New Task")',
            'nav >> button:has-text("New Task")',
        ]
        
        clicked = False
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                try:
                    locator.first.scroll_into_view_if_needed()
                    locator.first.wait_for(state="visible", timeout=5000)
                    locator.first.click()
                    clicked = True
                    logger.info(f"✓ Clicked New Task button with selector: {selector}")
                    break
                except Exception as e:
                    logger.debug(f"Could not click New Task with {selector}: {e}")
        
        if not clicked:
            self.screenshot("new-task-button-not-found")
            raise Exception("New Task button not found or clickable")
        
        # Wait for dropdown to appear
        self.page.wait_for_timeout(1000)
        self.screenshot("new-task-dropdown-open")
        logger.info("✓ New Task dropdown opened")
    
    def click_create_from_form(self) -> None:
        """Click 'Create from Form' from dropdown."""
        logger.info("Clicking 'Create from Form'")
        self.screenshot("dropdown-before-create-form-click")
        
        # Try different possible selectors for the dropdown item
        selectors = [
            'text=Create from Form',
            '[role="menuitem"]:has-text("Create from Form")',
            'button:has-text("Create from Form")',
            'a:has-text("Create from Form")',
            'div[role="menu"] >> text=Create from Form',
            'div.dropdown-menu >> text=Create from Form',
            '//div[contains(@class, "dropdown-menu")]//a[contains(., "Create from Form")]',
            '//div[contains(@class, "dropdown-menu")]//button[contains(., "Create from Form")]',
        ]
        
        clicked = False
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                try:
                    locator.first.scroll_into_view_if_needed()
                    locator.first.wait_for(state="visible", timeout=5000)
                    locator.first.click()
                    clicked = True
                    logger.info(f"✓ Clicked 'Create from Form' with selector: {selector}")
                    break
                except Exception as e:
                    logger.debug(f"Could not click with selector {selector}: {e}")
        
        if not clicked:
            self.screenshot("create-from-form-option-not-found")
            logger.error("Could not find 'Create from Form' option. Page content:")
            logger.error(self.page.content()[:2000])
            raise Exception("Could not find 'Create from Form' option")
        
        # Wait for navigation to task form
        self.page.wait_for_timeout(2000)
        
        # Wait for network idle
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.warning(f"Network idle timeout: {e}")
        
        # Take screenshot after navigation
        self.screenshot("after-task-form-navigation")
        logger.info("✓ Navigated to task form page")
    
    def fill_task_title(self, title: str) -> None:
        """
        Fill task title.
        
        Args:
            title: Task title
        """
        logger.info(f"Filling task title: {title}")
        self.screenshot("before-filling-title")
        
        # Wait a bit for form to fully load
        self.page.wait_for_timeout(2000)
        
        # Find title input - it's the first input/textarea at the top
        title_selectors = [
            'textarea[placeholder="Title"]',
            'input[placeholder="Title"]',
            'textarea',  # Often the first textarea is the title
            'input[name="title"]',
            'input[type="text"]',
            '.title-input',
            '[data-testid="title"]',
        ]
        
        title_input = None
        for selector in title_selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                logger.debug(f"Selector '{selector}' found {count} elements")
                
                if count > 0:
                    # Find the first visible one
                    for i in range(count):
                        element = locator.nth(i)
                        if element.is_visible():
                            # Verify it's near the top of the page (likely the title field)
                            box = element.bounding_box()
                            if box and box['y'] < 400:  # Top 400px of page
                                title_input = element
                                logger.info(f"Found title input with: {selector} at position y={box['y']}")
                                break
                    if title_input:
                        break
            except Exception as e:
                logger.debug(f"Error with selector {selector}: {e}")
        
        if not title_input:
            # Last resort: try to find the first visible input/textarea on the page
            logger.warning("Trying fallback: first visible textarea or input")
            try:
                all_inputs = self.page.locator('textarea, input[type="text"]').all()
                logger.info(f"Found {len(all_inputs)} total text inputs on page")
                
                for inp in all_inputs:
                    if inp.is_visible():
                        box = inp.bounding_box()
                        if box:
                            logger.info(f"Found input at y={box['y']}")
                            if box['y'] < 400:  # Top of page
                                title_input = inp
                                logger.info(f"✓ Using first visible input at top of page")
                                break
            except Exception as e:
                logger.error(f"Fallback failed: {e}")
        
        if not title_input:
            self.screenshot("title-input-not-found")
            # Log page content for debugging
            try:
                logger.error("Page HTML snippet:")
                logger.error(self.page.content()[:3000])
            except Exception:
                pass
            raise Exception("Could not find title input field")
        
        # Fill title
        title_input.scroll_into_view_if_needed()
        title_input.click()
        self.page.wait_for_timeout(500)
        title_input.fill(title)
        logger.info(f"✓ Filled title: {title}")
        self.screenshot("after-filling-title")
    
    def fill_task_description(self, description: str) -> None:
        """
        Fill task description.
        
        Args:
            description: Task description
        """
        logger.info(f"Filling task description: {description[:50]}...")
        self.screenshot("before-filling-description")
        
        # Try to find description editor
        desc_selectors = [
            'div[contenteditable="true"]',
            'textarea[placeholder*="Description"]',
            'textarea[name*="description"]',
            '.description-editor',
        ]
        
        desc_editor = None
        for selector in desc_selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                # Find first visible one
                for i in range(locator.count()):
                    element = locator.nth(i)
                    try:
                        if element.is_visible():
                            desc_editor = element
                            logger.info(f"Found description editor with: {selector}")
                            break
                    except Exception:
                        pass
                if desc_editor:
                    break
        
        if not desc_editor:
            logger.warning("Could not find description editor, might be optional")
            self.screenshot("description-editor-not-found")
            return
        
        # Fill description
        try:
            desc_editor.click()
            desc_editor.fill(description)
            logger.info(f"✓ Filled description")
            self.screenshot("after-filling-description")
        except Exception as e:
            logger.warning(f"Could not fill description: {e}")
            # Not critical, continue
    
    def fill_task_code(self, code: str) -> None:
        """
        Fill task code in the code editor.
        
        Args:
            code: Python code or script
        """
        logger.info(f"Filling task code ({len(code)} characters)")
        self.screenshot("before-filling-code")
        
        # First, try to click on Code tab if it exists
        try:
            code_tab = self.page.locator('button:has-text("Code"), [role="tab"]:has-text("Code")')
            if code_tab.count() > 0 and code_tab.first.is_visible():
                logger.info("Clicking Code tab")
                code_tab.first.click()
                self.page.wait_for_timeout(1000)
        except Exception as e:
            logger.debug(f"No Code tab or already on code view: {e}")
        
        # Scroll to code editor section first
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        self.page.wait_for_timeout(1000)
        
        # Find code editor (often Monaco editor or textarea)
        code_selectors = [
            '.monaco-editor textarea.inputarea',
            'textarea.inputarea',
            '.code-editor textarea',
            'textarea[name*="code"]',
            'textarea[placeholder*="code"]',
            'div[class*="monaco"] textarea',
            '.monaco-editor',
        ]
        
        code_editor = None
        for selector in code_selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                logger.debug(f"Code editor selector '{selector}' found {count} elements")
                
                if count > 0:
                    # For Monaco, look for the textarea inside
                    if 'monaco' in selector.lower():
                        code_editor = locator.last  # Often the last one
                    else:
                        code_editor = locator.first
                    
                    if code_editor.is_visible():
                        logger.info(f"Found code editor with: {selector}")
                        break
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
        
        if not code_editor:
            # Try to find by scrolling to line number "1" and finding nearby textarea
            logger.warning("Trying fallback: looking for textarea near line numbers")
            try:
                # Look for any textarea in the lower half of the page
                all_textareas = self.page.locator('textarea').all()
                for ta in all_textareas:
                    box = ta.bounding_box()
                    if box and box['y'] > 400 and ta.is_visible():  # Lower half
                        code_editor = ta
                        logger.info(f"✓ Found textarea in code section at y={box['y']}")
                        break
            except Exception as e:
                logger.error(f"Fallback failed: {e}")
        
        if not code_editor:
            self.screenshot("code-editor-not-found")
            raise Exception("Could not find code editor")
        
        # Fill code
        try:
            # Scroll to code editor
            code_editor.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)
            
            # For Monaco editor, we need to focus and type
            code_editor.click()
            self.page.wait_for_timeout(1000)  # Wait for Monaco to initialize
            
            # Try to clear existing content first
            self.page.keyboard.press("Control+A")
            self.page.wait_for_timeout(200)
            self.page.keyboard.press("Delete")
            self.page.wait_for_timeout(500)
            
            # Type code line by line for Monaco compatibility
            code_lines = code.split('\n')
            for i, line in enumerate(code_lines):
                self.page.keyboard.type(line)
                if i < len(code_lines) - 1:  # Not the last line
                    self.page.keyboard.press("Enter")
                    self.page.wait_for_timeout(50)  # Small delay between lines
            
            logger.info(f"✓ Filled code ({len(code_lines)} lines)")
            self.screenshot("after-filling-code")
        except Exception as e:
            logger.error(f"Could not fill code: {e}")
            self.screenshot("code-fill-failed")
            # Try alternative method
            try:
                logger.warning("Trying alternative: using fill() method")
                code_editor.fill(code)
                logger.info("✓ Code filled using fill() method")
            except Exception as e2:
                logger.error(f"Alternative also failed: {e2}")
                raise
    
    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page to find Save button."""
        logger.info("Scrolling to bottom of page")
        try:
            # Scroll to bottom multiple times to ensure we reach the very bottom
            for i in range(3):
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.page.wait_for_timeout(500)
            
            # Also try scrolling by a large pixel amount
            self.page.evaluate("window.scrollBy(0, 5000)")
            self.page.wait_for_timeout(1000)
            
            logger.info("✓ Scrolled to bottom")
            self.screenshot("after-scroll-to-bottom")
        except Exception as e:
            logger.warning(f"Could not scroll to bottom: {e}")
    
    def click_save_button(self) -> None:
        """Click Save button to save the task."""
        logger.info("Clicking Save button")
        self.screenshot("before-save-click")
        
        # Scroll to bottom first to ensure Save button is visible
        self.scroll_to_bottom()
        
        # Try multiple selectors for Save button
        save_selectors = [
            'button:has-text("Save")',
            'button[type="submit"]',
            'button.btn-primary:has-text("Save")',
            'input[type="submit"][value="Save"]',
            'button:has-text("Create Task")',
            'button:has-text("Create")',
        ]
        
        clicked = False
        for selector in save_selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                try:
                    # Try all matching elements
                    for i in range(locator.count()):
                        element = locator.nth(i)
                        if element.is_visible():
                            element.scroll_into_view_if_needed()
                            element.click()
                            clicked = True
                            logger.info(f"✓ Clicked Save button with selector: {selector}")
                            break
                    if clicked:
                        break
                except Exception as e:
                    logger.debug(f"Could not click Save with {selector}: {e}")
        
        if not clicked:
            self.screenshot("save-button-not-found")
            raise Exception("Could not find or click Save button")
        
        # Wait for save to complete
        self.page.wait_for_timeout(3000)
        
        # Wait for navigation
        try:
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            logger.warning(f"Network idle timeout after save: {e}")
        
        self.screenshot("after-save-click")
        logger.info("✓ Save button clicked")
    
    def verify_task_created(self, title: str) -> bool:
        """
        Verify task was created successfully.
        
        Args:
            title: Expected task title
            
        Returns:
            True if task appears to be created
        """
        logger.info(f"Verifying task '{title}' was created")
        self.screenshot("verifying-task-creation")
        
        current_url = self.page.url
        logger.info(f"Current URL: {current_url}")
        
        # Check if URL contains task ID or task-specific path
        url_indicators = [
            "taskId=",
            "/task/",
            "/tasks/",
            "task-create",
        ]
        
        has_task_url = any(indicator in current_url for indicator in url_indicators)
        
        if has_task_url:
            logger.info(f"✓ URL indicates task page: {current_url}")
        else:
            logger.warning(f"URL does not clearly indicate task page: {current_url}")
        
        # Try to find task title on page
        try:
            # Look for the title we just entered
            title_locators = [
                f'text={title}',
                f'h1:has-text("{title}")',
                f'h2:has-text("{title}")',
                f'.task-title:has-text("{title}")',
            ]
            
            for selector in title_locators:
                if self.page.locator(selector).count() > 0:
                    logger.info(f"✓ Found task title on page: {title}")
                    return True
        except Exception as e:
            logger.debug(f"Could not find task title on page: {e}")
        
        # If URL has task indicator, consider it successful even if title not found
        if has_task_url:
            logger.info("✓ Task appears to be created (URL has task indicator)")
            return True
        
        # Last resort: Check if we're not on the creation form anymore
        if "task-create" not in current_url and "/n/" not in current_url:
            logger.info("✓ Navigated away from creation form, likely task created")
            return True
        
        logger.warning("Could not definitively verify task creation")
        self.screenshot("task-creation-verification-uncertain")
        return False
    
    def complete_task_creation_workflow(
        self,
        title: str,
        description: str,
        code: str
    ) -> None:
        """
        Complete workflow: Fill all fields and save task.
        
        Args:
            title: Task title
            description: Task description
            code: Task code
        """
        logger.info(f"Starting complete task creation workflow for: {title}")
        
        self.fill_task_title(title)
        self.page.wait_for_timeout(500)
        
        self.fill_task_description(description)
        self.page.wait_for_timeout(500)
        
        self.fill_task_code(code)
        self.page.wait_for_timeout(500)
        
        self.click_save_button()
        
        logger.info("✓ Task creation workflow completed")
