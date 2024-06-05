pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SSH_CREDENTIALS = credentials('ssh-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("your-dockerhub-username/medication-search:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'DOCKERHUB_CREDENTIALS') {
                        docker.image("your-dockerhub-username/medication-search:latest").push()
                    }
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                sshagent(credentials: ['SSH_CREDENTIALS']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no $SSH_USER@$SSH_HOST << EOF
                    docker pull your-dockerhub-username/medication-search:latest
                    docker stop medication-search || true
                    docker rm medication-search || true
                    docker run -d -p 80:5000 --name medication-search your-dockerhub-username/medication-search:latest
                    EOF
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
