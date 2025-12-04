# Jenkins Integration for DagKnows Test Suite

## Problem Statement

The test suite was initially designed for localhost testing, but your production setup has:

1. **External Docker Network**: Services use `saaslocalnetwork` network
2. **Encryption**: Services communicate using `APP_SECRET_KEY` and AES encryption
3. **TLS/SSL**: Services use mounted certificates (`/tls`, `/etc/letsencrypt`)
4. **Service Discovery**: Services reference each other by name (e.g., `http://taskservice:2235`)
5. **AWS ECS Agents**: Jenkins agents run on AWS ECS via Terraform
6. **No Localhost Access**: Services aren't accessible at `localhost:port`

## Solution Options

### Option 1: **In-Network Test Container** (Recommended)

Run tests inside a container that's part of the same Docker network as your services.

#### Approach

```yaml
# tests/docker-compose-jenkins.yml
version: '3.8'

networks:
  saaslocalnetwork:
    external: true  # Use existing network

services:
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    networks:
      - saaslocalnetwork
    environment:
      # Service URLs use service names, not localhost
      - DAGKNOWS_ELASTIC_URL=http://elasticsearch:9200
      - DAGKNOWS_TASKSERVICE_URL=http://taskservice:2235
      - DAGKNOWS_REQ_ROUTER_URL=http://req-router:8888
      - DAGKNOWS_SETTINGS_URL=http://settings:2225
      
      # Database connection
      - POSTGRESQL_DB_HOST=postgres
      - POSTGRESQL_DB_PORT=5432
      - POSTGRESQL_DB_NAME=${POSTGRESQL_DB_NAME}
      - POSTGRESQL_DB_USER=${POSTGRESQL_DB_USER}
      - POSTGRESQL_DB_PASSWORD=${POSTGRESQL_DB_PASSWORD}
      
      # Authentication bypass for tests
      - ALLOW_DK_USER_INFO_HEADER=true
      - ENFORCE_LOGIN=false
      
      # Test mode
      - TESTING=true
      - TEST_MODE=true
      
      # Inherit encryption keys
      - APP_SECRET_KEY=${APP_SECRET_KEY}
      - api_key=${api_key}
    
    volumes:
      - .:/app/tests
      - ../taskservice/src:/app/taskservice/src:ro
      - ../req_router/src:/app/req_router/src:ro
      - test_results:/app/tests/results
    
    working_dir: /app/tests
    command: pytest ${PYTEST_ARGS:-unit/ -v}

volumes:
  test_results:
```

#### Jenkins Pipeline

```groovy
// Jenkinsfile-network
pipeline {
    agent {
        label 'docker-agent'  // Your ECS agent
    }
    
    environment {
        APP_SECRET_KEY = credentials('app-secret-key')
        POSTGRESQL_DB_PASSWORD = credentials('postgres-password')
        api_key = credentials('api-key')
    }
    
    stages {
        stage('Run Tests') {
            steps {
                dir('tests') {
                    sh '''
                        # Tests run in container on same network as services
                        docker-compose -f docker-compose-jenkins.yml run --rm test-runner
                    '''
                }
            }
        }
    }
    
    post {
        always {
            junit 'tests/results/junit.xml'
            archiveArtifacts 'tests/results/**/*'
            sh 'docker-compose -f tests/docker-compose-jenkins.yml down'
        }
    }
}
```

**Pros:**
- ✅ Direct access to services on internal network
- ✅ No firewall/routing issues
- ✅ Inherits encryption keys
- ✅ Minimal changes to existing infrastructure

**Cons:**
- ⚠️ Requires services to be running
- ⚠️ Depends on production/staging environment

---

### Option 2: **Test Environment with Service Stack**

Deploy a complete isolated test environment within Jenkins.

#### Approach

