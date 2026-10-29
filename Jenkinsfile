pipeline {
    agent any
    environment {
        PATH = "C:\\Users\\DELL\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;C:\\Program Files\\Python313\\Scripts;${env.PATH}"
        DOCKER_HOST = 'tcp://localhost:2375'
        KUBECONFIG = 'C:\\Users\\DELL\\.kube\\config'
    }
    stages {
        stage('Automated Selenium Testing') {
            steps {
                echo "Running Selenium Tests using pytest"
                bat 'pip install --default-timeout=1000 -r requirements.txt'
                
                // NEW FAILSAFE: Kill old ghost processes before starting, ignore errors if none exist
                bat 'taskkill /F /IM python.exe || exit 0'
                
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 5 > nul'
                bat 'python -m pytest -v tests/test_portal.py'
                bat 'taskkill /F /IM python.exe'
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