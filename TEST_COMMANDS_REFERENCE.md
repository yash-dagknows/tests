# Test Commands Reference Guide

Complete reference for running individual tests and test suites.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Commands](#quick-commands)
- [Smoke Tests](#smoke-tests)
- [Unit Tests - TaskService](#unit-tests---taskservice)
- [Unit Tests - ReqRouter](#unit-tests---reqrouter)
- [Integration Tests](#integration-tests)
- [End-to-End Tests](#end-to-end-tests)
- [Debugging Commands](#debugging-commands)

## Prerequisites

Before running any tests, ensure:

1. **dkapp services are running**
   ```bash
   cd ~/dkapp && docker-compose ps
   ```

2. **Environment is loaded**
   ```bash
   cd ~/tests
   export $(grep -v '^#' .env.local | xargs)
   ```

## Quick Commands

### Run All Test Suites

```bash
cd ~/tests

# All smoke tests (fastest, ~30 seconds)
make -f Makefile.local quick

# All unit tests (~2-5 minutes)
make -f Makefile.local unit

# All integration tests (~10-15 minutes)
make -f Makefile.local integration

# All E2E tests (~20-30 minutes)
make -f Makefile.local e2e

# Everything (~30-45 minutes)
make -f Makefile.local test-all

# With coverage report
make -f Makefile.local coverage
```

### Run Tests by Directory

```bash
# All tests in a directory
docker-compose -f docker-compose-local.yml run --rm test-runner pytest smoke/ -v
docker-compose -f docker-compose-local.yml run --rm test-runner pytest unit/ -v
docker-compose -f docker-compose-local.yml run --rm test-runner pytest integration/ -v
docker-compose -f docker-compose-local.yml run --rm test-runner pytest e2e/ -v
```

### Run Tests by Marker

```bash
# Smoke tests only
docker-compose -f docker-compose-local.yml run --rm test-runner pytest -m smoke -v

# Unit tests only
docker-compose -f docker-compose-local.yml run --rm test-runner pytest -m unit -v

# Integration tests only
docker-compose -f docker-compose-local.yml run --rm test-runner pytest -m integration -v

# E2E tests only
docker-compose -f docker-compose-local.yml run --rm test-runner pytest -m e2e -v

# Task-related tests
docker-compose -f docker-compose-local.yml run --rm test-runner pytest -m task -v

# Tenant-related tests
docker-compose -f docker-compose-local.yml run --rm test-runner pytest -m tenant -v
```

---

## Smoke Tests

Quick validation tests (< 1 minute total)

### Run All Smoke Tests

```bash
cd ~/tests
make -f Makefile.local quick
```

Or manually:

```bash
docker-compose -f docker-compose-local.yml run --rm test-runner pytest smoke/ -v
```

### Individual Smoke Tests

#### Initialization Tests (smoke/test_00_initialization.py)

```bash
# Test 1: Elasticsearch indices exist or create
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_00_initialization.py::test_elasticsearch_indices_exist_or_create -v

# Test 2: Database connection
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_00_initialization.py::test_database_connection -v

# Test 3: Ready for testing
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_00_initialization.py::test_ready_for_testing -v
```

#### Authentication Debug Tests (smoke/test_auth_debug.py)

```bash
# Test 4: TaskService status (no auth)
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_auth_debug.py::test_taskservice_status_no_auth -v

# Test 5: Check ALLOW_DK_USER_INFO_HEADER
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_auth_debug.py::test_check_allow_dk_user_info_header -v

# Test 6: Create minimal task with auth
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_auth_debug.py::test_create_minimal_task_with_auth -v
```

#### Simple Smoke Tests (smoke/test_simple_smoke.py)

```bash
# Test 7: Elasticsearch is up
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_simple_smoke.py::test_elasticsearch_is_up -v

# Test 8: TaskService status unauthenticated
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_simple_smoke.py::test_taskservice_status_unauthenticated -v

# Test 9: ReqRouter readiness
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_simple_smoke.py::test_reqrouter_readiness -v

# Test 10: Check TaskService auth mode
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_simple_smoke.py::test_check_taskservice_auth_mode -v
```

#### General Smoke Tests (smoke/test_smoke.py)

```bash
# Test 11: Services are reachable
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_smoke.py::test_services_are_reachable -v

# Test 12: Test suite is configured
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_smoke.py::test_test_suite_is_configured -v

# Test 13: TaskService status endpoint
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_smoke.py::test_taskservice_status_endpoint -v

# Test 14: ReqRouter readiness endpoint
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_smoke.py::test_req_router_readiness_endpoint -v

# Test 15: Elasticsearch cluster health
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest smoke/test_smoke.py::test_elasticsearch_cluster_health -v
```

---

## Unit Tests - TaskService

### Task CRUD Tests (unit/taskservice/test_task_crud.py)

**Note**: Tests are organized by task type (Python, PowerShell, Command) to match supported script_types.

#### Run All CRUD Tests

```bash
cd ~/tests

# All tests in file (26 tests)
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py -v
```

#### TestPythonTaskCRUD - Python Script Tasks (6 tests)

```bash
# Run all Python task tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPythonTaskCRUD -v

# Test 16: Create Python task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPythonTaskCRUD::test_create_python_task -v

# Test 17: Create Python task with custom ID
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPythonTaskCRUD::test_create_python_task_with_custom_id -v

# Test 18: Get Python task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPythonTaskCRUD::test_get_python_task -v

# Test 19: Update Python task script
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPythonTaskCRUD::test_update_python_task -v

# Test 20: Update Python task metadata
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPythonTaskCRUD::test_update_python_task_metadata -v

# Test 21: Delete Python task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPythonTaskCRUD::test_delete_python_task -v
```

#### TestPowerShellTaskCRUD - PowerShell Script Tasks (3 tests)

```bash
# Run all PowerShell task tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPowerShellTaskCRUD -v

# Test 22: Create PowerShell task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPowerShellTaskCRUD::test_create_powershell_task -v

# Test 23: Get PowerShell task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPowerShellTaskCRUD::test_get_powershell_task -v

# Test 24: Update PowerShell task script
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestPowerShellTaskCRUD::test_update_powershell_task_script -v
```

#### TestCommandTaskCRUD - Command-Type Tasks (7 tests)

```bash
# Run all Command task tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD -v

# Test 25: Create command task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD::test_create_command_task -v

# Test 26: Create command task with custom ID
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD::test_create_command_task_with_custom_id -v

# Test 27: Get command task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD::test_get_command_task -v

# Test 28: Update command task commands
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD::test_update_command_task_commands -v

# Test 29: Update command task add commands
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD::test_update_command_task_add_commands -v

# Test 30: Update command task metadata
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD::test_update_command_task_metadata -v

# Test 31: Delete command task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestCommandTaskCRUD::test_delete_command_task -v
```

#### TestTaskGeneralOperations - General Task Operations (3 tests)

```bash
# Run all general operation tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskGeneralOperations -v

# Test 32: Create task with duplicate ID fails
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskGeneralOperations::test_create_task_duplicate_id_fails -v

# Test 33: Get nonexistent task fails
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskGeneralOperations::test_get_nonexistent_task_fails -v

# Test 34: Delete nonexistent task is idempotent
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskGeneralOperations::test_delete_nonexistent_task_idempotent -v
```

#### TestTaskWithParameters - Parametrized Tasks (3 tests)

```bash
# Run all parameter tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskWithParameters -v

# Test 35: Create Python task with params
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskWithParameters::test_create_python_task_with_params -v

# Test 36: Create command task with params
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskWithParameters::test_create_command_task_with_params -v

# Test 37: Task param validation
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskWithParameters::test_task_param_validation -v
```

#### TestTaskTags - Tag Management (4 tests)

```bash
# Run all tag tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskTags -v

# Test 38: Create Python task with tags
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskTags::test_create_python_task_with_tags -v

# Test 39: Create command task with tags
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskTags::test_create_command_task_with_tags -v

# Test 40: Update task tags
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskTags::test_update_task_tags -v

# Test 41: Clear task tags
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskTags::test_clear_task_tags -v
```

### Task Search Tests (unit/taskservice/test_task_search.py)

#### Run All Search Tests

```bash
# All search tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py -v

# Only TestTaskSearch class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskSearch -v

# Only TestTaskList class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskList -v
```

#### TestTaskSearch - Search Operations

```bash
# Test 42: Search tasks by title
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskSearch::test_search_tasks_by_title -v

# Test 43: Search tasks by tag
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskSearch::test_search_tasks_by_tag -v

# Test 44: Search tasks by description
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskSearch::test_search_tasks_by_description -v

# Test 45: Search nonexistent task
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskSearch::test_search_nonexistent_task -v
```

#### TestTaskList - List Operations

```bash
# Test 46: List tasks
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskList::test_list_tasks -v

# Test 47: List tasks with pagination
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskList::test_list_tasks_with_pagination -v

# Test 48: List tasks with filters
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskList::test_list_tasks_with_filters -v
```

### Workspace Tests (unit/taskservice/test_workspace.py)

#### Run All Workspace Tests

```bash
# All workspace tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py -v

# Only TestWorkspaceCRUD class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceCRUD -v

# Only TestWorkspaceTaskAssociation class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceTaskAssociation -v
```

#### TestWorkspaceCRUD - Workspace Operations

```bash
# Test 49: Create workspace
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceCRUD::test_create_workspace -v

# Test 50: Get workspace
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceCRUD::test_get_workspace -v

# Test 51: Update workspace
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceCRUD::test_update_workspace -v

# Test 52: Delete workspace
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceCRUD::test_delete_workspace -v

# Test 53: List workspaces
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceCRUD::test_list_workspaces -v
```

#### TestWorkspaceTaskAssociation - Workspace-Task Relations

```bash
# Test 54: Create task in workspace
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceTaskAssociation::test_create_task_in_workspace -v

# Test 55: List tasks in workspace
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_workspace.py::TestWorkspaceTaskAssociation::test_list_tasks_in_workspace -v
```

---

## Unit Tests - ReqRouter

### Authentication Tests (unit/req_router/test_auth.py)

#### Run All Auth Tests

```bash
# All auth tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py -v

# Only TestAuthentication class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py::TestAuthentication -v

# Only TestAuthorizationHeaders class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py::TestAuthorizationHeaders -v
```

#### TestAuthentication - Login/Logout

```bash
# Test 46: Login success
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py::TestAuthentication::test_login_success -v

# Test 47: Login wrong password fails
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py::TestAuthentication::test_login_wrong_password_fails -v

# Test 48: Login nonexistent user fails
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py::TestAuthentication::test_login_nonexistent_user_fails -v

# Test 49: Logout
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py::TestAuthentication::test_logout -v
```

#### TestAuthorizationHeaders - Header Validation

```bash
# Test 50: Authenticated request includes token
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py::TestAuthorizationHeaders::test_authenticated_request_includes_token -v

# Test 51: Unauthenticated request fails
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_auth.py::TestAuthorizationHeaders::test_unauthenticated_request_fails -v
```

### Tenant Management Tests (unit/req_router/test_tenant_mgmt.py)

#### Run All Tenant Tests

```bash
# All tenant tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_tenant_mgmt.py -v

# Only TestTenantCreation class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_tenant_mgmt.py::TestTenantCreation -v

# Only TestTenantValidation class
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_tenant_mgmt.py::TestTenantValidation -v
```

#### TestTenantCreation - Tenant Creation

```bash
# Test 52: Create tenant
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_tenant_mgmt.py::TestTenantCreation::test_create_tenant -v

# Test 53: Create tenant with org name
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_tenant_mgmt.py::TestTenantCreation::test_create_tenant_with_org_name -v

# Test 54: Create tenant duplicate email fails
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_tenant_mgmt.py::TestTenantCreation::test_create_tenant_duplicate_email_fails -v
```

#### TestTenantValidation - Input Validation

```bash
# Test 55: Create tenant missing email fails
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_tenant_mgmt.py::TestTenantValidation::test_create_tenant_missing_email_fails -v

# Test 56: Create tenant invalid email fails
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/test_tenant_mgmt.py::TestTenantValidation::test_create_tenant_invalid_email_fails -v
```

---

## Integration Tests

### Run All Integration Tests

```bash
cd ~/tests
make -f Makefile.local integration
```

Or manually:

```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/ -v
```

### Tenant Creation Flow (integration/test_tenant_creation.py)

#### Run All Tenant Flow Tests

```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_tenant_creation.py -v
```

#### Individual Tests

```bash
# Test 57: Tenant creation creates workspace
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_tenant_creation.py::TestTenantCreationFlow::test_tenant_creation_creates_workspace -v

# Test 58: Tenant creation creates indices
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_tenant_creation.py::TestTenantCreationFlow::test_tenant_creation_creates_indices -v

# Test 59: Tenant can create task after creation
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_tenant_creation.py::TestTenantCreationFlow::test_tenant_can_create_task_after_creation -v

# Test 60: Tenant user stored in postgres
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_tenant_creation.py::TestTenantDatabaseOperations::test_tenant_user_stored_in_postgres -v

# Test 61: Tenant org stored in postgres
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_tenant_creation.py::TestTenantDatabaseOperations::test_tenant_org_stored_in_postgres -v
```

### Task Workflow Tests (integration/test_task_workflow.py)

#### Run All Task Workflow Tests

```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_task_workflow.py -v
```

#### Individual Tests

```bash
# Test 62: Create task via req-router
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_task_workflow.py::TestTaskWorkflowViaReqRouter::test_create_task_via_req_router -v

# Test 63: Task CRUD workflow via req-router
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_task_workflow.py::TestTaskWorkflowViaReqRouter::test_task_crud_workflow_via_req_router -v

# Test 64: Search task via req-router
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_task_workflow.py::TestTaskWorkflowViaReqRouter::test_search_task_via_req_router -v

# Test 65: Task created in taskservice visible in req-router
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_task_workflow.py::TestTaskServiceDirectVsReqRouter::test_task_created_in_taskservice_visible_in_req_router -v

# Test 66: Task created via req-router visible in taskservice
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_task_workflow.py::TestTaskServiceDirectVsReqRouter::test_task_created_via_req_router_visible_in_taskservice -v

# Test 67: Task stored in elasticsearch
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_task_workflow.py::TestTaskElasticsearchOperations::test_task_stored_in_elasticsearch -v

# Test 68: Task updated in elasticsearch
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest integration/test_task_workflow.py::TestTaskElasticsearchOperations::test_task_updated_in_elasticsearch -v
```

---

## End-to-End Tests

### Run All E2E Tests

```bash
cd ~/tests
make -f Makefile.local e2e
```

Or manually:

```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest e2e/ -v
```

### Complete Tenant Setup (e2e/test_complete_tenant_setup.py)

```bash
# Test 69: Complete tenant onboarding workflow
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest e2e/test_complete_tenant_setup.py::TestCompleteTenantSetup::test_complete_tenant_onboarding_workflow -v

# Test 70: Tenant creates and manages workspace
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest e2e/test_complete_tenant_setup.py::TestTenantWorkspaceManagement::test_tenant_creates_and_manages_workspace -v
```

### Task Lifecycle (e2e/test_task_lifecycle.py)

```bash
# Test 71: Complete task lifecycle
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest e2e/test_task_lifecycle.py::TestCompleteTaskLifecycle::test_complete_task_lifecycle -v

# Test 72: Parametrized task workflow
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest e2e/test_task_lifecycle.py::TestTaskWithParameters::test_parametrized_task_workflow -v
```

### AI Session Workflow (e2e/test_ai_session_workflow.py)

```bash
# Test 73: AI service architecture documented
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest e2e/test_ai_session_workflow.py::TestAIServicePlaceholder::test_ai_service_architecture_documented -v

# Test 74: AI service endpoints defined
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest e2e/test_ai_session_workflow.py::TestAIServicePlaceholder::test_ai_service_endpoints_defined -v
```

---

## Debugging Commands

### Run with Extra Verbosity

```bash
# Very verbose output
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -vv -s

# Show print statements
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -v -s

# Show full tracebacks
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -v --tb=long
```

### Stop on First Failure

```bash
# Stop on first error or failure
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v -x

# Run last failed test
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v --lf
```

### Run with PDB Debugger

```bash
# Drop into debugger on failure
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -v --pdb

# Drop into debugger on error
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -v --pdbcls=IPython.terminal.debugger:TerminalPdb --pdb
```

### Run Specific Test Pattern

```bash
# Run all tests matching "create"
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v -k "create"

# Run all tests matching "task" and "create"
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v -k "task and create"

# Run all tests NOT matching "slow"
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v -k "not slow"
```

### Generate Reports

```bash
# HTML report
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v --html=results/report.html --self-contained-html

# JUnit XML report (for CI)
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v --junitxml=results/junit.xml

# JSON report
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v --json-report --json-report-file=results/report.json
```

---

## Convenience Script

Create `~/tests/run-test.sh`:

```bash
#!/bin/bash
# Quick script to run any test

cd ~/tests
export $(grep -v '^#' .env.local | xargs)

TEST_PATH=${1:-smoke/}

echo "Running: $TEST_PATH"
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest "$TEST_PATH" -v
```

Make it executable:

```bash
chmod +x run-test.sh
```

### Usage Examples

```bash
# Run smoke tests
./run-test.sh smoke/

# Run specific test
./run-test.sh unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task

# Run test file
./run-test.sh unit/taskservice/test_task_crud.py

# Run test class
./run-test.sh unit/taskservice/test_task_crud.py::TestTaskCRUD

# Run all unit tests
./run-test.sh unit/

# With extra args
./run-test.sh "unit/ -x -vv"
```

---

## Quick Reference Matrix

| Category | Command | Time | Tests |
|----------|---------|------|-------|
| Smoke | `make -f Makefile.local quick` | ~30s | 17 |
| Unit - All | `make -f Makefile.local unit` | 2-5m | ~45 |
| Unit - TaskService | `pytest unit/taskservice/ -v` | 1-3m | ~30 |
| Unit - ReqRouter | `pytest unit/req_router/ -v` | 1-2m | ~8 |
| Integration | `make -f Makefile.local integration` | 10-15m | ~12 |
| E2E | `make -f Makefile.local e2e` | 20-30m | ~8 |
| All | `make -f Makefile.local test-all` | 30-45m | ~75 |

---

## Common Test Patterns

### Run Tests by Category

```bash
# All TaskService tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/ -v

# All ReqRouter tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/req_router/ -v

# All tests with "task" in name
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest -v -k task

# All tests with "workspace" in name
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest -v -k workspace
```

### Run Failed Tests Only

```bash
# Re-run only failed tests from last run
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v --lf

# Re-run failed tests first, then others
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v --ff
```

### Parallel Execution

```bash
# Run tests in parallel (faster)
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v -n auto

# Run with 4 workers
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v -n 4
```

---

## Tips & Tricks

### 1. Always Load Environment First

```bash
cd ~/tests
export $(grep -v '^#' .env.local | xargs)
```

### 2. Use Make Commands for Simplicity

```bash
make -f Makefile.local quick       # Smoke tests
make -f Makefile.local unit        # Unit tests
make -f Makefile.local integration # Integration tests
```

### 3. Stop on First Failure for Debugging

```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/ -v -x
```

### 4. Show Print Statements

```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py -v -s
```

### 5. Run Specific Test with Full Output

```bash
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -vv -s --tb=long
```

---

## Summary

**Total Tests Available:** ~75 tests
- Smoke: 17 tests
- Unit: 45 tests
- Integration: 12 tests
- E2E: 8 tests

**Quick Start:**
```bash
cd ~/tests
export $(grep -v '^#' .env.local | xargs)
make -f Makefile.local quick  # Start here
make -f Makefile.local unit   # Then this
```

**All commands are in this file - bookmark it for reference!** 📚

