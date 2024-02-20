pipeline {
    agent any

    tools {
        // Asegúrate de tener python y pytest instalados en el agente donde se ejecutará esto
        python 'Python3'
    }

    stages {
        stage('Checkout') {
            steps {
                // Este comando clona tu repositorio de GitHub
                checkout scm
            }
        }

        stage('Test') {
            steps {
                // Ejecuta tu archivo de pruebas
                sh 'echo "Test stage"'
            }
        }
    }
}
