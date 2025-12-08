"""
Test data factories and fixtures for generating test data.
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List
from faker import Faker

fake = Faker()


class TestDataFactory:
    """Factory for generating test data."""
    
    @staticmethod
    def random_string(length: int = 10) -> str:
        """Generate a random string."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    @staticmethod
    def random_email() -> str:
        """Generate a random email address."""
        return fake.email()
    
    @staticmethod
    def random_org_name() -> str:
        """Generate a random organization name."""
        return f"{fake.company().replace(' ', '-').lower()}-{int(datetime.now().timestamp())}"
    
    # ========================================
    # User Data
    # ========================================
    
    @staticmethod
    def create_user_data(
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        organization: str = None,
        password: str = "TestPass123!",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate user data for testing."""
        return {
            "email": email or fake.email(),
            "first_name": first_name or fake.first_name(),
            "last_name": last_name or fake.last_name(),
            "organization": organization or TestDataFactory.random_org_name(),
            "password": password,
            **kwargs
        }
    
    # ========================================
    # Tenant Data
    # ========================================
    
    @staticmethod
    def create_tenant_data(
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        organization: str = None,
        password: str = "TenantPass123!",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate tenant data for testing."""
        return {
            "email": email or fake.email(),
            "first_name": first_name or fake.first_name(),
            "last_name": last_name or fake.last_name(),
            "organization": organization or TestDataFactory.random_org_name(),
            "password": password,
            **kwargs
        }
    
    # ========================================
    # Task Data
    # ========================================
    
    @staticmethod
    def create_task_data(
        title: str = None,
        description: str = None,
        script: str = None,
        script_type: str = "python",
        tags: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate task data for testing (Python script by default)."""
        return {
            "title": title or f"Test Task {int(datetime.now().timestamp())}",
            "description": description or fake.sentence(),
            "script": script or "print('Hello World')",
            "script_type": script_type,
            "tags": tags or ["test"],
            **kwargs
        }
    
    @staticmethod
    def create_python_task_data(
        title: str = None,
        description: str = None,
        script: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate Python task data for testing."""
        return {
            "title": title or f"Python Task {int(datetime.now().timestamp())}",
            "description": description or fake.sentence(),
            "script": script or "print('Hello from Python')",
            "script_type": "python",
            "tags": tags or ["test", "python"],
            **kwargs
        }
    
    @staticmethod
    def create_shell_task_data(
        title: str = None,
        description: str = None,
        script: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate shell script task data for testing."""
        return {
            "title": title or f"Shell Task {int(datetime.now().timestamp())}",
            "description": description or fake.sentence(),
            "script": script or "echo 'Hello from Shell'",
            "script_type": "shell",
            "tags": tags or ["test", "shell"],
            **kwargs
        }
    
    @staticmethod
    def create_bash_task_data(
        title: str = None,
        description: str = None,
        script: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate bash script task data for testing."""
        return {
            "title": title or f"Bash Task {int(datetime.now().timestamp())}",
            "description": description or fake.sentence(),
            "script": script or "#!/bin/bash\necho 'Hello from Bash'",
            "script_type": "bash",
            "tags": tags or ["test", "bash"],
            **kwargs
        }
    
    @staticmethod
    def create_task_with_params(
        title: str = None,
        input_params: List[Dict] = None,
        output_params: List[Dict] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate task data with parameters."""
        task_data = TestDataFactory.create_task_data(title=title, **kwargs)
        
        if input_params is None:
            input_params = [
                {"name": "param1", "type": "string", "required": True},
                {"name": "param2", "type": "string", "required": False},
            ]
        
        if output_params is None:
            output_params = [
                {"name": "result", "type": "string"},
            ]
        
        task_data.update({
            "input_params": input_params,
            "output_params": output_params,
        })
        
        return task_data
    
    @staticmethod
    def create_task_with_commands(
        title: str = None,
        commands: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate task data with command list."""
        task_data = TestDataFactory.create_task_data(title=title, **kwargs)
        task_data.pop("script", None)  # Remove script field
        
        if commands is None:
            commands = [
                "ls -la",
                "pwd",
                "date",
            ]
        
        task_data.update({
            "script_type": "command",
            "commands": commands,
        })
        
        return task_data
    
    # ========================================
    # Workspace Data
    # ========================================
    
    @staticmethod
    def create_workspace_data(
        name: str = None,
        description: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate workspace data for testing."""
        return {
            "name": name or f"Test Workspace {int(datetime.now().timestamp())}",
            "description": description or fake.sentence(),
            **kwargs
        }
    
    # ========================================
    # Role Data
    # ========================================
    
    @staticmethod
    def create_role_data(
        name: str = None,
        permissions: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate role data for testing."""
        if permissions is None:
            permissions = ["read", "write", "execute"]
        
        return {
            "name": name or f"test-role-{int(datetime.now().timestamp())}",
            "permissions": permissions,
            **kwargs
        }
    
    # ========================================
    # Job Data
    # ========================================
    
    @staticmethod
    def create_job_data(
        task_id: str = None,
        params: Dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate job data for testing."""
        return {
            "task_id": task_id or f"task-{TestDataFactory.random_string()}",
            "params": params or {},
            "scheduled_at": (datetime.now() + timedelta(hours=1)).isoformat(),
            **kwargs
        }
    
    # ========================================
    # AI Session Data
    # ========================================
    
    @staticmethod
    def create_ai_session_data(
        title: str = None,
        initial_message: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate AI session data for testing."""
        return {
            "title": title or f"AI Session {int(datetime.now().timestamp())}",
            "initial_message": initial_message or "Help me troubleshoot an issue",
            "model": "gpt-4",
            **kwargs
        }
    
    # ========================================
    # Conversation Data
    # ========================================
    
    @staticmethod
    def create_conversation_data(
        subject: str = None,
        participants: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate conversation data for testing."""
        return {
            "subject": subject or f"Test Conversation {int(datetime.now().timestamp())}",
            "participants": participants or [],
            **kwargs
        }
    
    # ========================================
    # Bulk Data Generation
    # ========================================
    
    @staticmethod
    def create_multiple_tasks(count: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Generate multiple task data objects."""
        return [
            TestDataFactory.create_task_data(
                title=f"Task {i+1} - {int(datetime.now().timestamp())}",
                **kwargs
            )
            for i in range(count)
        ]
    
    @staticmethod
    def create_multiple_users(count: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Generate multiple user data objects."""
        return [
            TestDataFactory.create_user_data(**kwargs)
            for _ in range(count)
        ]
    
    @staticmethod
    def create_multiple_workspaces(count: int = 3, **kwargs) -> List[Dict[str, Any]]:
        """Generate multiple workspace data objects."""
        return [
            TestDataFactory.create_workspace_data(
                name=f"Workspace {i+1} - {int(datetime.now().timestamp())}",
                **kwargs
            )
            for i in range(count)
        ]


# Convenience functions
def create_basic_task(title: str = "Basic Test Task") -> Dict[str, Any]:
    """Create a basic Python task with minimal fields."""
    return {
        "title": title,
        "description": "A basic test task",
        "script": "print('test')",
        "script_type": "python",
        "tags": ["test"],
    }


def create_python_task(title: str = "Python Test Task") -> Dict[str, Any]:
    """Create a Python task."""
    return {
        "title": title,
        "description": "A Python test task",
        "script": "print('Hello from Python')",
        "script_type": "python",
        "tags": ["python", "test"],
    }


def create_bash_task(title: str = "Bash Test Task") -> Dict[str, Any]:
    """Create a Bash task."""
    return {
        "title": title,
        "description": "A Bash test task",
        "script": "#!/bin/bash\necho 'Hello from Bash'",
        "script_type": "bash",
        "tags": ["bash", "test"],
    }


def create_command_task(title: str = "Command Test Task") -> Dict[str, Any]:
    """Create a command-type task."""
    return {
        "title": title,
        "description": "A command-type test task",
        "script_type": "command",
        "commands": ["echo 'test'", "pwd"],
        "tags": ["command", "test"],
    }

