"""
AI Chat Page Object.

Handles AI chat session interactions.
"""

import logging
from typing import Optional
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ChatPage(BasePage):
    """AI Chat page object."""
    
    # Selectors
    NEW_CHAT_BUTTON = 'button:has-text("New Chat"), button:has-text("New Session")'
    CHAT_INPUT = 'textarea[placeholder*="message"], input[placeholder*="message"]'
    SEND_BUTTON = 'button[type="submit"], button:has-text("Send")'
    CHAT_MESSAGE = '.chat-message, .message'
    AI_RESPONSE = '.ai-response, .assistant-message'
    CHAT_HISTORY = '.chat-history, .messages-container'
    
    def __init__(self, page):
        """Initialize chat page."""
        super().__init__(page)
    
    def navigate_to_chat(self) -> None:
        """Navigate to chat page."""
        logger.info("Navigating to AI chat")
        self.goto("/chat")
        self.wait_for_load()
    
    def click_new_chat(self) -> None:
        """Start a new chat session."""
        logger.info("Starting new chat session")
        new_chat_button = self.page.locator(self.NEW_CHAT_BUTTON)
        if new_chat_button.count() > 0:
            new_chat_button.first.click()
            self.page.wait_for_timeout(1000)
    
    def type_message(self, message: str) -> None:
        """
        Type message in chat input.
        
        Args:
            message: Message to type
        """
        logger.info(f"Typing message: {message[:50]}...")
        
        # Find chat input (various possible selectors)
        chat_input = None
        selectors = [
            'textarea[placeholder*="message"]',
            'input[placeholder*="message"]',
            'textarea',
            'div[contenteditable="true"]'
        ]
        
        for selector in selectors:
            if self.page.locator(selector).count() > 0:
                chat_input = self.page.locator(selector).first
                break
        
        if chat_input:
            chat_input.click()
            chat_input.fill(message)
        else:
            logger.error("Could not find chat input field")
            raise Exception("Chat input field not found")
    
    def click_send(self) -> None:
        """Click send button or press Enter."""
        logger.info("Sending message")
        
        # Try to find send button
        send_button = self.page.locator(self.SEND_BUTTON)
        if send_button.count() > 0:
            send_button.first.click()
        else:
            # Press Enter as alternative
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
        
        # Wait for new message to appear in chat history
        # This is tricky as we need to detect new messages
        self.page.wait_for_timeout(2000)  # Initial wait
        
        # Look for AI response indicators
        ai_indicators = [
            '.ai-response',
            '.assistant-message',
            '[data-role="assistant"]',
            '.message.ai'
        ]
        
        for selector in ai_indicators:
            if self.page.locator(selector).count() > 0:
                logger.info("✓ AI response received")
                return
        
        # Fallback: wait for loading to finish
        loading_selectors = ['.loading', '.spinner', '.thinking']
        for selector in loading_selectors:
            if self.page.locator(selector).count() > 0:
                self.page.locator(selector).wait_for(state="hidden", timeout=timeout)
        
        logger.info("✓ AI processing completed")
    
    def get_last_ai_response(self) -> Optional[str]:
        """
        Get the last AI response text.
        
        Returns:
            AI response text or None
        """
        try:
            # Try different selectors for AI responses
            ai_messages = self.page.locator(self.AI_RESPONSE)
            if ai_messages.count() > 0:
                return ai_messages.last.text_content()
            
            # Alternative: get all messages and find last one
            all_messages = self.page.locator(self.CHAT_MESSAGE)
            if all_messages.count() > 0:
                return all_messages.last.text_content()
            
            return None
        except Exception as e:
            logger.error(f"Could not get AI response: {e}")
            return None
    
    def start_chat_and_send_prompt(self, prompt: str) -> str:
        """
        Complete flow: start new chat, send prompt, wait for response.
        
        Args:
            prompt: Initial prompt
            
        Returns:
            AI response text
        """
        logger.info(f"=== Starting chat session with prompt ===")
        logger.info(f"Prompt: {prompt}")
        
        # Start new chat
        self.click_new_chat()
        
        # Send prompt
        self.send_message(prompt)
        
        # Wait for response
        self.wait_for_ai_response()
        
        # Get response
        response = self.get_last_ai_response()
        logger.info(f"AI Response: {response[:100] if response else 'None'}...")
        
        return response
    
    def verify_chat_session_active(self) -> bool:
        """
        Verify chat session is active.
        
        Returns:
            True if chat is active, False otherwise
        """
        return self.is_visible(self.CHAT_INPUT, timeout=2000)

