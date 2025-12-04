// Simple Jenkins Pipeline for Quick Test Runs
// Use this for fast feedback during development

pipeline {
    agent any
    
    stages {
        stage('Quick Tests') {
            steps {
                echo 'Running quick unit tests...'
                dir('tests') {
                    sh '''
                        pip install -r requirements.txt
                        pytest unit/ -v -m "unit and not slow" --tb=short
                    '''
                }
            }
        }
    }
    
    post {
        always {
            junit allowEmptyResults: true, testResults: 'tests/results/junit.xml'
        }
    }
}

