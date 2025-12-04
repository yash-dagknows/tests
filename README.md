# DagKnows Test Suite

This directory contains the comprehensive test suite for the DagKnows application, covering unit tests, integration tests, and end-to-end workflow tests.

## Table of Contents
- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Types](#test-types)
- [CI/CD Integration](#cicd-integration)
- [Writing New Tests](#writing-new-tests)

## Overview

The test suite is designed to:
- Validate individual service functionality (unit tests)
- Test service-to-service communication (integration tests)
- Verify complete business workflows (E2E tests)
- Ensure system reliability before deployment
- Provide fast feedback in CI/CD pipelines

### Testing Approach

- **No Browser Automation**: We use API-level testing (not Selenium) since we're testing backend services
- **Docker-based**: Tests run in isolated containers matching production environment
- **pytest Framework**: All tests use pytest for consistency
- **Multi-service Orchestration**: Docker Compose manages service dependencies

## Test Structure

```
tests/
├── README.md                    # This file
├── pytest.ini                   # Pytest configuration
├── conftest.py                  # Shared fixtures and test setup
├── requirements.txt             # Test dependencies
├── docker-compose-test.yml      # Test environment orchestration
├── .env.test                    # Test environment variables
│
├── unit/                        # Unit tests (fast, isolated)
│   ├── taskservice/
│   │   ├── test_task_crud.py
│   │   ├── test_task_search.py
│   │   ├── test_workspace.py
│   │   └── test_permissions.py
│   └── req_router/
│       ├── test_tenant_mgmt.py
│       ├── test_user_mgmt.py
│       └── test_auth.py
│
├── integration/                 # Integration tests (service-to-service)
│   ├── test_tenant_creation.py
│   ├── test_task_workflow.py
│   ├── test_permissions_flow.py
│   └── test_proxy_communication.py
│
├── e2e/                        # End-to-end workflow tests
│   ├── test_complete_tenant_setup.py
│   ├── test_task_lifecycle.py
│   ├── test_ai_session_workflow.py
│   └── test_multi_user_collaboration.py
│
├── load/                       # Load and performance tests
│   ├── locustfile.py
│   └── test_api_performance.py
│
└── utils/                      # Test utilities and helpers
    ├── __init__.py
    ├── api_client.py           # API client wrapper
    ├── fixtures.py             # Common test data
    ├── assertions.py           # Custom assertions
    └── cleanup.py              # Test cleanup utilities
```

## Running Tests

### Prerequisites

1. Docker and Docker Compose installed
2. Python 3.10+ installed
3. Environment variables configured (see `.env.test`)

### Quick Start

```bash
# From the repository root
cd tests

# Install test dependencies
pip install -r requirements.txt

# Run all tests
make test

# Run specific test categories
make test-unit          # Unit tests only
make test-integration   # Integration tests only
make test-e2e          # End-to-end tests only

# Run with coverage
make test-coverage

# Run specific test file
pytest unit/taskservice/test_task_crud.py -v

# Run specific test function
pytest unit/taskservice/test_task_crud.py::test_create_task -v
```

### Using Docker Compose

```bash
# Start test environment
docker-compose -f docker-compose-test.yml up -d

# Wait for services to be healthy
./utils/wait-for-services.sh

# Run tests against the environment
pytest

# Stop test environment
docker-compose -f docker-compose-test.yml down -v
```

## Test Types

### 1. Unit Tests (`tests/unit/`)

**Purpose**: Test individual functions, classes, and modules in isolation.

**Characteristics**:
- Fast execution (< 1 second per test)
- Mock external dependencies
- No database or network calls
- High code coverage focus

**Example**:
```python
def test_task_validation():
    """Test task data validation logic"""
    task_data = {"title": "Test", "script": "echo hello"}
    result = validate_task(task_data)
    assert result.is_valid
```

### 2. Integration Tests (`tests/integration/`)

**Purpose**: Test interaction between multiple services/components.

**Characteristics**:
- Medium execution time (1-10 seconds per test)
- Use real services in test environment
- Test API contracts and data flow
- Verify service dependencies

**Example**:
```python
def test_tenant_creates_workspace(api_client):
    """Test that tenant creation also creates default workspace"""
    tenant = api_client.create_tenant({
        "email": "test@example.com",
        "organization": "TestOrg"
    })
    workspaces = api_client.get_workspaces(tenant.id)
    assert len(workspaces) > 0
```

### 3. End-to-End Tests (`tests/e2e/`)

**Purpose**: Test complete business workflows from start to finish.

**Characteristics**:
- Slower execution (10-60 seconds per test)
- Simulate real user scenarios
- Test critical business paths
- Multiple service interactions

**Example**:
```python
def test_complete_task_workflow(api_client):
    """Test complete task creation, editing, and execution workflow"""
    # Create tenant
    tenant = api_client.create_tenant(...)
    
    # Create task
    task = api_client.create_task(tenant.id, {...})
    
    # Edit task
    api_client.update_task(task.id, {"script": "updated"})
    
    # Execute task
    result = api_client.execute_task(task.id)
    
    assert result.status == "success"
```

### 4. Load Tests (`tests/load/`)

**Purpose**: Test system performance under load.

**Characteristics**:
- Uses Locust framework
- Simulates concurrent users
- Measures response times
- Identifies bottlenecks

## CI/CD Integration

### Jenkins Pipeline

The test suite is designed for Jenkins integration:

```groovy
// Jenkinsfile example
stage('Test') {
    steps {
        sh 'cd tests && pip install -r requirements.txt'
        sh 'cd tests && pytest --junitxml=results.xml --cov=src --cov-report=xml'
    }
    post {
        always {
            junit 'tests/results.xml'
            publishCoverage adapters: [coberturaAdapter('tests/coverage.xml')]
        }
    }
}
```

### Test Reports

- **JUnit XML**: `pytest --junitxml=results.xml`
- **Coverage Report**: `pytest --cov=src --cov-report=html`
- **Allure Reports**: `pytest --alluredir=allure-results`

### Environment Variables

Set these in Jenkins for CI runs:
```bash
DAGKNOWS_ELASTIC_URL=http://elasticsearch:9200
POSTGRESQL_DB_HOST=postgres
POSTGRESQL_DB_PASSWORD=testpass
ENFORCE_LOGIN=false  # Disable for test environment
```

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### Best Practices

1. **Use Fixtures**: Leverage pytest fixtures for setup/teardown
   ```python
   @pytest.fixture
   def test_tenant(api_client):
       tenant = api_client.create_tenant(...)
       yield tenant
       api_client.delete_tenant(tenant.id)
   ```

2. **Clear Assertions**: Use descriptive assertion messages
   ```python
   assert task.status == "created", f"Expected 'created' but got '{task.status}'"
   ```

3. **Cleanup**: Always cleanup test data
   ```python
   def test_something(api_client):
       task_id = api_client.create_task(...)
       try:
           # test code
       finally:
           api_client.delete_task(task_id)
   ```

4. **Parametrize**: Use pytest.mark.parametrize for multiple scenarios
   ```python
   @pytest.mark.parametrize("role,expected", [
       ("admin", True),
       ("user", False),
   ])
   def test_permissions(role, expected):
       assert has_permission(role) == expected
   ```

5. **Markers**: Use markers to categorize tests
   ```python
   @pytest.mark.slow
   @pytest.mark.integration
   def test_large_workflow():
       ...
   ```

### Adding a New Test

1. Choose appropriate directory (unit/integration/e2e)
2. Create test file following naming convention
3. Import necessary fixtures from conftest.py
4. Write test with clear docstring
5. Run test locally to verify
6. Update this README if adding new patterns

### Example Test Template

```python
"""
Test module for [feature name]
"""
import pytest
from utils.api_client import APIClient

def test_feature_description(api_client):
    """
    Test that [specific behavior] works correctly.
    
    Given: [initial state]
    When: [action taken]
    Then: [expected result]
    """
    # Arrange
    initial_data = {...}
    
    # Act
    result = api_client.do_something(initial_data)
    
    # Assert
    assert result.success
    assert result.data == expected_data
```

## Troubleshooting

### Common Issues

1. **Services not starting**: Check docker-compose logs
   ```bash
   docker-compose -f docker-compose-test.yml logs
   ```

2. **Elasticsearch connection errors**: Ensure ES is healthy
   ```bash
   curl http://localhost:9200/_cluster/health
   ```

3. **Test data conflicts**: Clean test database
   ```bash
   make clean-test-data
   ```

4. **Permission errors**: Ensure test user has correct roles
   ```bash
   pytest -v --log-cli-level=DEBUG
   ```

## Performance Benchmarks

Target test execution times:
- Unit tests: < 5 minutes
- Integration tests: < 15 minutes
- E2E tests: < 30 minutes
- Full suite: < 45 minutes

## Contributing

When adding tests:
1. Ensure all tests pass locally
2. Add appropriate markers
3. Update documentation
4. Maintain >80% code coverage
5. Follow existing patterns and conventions

## Support

For questions or issues:
- Check existing test examples
- Review this documentation
- Consult the team's testing guidelines

