"""
Task Page Object.

Handles task creation, editing, and management UI interactions.
"""

import logging
from typing import Optional
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class TaskPage(BasePage):
    """Task page object (for task creation and management)."""
    
    # Selectors
    CREATE_RUNBOOK_BUTTON = 'button:has-text("Create runbook")'
    TASK_TITLE_INPUT = 'input[placeholder="Task title"]'
    SAVE_BUTTON = 'button:has-text("Save")'
    CANCEL_BUTTON = 'button:has-text("Cancel")'
    SCRIPT_TYPE_DROPDOWN = 'select, role=combobox'
    COMMAND_TEXTAREA = 'textarea, div[contenteditable="true"]'
    ADD_CHILD_TASK_ICON = 'i.fa-plus'
    TASK_TITLE_READONLY = '.task_title_container_readonly'
    
    def __init__(self, page):
        """Initialize task page."""
        super().__init__(page)
    
    def navigate_to_home(self) -> None:
        """Navigate to home/dashboard."""
        logger.info("Navigating to home")
        self.goto("/")
        self.wait_for_load()
    
    def click_create_runbook(self) -> None:
        """Click 'Create Runbook' button."""
        logger.info("Clicking 'Create Runbook' button")
        self.page.get_by_role("button", name="Create runbook").wait_for(state="visible")
        self.page.get_by_role("button", name="Create runbook").click()
        # Wait for modal/form to appear
        self.page.get_by_role("button", name="Save").wait_for(state="visible")
    
    def fill_task_title(self, title: str) -> None:
        """
        Fill task title.
        
        Args:
            title: Task title
        """
        logger.info(f"Filling task title: {title}")
        self.page.get_by_placeholder("Task title").click()
        self.page.get_by_placeholder("Task title").fill(title)
    
    def select_script_type(self, script_type: str) -> None:
        """
        Select script type.
        
        Args:
            script_type: One of 'command', 'python', 'powershell'
        """
        logger.info(f"Selecting script type: {script_type}")
        # Click dropdown
        self.page.get_by_role("combobox").click()
        # Select option
        self.page.get_by_role("combobox").select_option(script_type)
    
    def fill_command(self, command: str) -> None:
        """
        Fill command/script.
        
        Args:
            command: Command or script text
        """
        logger.info("Filling command/script")
        # Find the command textarea
        command_field = self.page.get_by_role("textbox").filter(has_text="Command")
        if command_field.count() > 0:
            command_field.locator("div").click()
            command_field.type(command)
        else:
            # Try alternative selector
            self.page.locator('textarea, div[contenteditable="true"]').first.fill(command)
    
    def click_save(self) -> None:
        """Click save button."""
        logger.info("Clicking save button")
        self.page.get_by_role("button", name="Save").click()
    
    def wait_for_task_created(self, title: str, timeout: int = 10000) -> None:
        """
        Wait for task to be created and visible.
        
        Args:
            title: Task title to wait for
            timeout: Wait timeout in ms
        """
        logger.info(f"Waiting for task '{title}' to be created")
        xpath = f"//div[contains(@class, 'task_title_container_readonly')]//*[text()='{title}']"
        self.page.locator(xpath).wait_for(state="visible", timeout=timeout)
        logger.info(f"✓ Task '{title}' is visible")
    
    def create_top_level_task(
        self,
        title: str,
        script_type: str = "command",
        commands: Optional[str] = None
    ) -> None:
        """
        Create a top-level task (complete flow).
        
        Args:
            title: Task title
            script_type: Script type (command, python, powershell)
            commands: Command/script content (optional)
        """
        logger.info(f"=== Creating top-level task: {title} ===")
        
        # Step 1: Click create button
        self.page.wait_for_timeout(3000)  # Wait for page to stabilize
        self.click_create_runbook()
        
        # Step 2: Fill title
        self.fill_task_title(title)
        
        # Step 3: Select script type (if not default)
        if script_type and script_type != "command":
            self.select_script_type(script_type)
        
        # Step 4: Fill command (if provided)
        if commands:
            self.fill_command(commands)
        
        # Step 5: Save
        self.click_save()
        
        # Step 6: Wait for task to appear
        self.wait_for_task_created(title)
        
        logger.info(f"=== Task '{title}' created successfully ===")
    
    def hover_over_task(self, title: str) -> None:
        """
        Hover over a task to reveal actions.
        
        Args:
            title: Task title
        """
        xpath = f"//div[contains(@class, 'task_title_container_readonly')]//*[text()='{title}']"
        self.page.locator(xpath).hover()
    
    def click_add_child_task(self, parent_title: str) -> None:
        """
        Click add child task icon for a parent task.
        
        Args:
            parent_title: Parent task title
        """
        logger.info(f"Adding child task to: {parent_title}")
        self.hover_over_task(parent_title)
        xpath = f"//div[contains(@class, 'task_title_container_readonly')]//*[text()='{parent_title}']/following-sibling::div[contains(@class,'icons_container')]//i[contains(@class,'fa-plus')]"
        self.page.locator(xpath).click()
    
    def create_child_task(
        self,
        parent_title: str,
        child_title: str,
        script_type: str = "command",
        commands: Optional[str] = None
    ) -> None:
        """
        Create a child task under a parent.
        
        Args:
            parent_title: Parent task title
            child_title: Child task title
            script_type: Script type
            commands: Command/script content
        """
        logger.info(f"=== Creating child task '{child_title}' under '{parent_title}' ===")
        
        # Click add child task icon
        self.click_add_child_task(parent_title)
        
        # Fill title
        self.fill_task_title(child_title)
        
        # Select script type
        if script_type:
            self.select_script_type(script_type)
        
        # Fill command
        if commands:
            self.fill_command(commands)
        
        # Save
        self.click_save()
        
        # Wait for child task to appear
        self.page.wait_for_timeout(6000)  # Wait for autocomplete to disappear
        child_xpath = f"//a[text()='{child_title}']"
        self.page.locator(child_xpath).wait_for(state="visible")
        
        logger.info(f"=== Child task '{child_title}' created successfully ===")
    
    def delete_task(self, title: str) -> None:
        """
        Delete a task.
        
        Args:
            title: Task title
        """
        logger.info(f"Deleting task: {title}")
        self.hover_over_task(title)
        delete_xpath = f"//div[contains(@class, 'task_title_container_readonly')]//*[text()='{title}']/parent::*/parent::*//div[contains(@class,'icons_container')]//i[contains(@class,'fa-trash-can')]"
        self.page.locator(delete_xpath).click()
        
        # Confirm deletion if modal appears
        self.page.wait_for_timeout(1000)
        confirm_button = self.page.locator('button:has-text("Delete"), button:has-text("Confirm")')
        if confirm_button.count() > 0:
            confirm_button.first.click()
        
        # Wait for task to disappear
        task_xpath = f"//a[text()='{title}']"
        self.page.locator(task_xpath).wait_for(state="hidden", timeout=5000)
        logger.info(f"✓ Task '{title}' deleted")
    
    def verify_task_exists(self, title: str, timeout: int = 5000) -> bool:
        """
        Verify task exists on page.
        
        Args:
            title: Task title
            timeout: Wait timeout in ms
            
        Returns:
            True if task exists, False otherwise
        """
        xpath = f"//a[text()='{title}']"
        return self.is_visible(xpath, timeout=timeout)