```yaml
# tests/docker-compose-jenkins-isolated.yml
version: '3.8'

networks:
  test-network:
    name: dagknows_test_network_${BUILD_NUMBER}

services:
  # Infrastructure
  postgres:
    image: postgres:15-alpine
    networks:
      - test-network
    environment:
      POSTGRES_DB: dagknows_test
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRESQL_DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 10

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.9.2
    networks:
      - test-network
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 20

  # Application Services (use latest or test images)
  taskservice:
    image: public.ecr.aws/n5k3t9x2/taskservice:${TEST_TAG:-latest}
    networks:
      - test-network
    depends_on:
      postgres:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
    environment:
      - DAGKNOWS_ELASTIC_URL=http://elasticsearch:9200
      - POSTGRESQL_DB_HOST=postgres
      - POSTGRESQL_DB_PORT=5432
      - POSTGRESQL_DB_NAME=dagknows_test
      - POSTGRESQL_DB_USER=postgres
      - POSTGRESQL_DB_PASSWORD=${POSTGRESQL_DB_PASSWORD}
      - ALLOW_DK_USER_INFO_HEADER=true
      - ENFORCE_LOGIN=false
      - TESTING=true
    healthcheck:
      test: ["CMD-SHELL", "python -c 'import urllib.request; urllib.request.urlopen(\"http://localhost:2235/health\").read()'"]
      interval: 10s
      timeout: 5s
      retries: 20

  req-router:
    image: public.ecr.aws/n5k3t9x2/req_router:${TEST_TAG:-latest}
    networks:
      - test-network
    depends_on:
      taskservice:
        condition: service_healthy
    environment:
      - DAGKNOWS_TASKSERVICE_URL=http://taskservice:2235
      - DAGKNOWS_ELASTIC_URL=http://elasticsearch:9200
      - POSTGRESQL_DB_HOST=postgres
      - POSTGRESQL_DB_PORT=5432
      - POSTGRESQL_DB_NAME=dagknows_test
      - POSTGRESQL_DB_USER=postgres
      - POSTGRESQL_DB_PASSWORD=${POSTGRESQL_DB_PASSWORD}
      - APP_SECRET_KEY=${APP_SECRET_KEY}
      - ALLOW_DK_USER_INFO_HEADER=true
      - ENFORCE_LOGIN=false
      - TESTING=true
      - USER_ENABLE_EMAIL=false
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8888/health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 20

  # Test Runner
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    networks:
      - test-network
    depends_on:
      req-router:
        condition: service_healthy
      taskservice:
        condition: service_healthy
    environment:
      - DAGKNOWS_ELASTIC_URL=http://elasticsearch:9200
      - DAGKNOWS_TASKSERVICE_URL=http://taskservice:2235
      - DAGKNOWS_REQ_ROUTER_URL=http://req-router:8888
      - POSTGRESQL_DB_HOST=postgres
      - POSTGRESQL_DB_PORT=5432
      - POSTGRESQL_DB_NAME=dagknows_test
      - POSTGRESQL_DB_USER=postgres
      - POSTGRESQL_DB_PASSWORD=${POSTGRESQL_DB_PASSWORD}
      - APP_SECRET_KEY=${APP_SECRET_KEY}
      - TESTING=true
    volumes:
      - .:/app/tests
      - test_results:/app/tests/results
    command: pytest ${PYTEST_ARGS:--v --junitxml=results/junit.xml}

volumes:
  test_results:
```

#### Jenkins Pipeline

