// Jenkins Pipeline for E2E Tests (API Only)
// Runs API-based E2E tests against dev.dagknows.com or configured environment
// Repository: tests (not dagknows_src)

pipeline {
    agent {
        node {
            label 'docker'  // Use existing Docker agent - dependencies installed in venv
        }
    }

    environment {
        // Test environment configuration
        TEST_ENV = "${params.TEST_ENV ?: 'dev'}"
        DAGKNOWS_URL = "${params.DAGKNOWS_URL ?: 'https://dev.dagknows.com'}"
        DAGKNOWS_PROXY = "${params.DAGKNOWS_PROXY ?: '?proxy=dev1'}"
        
        // Test execution options
        TEST_MARKERS = "${params.TEST_MARKERS ?: 'api'}"  // Default to API tests only
        
        // Directories (tests repository structure)
        E2E_DIR = "${WORKSPACE}/e2e_tests"
        REPORTS_DIR = "${WORKSPACE}/e2e_tests/reports"
    }

    parameters {
        choice(
            name: 'TEST_ENV',
            choices: ['dev', 'staging', 'prod'],
            description: 'Target environment for E2E tests'
        )
        string(
            name: 'DAGKNOWS_URL',
            defaultValue: 'https://dev.dagknows.com',
            description: 'Base URL for DagKnows application'
        )
        string(
            name: 'DAGKNOWS_PROXY',
            defaultValue: '?proxy=dev1',
            description: 'Proxy parameter for requests'
        )
        string(
            name: 'TEST_MARKERS',
            defaultValue: 'api',
            description: 'Pytest markers to filter tests (e.g., "api and not slow")'
        )
        string(
            name: 'BRANCH',
            defaultValue: 'main',
            description: 'Git branch to checkout'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'yash-dagknows-github-pat', usernameVariable: 'USERNAME', passwordVariable: 'GIT_TOKEN')]) {
                        sh """
                        git clone -b ${params.BRANCH} https://"\$GIT_TOKEN":x-oauth-basic@github.com/dagknows/tests.git
                        cd tests
                        """
                    }
                }
            }
        }

        stage('Setup Test Environment') {
            steps {
                dir("${env.E2E_DIR}") {
                    script {
                        echo "Setting up Python virtual environment..."
                        echo "Installing all dependencies (API + UI tests) in venv..."
                        sh """
                        python3 -m venv venv || python3 -m virtualenv venv
                        source venv/bin/activate
                        pip install --upgrade pip
                        # Install all dependencies including Playwright (for future UI tests)
                        pip install -r requirements.txt
                        # Install Playwright browsers (even though we'll run API tests first)
                        # This ensures everything is ready when we enable UI tests later
                        playwright install chromium || echo "Playwright browser install skipped (will install per-user if needed)"
                        """
                    }
                }
            }
        }

        stage('Configure Test Environment') {
            steps {
                dir("${env.E2E_DIR}") {
                    script {
                        // Get JWT token from Jenkins credentials
                        withCredentials([string(credentialsId: 'dagknows-jwt-token', variable: 'JWT_TOKEN')]) {
                            sh """
                            # Create .env file from template
                            cp env.template .env
                            
                            # Set environment variables
                            echo "DAGKNOWS_URL=${env.DAGKNOWS_URL}" >> .env
                            echo "DAGKNOWS_PROXY=${env.DAGKNOWS_PROXY}" >> .env
                            echo "DAGKNOWS_TOKEN=\${JWT_TOKEN}" >> .env
                            echo "TEST_USER_EMAIL=test@dagknows.com" >> .env
                            echo "TEST_USER_PASSWORD=test_password" >> .env
                            """
                        }
                    }
                }
            }
        }

        stage('Run API E2E Tests') {
            steps {
                dir("${env.E2E_DIR}") {
                    script {
                        // Ensure reports directory exists
                        sh "mkdir -p ${env.REPORTS_DIR}"
                        
                        def markerFilter = env.TEST_MARKERS ? "-m '${env.TEST_MARKERS}'" : "-m 'api'"
                        sh """
                        source venv/bin/activate
                        pytest api_tests/ -v \\
                            --html=${env.REPORTS_DIR}/api-report.html \\
                            --self-contained-html \\
                            --junitxml=${env.REPORTS_DIR}/api-junit.xml \\
                            ${markerFilter} || true
                        """
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: "${env.REPORTS_DIR}/api-report.html, ${env.REPORTS_DIR}/api-junit.xml"
                }
            }
        }

        // UI E2E Tests Stage (commented out - will be enabled later)
        // Uncomment this stage when ready to run UI tests
        // 
        // When uncommenting, use this stage:
        // stage('Run UI E2E Tests') {
        //     steps {
        //         dir("${env.E2E_DIR}") {
        //             script {
        //                 sh "mkdir -p ${env.REPORTS_DIR}"
        //                 sh """
        //                 export DISPLAY=:99
        //                 Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
        //                 """
        //                 def markerFilter = env.TEST_MARKERS ? "-m '${env.TEST_MARKERS}'" : "-m 'ui'"
        //                 sh """
        //                 source venv/bin/activate
        //                 pytest ui_tests/ -v \\
        //                     --html=${env.REPORTS_DIR}/ui-report.html \\
        //                     --self-contained-html \\
        //                     --junitxml=${env.REPORTS_DIR}/ui-junit.xml \\
        //                     ${markerFilter} || true
        //                 """
        //             }
        //         }
        //     }
        //     post {
        //         always {
        //             archiveArtifacts artifacts: "${env.REPORTS_DIR}/ui-report.html, ${env.REPORTS_DIR}/ui-junit.xml"
        //             archiveArtifacts artifacts: "${env.REPORTS_DIR}/screenshots/"
        //         }
        //     }
        // }
    }

    post {
        always {
            script {
                // Publish test results
                junit allowEmptyResults: true, testResults: "${env.REPORTS_DIR}/**/*.xml"
                
                // Publish HTML reports
                publishHTML([
                    reportDir: "${env.REPORTS_DIR}",
                    reportFiles: 'api-report.html',  // Add 'ui-report.html' when UI tests are enabled
                    reportName: 'E2E Test Report',
                    keepAll: true
                ])
            }
        }
        success {
            echo "✅ E2E API tests completed successfully"
        }
        failure {
            echo "❌ E2E API tests failed - check reports for details"
            // Optionally send notifications (Slack, email, etc.)
        }
        unstable {
            echo "⚠️ E2E API tests completed with warnings"
        }
    }
}

