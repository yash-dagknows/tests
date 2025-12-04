"""
Custom assertion utilities for testing.
"""

from typing import Dict, Any, List
from deepdiff import DeepDiff


def assert_response_success(response: Dict, message: str = None):
    """Assert that API response indicates success."""
    msg = message or "Expected successful response"
    
    # Check various success indicators
    if 'success' in response:
        assert response['success'], f"{msg}: {response}"
    elif 'error' in response:
        assert not response['error'], f"{msg}: {response['error']}"
    elif 'status' in response:
        assert response['status'] in ['ok', 'success', 'created'], f"{msg}: {response}"


def assert_response_error(response: Dict, expected_error: str = None):
    """Assert that API response indicates an error."""
    assert 'error' in response or response.get('success') is False, \
        f"Expected error response but got: {response}"
    
    if expected_error:
        error_msg = response.get('error', '') or response.get('message', '')
        assert expected_error.lower() in error_msg.lower(), \
            f"Expected error containing '{expected_error}' but got: {error_msg}"


def assert_task_equals(actual: Dict, expected: Dict, ignore_fields: List[str] = None):
    """
    Assert that two tasks are equal, ignoring certain fields.
    
    Args:
        actual: The actual task data
        expected: The expected task data
        ignore_fields: List of field names to ignore in comparison
    """
    if ignore_fields is None:
        ignore_fields = [
            'id', 'created_at', 'updated_at', 'created_by', 
            'modified_by', 'version', '_index', '_id', '_source'
        ]
    
    # Create copies to avoid modifying originals
    actual_copy = actual.copy()
    expected_copy = expected.copy()
    
    # Remove ignored fields
    for field in ignore_fields:
        actual_copy.pop(field, None)
        expected_copy.pop(field, None)
    
    # Compare
    diff = DeepDiff(expected_copy, actual_copy, ignore_order=True)
    assert not diff, f"Tasks don't match:\n{diff}"


def assert_dict_contains(actual: Dict, expected_subset: Dict):
    """Assert that actual dict contains all key-value pairs from expected_subset."""
    for key, expected_value in expected_subset.items():
        assert key in actual, f"Key '{key}' not found in {actual.keys()}"
        actual_value = actual[key]
        
        if isinstance(expected_value, dict) and isinstance(actual_value, dict):
            assert_dict_contains(actual_value, expected_value)
        else:
            assert actual_value == expected_value, \
                f"Value mismatch for key '{key}': expected {expected_value}, got {actual_value}"


def assert_list_contains_item(items: List[Dict], expected_item: Dict, key_field: str = 'id'):
    """Assert that a list contains an item matching expected_item."""
    for item in items:
        if item.get(key_field) == expected_item.get(key_field):
            assert_dict_contains(item, expected_item)
            return
    
    raise AssertionError(
        f"List does not contain item with {key_field}={expected_item.get(key_field)}"
    )


def assert_valid_timestamp(timestamp_str: str):
    """Assert that a string is a valid ISO timestamp."""
    from datetime import datetime
    try:
        datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except (ValueError, AttributeError) as e:
        raise AssertionError(f"Invalid timestamp format: {timestamp_str}") from e


def assert_valid_uuid(uuid_str: str):
    """Assert that a string is a valid UUID."""
    import uuid
    try:
        uuid.UUID(uuid_str)
    except (ValueError, AttributeError) as e:
        raise AssertionError(f"Invalid UUID format: {uuid_str}") from e


def assert_has_required_fields(data: Dict, required_fields: List[str]):
    """Assert that data dict has all required fields."""
    missing_fields = [f for f in required_fields if f not in data]
    assert not missing_fields, \
        f"Missing required fields: {missing_fields}. Available fields: {list(data.keys())}"


def assert_permissions(user_info: Dict, required_permissions: List[str]):
    """Assert that user has all required permissions."""
    user_permissions = user_info.get('permissions', [])
    missing_perms = [p for p in required_permissions if p not in user_permissions]
    assert not missing_perms, \
        f"User missing permissions: {missing_perms}. Has: {user_permissions}"

