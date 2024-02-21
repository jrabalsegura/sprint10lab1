pipeline {
    agent any
    environment {
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
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
                    docker.build("mi-aplicacion-flask:${env.BUILD_ID}")
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main' 
            }
            steps {
                script {
                    // Iniciar sesión en el registro Docker (ajustar según sea necesario)
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                        // Empujar la imagen al registro Docker
                        docker.image("mi-aplicacion-flask:${env.BUILD_ID}").push()
                    }
                }
            }
        }
    }
}

