pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = 'docker-login'
        SSH_CREDENTIALS = 'ssh-credentials'
        GITHUB_CREDENTIALS = 'github-ssh'
        DOCKER_HUB_USERNAME = "olamyde"
        APPLICATION_NAME = "medication_search"
        APPLICATION_TAG = "latest"
        SONARQUBE_SERVER = 'Sonerqube' // Define the SonarQube server name configured in Jenkins
        SONARQUBE_PROJECT_KEY = 'MedicationApp' // Define the SonarQube project key
        SONARQUBE_SCANNER = 'SonarQubeScanner' // Define the SonarQube Scanner tool name
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'git@github.com:olamyde/Medication_App.git'
            }
        }
        stage('SonarQube Code Analysis') {
            steps {
                script {
                    withSonarQubeEnv(env.SONARQUBE_SERVER) {
                        sh "${env.SONARQUBE_SCANNER} -Dsonar.projectKey=${env.SONARQUBE_PROJECT_KEY} -Dsonar.sources=. -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.login=${SONAR_AUTH_TOKEN}"
                    }
                }
            }
        }
        stage('Checking the code') {
            steps {
                script {
                    sh 'ls -l'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t ${env.DOCKER_HUB_USERNAME}/${env.APPLICATION_NAME}:${env.APPLICATION_TAG} .
                        docker images | grep ${env.APPLICATION_TAG}
                    """
                }
            }
        }
        stage('Docker Login into') {
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        // Use Docker CLI to login
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
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
                script {
                    sh """
                        # docker run -itd -p 5001:5000 --name medication_search ${env.DOCKER_HUB_USERNAME}/${env.APPLICATION_NAME}:${env.APPLICATION_TAG}
                        # docker ps |grep ${env.APPLICATION_NAME}
                    """
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
