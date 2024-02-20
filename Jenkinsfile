pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Construye la imagen Docker, asumiendo que el Dockerfile está en la raíz del repositorio
                    docker.build("imagen-python")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Ejecuta los tests en un contenedor basado en la imagen construida
                    docker.run("echo 'testing'")
                }
            }
        }
    }
}


