// Jenkinsfile for DagKnows Test Suite
// This pipeline runs the test suite in Jenkins CI/CD

pipeline {
    agent any
    
    // Environment variables
    environment {
        // Test environment configuration
        TESTING = 'true'
        FLASK_ENV = 'testing'
        PYTHONUNBUFFERED = '1'
        
        // Service URLs (adjust for your Jenkins environment)
        DAGKNOWS_ELASTIC_URL = 'http://elasticsearch:9200'
        DAGKNOWS_TASKSERVICE_URL = 'http://taskservice:2235'
        DAGKNOWS_REQ_ROUTER_URL = 'http://req-router:8888'
        
        // Database configuration
        POSTGRESQL_DB_HOST = 'postgres'
        POSTGRESQL_DB_PORT = '5432'
        POSTGRESQL_DB_NAME = 'dagknows_test'
        POSTGRESQL_DB_USER = 'postgres'
        POSTGRESQL_DB_PASSWORD = credentials('postgres-test-password')
        
        // Test configuration
        ENFORCE_LOGIN = 'false'
        ALLOW_DK_USER_INFO_HEADER = 'true'
        
        // Report paths
        JUNIT_REPORT = 'tests/results/junit.xml'
        COVERAGE_REPORT = 'tests/results/coverage.xml'
        HTML_REPORT = 'tests/results/htmlcov'
    }
    
    // Build parameters
    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'unit', 'integration', 'e2e', 'smoke'],
            description: 'Which test suite to run'
        )
        booleanParam(
            name: 'RUN_COVERAGE',
            defaultValue: true,
            description: 'Generate coverage report'
        )
        booleanParam(
            name: 'PARALLEL_EXECUTION',
            defaultValue: false,
            description: 'Run tests in parallel'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up test environment...'
                dir('tests') {
                    sh '''
                        # Create virtual environment
                        python3 -m venv venv
                        . venv/bin/activate
                        
                        # Upgrade pip
                        pip install --upgrade pip
                        
                        # Install dependencies
                        pip install -r requirements.txt
                        
                        # Create necessary directories
                        mkdir -p results logs
                        
                        # Copy environment file
                        cp .env.test.example .env.test || true
                    '''
                }
            }
        }
        
        stage('Start Services') {
            steps {
                echo 'Starting test services...'
                dir('tests') {
                    sh '''
                        # Start services using docker-compose
                        docker-compose -f docker-compose-test.yml up -d
                        
                        # Wait for services to be ready
                        ./utils/wait-for-services.sh
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    dir('tests') {
                        sh '. venv/bin/activate'
                        
                        // Determine which tests to run
                        def pytest_args = '-v --color=yes'
                        
                        // Add JUnit XML output
                        pytest_args += " --junitxml=${JUNIT_REPORT}"
                        
                        // Add coverage if requested
                        if (params.RUN_COVERAGE) {
                            pytest_args += " --cov=../taskservice/src --cov=../req_router/src"
                            pytest_args += " --cov-report=xml:${COVERAGE_REPORT}"
                            pytest_args += " --cov-report=html:${HTML_REPORT}"
                            pytest_args += " --cov-report=term"
                        }
                        
                        // Add parallel execution if requested
                        if (params.PARALLEL_EXECUTION) {
                            pytest_args += " -n auto"
                        }
                        
                        // Select test suite
                        def test_path = ''
                        switch(params.TEST_SUITE) {
                            case 'unit':
                                test_path = 'unit/'
                                break
                            case 'integration':
                                test_path = 'integration/'
                                break
                            case 'e2e':
                                test_path = 'e2e/'
                                break
                            case 'smoke':
                                pytest_args += ' -m smoke'
                                break
                            default:
                                test_path = ''
                        }
                        
                        echo "Running tests with: pytest ${pytest_args} ${test_path}"
                        
                        // Run tests
                        sh """
                            . venv/bin/activate
                            cd tests
                            pytest ${pytest_args} ${test_path} || true
                        """
                    }
                }
            }
        }
        
        stage('Analyze Results') {
            steps {
                echo 'Analyzing test results...'
                // This stage can be extended with additional analysis
            }
        }
    }
    
    post {
        always {
            // Publish test results
            junit allowEmptyResults: true, testResults: "${JUNIT_REPORT}"
            
            // Publish coverage report
            script {
                if (params.RUN_COVERAGE && fileExists("${COVERAGE_REPORT}")) {
                    publishCoverage adapters: [
                        coberturaAdapter("${COVERAGE_REPORT}")
                    ]
                    
                    // Archive HTML coverage report
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: "${HTML_REPORT}",
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
            
            // Archive test logs
            archiveArtifacts artifacts: 'tests/logs/**/*.log', allowEmptyArchive: true
            archiveArtifacts artifacts: 'tests/results/**/*', allowEmptyArchive: true
            
            // Stop and cleanup test services
            dir('tests') {
                sh '''
                    docker-compose -f docker-compose-test.yml down -v || true
                '''
            }
            
            // Cleanup workspace
            cleanWs(
                deleteDirs: true,
                patterns: [
                    [pattern: 'tests/venv/', type: 'INCLUDE'],
                    [pattern: 'tests/.pytest_cache/', type: 'INCLUDE'],
                    [pattern: 'tests/__pycache__/', type: 'INCLUDE']
                ]
            )
        }
        
        success {
            echo 'Tests passed successfully!'
            // Add notifications here (e.g., Slack, email)
        }
        
        failure {
            echo 'Tests failed!'
            // Add failure notifications here
        }
        
        unstable {
            echo 'Tests are unstable!'
            // Add unstable notifications here
        }
    }
}

