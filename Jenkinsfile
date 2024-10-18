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
    stage('SonarQube analysis') {
            agent {
                docker {
                  image 'sonarsource/sonar-scanner-cli:5.0.1'
                }
               }
               environment {
        CI = 'true'
        //  scannerHome = tool 'Sonar'
        scannerHome='/opt/sonar-scanner'
    }
            steps{
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner"
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
