# Task Types Fix Summary

## Issue
Tests were creating tasks with invalid `script_type` values ("bash", "shell") that are not supported by the application. This caused tasks to not have their script_type properly selected in the UI.

## Supported Script Types

Based on the application code (`taskservice/src/service.py`), the **ONLY valid script types** are:

1. **`python`** - For Python scripts
2. **`powershell`** - For PowerShell scripts
3. **`command`** - For command-list tasks (uses `commands` array instead of `script` field)
4. **`script`** - Automatically converted to "python" by the backend

### NOT Supported:
- ❌ `bash` - Not a valid script_type
- ❌ `shell` - Not a valid script_type

## Changes Made

### 1. Test Data Factory (`tests/utils/fixtures.py`)

**Removed**:
- `create_shell_task_data()` - Invalid script_type
- `create_bash_task_data()` - Invalid script_type
- `create_bash_task()` convenience function

**Added**:
- `create_powershell_task_data()` - Creates PowerShell tasks
- `create_powershell_task()` convenience function

**Kept**:
- `create_python_task_data()` - For Python scripts ✅
- `create_task_with_commands()` - For command-type tasks ✅
- `create_python_task()` convenience function ✅
- `create_command_task()` convenience function ✅

### 2. Test Suite (`tests/unit/taskservice/test_task_crud.py`)

**Replaced**:
- `TestShellTaskCRUD` → `TestPowerShellTaskCRUD`
  - 3 tests for PowerShell tasks (create, get, update)

**Updated**:
- All imports now reference valid task types
- Documentation updated to reflect supported types
- All tests now create tasks with valid script_types

### 3. Test Structure

Now testing:
- ✅ **Python tasks** (script_type: "python") - 7 tests
- ✅ **PowerShell tasks** (script_type: "powershell") - 3 tests
- ✅ **Command tasks** (script_type: "command") - 7 tests
- ✅ General operations - 3 tests
- ✅ Parameters - 3 tests
- ✅ Tags - 4 tests

**Total: 27 tests** covering all valid script types

## Verification

To verify the fix works, check that:
1. Created Python tasks show "python" selected in the script_type dropdown
2. Created PowerShell tasks show "powershell" selected in the script_type dropdown
3. Created Command tasks show "command" selected in the script_type dropdown

## Run Tests

```bash
# Run all CRUD tests
cd ~/tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py -v

# Run specific type tests
pytest unit/taskservice/test_task_crud.py::TestPythonTaskCRUD -v
pytest unit/taskservice/test_task_crud.py::TestPowerShellTaskCRUD -v
pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD -v
```

## Files Changed

- `tests/utils/fixtures.py` - Removed invalid script types, added PowerShell
- `tests/unit/taskservice/test_task_crud.py` - Replaced shell tests with PowerShell tests
- `tests/conftest.py` - Already using Python (no changes needed)

## Key Takeaway

**Always use script types that match what the application actually supports:**
- Python scripts → `script_type: "python"`
- PowerShell scripts → `script_type: "powershell"`
- Command lists → `script_type: "command"` with `commands` array

This ensures the UI displays the correct script_type and tests accurately reflect application behavior.

