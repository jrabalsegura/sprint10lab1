pipeline {
    agent any
    environment {
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        AWS_ECR_CREDENTIALS_ID = 'aws-ecr-credentials'
        ECR_REGISTRY = '149032109728.dkr.ecr.eu-west-1.amazonaws.com/proyectofinal'
        IMAGE_NAME = "gallasmur/mi-aplicacion-flask-${BRANCH_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Paso 1: Clonar el repositorio
                checkout scm
            }
        }

        stage('Setup and Test') {
            
            steps {
                // Paso 2: Instalar dependencias desde requirements.txt
                sh '''
                pip install -r requirements.txt
                '''

                // Paso 3: Ejecutar tests
                sh '''
                pytest tests/test.py
                '''

                // Paso 4: Comprobar que cobertura es mayor al 80%
                sh '''
                pytest --cov=app tests/test.py --cov-report term --cov-fail-under=80
                '''
            }
        }

        stage('Linting') {
            steps {
                sh 'flake8 app/'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {

                    if (env.BRANCH_NAME == 'main') {                      
                        docker.build("${IMAGE_NAME}:${env.BUILD_ID}")                 
                    } else {
                         docker.build("${IMAGE_NAME}:latest")
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    def imageTag = "${env.BUILD_ID}"
                    def dockerImageName = "${IMAGE_NAME}:${imageTag}"
                    def ecrImageName = "${ECR_REGISTRY}:${imageTag}"

                    if (env.BRANCH_NAME == 'main') {
                        
                        // Etiquetar la imagen para Amazon ECR
                        sh("docker tag ${dockerImageName} ${ecrImageName}")
                        
                        withAWS(credentials: AWS_ECR_CREDENTIALS_ID, region: 'eu-west-1') {
                            sh "aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                            docker.image(ecrImageName).push()
                        }
                    } else {
                        docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                            docker.image("${IMAGE_NAME}:latest").push()
                        }
                    }
                }
            }
        }
    }
}

