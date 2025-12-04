"""
Test cleanup utilities for managing test resources.
"""

import logging
from typing import List, Dict, Any, Callable

logger = logging.getLogger(__name__)


class TestCleanup:
    """Tracks and cleans up test resources."""
    
    def __init__(self):
        self.resources: List[Dict[str, Any]] = []
    
    def track(
        self,
        resource_type: str,
        resource_id: str,
        cleanup_func: Callable,
        metadata: Dict[str, Any] = None
    ):
        """
        Track a resource for cleanup.
        
        Args:
            resource_type: Type of resource (e.g., 'task', 'user', 'tenant')
            resource_id: Unique identifier for the resource
            cleanup_func: Function to call for cleanup
            metadata: Optional additional metadata
        """
        self.resources.append({
            'type': resource_type,
            'id': resource_id,
            'cleanup_func': cleanup_func,
            'metadata': metadata or {},
        })
        logger.debug(f"Tracking {resource_type} {resource_id} for cleanup")
    
    def cleanup_all(self):
        """Clean up all tracked resources in reverse order."""
        if not self.resources:
            logger.debug("No resources to cleanup")
            return
        
        logger.info(f"Cleaning up {len(self.resources)} resources...")
        
        # Cleanup in reverse order (LIFO)
        for resource in reversed(self.resources):
            try:
                logger.debug(
                    f"Cleaning up {resource['type']} {resource['id']}"
                )
                resource['cleanup_func']()
                logger.debug(
                    f"Successfully cleaned up {resource['type']} {resource['id']}"
                )
            except Exception as e:
                logger.warning(
                    f"Failed to cleanup {resource['type']} {resource['id']}: {e}"
                )
        
        self.resources.clear()
        logger.info("Cleanup complete")
    
    def cleanup_by_type(self, resource_type: str):
        """Clean up all resources of a specific type."""
        resources_to_cleanup = [
            r for r in self.resources if r['type'] == resource_type
        ]
        
        for resource in reversed(resources_to_cleanup):
            try:
                resource['cleanup_func']()
                self.resources.remove(resource)
            except Exception as e:
                logger.warning(
                    f"Failed to cleanup {resource['type']} {resource['id']}: {e}"
                )
    
    def get_tracked_resources(self, resource_type: str = None) -> List[Dict[str, Any]]:
        """Get list of tracked resources, optionally filtered by type."""
        if resource_type:
            return [r for r in self.resources if r['type'] == resource_type]
        return self.resources.copy()

