# Getting Started with DagKnows Test Suite

This guide will help you set up and run the test suite for the first time.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
  ```bash
  python3 --version
  ```

- **Docker and Docker Compose**
  ```bash
  docker --version
  docker-compose --version
  ```

- **Git** (for cloning the repository)
  ```bash
  git --version
  ```

## Quick Start (5 minutes)

### 1. Navigate to the tests directory

```bash
cd /path/to/dagknows_src/tests
```

### 2. Install dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install test dependencies
pip install -r requirements.txt
```

### 3. Setup environment

```bash
# Copy example environment file
cp .env.test.example .env.test

# Edit .env.test if needed (optional for default setup)
# nano .env.test
```

### 4. Run your first test

```bash
# Run unit tests (no services required)
pytest unit/ -v
```

🎉 **Congratulations!** You've run your first test!

## Running Tests with Services

For integration and E2E tests, you need to start the services first.

### Option 1: Using Make (Recommended)

```bash
# Start services and run all tests
make test-integration

# Or run E2E tests
make test-e2e

# Stop services when done
make stop-services
```

### Option 2: Using Docker Compose Directly

```bash
# Start all test services
docker-compose -f docker-compose-test.yml up -d

# Wait for services to be ready
./utils/wait-for-services.sh

# Run tests
pytest integration/ -v

# Stop services
docker-compose -f docker-compose-test.yml down -v
```

### Option 3: Using the Test Script

```bash
# Run all tests with services
./ci/run-tests-ci.sh all true

# Run only unit tests (no services)
./ci/run-tests-ci.sh unit false
```

## Understanding Test Categories

### Unit Tests (`tests/unit/`)

**What**: Test individual functions and classes in isolation
**Speed**: ⚡ Fast (< 5 minutes)
**Services**: None required
**Coverage**: Code logic, validation, data structures

```bash
# Run all unit tests
pytest unit/ -v

# Run taskservice unit tests only
pytest unit/taskservice/ -v

# Run specific test file
pytest unit/taskservice/test_task_crud.py -v
```

### Integration Tests (`tests/integration/`)

**What**: Test interaction between services
**Speed**: 🚶 Medium (5-15 minutes)
**Services**: Elasticsearch, PostgreSQL, TaskService, ReqRouter
**Coverage**: API contracts, data flow, service communication

```bash
# Start services first
make start-services

# Run integration tests
pytest integration/ -v

# Stop services
make stop-services
```

### End-to-End Tests (`tests/e2e/`)

**What**: Test complete workflows from user perspective
**Speed**: 🐢 Slow (15-30 minutes)
**Services**: All services running
**Coverage**: Complete business flows, multi-service workflows

```bash
# Start services first
make start-services

# Run E2E tests
pytest e2e/ -v

# Stop services
make stop-services
```

## Running Specific Tests

### By Test Name

```bash
# Run a specific test function
pytest tests/unit/taskservice/test_task_crud.py::TestTaskCRUD::test_create_basic_task -v
```

### By Marker

```bash
# Run only smoke tests
pytest -m smoke -v

# Run only tenant-related tests
pytest -m tenant -v

# Run fast tests (exclude slow)
pytest -m "not slow" -v
```

### By Pattern

```bash
# Run all tests with "create" in the name
pytest -k "create" -v

# Run all task-related tests
pytest -k "task" -v
```

## Viewing Test Results

### Console Output

Tests will output results to the console with:
- ✓ Green dots for passing tests
- F Red F's for failures
- s Yellow s's for skipped tests

### HTML Report

```bash
# Generate HTML report
pytest --html=results/report.html --self-contained-html

# Open in browser
open results/report.html  # macOS
xdg-open results/report.html  # Linux
start results/report.html  # Windows
```

### Coverage Report

```bash
# Run with coverage
pytest --cov=../taskservice/src --cov=../req_router/src \
       --cov-report=html:results/htmlcov

# Open coverage report
open results/htmlcov/index.html
```

## Troubleshooting

### Tests are failing

1. **Check services are running**
   ```bash
   docker-compose -f docker-compose-test.yml ps
   ```

2. **Check service health**
   ```bash
   make check-services
   ```

3. **View service logs**
   ```bash
   docker-compose -f docker-compose-test.yml logs taskservice
   docker-compose -f docker-compose-test.yml logs req-router
   ```

4. **Clean and restart**
   ```bash
   make clean-services
   make start-services
   ```

### Services won't start

1. **Check if ports are already in use**
   ```bash
   lsof -i :9200  # Elasticsearch
   lsof -i :5432  # PostgreSQL
   lsof -i :2235  # TaskService
   lsof -i :8888  # ReqRouter
   ```

2. **Stop conflicting services**
   ```bash
   docker-compose -f ../app_docker_compose_build_deploy/local-docker-compose.yml down
   ```

3. **Clean Docker volumes**
   ```bash
   docker volume prune
   ```

### Import errors

1. **Verify Python path**
   ```bash
   echo $PYTHONPATH
   ```

2. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check Python version**
   ```bash
   python --version  # Should be 3.10+
   ```

### Elasticsearch issues

1. **Check Elasticsearch is responding**
   ```bash
   curl http://localhost:9200/_cluster/health
   ```

2. **Increase Docker memory**
   - Docker Desktop → Preferences → Resources → Memory: 4GB+

3. **Check Elasticsearch logs**
   ```bash
   docker-compose -f docker-compose-test.yml logs elasticsearch
   ```

## Next Steps

Now that you have the tests running:

1. **Explore the test structure**
   - Read through existing tests
   - Understand the fixtures in `conftest.py`
   - Review the API clients in `utils/api_client.py`

2. **Write your first test**
   - Follow the patterns in existing tests
   - Use the test data factories
   - Add appropriate markers

3. **Run tests in CI**
   - See `ci/run-tests-ci.sh` for CI execution
   - Review `Jenkinsfile` for Jenkins integration

4. **Contribute**
   - Add tests for new features
   - Improve test coverage
   - Share your feedback

## Useful Commands

```bash
# Run tests in parallel (faster)
pytest -n auto

# Run tests with detailed output
pytest -vv -s

# Run tests with debugger on failure
pytest --pdb

# Re-run only failed tests
pytest --lf

# Run tests in watch mode
pytest -f

# Generate all reports
make test-coverage

# Clean everything
make clean-all
```

## Getting Help

- **Documentation**: See [README.md](README.md) for detailed information
- **Test Writing**: See test examples in `unit/`, `integration/`, `e2e/`
- **API Reference**: See `utils/api_client.py` for available methods
- **CI/CD**: See `Jenkinsfile` for pipeline configuration

## Best Practices

1. **Always cleanup test data** - Use fixtures and cleanup_tracker
2. **Write descriptive test names** - `test_user_can_create_task_with_parameters`
3. **Use appropriate markers** - `@pytest.mark.unit`, `@pytest.mark.integration`
4. **Keep tests independent** - Each test should work in isolation
5. **Use test data factories** - Don't hardcode test data
6. **Add docstrings** - Explain what the test does and why
7. **Run tests before committing** - `make test-unit` at minimum

Happy Testing! 🚀

