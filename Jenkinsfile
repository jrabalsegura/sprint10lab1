pipeline {
    agent any

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
    }
}

