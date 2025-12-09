"""
Authentication helpers for E2E tests.

Provides reusable authentication functions for both API and UI tests.
"""

import logging
from typing import Dict, Any, Optional
import requests
from config.env import config
from config.test_users import TestUser, ADMIN_USER

logger = logging.getLogger(__name__)


class AuthHelper:
    """Helper class for authentication operations."""
    
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize auth helper.
        
        Args:
            base_url: Base URL (defaults to config)
            token: JWT token (defaults to config)
        """
        self.base_url = base_url or config.BASE_URL
        self.token = token or config.JWT_TOKEN
        self.session = requests.Session()
        
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary with Authorization header
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def login_via_api(self, user: TestUser) -> Dict[str, Any]:
        """
        Login via API endpoint (for API tests).
        
        Args:
            user: TestUser instance with credentials
            
        Returns:
            Response from sign-in API
        """
        url = f"{self.base_url}/user/sign-in"
        payload = {
            "email": user.email,
            "password": user.password,
            "org": user.org,
            "from_nuxt": 1
        }
        
        logger.info(f"Logging in user: {user.email}")
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        if data.get("responsecode") == "True":
            logger.info(f"✓ Login successful for {user.email}")
            # Extract token from response if available
            if "token" in data:
                self.token = data["token"]
        else:
            logger.error(f"✗ Login failed: {data.get('message')}")
            raise Exception(f"Login failed: {data.get('message')}")
        
        return data
    
    def verify_token(self) -> bool:
        """
        Verify JWT token is valid.
        
        Returns:
            True if token is valid, False otherwise
        """
        try:
            # Try a simple API call to verify token
            url = config.get_api_url("/api/v1/tasks/")
            headers = self.get_auth_headers()
            
            response = self.session.get(
                url, 
                headers=headers,
                params={"page_size": 1},
                timeout=10
            )
            
            return response.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return False
    
    def logout_via_api(self) -> None:
        """Logout via API (clears session)."""
        try:
            url = f"{self.base_url}/vlogout"
            self.session.get(url)
            logger.info("✓ Logout successful")
        except Exception as e:
            logger.warning(f"Logout failed: {e}")


# Singleton instance
_auth_helper = None


def get_auth_helper() -> AuthHelper:
    """
    Get singleton AuthHelper instance.
    
    Returns:
        AuthHelper instance
    """
    global _auth_helper
    if _auth_helper is None:
        _auth_helper = AuthHelper()
    return _auth_helper

