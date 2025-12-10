# Task CRUD API E2E Test

## Overview

This is an **API-based End-to-End (E2E) test** for task CRUD operations. It sends HTTP requests directly to `dev.dagknows.com` (or configured base URL) to test task creation, reading, updating, and deletion.

**Key Points:**
- ✅ Uses `/api/v1/tasks/` endpoint (the new endpoint, not the legacy `/api/tasks/`)
- ✅ Sends requests directly to the API (no browser/UI automation)
- ✅ Matches how the backend actually processes requests
- ✅ Currently implements **task creation only** (update/delete will be added later)

## Architecture

### Endpoint Routing

The codebase has two endpoints:
- **Legacy**: `/api/tasks/` - Used by frontend, gets proxied by `req-router` to `/api/v1/tasks/`
- **New**: `/api/v1/tasks/` - Direct endpoint registered in `taskservice`, used by API clients

**Why we use `/api/v1/tasks/`:**
1. It's the new/correct endpoint
2. More direct (doesn't go through req-router forwarding)
3. Matches what the backend actually implements
4. Better for API-based testing

### Request Flow

```
Frontend: /api/tasks/ → req-router → /api/v1/tasks/ → taskservice
API Test:  /api/v1/tasks/ → taskservice (direct)
```

## Test Structure

### Test File
- **Location**: `api_tests/test_task_crud_api.py`
- **Test Class**: `TestTaskCRUDE2E`
- **Test Method**: `test_create_task_via_api`

### Test Flow

1. **Prepare task data** - Title, description, Python code
2. **Create task** - POST `/api/v1/tasks/` with `{"task": task_data}`
3. **Verify response** - Check task ID, title, description
4. **Get task** - GET `/api/v1/tasks/{task_id}` to verify it exists
5. **List tasks** - Verify task appears in task list
6. **Cleanup** - DELETE `/api/v1/tasks/{task_id}`

## Running the Test

### Quick Start

```bash
cd /path/to/tests/e2e_tests
./run_task_crud_api_test.sh
```

### Options

```bash
# Run against dev.dagknows.com (default)
./run_task_crud_api_test.sh

# Run against local Docker setup
./run_task_crud_api_test.sh --local

# Run with verbose output
./run_task_crud_api_test.sh -v
```

### Manual Run

```bash
# Activate virtual environment
source venv/bin/activate

# Set environment variables
export DAGKNOWS_URL="https://dev.dagknows.com"
export DAGKNOWS_PROXY="?proxy=dev1"
export JWT_TOKEN="your_jwt_token_here"

# Run test
pytest api_tests/test_task_crud_api.py::TestTaskCRUDE2E::test_create_task_via_api -v
```

### Local Docker Setup

```bash
export DAGKNOWS_URL="http://localhost:3000"
export DAGKNOWS_PROXY="?proxy=yashlocal"
export JWT_TOKEN="your_local_jwt_token"

pytest api_tests/test_task_crud_api.py::TestTaskCRUDE2E::test_create_task_via_api -v
```

## Configuration

### Environment Variables

- **`DAGKNOWS_URL`**: Base URL (default: `https://dev.dagknows.com`)
- **`DAGKNOWS_PROXY`**: Proxy parameter (default: `?proxy=dev1`)
- **`JWT_TOKEN`**: JWT access token for authentication

### API Client

The test uses `DagKnowsAPIClient` from `fixtures/api_client.py`:
- Automatically adds authentication headers
- Handles proxy parameters
- Uses `/api/v1/tasks/` endpoints

## Test Data

The test creates a task with:
- **Title**: `E2E API Test Task {timestamp}`
- **Description**: `Task created via API E2E test at {timestamp}`
- **Script Type**: `python`
- **Code**: Simple Python print statements

## Future Enhancements

The test currently only implements **task creation**. Future additions will include:

1. **Update Task** - PUT `/api/v1/tasks/{task_id}` with updated data
2. **Delete Task** - DELETE `/api/v1/tasks/{task_id}`
3. **Task with Child Tasks** - Create parent and child tasks
4. **Task Execution** - Execute created tasks
5. **Task Permissions** - Test task sharing and permissions

## Troubleshooting

### Authentication Errors

If you get `401 Unauthorized`:
- Check that `JWT_TOKEN` is set correctly
- Verify token hasn't expired
- Ensure token has proper permissions

### Endpoint Not Found (404)

If you get `404 Not Found`:
- Verify `DAGKNOWS_URL` is correct
- Check that proxy parameter is set correctly
- Ensure the service is running

### Task Creation Fails

If task creation fails:
- Check logs for detailed error messages
- Verify task data structure matches expected format
- Ensure workspace ID is valid (if provided)

## Related Files

- **Test File**: `api_tests/test_task_crud_api.py`
- **API Client**: `fixtures/api_client.py`
- **Run Script**: `run_task_crud_api_test.sh`
- **Config**: `config/env.py`, `config/test_users.py`

## Notes

- This is an **E2E test**, not a unit test - it hits real endpoints
- Tasks created during tests are automatically cleaned up
- The test uses the same authentication mechanism as the frontend
- All API calls match the structure used by the frontend (wrapped in `{"task": ...}`)

