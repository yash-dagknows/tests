"""
API Client utilities for testing DagKnows services.

Provides convenient wrappers around HTTP/gRPC calls to services.
"""

import requests
import json
import logging
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class APIClient:
    """Base API client for making HTTP requests to services."""
    
    def __init__(self, base_url: str, test_mode: bool = True):
        self.base_url = base_url.rstrip('/')
        self.test_mode = test_mode
        self.session = requests.Session()
        self.auth_token = None
        self.user_info = None
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        
        if test_mode:
            # In test mode, we can bypass authentication
            self.session.headers.update({
                'X-Test-Mode': 'true',
            })
    
    def set_auth_token(self, token: str):
        """Set authentication token for requests."""
        self.auth_token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def set_user_info(self, user_info: Dict[str, Any]):
        """Set user info header for test requests."""
        self.user_info = user_info
        if self.test_mode:
            # In test mode, we can pass user info via header
            self.session.headers.update({
                'X-DagKnows-User-Info': json.dumps(user_info)
            })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request to the service."""
        url = urljoin(f"{self.base_url}/", endpoint.lstrip('/'))
        
        logger.debug(f"{method} {url}")
        if json_data:
            logger.debug(f"Request body: {json.dumps(json_data, indent=2)}")
        
        response = self.session.request(
            method=method,
            url=url,
            json=json_data,
            params=params,
            timeout=30,
            **kwargs
        )
        
        logger.debug(f"Response status: {response.status_code}")
        if response.text:
            try:
                logger.debug(f"Response body: {json.dumps(response.json(), indent=2)}")
            except:
                logger.debug(f"Response body: {response.text[:500]}")
        
        return response
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Dict:
        """Make GET request."""
        response = self._make_request('GET', endpoint, params=params, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, json_data: Dict, **kwargs) -> Dict:
        """Make POST request."""
        response = self._make_request('POST', endpoint, json_data=json_data, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def put(self, endpoint: str, json_data: Dict, **kwargs) -> Dict:
        """Make PUT request."""
        response = self._make_request('PUT', endpoint, json_data=json_data, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def patch(self, endpoint: str, json_data: Dict, **kwargs) -> Dict:
        """Make PATCH request."""
        response = self._make_request('PATCH', endpoint, json_data=json_data, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def delete(self, endpoint: str, **kwargs) -> Dict:
        """Make DELETE request."""
        response = self._make_request('DELETE', endpoint, **kwargs)
        response.raise_for_status()
        if response.text:
            return response.json()
        return {}


class TaskServiceClient(APIClient):
    """Client for TaskService API."""
    
    def __init__(self, base_url: str = "http://localhost:2235", test_mode: bool = True):
        super().__init__(base_url, test_mode)
        self.api_base = "/api/v1"
    
    # ========================================
    # Task Operations
    # ========================================
    
    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task."""
        return self.post(f"{self.api_base}/tasks", task_data)
    
    def get_task(self, task_id: str) -> Dict:
        """Get task by ID."""
        return self.get(f"{self.api_base}/tasks/{task_id}")
    
    def update_task(self, task_id: str, updates: Dict, update_fields: List[str] = None) -> Dict:
        """Update a task."""
        payload = updates.copy()
        if update_fields:
            payload['update_fields'] = update_fields
        return self.patch(f"{self.api_base}/tasks/{task_id}", payload)
    
    def delete_task(self, task_id: str) -> Dict:
        """Delete a task."""
        return self.delete(f"{self.api_base}/tasks/{task_id}")
    
    def list_tasks(self, params: Optional[Dict] = None) -> Dict:
        """List tasks with optional filters."""
        return self.get(f"{self.api_base}/tasks", params=params)
    
    def search_tasks(self, query: str, params: Optional[Dict] = None) -> Dict:
        """Search tasks."""
        search_params = params or {}
        search_params['q'] = query
        return self.get(f"{self.api_base}/tasks/search", params=search_params)
    
    # ========================================
    # Workspace Operations
    # ========================================
    
    def create_workspace(self, workspace_data: Dict) -> Dict:
        """Create a new workspace."""
        return self.post(f"{self.api_base}/workspaces", workspace_data)
    
    def get_workspace(self, workspace_id: str) -> Dict:
        """Get workspace by ID."""
        return self.get(f"{self.api_base}/workspaces/{workspace_id}")
    
    def update_workspace(self, workspace_id: str, updates: Dict) -> Dict:
        """Update a workspace."""
        return self.patch(f"{self.api_base}/workspaces/{workspace_id}", updates)
    
    def delete_workspace(self, workspace_id: str) -> Dict:
        """Delete a workspace."""
        return self.delete(f"{self.api_base}/workspaces/{workspace_id}")
    
    def list_workspaces(self, params: Optional[Dict] = None) -> Dict:
        """List workspaces."""
        return self.get(f"{self.api_base}/workspaces", params=params)
    
    # ========================================
    # Role & Permission Operations
    # ========================================
    
    def create_role(self, role_data: Dict) -> Dict:
        """Create a new role."""
        return self.post(f"{self.api_base}/iam/roles", role_data)
    
    def get_role(self, role_name: str) -> Dict:
        """Get role by name."""
        return self.get(f"{self.api_base}/iam/roles/{role_name}")
    
    def assign_role(self, user_id: str, role_name: str, resource_type: str, resource_id: str) -> Dict:
        """Assign role to user for a resource."""
        payload = {
            "user_id": user_id,
            "role_name": role_name,
            "resource_type": resource_type,
            "resource_id": resource_id,
        }
        return self.post(f"{self.api_base}/iam/role-associations", payload)
    
    # ========================================
    # Job Operations
    # ========================================
    
    def create_job(self, job_data: Dict) -> Dict:
        """Create a new job."""
        return self.post(f"{self.api_base}/jobs", job_data)
    
    def get_job(self, job_id: str) -> Dict:
        """Get job by ID."""
        return self.get(f"{self.api_base}/jobs/{job_id}")
    
    def list_jobs(self, params: Optional[Dict] = None) -> Dict:
        """List jobs."""
        return self.get(f"{self.api_base}/jobs", params=params)
    
    # ========================================
    # Stats Operations
    # ========================================
    
    def get_task_stats(self, params: Optional[Dict] = None) -> Dict:
        """Get task statistics."""
        return self.get(f"{self.api_base}/stats/tasks", params=params)
    
    def get_workspace_stats(self, workspace_id: str) -> Dict:
        """Get workspace statistics."""
        return self.get(f"{self.api_base}/stats/workspaces/{workspace_id}")


