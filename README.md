# Creación de Pipeline de CI

Parte 2 del proyecto final de Bootcamp Devops. Instrucciones de configuración y uso.

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado en una máquina Linux local:
- Docker
- AWS CLI
- Git

## Configuración del Entorno

### GitHub

Jenkins está configurado para hacer polling a GitHub cada 5 minutos utilizando la expresión "H/5 * * * *", detectando cambios en el repositorio para ejecutar el pipeline automáticamente.

### Jenkins

Para poder ejecutar la pipeline correctamente, necesitas instalar los siguientes plugins:
- AWS Pipeline
- Docker Pipeline

### Credenciales

Es necesario configurar las credenciales en Jenkins para:
- Docker Hub: Utilizado para empujar y extraer imágenes del Docker Hub, cuando se trata de una rama de desarrollo.
- AWS: Utilizado para interactuar con los servicios de AWS, incluyendo el Amazon Elastic Container Registry (ECR), cuando estamos en la rama main, y, por tanto, producción.

### Amazon ECR

Debes tener un repositorio ECR creado previamente en AWS para almacenar las imágenes Docker generadas por el pipeline, cuya dirección debe ir en la variable ECR_REGISTRY de Jenkinsfile.

## Configuración Local

Para ejecutar Jenkins localmente y trabajar con AWS y Docker, necesitarás configurar AWS CLI en tu PC. Sigue la [documentación oficial de AWS](https://aws.amazon.com/cli/) para configurar AWS CLI con tus credenciales de AWS.

Además el usuario jenkins debe tener permisos sobre el grupo docker (https://devops4solutions.com/integrate-jenkins-with-docker/).

## Despliegue de Imágenes Docker

Este proyecto está configurado para manejar el despliegue de imágenes Docker de forma diferenciada, dependiendo del branch en el que se realicen los cambios:

### Branch `main` (Producción)

- Las imágenes Docker generadas a partir de cambios en el branch `main` se consideran listas para producción.
- Estas imágenes se suben automáticamente a **Amazon Elastic Container Registry (ECR)**, siguiendo las mejores prácticas para el manejo de imágenes de producción.
- Para configurar este comportamiento, se utiliza el plugin AWS Pipeline en Jenkins, y se requieren credenciales de AWS adecuadamente configuradas.

### Otros Branches (Desarrollo)

- Las imágenes Docker generadas a partir de cambios en cualquier branch que no sea `main` se consideran versiones de desarrollo.
- Estas imágenes se suben automáticamente a **Docker Hub**, permitiendo a los desarrolladores probar la imagen en sus máquinas locales de forma rápida y sencilla.
- Para configurar este comportamiento, se utiliza el plugin Docker Pipeline en Jenkins, y se requieren credenciales de Docker Hub adecuadamente configuradas.

## Instrucciones de Configuración

Para habilitar el flujo de trabajo descrito anteriormente, asegúrate de seguir las instrucciones de configuración de credenciales y plugins mencionadas en las secciones [Credenciales](#credenciales), [Jenkins](#jenkins), [Amazon ECR](#amazon-ecr) y [Configuración Local](#configuración-local).

## Notas Importantes

- Asegúrate de que las políticas de IAM y los permisos de AWS estén correctamente configurados para permitir a Jenkins subir imágenes a ECR.
- Para Docker Hub, verifica que las credenciales proporcionadas a Jenkins tengan permisos para subir imágenes al repositorio correspondiente.

### Clonar el Repositorio

git clone https://github.com/jrabalsegura/sprint10lab1.git

## Despliegue posterior en EKS

Tras haber sido creada la infraestructura cómo código en Terraform, podríamos continuar el despliegue desde este mismo script Jenkins. El código podría ser algo así:

```groovy
stage('Deploy to EKS') {
    when {
        branch 'main'
    }
    steps {
        script {
            sh "aws eks --region eu-west-1 update-kubeconfig --name nombre-de-cluster-eks"

            // Habría que tener configurado el manifiesto de Kubernetes para que estuviera configurado con la etiqueta 'latest' y por lo tanto siempre apuntara a la imagen de producción más reciente.

            // Además en el manifiesto también indicariamos que el update será del tipo RollingUpdate

            // Aplicar el manifiesto al clúster de EKS
            sh "kubectl apply -f k8s/deployment.yaml"

            // Opcional: Verificar el despliegue
            sh "kubectl rollout status deployment/<nombre-de-tu-deployment>"
        }
    }
}

```

Además, en Terraform habrían quedado configurados servicios como CloudWatch y ELB, con lo que esta pipeline solo nos ocupamos del despiegue al cluster de la nueva versión de la aplicación.