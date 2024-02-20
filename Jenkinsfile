pipeline {
    agent any

    stages {
        stage('Setup Python Environment') {
            steps {
                // Crea un entorno virtual de Python e instala las dependencias
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install pytest
                '''
            }
        }

        stage('Checkout') {
            steps {
                // Este comando clona tu repositorio de GitHub
                checkout scm
            }
        }

        stage('Test') {
            steps {
                // Activa el entorno virtual y ejecuta tus pruebas
                sh '''
                . venv/bin/activate
                python -m pytest test.py
                '''
            }
        }
    }
}

