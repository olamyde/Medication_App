pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = 'docker-login'
        SSH_CREDENTIALS = 'ssh-credentials'
        GITHUB_CREDENTIALS = 'github-ssh'
        DOCKER_HUB_USERNAME = "olamyde"
        APPLICATION_NAME = "medication_search"
        APPLICATION_TAG = "latest"
        SONARQUBE_SERVER = 'SonarQube' // Define the SonarQube server name configured in Jenkins
        SONARQUBE_PROJECT_KEY = 'MedicationApp' // Define the SonarQube project key
        SONARQUBE_SCANNER = 'SonarQubeScanner' // Define the SonarQube Scanner tool name
    }
    stages {
        stage('SonarQube analysis') {
            steps {
                script {
                    // Pull and run the SonarQube scanner Docker image
                    docker.image('sonarsource/sonar-scanner-cli:5.0.1').inside {
                        withSonarQubeEnv('SonarQube') {
                            sh """
                                sonar-scanner \
                                -Dsonar.projectKey=${env.SONARQUBE_PROJECT_KEY} \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=${env.SONARQUBE_SERVER}
                            """
                        }
                    }
                }
            }
        }
        stage('Checking the code') {
            steps {
                script {
                    // List the directory contents to verify the workspace
                    sh 'ls -l'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image and tag it appropriately
                    sh """
                        docker build -t ${env.DOCKER_HUB_USERNAME}/${env.APPLICATION_NAME}:${env.APPLICATION_TAG} .
                        docker images | grep ${env.APPLICATION_TAG}
                    """
                }
            }
        }
        stage('Docker Login') {
            steps {
                script {
                    // Login to DockerHub using stored credentials
                    withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    }
                }
            }
        }
        stage('Pushing Application to DockerHub') {
            steps {
                script {
                    // Push the Docker image to DockerHub
                    sh "docker push ${env.DOCKER_HUB_USERNAME}/${env.APPLICATION_NAME}:${env.APPLICATION_TAG}"
                }
            }
        }
        stage('Deploy to Server') {
            steps {
                script {
                    // Deploy the application by running it as a Docker container
                    sh """
                        docker run -itd -p 5001:5000 --name ${env.APPLICATION_NAME} ${env.DOCKER_HUB_USERNAME}/${env.APPLICATION_NAME}:${env.APPLICATION_TAG}
                        docker ps | grep ${env.APPLICATION_NAME}
                    """
                }
            }
        }
    }
    post {
        always {
            // Clean the workspace after each build
            cleanWs()
        }
    }
}