class ReqRouterClient(APIClient):
    """Client for ReqRouter API."""
    
    def __init__(self, base_url: str = "http://localhost:8888", test_mode: bool = True):
        super().__init__(base_url, test_mode)
    
    # ========================================
    # Authentication
    # ========================================
    
    def login(self, email: str, password: str) -> str:
        """Login and get authentication token."""
        response = self.post('/api/signin', {
            'email': email,
            'password': password
        })
        return response.get('access_token') or response.get('token')
    
    def logout(self) -> Dict:
        """Logout current user."""
        return self.post('/api/signout', {})
    
    # ========================================
    # Tenant Management
    # ========================================
    
    def create_tenant(self, tenant_data: Dict) -> Dict:
        """
        Create a new tenant.
        
        Args:
            tenant_data: Dict with keys: email, first_name, last_name, organization, password
        """
        return self.post('/add_tenant_register', tenant_data)
    
    def delete_tenant(self, tenant_id: str) -> Dict:
        """Delete a tenant (admin only)."""
        return self.delete(f'/api/tenants/{tenant_id}')
    
    # ========================================
    # User Management
    # ========================================
    
    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user."""
        return self.post('/api/users', user_data)
    
    def get_user(self, user_id: str) -> Dict:
        """Get user by ID."""
        return self.get(f'/api/users/{user_id}')
    
    def update_user(self, user_id: str, updates: Dict) -> Dict:
        """Update user."""
        return self.patch(f'/api/users/{user_id}', updates)
    
    def delete_user(self, user_id: str) -> Dict:
        """Delete user."""
        return self.delete(f'/api/users/{user_id}')
    
    def list_users(self, params: Optional[Dict] = None) -> Dict:
        """List users."""
        return self.get('/api/users', params=params)
    
    # ========================================
    # Task Operations (proxied to TaskService)
    # ========================================
    
    def create_task(self, task_data: Dict) -> Dict:
        """Create a task (proxied to TaskService)."""
        return self.post('/api/tasks', task_data)
    
    def get_task(self, task_id: str) -> Dict:
        """Get task (proxied to TaskService)."""
        return self.get(f'/api/tasks/{task_id}')
    
    def update_task(self, task_id: str, updates: Dict) -> Dict:
        """Update task (proxied to TaskService)."""
        return self.patch(f'/api/tasks/{task_id}', updates)
    
    def delete_task(self, task_id: str) -> Dict:
        """Delete task (proxied to TaskService)."""
        return self.delete(f'/api/tasks/{task_id}')
    
    def search_tasks(self, query: str) -> Dict:
        """Search tasks (proxied to TaskService)."""
        return self.get('/api/tasks/search', params={'q': query})
    
    # ========================================
    # Health Check
    # ========================================
    
    def health(self) -> Dict:
        """Check service health."""
        return self.get('/health')


# Backward compatibility aliases
class Client(TaskServiceClient):
    """Alias for TaskServiceClient for backward compatibility."""
    pass

