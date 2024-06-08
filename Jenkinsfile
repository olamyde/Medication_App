pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        SSH_CREDENTIALS = credentials('ssh-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                git 'git@github.com:olamyde/Medication_App.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("olamyde/medication_search:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'DOCKERHUB_CREDENTIALS') {
                        docker.image("olamyde/medication_search:latest").push()
                    }
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                sshagent(credentials: ['SSH_CREDENTIALS']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no $SSH_USER@$SSH_HOST << EOF
                    docker pull olamyde/medication_search:latest
                    docker stop medication_search || true
                    docker rm medication_search || true
                    docker run -d -p 80:5000 --name medication_search olamyde/medication_search:latest
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
