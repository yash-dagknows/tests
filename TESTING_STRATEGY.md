# DagKnows Testing Strategy

This document outlines the testing strategy and philosophy for the DagKnows application.

## Table of Contents

- [Overview](#overview)
- [Testing Pyramid](#testing-pyramid)
- [Test Types](#test-types)
- [Why Not Selenium?](#why-not-selenium)
- [Testing Best Practices](#testing-best-practices)
- [Coverage Goals](#coverage-goals)
- [CI/CD Integration](#cicd-integration)

## Overview

The DagKnows testing strategy is based on the **Testing Pyramid** principle, which emphasizes:

1. **Many fast unit tests** at the base
2. **Fewer integration tests** in the middle
3. **Few end-to-end tests** at the top

This approach provides:
- Fast feedback during development
- High confidence in code quality
- Maintainable test suite
- Efficient use of CI/CD resources

## Testing Pyramid

```
       /\
      /  \     E2E Tests (Slow, Expensive, Few)
     /____\    - Complete workflows
    /      \   - User scenarios
   /        \  - Critical paths
  /__________\ 
 /            \ Integration Tests (Medium, Moderate, Some)
/              \ - Service-to-service
/______________\ - API contracts
|              | - Data flow
|              |
|              | Unit Tests (Fast, Cheap, Many)
|              | - Functions & Classes
|______________| - Logic & Validation
```

### Distribution

- **Unit Tests**: 70% of tests
- **Integration Tests**: 20% of tests
- **E2E Tests**: 10% of tests

## Test Types

### 1. Unit Tests

**Purpose**: Verify individual components work correctly in isolation.

**Characteristics**:
- Test single functions, methods, or classes
- Mock external dependencies
- No database or network calls
- Execute in milliseconds
- Run frequently during development

**Examples**:
- Task validation logic
- Data transformation functions
- Permission checking
- Input sanitization

**When to Write**:
- For all business logic
- For utility functions
- For validation rules
- For data transformations

**Tools**:
- pytest for test execution
- pytest-mock for mocking
- Unit test fixtures

### 2. Integration Tests

**Purpose**: Verify multiple components work together correctly.

**Characteristics**:
- Test interactions between services
- Use real databases and services
- Test API contracts
- Execute in seconds
- Run before deployment

**Examples**:
- req-router → taskservice communication
- Task creation → Elasticsearch indexing
- Tenant creation → Settings → TaskService flow
- Database operations

**When to Write**:
- For service-to-service communication
- For database operations
- For external API integrations
- For authentication flows

**Tools**:
- pytest with real services
- Docker Compose for services
- API clients for testing

### 3. End-to-End Tests

**Purpose**: Verify complete user workflows work from start to finish.

**Characteristics**:
- Test complete business scenarios
- Use all services together
- Simulate real user behavior
- Execute in minutes
- Run before major releases

**Examples**:
- Complete tenant onboarding
- Task creation → editing → execution
- Multi-user collaboration
- Full workspace management

**When to Write**:
- For critical user journeys
- For complex multi-step workflows
- For cross-service features
- For release validation

**Tools**:
- pytest with all services
- Full Docker Compose stack
- Comprehensive fixtures

## Why Not Selenium?

**Selenium is NOT needed for this test suite** because:

### Our Application Architecture

1. **Backend Services**: We're testing backend APIs (Python/Flask), not browser UI
2. **API-First**: Services communicate via REST/gRPC, not browser interactions
3. **Headless Testing**: API testing is faster and more reliable than browser testing

### When to Use Selenium

Selenium would be appropriate for:
- Testing the **dagknows_nuxt** frontend (Vue.js/Nuxt UI)
- Testing browser-specific behavior
- Testing JavaScript interactions
- Testing visual/CSS rendering

### Our Approach Instead

For backend services (taskservice, req-router):
- ✅ **Use pytest + requests**: Test REST APIs directly
- ✅ **Use gRPC testing**: Test gRPC services directly
- ✅ **Use API clients**: Test service interactions
- ✅ **Mock browser behavior**: Simulate user actions via API

For frontend (if needed later):
- Consider **Cypress** or **Playwright** (modern alternatives to Selenium)
- These are faster, more reliable, and easier to maintain
- Better developer experience and debugging

### Benefits of Our Approach

1. **Speed**: API tests are 10-100x faster than browser tests
2. **Reliability**: No flaky tests from browser timing issues
3. **CI/CD**: Faster feedback in pipelines
4. **Debugging**: Easier to debug failed tests
5. **Maintenance**: Less brittle, easier to maintain

## Testing Best Practices

### General Principles

1. **Test Behavior, Not Implementation**
   - Focus on what the code does, not how it does it
   - Test from the user's perspective

2. **Keep Tests Independent**
   - Each test should run in isolation
   - Tests should not depend on each other
   - Use fixtures for setup/teardown

3. **Use Descriptive Names**
   ```python
   # Good
   def test_user_cannot_delete_other_users_tasks():
       ...
   
   # Bad
   def test_delete():
       ...
   ```

4. **Follow AAA Pattern**
   ```python
   def test_something():
       # Arrange - Setup test data
       task_data = create_task_data()
       
       # Act - Perform the action
       result = create_task(task_data)
       
       # Assert - Verify the result
       assert result.success
   ```

5. **Test One Thing at a Time**
   - Each test should verify one specific behavior
   - Don't test multiple scenarios in one test

6. **Use Test Data Factories**
   ```python
   # Good
   task = test_data_factory.create_task_data()
   
   # Bad
   task = {
       "title": "Test Task",
       "script": "echo test",
       # ... hardcoded data
   }
   ```

### Unit Test Best Practices

1. **Mock External Dependencies**
   ```python
   @patch('taskservice.elasticsearch_client')
   def test_task_creation(mock_es):
       mock_es.index.return_value = {"result": "created"}
       # Test logic
   ```

2. **Test Edge Cases**
   - Empty inputs
   - Invalid data
   - Boundary conditions
   - Error handling

3. **Keep Tests Fast**
   - Avoid sleep() calls
   - Mock slow operations
   - Use in-memory databases if possible

### Integration Test Best Practices

1. **Use Real Services**
   - Don't mock database calls
   - Use actual service endpoints
   - Test real data flow

2. **Clean Up Test Data**
   ```python
   @pytest.fixture
   def test_task(api_client):
       task = api_client.create_task(...)
       yield task
       api_client.delete_task(task.id)  # Cleanup
   ```

3. **Wait for Async Operations**
   ```python
   # After creating a task, wait for Elasticsearch indexing
   time.sleep(1)
   # Or use proper polling
   ```

### E2E Test Best Practices

1. **Focus on Happy Paths**
   - Test the most common user journeys
   - Validate critical business flows

2. **Add Print Statements**
   ```python
   print("[E2E] Step 1: Creating tenant...")
   # Makes debugging easier
   ```

3. **Handle Service Delays**
   - Add appropriate wait times
   - Use retry logic for flaky operations

4. **Keep E2E Tests Minimal**
   - Only test scenarios that can't be covered by unit/integration tests

## Coverage Goals

### Target Coverage

- **Overall**: 80%+ code coverage
- **Critical Paths**: 100% coverage
- **New Code**: 90%+ coverage required

### What to Cover

**High Priority (Must Have Coverage)**:
- Authentication and authorization
- Data validation and sanitization
- Critical business logic
- Security-sensitive code
- Data persistence operations

**Medium Priority (Should Have Coverage)**:
- API endpoints
- Service integrations
- Error handling
- Data transformations

**Low Priority (Nice to Have Coverage)**:
- Utility functions
- Constants and configurations
- Simple getters/setters

### What NOT to Cover

- Third-party library code
- Auto-generated code (protobuf, etc.)
- Configuration files
- Migration scripts (covered separately)

## CI/CD Integration

### Pipeline Stages

1. **Quick Feedback (< 5 min)**
   - Run unit tests
   - Run linting
   - Fast smoke tests

2. **Integration Testing (< 15 min)**
   - Start services
   - Run integration tests
   - Generate coverage

3. **E2E Testing (< 30 min)**
   - Full stack deployment
   - Run E2E tests
   - Performance tests

4. **Deployment**
   - Only if all tests pass
   - Deploy to staging/production

### Jenkins Integration

Our Jenkinsfile provides:
- Parameterized test execution
- Coverage reporting
- Test result archiving
- Failure notifications

```groovy
// Run specific test suite
./Jenkinsfile TEST_SUITE=unit

// Run with coverage
./Jenkinsfile RUN_COVERAGE=true
```

### Pre-commit Checks

Before committing code:
```bash
# Run fast tests
make test-unit

# Check coverage
make test-coverage

# Lint code
make lint
```

### Pre-deployment Checks

Before deploying:
```bash
# Run all tests
make test

# Run smoke tests
make test-smoke

# Verify critical paths
pytest -m smoke -v
```

## Continuous Improvement

### Metrics to Track

1. **Test Coverage**: Aim for 80%+
2. **Test Execution Time**: Keep under 30 minutes
3. **Test Stability**: < 1% flaky tests
4. **Bug Escape Rate**: Bugs found in production

### Regular Reviews

- **Weekly**: Review failed tests in CI
- **Monthly**: Analyze test coverage trends
- **Quarterly**: Evaluate testing strategy effectiveness

### When to Add Tests

1. **Before fixing bugs**: Write test that reproduces the bug
2. **For new features**: Write tests alongside feature code
3. **For regression**: Add test when bug is found in production
4. **For refactoring**: Ensure existing tests pass

## Conclusion

This testing strategy ensures:
- ✅ Fast feedback during development
- ✅ High confidence in code quality
- ✅ Maintainable test suite
- ✅ Efficient CI/CD pipelines
- ✅ Reduced production bugs

Remember: **Good tests are an investment that pays off over time!**

