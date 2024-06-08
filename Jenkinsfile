pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS= 'dockerhub-credentials'
	    SSH_CREDENTIALS= 'ssh-credentials'
	    GITHUB_CREDENTIALS = 'github-ssh-key'
        DOCKER_HUB_USERNAME="olamyde"
        APPLICATION_NAME="medication_search"
	    APPLICATION_TAG="latest"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'git@github.com:olamyde/Medication_App.git', credentialsId: 'github-ssh-key'
                }
            }
        }
        stage('Checking the code') {
            steps {
                script {
                    sh """
                        ls -l
                    """ 
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t ${env.DOCKER_HUB_USERNAME}/${env.APPLICATION_NAME}:${env.APPLICATION_TAG} .
                        docker images |grep ${env.APPLICATION_TAG}
                    """ 
                }
            }
        }
        stage('Docker Login into') {
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        // Use Docker CLI to login
                        sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                    }
                }
            }
        }
        stage('Pushing Application into DockerHub') {
            steps {
                script {
                    sh """
                        docker push ${env.DOCKER_HUB_USERNAME}/${env.APPLICATION_NAME}:${env.APPLICATION_TAG}
                    """
                }
            }
        }
        stage('Deploy to Server') {
            steps {
                sshagent(credentials: ['SSH_CREDENTIALS']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no $olamyde@$S127.0.0.1 << EOF
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