```groovy
// Jenkinsfile-isolated
pipeline {
    agent {
        label 'docker-agent'
    }
    
    environment {
        APP_SECRET_KEY = credentials('app-secret-key')
        POSTGRESQL_DB_PASSWORD = credentials('postgres-test-password')
        TEST_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = "dagknows_test_${env.BUILD_NUMBER}"
    }
    
    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['unit', 'integration', 'e2e', 'all'],
            description: 'Test suite to run'
        )
    }
    
    stages {
        stage('Setup') {
            steps {
                echo "Setting up test environment ${COMPOSE_PROJECT_NAME}"
            }
        }
        
        stage('Start Services') {
            steps {
                dir('tests') {
                    sh '''
                        # Start all services
                        docker-compose -f docker-compose-jenkins-isolated.yml up -d
                        
                        # Wait for services to be healthy
                        ./ci/wait-for-services-jenkins.sh
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                dir('tests') {
                    script {
                        def pytest_args = ""
                        switch(params.TEST_SUITE) {
                            case 'unit':
                                pytest_args = "unit/ -v"
                                break
                            case 'integration':
                                pytest_args = "integration/ -v"
                                break
                            case 'e2e':
                                pytest_args = "e2e/ -v"
                                break
                            default:
                                pytest_args = "-v"
                        }
                        
                        sh """
                            export PYTEST_ARGS='${pytest_args} --junitxml=results/junit.xml --html=results/report.html'
                            docker-compose -f docker-compose-jenkins-isolated.yml run --rm test-runner
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Collect results
            junit allowEmptyResults: true, testResults: 'tests/results/junit.xml'
            
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'tests/results',
                reportFiles: 'report.html',
                reportName: 'Test Report'
            ])
            
            // Cleanup
            dir('tests') {
                sh '''
                    docker-compose -f docker-compose-jenkins-isolated.yml logs > jenkins-services.log || true
                    docker-compose -f docker-compose-jenkins-isolated.yml down -v || true
                '''
            }
            
            archiveArtifacts artifacts: 'tests/results/**/*,tests/jenkins-services.log', allowEmptyArchive: true
        }
        
        success {
            echo 'Tests passed!'
        }
        
        failure {
            echo 'Tests failed!'
            // Add notifications here
        }
    }
}
```

**Pros:**
- ✅ Isolated test environment
- ✅ No dependency on production services
- ✅ Reproducible
- ✅ Parallel test runs possible

**Cons:**
- ⚠️ Slower (spins up full stack)
- ⚠️ Requires more resources

---

### Option 3: **Hybrid - Unit Tests Standalone, Integration with Services**

Separate unit tests (fast, no services) from integration tests (with services).

#### Jenkins Pipeline

```groovy
// Jenkinsfile-hybrid
pipeline {
    agent {
        label 'docker-agent'
    }
    
    environment {
        APP_SECRET_KEY = credentials('app-secret-key')
        POSTGRESQL_DB_PASSWORD = credentials('postgres-test-password')
    }
    
    stages {
        stage('Unit Tests') {
            steps {
                echo 'Running fast unit tests (no services required)'
                dir('tests') {
                    sh '''
                        # Run unit tests directly (no Docker needed)
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        pytest unit/ -v --junitxml=results/junit-unit.xml
                    '''
                }
            }
        }
        
        stage('Integration Tests') {
            when {
                expression { 
                    // Only run integration tests on main branch or when requested
                    return env.BRANCH_NAME == 'main' || params.FULL_TEST_SUITE 
                }
            }
            steps {
                echo 'Running integration tests with services'
                dir('tests') {
                    sh '''
                        # Use network-aware compose file
                        docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
                            pytest integration/ -v --junitxml=results/junit-integration.xml
                    '''
                }
            }
        }
        
        stage('E2E Tests') {
            when {
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                echo 'Running E2E tests'
                dir('tests') {
                    sh '''
                        docker-compose -f docker-compose-jenkins.yml run --rm test-runner \
                            pytest e2e/ -v --junitxml=results/junit-e2e.xml
                    '''
                }
            }
        }
    }
    
    post {
        always {
            junit 'tests/results/junit-*.xml'
            sh 'docker-compose -f tests/docker-compose-jenkins.yml down || true'
        }
    }
}
```

**Pros:**
- ✅ Fast feedback (unit tests)
- ✅ Comprehensive when needed (integration/E2E)
- ✅ Resource efficient

**Cons:**
- ⚠️ More complex pipeline logic

---

## Required Changes to Test Suite

### 1. Update API Client for Service Discovery

