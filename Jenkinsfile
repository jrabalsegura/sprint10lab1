pipeline {
    agent any
    environment {
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        AWS_ECR_CREDENTIALS_ID = 'aws-ecr-credentials'
        ECR_REGISTRY = '149032109728.dkr.ecr.eu-west-1.amazonaws.com/proyectofinal'
        IMAGE_NAME = "gallasmur/mi-aplicacion-flask-${getGitBranchName()}"
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
                    // Paso 5: Construir la imagen Docker
                    docker.build("${IMAGE_NAME}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    
                    def branchName = getGitBranchName()
                    def imageTag = "${env.BUILD_ID}"
                    def dockerImageName = "gallasmur/mi-aplicacion-flask-${branchName}:${imageTag}"
                    def ecrImageName = "${ECR_REGISTRY}/mi-aplicacion-flask-${branchName}:${imageTag}"

                    if (branchName == 'main') {
                        
                        // Etiquetar la imagen para Amazon ECR
                        sh("docker tag ${dockerImageName} ${ecrImageName}")
                        
                        withAWS(credentials: AWS_ECR_CREDENTIALS_ID, region: 'eu-west-1') {
                            sh "aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                            sh "docker push ${ecrImageName}"
                        }
                    } else {
                        // Iniciar sesión en el registro Docker
                        docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                            // Empujar la imagen al registro Docker
                            docker.image("gallasmur/mi-aplicacion-flask-${getGitBranchName()}:${env.BUILD_ID}").push()
                        }
                    }
                }
            }
        }
    }
}

def getGitBranchName() {
    return scm.branches[0].name.substring(2)
}

