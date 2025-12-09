"""
Test user configurations for E2E tests.

Defines the test user for E2E testing.
"""

import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class TestUser:
    """Test user configuration."""
    
    email: str
    password: str
    org: str
    role: str
    first_name: str = ""
    last_name: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API payloads."""
        return {
            "email": self.email,
            "password": self.password,
            "org": self.org,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


# Test user (Admin role)
# Email: yash+user@dagknows.com
# Password: 1Hey2Yash*
# Org: dagknows
ADMIN_USER = TestUser(
    email=os.getenv("TEST_USER_EMAIL", "yash+user@dagknows.com"),
    password=os.getenv("TEST_USER_PASSWORD", "1Hey2Yash*"),
    org=os.getenv("TEST_ORG", "dagknows"),
    role="Admin",
    first_name="Yash",
    last_name="User"
)


def get_test_user(role: str = "Admin") -> TestUser:
    """
    Get test user.
    
    Args:
        role: User role (currently only Admin is configured)
        
    Returns:
        TestUser instance
    """
    return ADMIN_USER

