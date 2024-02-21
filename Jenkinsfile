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
                // Paso 2: Configurar un entorno virtual y activarlo
                sh '''
                apt-get install python3-venv
                python3 -m venv venv
                source venv/bin/activate
                '''

                // Paso 3: Instalar dependencias desde requirements.txt
                sh '''
                pip install -r requirements.txt
                '''

                // Paso 4: Ejecutar tests
                sh '''
                pytest test/test.py
                '''
            }
        }
    }
}

