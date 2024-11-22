pipeline { 
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = 'Docker-login'
        SSH_CREDENTIALS = 'ssh-credentials'
        GITHUB_CREDENTIALS = 'Github-ssh'
        DOCKER_HUB_USERNAME = "olamyde"
        APPLICATION_NAME = "medication_search"
        APPLICATION_TAG = "latest"
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
        timeout(time: 60, unit: 'MINUTES')
        timestamps()
    }
    stages {
        stage('testing') {
            agent {
                docker {
                    image 'python:latest'
                    // label 'docker-agent'
                }
            }
            steps {
                sh '''
                    cd ${WORKSPACE}
                    python 
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                sh '''
                export PATH=$PATH:/opt/sonarqube/sonar-scanner-5.0.1.3006/bin
                sonar-scanner -Dsonar.projectKey=Medication_App -Dsonar.host.url=http://172.20.2.221:9000/
                '''
            }
        }
    }   
        stage('Docker Login') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    }
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
        
        stage('Push Application to DockerHub') {
            steps {
                script {
                    sh "docker push ${env.DOCKER_HUB_USERNAME}/${env.APPLICATION_NAME}:${env.APPLICATION_TAG}"
                }
            }
        }
        
        stage('Deploy to Server') {
            steps {
                script {
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
            cleanWs()
        }
    }
}
