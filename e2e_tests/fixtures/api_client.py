"""
API Client for E2E tests.

Provides high-level API client matching how the frontend calls backend services.
"""

import logging
import time
from typing import Dict, Any, Optional, List
import requests
from config.env import config

logger = logging.getLogger(__name__)


class DagKnowsAPIClient:
    """
    High-level API client for DagKnows E2E tests.
    
    This client matches how the frontend (dagknows_nuxt) calls backend APIs.
    """
    
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL (defaults to config)
            token: JWT token (defaults to config)
        """
        self.base_url = base_url or config.BASE_URL
        self.token = token or config.JWT_TOKEN
        self.proxy_param = config.PROXY_PARAM
        self.session = requests.Session()
        self.session.headers.update(config.get_auth_headers())
        
    def _get_url(self, endpoint: str, with_proxy: bool = True) -> str:
        """Get full URL with optional proxy parameter."""
        base = self.base_url.rstrip('/')
        endpoint = endpoint.lstrip('/')
        
        if with_proxy and self.proxy_param:
            separator = '&' if '?' in endpoint else self.proxy_param
            return f"{base}/{endpoint}{separator}"
        else:
            return f"{base}/{endpoint}"
    
    def _request(
        self,
        method: str,
        endpoint: str,
        with_proxy: bool = True,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request."""
        url = self._get_url(endpoint, with_proxy=with_proxy)
        logger.debug(f"{method.upper()} {url}")
        
        response = self.session.request(method, url, **kwargs)
        
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            logger.error(f"Response: {response.text[:500]}")
            raise
        
        return response
    
    # ==================== TASK OPERATIONS ====================
    
    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new task (matches frontend behavior).
        
        Args:
            task_data: Task data dictionary
            
        Returns:
            Created task response
        """
        payload = {"task": task_data}
        response = self._request("POST", "/api/v1/tasks/", json=payload)
        return response.json()
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task by ID."""
        response = self._request("GET", f"/api/v1/tasks/{task_id}")
        return response.json()
    
    def update_task(
        self,
        task_id: str,
        task_data: Dict[str, Any],
        update_mask: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update task (matches frontend behavior - sends full object + update_mask).
        
        Args:
            task_id: Task ID
            task_data: Full task object (like frontend sends)
            update_mask: List of fields being updated
            
        Returns:
            Updated task response
        """
        payload = {
            "task": task_data,
            "update_mask": update_mask or []
        }
        response = self._request("PATCH", f"/api/v1/tasks/{task_id}", json=payload)
        return response.json()
    
    def delete_task(self, task_id: str, wsid: str = "__DEFAULT__") -> Optional[Dict[str, Any]]:
        """
        Delete task (matches frontend behavior).
        
        Args:
            task_id: Task ID
            wsid: Workspace ID
            
        Returns:
            Delete response or None
        """
        try:
            response = self._request(
                "DELETE",
                f"/api/v1/tasks/{task_id}",
                params={"wsid": wsid}
            )
            return response.json() if response.text else {}
        except requests.HTTPError as e:
            if e.response.status_code == 500:
                logger.warning(f"DELETE returned 500 (known backend issue), ignoring")
                return None
            raise
    
    def list_tasks(
        self,
        page_size: int = 20,
        page_key: Optional[str] = None,
        query: Optional[str] = None,
        **filters
    ) -> Dict[str, Any]:
        """
        List tasks (matches frontend list/search behavior).
        
        Args:
            page_size: Number of tasks per page
            page_key: Pagination key
            query: Search query (uses KNN search)
            **filters: Additional filters (tags, etc.)
            
        Returns:
            List response with tasks
        """
        params = {"page_size": page_size}
        if page_key:
            params["page_key"] = page_key
        if query:
            params["q"] = query  # KNN search like UI does
        params.update(filters)
        
        response = self._request("GET", "/api/v1/tasks/", params=params)
        return response.json()
    
    # ==================== ALERT OPERATIONS ====================
    
    def process_alert(self, alert_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send alert to processAlert endpoint.
        
        Args:
            alert_payload: Grafana or PagerDuty alert payload
            
        Returns:
            Alert processing response
        """
        url = config.get_process_alert_url()
        logger.info(f"Processing alert via {url}")
        
        response = self.session.post(
            url,
            json=alert_payload,
            headers=config.get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def search_alerts(self, **params) -> Dict[str, Any]:
        """Search alerts."""
        response = self._request("GET", "/api/alerts", params=params)
        return response.json()
    
    def get_alert(self, alert_id: str) -> Dict[str, Any]:
        """Get alert by ID."""
        response = self._request("GET", f"/api/alerts/{alert_id}")
        return response.json()
    
    # ==================== JOB OPERATIONS ====================
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get job execution status.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job status response
        """
        response = self._request("GET", f"/api/v1/jobs/{job_id}")
        return response.json()
    
    def wait_for_job_completion(
        self,
        job_id: str,
        timeout: int = 60,
        poll_interval: int = 2
    ) -> Dict[str, Any]:
        """
        Wait for job to complete.
        
        Args:
            job_id: Job ID
            timeout: Max wait time in seconds
            poll_interval: Polling interval in seconds
            
        Returns:
            Final job status
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_job_status(job_id)
            state = status.get("status", "").upper()
            
            if state in ["COMPLETED", "FAILED", "SUCCESS"]:
                logger.info(f"Job {job_id} finished with state: {state}")
                return status
            
            logger.debug(f"Job {job_id} status: {state}, waiting...")
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")
    
    # ==================== WORKSPACE OPERATIONS ====================
    
    def list_workspaces(self) -> List[Dict[str, Any]]:
        """List user's workspaces."""
        response = self._request("GET", "/api/workspaces")
        return response.json().get("workspaces", [])
    
    # ==================== SETTINGS OPERATIONS ====================
    
    def get_admin_settings(self) -> Dict[str, Any]:
        """Get admin settings."""
        response = self._request("POST", "/getSettings", json={}, with_proxy=True)
        return response.json()
    
    def set_incident_response_mode(self, mode: str) -> Dict[str, Any]:
        """
        Set incident response mode.
        
        Args:
            mode: One of 'deterministic', 'ai_selected', 'autonomous'
            
        Returns:
            Response from setFlags API
        """
        payload = {"incident_response_mode": mode}
        response = self._request("POST", "/setFlags", json=payload, with_proxy=True)
        return response.json()
    
    # ==================== AI/CHAT OPERATIONS ====================
    
    def start_chat_session(self, prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Start AI chat session.
        
        Args:
            prompt: Initial prompt
            context: Optional context for chat
            
        Returns:
            Chat session response
        """
        payload = {
            "prompt": prompt,
            "context": context or {}
        }
        response = self._request("POST", "/api/chat/start", json=payload)
        return response.json()
    
    def send_chat_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Send message in existing chat session.
        
        Args:
            session_id: Chat session ID
            message: Message to send
            
        Returns:
            AI response
        """
        payload = {
            "session_id": session_id,
            "message": message
        }
        response = self._request("POST", "/api/chat/message", json=payload)
        return response.json()


# Factory function
def create_api_client(
    base_url: Optional[str] = None,
    token: Optional[str] = None
) -> DagKnowsAPIClient:
    """
    Create API client instance.
    
    Args:
        base_url: Base URL (defaults to config)
        token: JWT token (defaults to config)
        
    Returns:
        DagKnowsAPIClient instance
    """
    return DagKnowsAPIClient(base_url=base_url, token=token)

