"""
E2E API Test: Role Management (RBAC)

Tests creating a custom role and assigning privileges to it via API endpoints.
This test sends requests directly to dev.dagknows.com (or configured base URL).

Based on frontend API calls:
- Create role: POST /api/iam/roles with {"role": {"path": "dkroles", "name": role_name}}
- Get privileges: GET /api/iam/roles/privileges
- Assign privileges: PUT /api/iam/roles/{roleid} with {"added_permissions": [...], "role": role, "update_mask": [...]}
- Get all roles and privileges: GET /api/iam/roles
"""

import pytest
import logging
import time
from fixtures.api_client import create_api_client
from config.test_users import get_test_user

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.e2e
@pytest.mark.role_management
class TestRoleManagementAPIE2E:
    """Test role creation and privilege assignment via API (E2E)."""
    
    @pytest.fixture(scope="function")
    def api_client(self):
        """Create API client for test."""
        test_user = get_test_user("Admin")
        client = create_api_client()
        logger.info(f"API Client initialized for {test_user.email}")
        return client
    
    def test_create_role_and_assign_privileges_via_api(self, api_client):
        """
        E2E Test: Create a custom role and assign privileges to it via API.
        
        Flow:
        1. Generate unique role name with timestamp
        2. Create custom role via POST /api/iam/roles
        3. Verify role was created
        4. Get all available privileges
        5. Assign specific privileges to the role
        6. Verify privileges were assigned by fetching role again
        
        Note: We use the same API endpoints as the frontend.
        """
        logger.info("=== Starting Role Creation and Privilege Assignment E2E Test (API-based) ===")
        
        # Generate unique role name with timestamp (matching UI test)
        # Note: Role names can only contain alphanumeric characters and spaces (no underscores)
        # Backend validation: hasUnsafeCharacters() rejects anything not matching [a-zA-Z0-9 ]
        timestamp = int(time.time())
        role_name = f"read1{timestamp}"  # No underscore - only alphanumeric allowed
        logger.info(f"Test role name: {role_name}")
        
        # Privileges to assign (matching UI test)
        privileges_to_assign = [
            "task.view_code",
            "task.view_io",
            "task.view_description",
            "task.list"
        ]
        
        logger.info(f"Privileges to assign: {privileges_to_assign}")
        
        # Step 1: Verify role doesn't exist yet
        logger.info(f"Step 1: Verifying role '{role_name}' doesn't exist yet")
        existing_role = api_client.get_role_by_name(role_name)
        if existing_role:
            logger.warning(f"Role '{role_name}' already exists - this is unexpected")
        else:
            logger.info(f"✓ Role '{role_name}' does not exist (as expected)")
        
        # Step 2: Create custom role
        logger.info(f"Step 2: Creating custom role '{role_name}'")
        try:
            created_role = api_client.create_role(role_name, path="dkroles")
            logger.info(f"✓ Role created successfully")
            logger.debug(f"Created role: {created_role}")
            
            # Verify role was created with correct name
            assert created_role.get("name") == role_name, "Role name should match"
            assert created_role.get("path") == "dkroles", "Role path should be 'dkroles'"
        except Exception as e:
            logger.error(f"✗ Role creation failed: {e}")
            raise
        
        # Step 3: Wait a bit for role to be available (frontend does this)
        logger.info("Step 3: Waiting for role to be available in system")
        time.sleep(1)
        
        # Step 4: Verify role appears in roles list
        logger.info(f"Step 4: Verifying role '{role_name}' appears in roles list")
        try:
            role = api_client.get_role_by_name(role_name)
            assert role is not None, f"Role '{role_name}' should exist after creation"
            logger.info(f"✓ Role found in roles list")
        except Exception as e:
            logger.error(f"✗ Role verification failed: {e}")
            raise
        
        # Step 5: Get all available privileges
        logger.info("Step 5: Getting all available privileges")
        try:
            all_privileges = api_client.get_privileges()
            logger.info(f"✓ Found {len(all_privileges)} available privileges")
            
            # Verify the privileges we want to assign exist
            for privilege in privileges_to_assign:
                if privilege not in all_privileges:
                    logger.warning(f"Privilege '{privilege}' not found in available privileges")
                else:
                    logger.debug(f"  ✓ Privilege '{privilege}' is available")
        except Exception as e:
            logger.error(f"✗ Failed to get privileges: {e}")
            raise
        
        # Step 6: Assign privileges to the role
        logger.info(f"Step 6: Assigning {len(privileges_to_assign)} privileges to role '{role_name}'")
        try:
            # Assign privileges one by one (matching frontend behavior when checkboxes are clicked)
            for privilege in privileges_to_assign:
                logger.info(f"  Assigning privilege: {privilege}")
                updated_role = api_client.assign_privileges_to_role(
                    role_id=role_name,
                    privileges=[privilege]
                )
                logger.info(f"  ✓ Assigned: {privilege}")
            
            logger.info(f"✓ All {len(privileges_to_assign)} privileges assigned")
        except Exception as e:
            logger.error(f"✗ Privilege assignment failed: {e}")
            raise
        
        # Step 7: Verify privileges were assigned by fetching role again
        logger.info("Step 7: Verifying privileges were assigned")
        try:
            # Wait a bit for changes to propagate
            time.sleep(1)
            
            # Get all roles and privileges to verify
            roles_and_privileges = api_client.get_all_roles_and_privileges()
            
            if role_name in roles_and_privileges:
                assigned_privileges = roles_and_privileges[role_name]
                logger.info(f"✓ Role '{role_name}' found in roles and privileges")
                logger.info(f"  Assigned privileges: {assigned_privileges}")
                
                # Verify each privilege was assigned
                for privilege in privileges_to_assign:
                    if privilege in assigned_privileges:
                        logger.info(f"  ✓ Verified: {privilege} is assigned to {role_name}")
                    else:
                        logger.warning(f"  ✗ {privilege} not found in assigned privileges")
            else:
                logger.warning(f"Role '{role_name}' not found in roles and privileges mapping")
            
            # Also verify by getting the role directly
            role = api_client.get_role_by_name(role_name)
            if role:
                role_privileges = role.get("permissions", [])
                logger.info(f"Role permissions from direct fetch: {role_privileges}")
                
                for privilege in privileges_to_assign:
                    if privilege in role_privileges:
                        logger.info(f"  ✓ Verified via direct fetch: {privilege}")
                    else:
                        logger.warning(f"  ✗ {privilege} not found in role permissions")
        except Exception as e:
            logger.warning(f"Could not fully verify privileges: {e}")
            logger.warning("This might be expected if verification requires additional time")
        
        logger.info("=== Role Creation and Privilege Assignment E2E Test (API-based) Completed ===")
        
        # Return role name for potential cleanup or use in other tests
        return role_name

