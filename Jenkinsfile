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
                // Paso 3: Instalar dependencias desde requirements.txt
                sh '''
                pip install -r requirements.txt
                '''

                // Paso 4: Ejecutar tests
                sh '''
                pytest tests/test.py
                '''
            }
        }
    }
}

