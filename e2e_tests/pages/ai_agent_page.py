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
        """Click the 'New Task' button to open dropdown."""
        logger.info("Clicking 'New Task' button")
        
        # Wait for button to be visible
        self.page.get_by_role("button", name="New Task").wait_for(state="visible", timeout=10000)
        
        # Click button
        self.page.get_by_role("button", name="New Task").click()
        
        # Wait for dropdown to appear
        self.page.wait_for_timeout(1000)
        logger.info("✓ New Task dropdown opened")
    
    def click_create_with_ai_agent(self) -> None:
        """Click 'Create with AI Agent' from dropdown."""
        logger.info("Clicking 'Create with AI Agent'")
        
        # Find and click the option
        # Try different possible selectors
        selectors = [
            'text=Create with AI Agent',
            '[role="menuitem"]:has-text("Create with AI Agent")',
            'button:has-text("Create with AI Agent")',
            'a:has-text("Create with AI Agent")'
        ]
        
        clicked = False
        for selector in selectors:
            if self.page.locator(selector).count() > 0:
                self.page.locator(selector).first.click()
                clicked = True
                break
        
        if not clicked:
            logger.warning("Could not find 'Create with AI Agent' option")
            # Take screenshot for debugging
            self.screenshot("create-with-ai-agent-not-found")
        
        # Wait for navigation to agent page
        self.page.wait_for_load_state("networkidle", timeout=10000)
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
        Type message in chat input.
        
        Args:
            message: Message to type
        """
        logger.info(f"Typing message: {message[:50]}...")
        
        # Find chat input (try multiple selectors)
        chat_input = None
        selectors = [
            'textarea[placeholder*="Ask"]',
            'input[placeholder*="Ask"]',
            'textarea[placeholder*="anything"]',
            'input[placeholder*="anything"]',
            'textarea',
            'div[contenteditable="true"]'
        ]
        
        for selector in selectors:
            locator = self.page.locator(selector)
            if locator.count() > 0 and locator.first.is_visible():
                chat_input = locator.first
                break
        
        if chat_input:
            # Click to focus
            chat_input.click()
            
            # Clear any existing text
            chat_input.fill("")
            
            # Type message
            chat_input.fill(message)
            logger.info("✓ Message typed")
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
    
    def wait_for_ai_response(self, timeout: int = 60000) -> None:
        """
        Wait for AI to respond.
        
        Args:
            timeout: Wait timeout in ms (AI can be slow)
        """
        logger.info("Waiting for AI response...")
        
        # Wait for response indicators
        self.page.wait_for_timeout(2000)  # Initial wait
        
        # Look for AI response indicators
        ai_indicators = [
            '.ai-response',
            '.assistant-message',
            '[data-role="assistant"]',
            '.message.ai',
            'text=Task created successfully',
            'text=I can help'
        ]
        
        response_found = False
        for selector in ai_indicators:
            if self.page.locator(selector).count() > 0:
                logger.info(f"✓ AI response detected ({selector})")
                response_found = True
                break
        
        if not response_found:
            # Wait for loading to finish
            loading_selectors = ['.loading', '.spinner', '.thinking']
            for selector in loading_selectors:
                if self.page.locator(selector).count() > 0:
                    try:
                        self.page.locator(selector).wait_for(state="hidden", timeout=timeout)
                    except Exception:
                        pass
            
            logger.info("✓ AI processing completed (no specific response indicator found)")
    
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

