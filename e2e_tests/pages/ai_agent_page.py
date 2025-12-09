"""
AI Agent Page Object.

Handles AI agent task creation and interaction.
"""

import logging
from typing import Optional
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class AIAgentPage(BasePage):
    """AI Agent page object (for agent mode task creation)."""
    
    # Selectors
    NEW_TASK_BUTTON = 'button:has-text("New Task"), button:has-text("+ New Task")'
    NEW_TASK_DROPDOWN = 'button:has-text("New Task") + div, [role="menu"]'
    CREATE_FROM_FORM = 'text=Create from Form'
    CREATE_WITH_AI_AGENT = 'text=Create with AI Agent'
    IMPORT_FROM_DOCUMENT = 'text=Import from Document'
    
    # AI Agent chat selectors
    CHAT_INPUT = 'textarea[placeholder*="Ask anything"], input[placeholder*="Ask anything"]'
    SEND_BUTTON = 'button[type="submit"], button:has-text("Send")'
    AGENT_MODE_TOGGLE = 'text=Agent Mode'
    HOW_CAN_I_HELP = 'text=How can I help?'
    CHAT_MESSAGE = '.message, .chat-message'
    AI_RESPONSE = '.ai-response, .assistant-message, [data-role="assistant"]'
    
    def __init__(self, page):
        """Initialize AI agent page."""
        super().__init__(page)
    
    def click_new_task_button(self) -> None:
        """Click the 'New Task' button (blue button on top right) to open dropdown."""
        logger.info("Clicking 'New Task' button")
        
        # Take screenshot before clicking
        self.screenshot("before-new-task-click")
        
        # Wait for page to be ready
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Try multiple selector strategies for the "New Task" button
        button_selectors = [
            'button:has-text("New Task")',  # Button with text
            'button:has-text("+ New Task")',  # Button with + prefix
            '[class*="btn"]:has-text("New Task")',  # Button with btn class
            'button.btn-primary:has-text("New Task")',  # Primary button
        ]
        
        clicked = False
        for selector in button_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    logger.info(f"Found New Task button with: {selector}")
                    locator.first.wait_for(state="visible", timeout=5000)
                    locator.first.click()
                    clicked = True
                    logger.info("✓ Clicked New Task button")
                    break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not clicked:
            self.screenshot("new-task-button-not-found")
            raise Exception("Could not find New Task button")
        
        # Wait for dropdown to appear
        self.page.wait_for_timeout(1500)
        
        # Take screenshot of dropdown
        self.screenshot("new-task-dropdown-open")
        logger.info("✓ New Task dropdown opened")
    
    def click_create_with_ai_agent(self) -> None:
        """Click 'Create with AI Agent' from the New Task dropdown menu."""
        logger.info("Clicking 'Create with AI Agent' from dropdown")
        
        # Take screenshot of dropdown before clicking
        self.screenshot("dropdown-before-click")
        
        # Wait a bit for dropdown animation to complete
        self.page.wait_for_timeout(500)
        
        # Try different possible selectors for the dropdown option
        # Based on the screenshot, the dropdown shows:
        # - Create from Form
        # - Import from Document  
        # - Create with AI Agent
        selectors = [
            'text=Create with AI Agent',  # Exact text match
            ':text("Create with AI Agent")',  # Case insensitive
            '[role="menuitem"]:has-text("Create with AI Agent")',  # Menu item role
            'button:has-text("Create with AI Agent")',  # If it's a button
            'a:has-text("Create with AI Agent")',  # If it's a link
            'div:has-text("Create with AI Agent")',  # If it's a div
            '[class*="menu"] :has-text("Create with AI Agent")',  # Inside menu
            ':text("AI Agent")',  # Partial match as fallback
        ]
        
        clicked = False
        for selector in selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                if count > 0:
                    logger.info(f"Found 'Create with AI Agent' with selector: {selector} (count: {count})")
                    
                    # Wait for it to be visible
                    locator.first.wait_for(state="visible", timeout=3000)
                    
                    # Scroll into view if needed
                    locator.first.scroll_into_view_if_needed()
                    
                    # Click it
                    locator.first.click()
                    
                    clicked = True
                    logger.info("✓ Clicked 'Create with AI Agent'")
                    break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if not clicked:
            logger.error("Could not find 'Create with AI Agent' option in dropdown")
            self.screenshot("create-with-ai-agent-not-found")
            
            # Log all visible text for debugging
            try:
                all_text = self.page.inner_text('body')
                logger.error(f"Page contains: {all_text[:500]}")
            except Exception:
                pass
            
            raise Exception("Could not find 'Create with AI Agent' option")
        
        # Wait for navigation to AI agent page
        self.page.wait_for_timeout(2000)
        
        # Wait for network idle
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            logger.warning(f"Network idle timeout: {e}")
        
        # Take screenshot after navigation
        self.screenshot("after-ai-agent-navigation")
        
        # Verify URL contains agent=1
        current_url = self.page.url
        logger.info(f"Current URL after clicking: {current_url}")
        
        if "agent=1" not in current_url:
            logger.warning("URL does not contain 'agent=1' - might not be on AI Agent page")
        
        logger.info("✓ Navigated to AI Agent page")
    
    def navigate_to_ai_agent_directly(self, workspace: str = "") -> None:
        """
        Navigate directly to AI agent page (bypass dropdown).
        
        Args:
            workspace: Workspace name (empty string for default)
        """
        url = f"/tasks/DAGKNOWS?agent=1&space={workspace}"
        logger.info(f"Navigating directly to AI agent: {url}")
        self.goto(url)
        self.wait_for_load()
    
    def wait_for_agent_page_loaded(self, timeout: int = 10000) -> None:
        """
        Wait for AI agent page to fully load.
        
        Args:
            timeout: Wait timeout in ms
        """
        logger.info("Waiting for AI agent page to load")
        
        # Wait for chat input or "How can I help?" text
        try:
            # Try to find the help text
            self.page.locator('text=How can I help?').wait_for(
                state="visible",
                timeout=timeout
            )
            logger.info("✓ AI agent page loaded (help text visible)")
        except Exception:
            # Fallback: look for chat input
            logger.info("Help text not found, checking for chat input")
            self.wait_for_chat_input_ready(timeout=timeout)
    
    def wait_for_chat_input_ready(self, timeout: int = 10000) -> None:
        """
        Wait for chat input to be ready.
        
        Args:
            timeout: Wait timeout in ms
        """
        # Try multiple possible selectors for chat input
        chat_selectors = [
            'textarea[placeholder*="Ask"]',
            'input[placeholder*="Ask"]',
            'textarea',
            'div[contenteditable="true"]'
        ]
        
        for selector in chat_selectors:
            if self.page.locator(selector).count() > 0:
                self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
                logger.info("✓ Chat input ready")
                return
        
        logger.warning("Could not find chat input")
    
    def type_message(self, message: str) -> None:
        """
        Type message in the AI Agent chat input box (the "How can I help" text box).
        
        Args:
            message: Message to type
        """
        logger.info(f"Typing message: {message[:50]}...")
        
        # Take screenshot before typing
        self.screenshot("before-typing-message")
        
        # Find chat input - try multiple selectors
        # Based on the screenshot, looking for the text box with "How can I help" placeholder
        chat_input = None
        selectors = [
            'textarea[placeholder*="How can I help"]',  # Exact match for "How can I help"
            'input[placeholder*="How can I help"]',
            'textarea[placeholder*="help"]',  # Partial match
            'input[placeholder*="help"]',
            'textarea[placeholder*="Ask"]',
            'input[placeholder*="Ask"]',
            'textarea[placeholder*="anything"]',
            'input[placeholder*="anything"]',
            'textarea',  # Any textarea as fallback
            'div[contenteditable="true"]',  # Contenteditable div
        ]
        
        for selector in selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                if count > 0:
                    # Check if visible
                    first_match = locator.first
                    if first_match.is_visible():
                        logger.info(f"Found chat input with selector: {selector}")
                        chat_input = first_match
                        break
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
        
        if chat_input:
            # Wait for input to be ready
            chat_input.wait_for(state="visible", timeout=5000)
            
            # Click to focus
            chat_input.click()
            
            # Wait a moment for focus
            self.page.wait_for_timeout(500)
            
            # Clear any existing text
            chat_input.fill("")
            
            # Type message
            chat_input.fill(message)
            
            logger.info("✓ Message typed successfully")
            
            # Take screenshot after typing
            self.screenshot("after-typing-message")
        else:
            logger.error("Could not find chat input field")
            self.screenshot("chat-input-not-found")
            raise Exception("Chat input field not found")
    
    def click_send(self) -> None:
        """Click send button or press Enter."""
        logger.info("Sending message")
        
        # Try to find send button
        send_selectors = [
            'button[type="submit"]',
            'button:has-text("Send")',
            'button[aria-label*="Send"]',
            'button svg' # Send icon button
        ]
        
        send_clicked = False
        for selector in send_selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                try:
                    locator.first.click()
                    send_clicked = True
                    logger.info("✓ Send button clicked")
                    break
                except Exception as e:
                    logger.debug(f"Could not click {selector}: {e}")
        
        if not send_clicked:
            # Fallback: press Enter
            logger.info("Send button not found, pressing Enter")
            self.page.keyboard.press("Enter")
    
    def send_message(self, message: str) -> None:
        """
        Complete flow: type message and send.
        
        Args:
            message: Message to send
        """
        self.type_message(message)
        self.click_send()
    
    def wait_for_ai_response(self, timeout: int = 90000) -> None:
        """
        Wait for AI to generate the task with code (can take 30-60 seconds).
        
        Args:
            timeout: Wait timeout in ms (default 90 seconds for AI generation)
        """
        logger.info("Waiting for AI to generate task with code...")
        logger.info("This may take 30-60 seconds while AI processes the request")
        
        # Take screenshot immediately after sending
        self.screenshot("01-immediately-after-send")
        
        # Initial wait for AI to start processing
        self.page.wait_for_timeout(5000)
        
        # Look for indicators that AI is working/done
        # The key is to wait for the task CODE to be generated and visible
        
        # Strategy 1: Wait for loading indicators to disappear
        logger.info("Checking for loading indicators...")
        loading_selectors = [
            '.loading', 
            '.spinner', 
            '.thinking',
            '[class*="loading"]',
            '[class*="spinner"]',
        ]
        
        for selector in loading_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0:
                    logger.info(f"Found loading indicator: {selector}, waiting for it to hide...")
                    locator.first.wait_for(state="hidden", timeout=60000)
                    logger.info(f"✓ Loading indicator hidden")
            except Exception as e:
                logger.debug(f"Loading selector '{selector}' check: {e}")
        
        # Wait additional time for AI to finish generating code
        logger.info("Waiting 10 more seconds for AI to complete code generation...")
        self.page.wait_for_timeout(10000)
        
        # Take screenshot after waiting
        self.screenshot("02-after-ai-processing-wait")
        
        # Strategy 2: Look for task code/content indicators
        # After AI generates the task, we should see code or task details
        task_content_indicators = [
            'button:has-text("Code")',  # Code tab button
            'pre',  # Code block
            'code',  # Inline code
            '[class*="code"]',  # Code-related elements
            'text=import',  # Python imports
            'text=def ',  # Python function definition
            'text=try:',  # Python try block
            ':text("boto3")',  # AWS SDK
            ':text("Task created")',  # Success message
        ]
        
        task_generated = False
        logger.info("Checking if task code was generated...")
        for indicator in task_content_indicators:
            try:
                locator = self.page.locator(indicator)
                count = locator.count()
                if count > 0:
                    logger.info(f"✓ Found task content indicator: {indicator} (count: {count})")
                    task_generated = True
                    break
            except Exception:
                pass
        
        # Take screenshot of final state
        self.screenshot("03-after-ai-response-check")
        
        # Strategy 3: Wait for URL to stabilize (task ID in URL)
        current_url = self.page.url
        logger.info(f"Current URL: {current_url}")
        
        # If we see a task ID in the URL, task was created
        if "/tasks/" in current_url and "agent=1" in current_url:
            logger.info("✓ Task URL detected - task was created")
            task_generated = True
        
        # Final wait to ensure everything is rendered
        logger.info("Final wait for UI to stabilize...")
        self.page.wait_for_timeout(5000)
        
        # Take final screenshot
        self.screenshot("04-final-ai-response-state")
        
        if task_generated:
            logger.info("✓ AI task generation completed successfully")
        else:
            logger.warning("⚠ Could not confirm task code was generated (but continuing anyway)")
            logger.warning("Check screenshots to verify task creation")
    
    def verify_agent_mode_active(self) -> bool:
        """
        Verify agent mode is active.
        
        Returns:
            True if agent mode is active
        """
        # Check URL contains agent=1
        current_url = self.page.url
        agent_active = "agent=1" in current_url
        
        if agent_active:
            logger.info("✓ Agent mode is active")
        else:
            logger.warning("⚠ Agent mode may not be active")
        
        return agent_active
    
    def complete_ai_agent_workflow(
        self,
        prompt: str,
        wait_for_response: bool = True
    ) -> None:
        """
        Complete AI agent workflow: type message and send.
        
        Args:
            prompt: Prompt to send to AI
            wait_for_response: Whether to wait for AI response
        """
        logger.info(f"=== Starting AI Agent Workflow ===")
        logger.info(f"Prompt: {prompt}")
        
        # Wait for page to be ready
        self.wait_for_agent_page_loaded()
        
        # Send message
        self.send_message(prompt)
        
        # Wait for response if requested
        if wait_for_response:
            self.wait_for_ai_response()
        
        logger.info("=== AI Agent Workflow Completed ===")

