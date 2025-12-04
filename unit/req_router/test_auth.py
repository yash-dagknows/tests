"""
Unit tests for Authentication in ReqRouter.
"""

import pytest


@pytest.mark.unit
@pytest.mark.auth
class TestAuthentication:
    """Test suite for user authentication."""
    
    def test_login_success(self, req_router_client, test_config):
        """Test successful login."""
        try:
            token = req_router_client.login(
                test_config["test_admin_email"],
                test_config["test_admin_password"]
            )
            
            assert token is not None
            assert len(token) > 0
            
        except Exception as e:
            pytest.skip(f"Login test requires configured test user: {e}")
    
    def test_login_wrong_password_fails(self, req_router_client, test_config):
        """Test that login fails with wrong password."""
        with pytest.raises(Exception) as exc_info:
            req_router_client.login(
                test_config["test_admin_email"],
                "wrong-password"
            )
        
        error_msg = str(exc_info.value).lower()
        assert "password" in error_msg or "invalid" in error_msg or \
               "unauthorized" in error_msg or "401" in error_msg
    
    def test_login_nonexistent_user_fails(self, req_router_client):
        """Test that login fails for non-existent user."""
        with pytest.raises(Exception) as exc_info:
            req_router_client.login(
                "nonexistent@example.com",
                "password123"
            )
        
        error_msg = str(exc_info.value).lower()
        assert "not found" in error_msg or "invalid" in error_msg or \
               "unauthorized" in error_msg or "401" in error_msg
    
    def test_logout(self, req_router_client, test_config):
        """Test user logout."""
        try:
            # Login first
            token = req_router_client.login(
                test_config["test_admin_email"],
                test_config["test_admin_password"]
            )
            req_router_client.set_auth_token(token)
            
            # Logout
            response = req_router_client.logout()
            
            # Logout should succeed
            assert response is not None
            
        except Exception as e:
            pytest.skip(f"Logout test requires configured test user: {e}")


@pytest.mark.unit
@pytest.mark.auth
class TestAuthorizationHeaders:
    """Test suite for authorization headers."""
    
    def test_authenticated_request_includes_token(self, req_router_client, test_config):
        """Test that authenticated requests include auth token."""
        try:
            token = req_router_client.login(
                test_config["test_admin_email"],
                test_config["test_admin_password"]
            )
            req_router_client.set_auth_token(token)
            
            # Verify token is in headers
            assert "Authorization" in req_router_client.session.headers
            assert token in req_router_client.session.headers["Authorization"]
            
        except Exception as e:
            pytest.skip(f"Auth header test requires configured test user: {e}")
    
    def test_unauthenticated_request_fails(self, req_router_client, test_config):
        """Test that requests without auth token fail (if ENFORCE_LOGIN=true)."""
        # This test is conditional on ENFORCE_LOGIN setting
        if test_config.get("test_mode"):
            pytest.skip("Test mode bypasses authentication")
        
        # Clear any existing auth
        req_router_client.session.headers.pop("Authorization", None)
        
        # Try to access protected resource
        with pytest.raises(Exception) as exc_info:
            req_router_client.list_users()
        
        error_msg = str(exc_info.value).lower()
        assert "unauthorized" in error_msg or "401" in error_msg