```python
# tests/utils/api_client_jenkins.py

import os

class JenkinsAPIClient(APIClient):
    """API client that works with Docker service names."""
    
    def __init__(self, service_name: str, port: int, test_mode: bool = True):
        # In Jenkins/Docker, use service name instead of localhost
        base_url = f"http://{service_name}:{port}"
        super().__init__(base_url, test_mode)
        
        # Add encryption support
        self.app_secret_key = os.getenv("APP_SECRET_KEY")
        self.api_key = os.getenv("api_key")
        
        if self.api_key:
            self.session.headers.update({
                'X-API-Key': self.api_key
            })


class JenkinsTaskServiceClient(JenkinsAPIClient):
    """TaskService client for Jenkins environment."""
    
    def __init__(self):
        service_name = os.getenv("TASKSERVICE_SERVICE_NAME", "taskservice")
        port = int(os.getenv("TASKSERVICE_PORT", "2235"))
        super().__init__(service_name, port)


class JenkinsReqRouterClient(JenkinsAPIClient):
    """ReqRouter client for Jenkins environment."""
    
    def __init__(self):
        service_name = os.getenv("REQ_ROUTER_SERVICE_NAME", "req-router")
        port = int(os.getenv("REQ_ROUTER_PORT", "8888"))
        super().__init__(service_name, port)
```

### 2. Update conftest.py

```python
# tests/conftest.py - Add this section

import os

# Detect if running in Jenkins/Docker environment
IS_JENKINS = os.getenv("JENKINS_HOME") or os.getenv("CI") == "true"
IS_DOCKER = os.path.exists("/.dockerenv")

@pytest.fixture(scope="session")
def taskservice_client_factory(test_config):
    """Factory that creates appropriate client based on environment."""
    if IS_JENKINS or IS_DOCKER:
        from utils.api_client_jenkins import JenkinsTaskServiceClient
        return JenkinsTaskServiceClient()
    else:
        from utils.api_client import TaskServiceClient
        return TaskServiceClient(test_config["taskservice_url"])

# Similar for req_router_client_factory
```

### 3. Service Health Check for Jenkins

```bash
# tests/ci/wait-for-services-jenkins.sh
#!/bin/bash
# Wait for services using Docker service names

set -e

SERVICES=(
    "elasticsearch:9200/_cluster/health"
    "taskservice:2235/health"
    "req-router:8888/health"
)

MAX_RETRIES=30
RETRY_DELAY=5

for service_endpoint in "${SERVICES[@]}"; do
    IFS=':' read -r service rest <<< "$service_endpoint"
    IFS='/' read -r port path <<< "$rest"
    
    echo "Waiting for $service at $service:$port/$path..."
    
    for i in $(seq 1 $MAX_RETRIES); do
        if curl -sf "http://$service:$port/$path" > /dev/null 2>&1; then
            echo "✓ $service is ready"
            break
        fi
        
        if [ $i -eq $MAX_RETRIES ]; then
            echo "✗ $service did not become ready"
            exit 1
        fi
        
        echo "Attempt $i/$MAX_RETRIES failed, retrying in ${RETRY_DELAY}s..."
        sleep $RETRY_DELAY
    done
done

echo "All services are ready!"
```

---

## Recommended Approach

**For Your Setup, I recommend Option 1 + Option 3 Hybrid:**

1. **For PR/Branch builds**: Run Option 3 (fast unit tests only)
2. **For main/master**: Run Option 1 (full integration with existing services)
3. **For releases**: Run Option 2 (isolated full stack)

### Implementation Steps

1. **Week 1: Setup Option 3 (Unit Tests)**
   ```bash
   cd tests
   cp Jenkinsfile Jenkinsfile.unit
   # Edit to only run unit tests
   ```

2. **Week 2: Setup Option 1 (Integration with services)**
   ```bash
   # Create docker-compose-jenkins.yml
   # Test with existing dev/staging environment
   ```

3. **Week 3: Add Option 2 (Isolated stack) for releases**
   ```bash
   # Create docker-compose-jenkins-isolated.yml
   # Setup as release gate
   ```

This gives you **fast feedback** (unit tests in <5 min) while ensuring **comprehensive testing** before production.

Would you like me to create the specific files for any of these options?

