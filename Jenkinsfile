pipeline {
    agent any
    options {
        timeout(time: 15, unit: 'MINUTES')
    }
    environment {
        PATH = "C:\\Users\\DELL\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;C:\\Program Files\\Python313\\Scripts;${env.PATH}"
        DOCKER_HOST = 'tcp://localhost:2375'
        KUBECONFIG = 'C:\\Users\\DELL\\.kube\\config'
    }
    stages {
        stage('Automated Selenium Testing') {
            steps {
                echo "Running Selenium Tests using pytest"
                bat 'pip install -r requirements.txt'
                
                // Kill any stale python processes before starting
                bat 'taskkill /F /IM python.exe > nul 2>&1 || exit 0'
                
                // Start Flask app in background cleanly detached from stdout/stderr
                bat 'start "" /B python app.py'
                bat 'ping 127.0.0.1 -n 5 > nul'
                bat 'python -m pytest -v tests/test_portal.py'
            }
            post {
                always {
                    // Ensure Flask server is stopped even if tests fail
                    bat 'taskkill /F /IM python.exe > nul 2>&1 || exit 0'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                echo "Build Docker Image"
                bat "docker build -t purebites:v1 ."
            }
        }
        stage('Docker Login') {
            steps {
                bat 'docker login -u hanisha99 -p hanisha@09032006'
            }
        }
        stage('Push to Docker Registry') {
            steps {
                echo "Push Docker Image to Docker Hub"
                bat "docker tag purebites:v1 hanisha99/hanisha_s_28:purebites-v1"
                bat "docker push hanisha99/hanisha_s_28:purebites-v1"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }
    post {
        success {
            echo 'Case Study Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
