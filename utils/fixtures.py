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
    
    # ========================================
    # Alert Data
    # ========================================
    
    @staticmethod
    def create_grafana_alert_data(
        alert_name: str = "TestAlert",
        alert_source: str = "grafana",
        status: str = "firing",
        severity: str = "warning",
        description: str = None,
        summary: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate Grafana-style alert payload for testing."""
        return create_grafana_alert_data(
            alert_name=alert_name,
            alert_source=alert_source,
            status=status,
            severity=severity,
            description=description or fake.sentence(),
            summary=summary or fake.sentence(nb_words=6),
            **kwargs
        )
    
    @staticmethod
    def create_pagerduty_alert_data(
        alert_name: str = "TestIncident",
        alert_source: str = "pagerduty",
        event_type: str = "incident.triggered",
        urgency: str = "high",
        description: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate PagerDuty-style alert payload for testing."""
        return create_pagerduty_alert_data(
            alert_name=alert_name,
            alert_source=alert_source,
            event_type=event_type,
            urgency=urgency,
            description=description or fake.sentence(),
            **kwargs
        )
    
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
    def create_powershell_task_data(
        title: str = None,
        description: str = None,
        script: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate PowerShell task data for testing."""
        return {
            "title": title or f"PowerShell Task {int(datetime.now().timestamp())}",
            "description": description or fake.sentence(),
            "script": script or "Write-Host 'Hello from PowerShell'",
            "script_type": "powershell",
            "tags": tags or ["test", "powershell"],
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


def create_powershell_task(title: str = "PowerShell Test Task") -> Dict[str, Any]:
    """Create a PowerShell task."""
    return {
        "title": title,
        "description": "A PowerShell test task",
        "script": "Write-Host 'Hello from PowerShell'",
        "script_type": "powershell",
        "tags": ["powershell", "test"],
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


def create_grafana_alert_data(
    alert_name: str = "TestAlert",
    alert_source: str = "grafana",
    status: str = "firing",
    severity: str = "warning",
    description: str = "Test alert description",
    summary: str = "Test alert summary",
    instance: str = "test-instance",
    job: str = "test-job"
) -> Dict[str, Any]:
    """Create a Grafana-style alert payload for testing.
    
    Args:
        alert_name: Name of the alert
        alert_source: Source system (e.g., "grafana", "pagerduty")
        status: Alert status ("firing" or "resolved")
        severity: Alert severity (e.g., "critical", "warning", "info")
        description: Alert description
        summary: Alert summary
        instance: Instance identifier
        job: Job identifier
    
    Returns:
        Dict containing Grafana alert webhook payload
    """
    import time
    timestamp = time.time()
    
    return {
        "receiver": "Test_Alert_Endpoint",
        "status": status,
        "alerts": [
            {
                "status": status,
                "labels": {
                    "alertname": alert_name,
                    "grafana_folder": "test_folder",
                    "instance": instance,
                    "job": job,
                    "severity": severity
                },
                "annotations": {
                    "description": description,
                    "summary": summary
                },
                "startsAt": f"{int(timestamp)}",
                "endsAt": "0" if status == "firing" else f"{int(timestamp + 300)}",
                "generatorURL": f"http://localhost:3000/grafana/alerting/{alert_name}",
                "fingerprint": f"test{int(timestamp)}",
                "values": {
                    "A": 1
                },
                "valueString": f"[var='A' labels={{__name__={alert_name}}} value=1]"
            }
        ],
        "groupLabels": {
            "alertname": alert_name,
            "grafana_folder": "test_folder"
        },
        "commonLabels": {
            "alertname": alert_name,
            "grafana_folder": "test_folder",
            "instance": instance,
            "job": job,
            "severity": severity
        },
        "commonAnnotations": {
            "description": description,
            "summary": summary
        },
        "externalURL": "http://localhost:3000/grafana/",
        "version": "1",
        "title": f"[{status.upper()}:1] {alert_name}",
        "state": "alerting" if status == "firing" else "resolved",
        "message": f"**{status}**\n\nAlert: {alert_name}\nDescription: {description}"
    }


def create_pagerduty_alert_data(
    alert_name: str = "TestIncident",
    alert_source: str = "pagerduty",
    event_type: str = "incident.triggered",
    urgency: str = "high",
    description: str = "Test incident description"
) -> Dict[str, Any]:
    """Create a PagerDuty-style alert payload for testing.
    
    Args:
        alert_name: Name/title of the incident
        alert_source: Source system (usually "pagerduty")
        event_type: PagerDuty event type (e.g., "incident.triggered", "incident.resolved")
        urgency: Incident urgency ("high" or "low")
        description: Incident description
    
    Returns:
        Dict containing PagerDuty webhook payload
    """
    import time
    timestamp = time.time()
    
    return {
        "event": {
            "id": f"event-test-{int(timestamp)}",
            "event_type": event_type,
            "occurred_at": f"{int(timestamp)}",
            "data": {
                "id": f"incident-test-{int(timestamp)}",
                "incident_key": alert_name,
                "type": "incident",
                "summary": alert_name,
                "description": description,
                "urgency": urgency,
                "status": "triggered" if event_type == "incident.triggered" else "resolved",
                "service": {
                    "id": "service-test",
                    "name": "Test Service",
                    "summary": "Test Service"
                },
                "priority": {
                    "id": "priority-test",
                    "name": "P1" if urgency == "high" else "P3",
                    "summary": "High Priority" if urgency == "high" else "Low Priority"
                },
                "created_at": f"{int(timestamp)}",
                "html_url": f"https://test.pagerduty.com/incidents/test-{int(timestamp)}"
            }
        }
    }

