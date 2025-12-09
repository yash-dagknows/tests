"""
Environment configuration for E2E tests.

Loads configuration from environment variables or .env file.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    """Test environment configuration."""
    
    # Base URLs
    BASE_URL: str = os.getenv("DAGKNOWS_URL", "https://dev.dagknows.com")
    
    # Authentication
    JWT_TOKEN: str = os.getenv(
        "DAGKNOWS_TOKEN",
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkYWdrbm93cy5jb20iLCJzdWIiOiJ5YXNoQGRhZ2tub3dzLmNvbSIsIm5iZiI6MTc2MTE0NjUxMSwiZXhwIjoxNzkyNjgyNjkxLCJqdGkiOiJZMENWR055N01CQzlKYjNQIiwiYXVkIjoiZGFna25vd3MiLCJyb2xlIjoiYWRtaW4iLCJ1c2VyX2NsYWltcyI6eyJ1aWQiOiIzOSIsInVuYW1lIjoieWFzaEBkYWdrbm93cy5jb20iLCJvcmciOiJkYWdrbm93cyIsImZpcnN0X25hbWUiOiJZYXNoIiwibGFzdF9uYW1lIjoiWWFkYXYiLCJyb2xlIjoiQWRtaW4iLCJhZXNfa2V5IjoiY1Q0RTU2aWxDOTlVXG4tcTZ1dlRBcU15VTBwMEFcbnFJWSIsIm9mc3QiOlszNzIsMTUwLDM0Miw0MzEsMTg3LDM5MSwzOTAsMTc0LDIzMywyNzksMjQ2LDQzNiw5MSw0MjYsMjU3LDIxNiwxNzEsMzMzLDExOCwzNjMsMjc0LDE1MiwzNzEsNDM2LDEzNiwyMjAsMTI3LDY3LDQyNSwzNzMsNDM5LDMyMF19fQ.IvHXxMMm4th-jm7IyektCTW3SXxlq4olv6gByzAliuFk1y2zbr91QBY_zdifz5_KnYNk4ruVr9xLrlahC3h7rGJaFU98OiiiLAQ49CFxgUO2iqyr6XcT3GgO5ptobTtOZNV4rmrPE_6hnjPRImernp5M6FhHhCZWktL9xQqZs9N9m2az1Jk-mi0yZLaNIA25pHWcqgdiF1xCbt5STWqFG2nmt1eq7x-FXnoryEqo1HvfOg74crBcubFORpTZ5AhNRpSdqemcpDd_6t0UliPuAg3VlwIedew9RBRvytr2j9GbBC_jgCh7YJ5oQqFjVItolhSMzuKHLRRHZib8Ikz6fA"
    )
    
    # Test User Credentials (for UI login)
    TEST_USER_EMAIL: str = os.getenv("TEST_USER_EMAIL", "yash+user@dagknows.com")
    TEST_USER_PASSWORD: str = os.getenv("TEST_USER_PASSWORD", "1Hey2Yash*")
    TEST_ORG: str = os.getenv("TEST_ORG", "dagknows")
    
    # Proxy parameter (critical for dev.dagknows.com)
    PROXY_PARAM: str = os.getenv("DAGKNOWS_PROXY", "?proxy=dev1")
    
    # Timeouts
    DEFAULT_TIMEOUT: int = int(os.getenv("TEST_TIMEOUT", "30"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    
    # Test data
    TEST_WORKSPACE: str = os.getenv("TEST_WORKSPACE", "__DEFAULT__")
    
    @classmethod
    def get_api_url(cls, endpoint: str) -> str:
        """
        Get full API URL for an endpoint.
        
        Args:
            endpoint: API endpoint path (e.g., "/api/v1/tasks")
            
        Returns:
            Full URL with proxy parameter if needed
        """
        base = cls.BASE_URL.rstrip('/')
        endpoint = endpoint.lstrip('/')
        
        if cls.PROXY_PARAM:
            # Check if endpoint already has query params
            separator = '&' if '?' in endpoint else cls.PROXY_PARAM
            return f"{base}/{endpoint}{separator if cls.PROXY_PARAM.startswith('?') else cls.PROXY_PARAM}"
        else:
            return f"{base}/{endpoint}"
    
    @classmethod
    def get_process_alert_url(cls) -> str:
        """Get processAlert endpoint URL with proxy parameter."""
        return f"{cls.BASE_URL}/processAlert{cls.PROXY_PARAM}"
    
    @classmethod
    def get_auth_headers(cls) -> dict:
        """Get authentication headers for API requests."""
        return {
            "Authorization": f"Bearer {cls.JWT_TOKEN}",
            "Content-Type": "application/json"
        }
    
    @classmethod
    def is_dev_environment(cls) -> bool:
        """Check if running against dev.dagknows.com."""
        return "dev.dagknows.com" in cls.BASE_URL
    
    @classmethod
    def is_local_environment(cls) -> bool:
        """Check if running against localhost."""
        return "localhost" in cls.BASE_URL or "127.0.0.1" in cls.BASE_URL
    
    @classmethod
    def get_proxy_param_for_url(cls) -> str:
        """
        Get proxy parameter based on environment.
        
        Returns:
            Proxy parameter string (e.g., "?proxy=dev1", "?proxy=yashlocal")
        """
        if cls.is_local_environment():
            return "?proxy=yashlocal"  # Required for local
        elif cls.is_dev_environment():
            return "?proxy=dev1"  # Required for dev.dagknows.com
        else:
            return cls.PROXY_PARAM  # Use configured value


# Global config instance
config = Config()


# Convenience functions
def get_base_url() -> str:
    """Get base URL."""
    return config.BASE_URL


def get_jwt_token() -> str:
    """Get JWT token."""
    return config.JWT_TOKEN


def get_api_url(endpoint: str) -> str:
    """Get full API URL for endpoint."""
    return config.get_api_url(endpoint)


def get_auth_headers() -> dict:
    """Get auth headers."""
    return config.get_auth_headers()

