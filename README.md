# Creación de un entorno local de desarrollo

Parte 1 del proyecto final de Bootcamp Devops. Instrucciones de desarrollo y testing local.

## Clonado del proyecto y testing

Para configurar un entorno de desarrollo local y comenzar a contribuir al proyecto, sigue estos pasos:

1. Clona el repositorio desde GitHub:

    ```bash
    git clone https://github.com/jrabalsegura/sprint10lab1.git
    ```

2. Instala las dependencias del proyecto:

    ```bash
    pip install -r requirements.txt
    ```

3. Para ejecutar los tests utiliza el siguiente comando:

    ```bash
    pytest tests/test.py
    ```

4. Para verificar que la cobertura de las pruebas es superior al 80%, ejecuta:

    ```bash
    pytest --cov=app tests/test.py --cov-report term --cov-fail-under=80
    ```

## Arquitectura del Software

La arquitectura de la solución se basa en proporcionar una infraestructura escalable, segura y eficiente, con alta disponibilidad, para desplegar una aplicación web moderna. Aquí se detallan los componentes principales:

- **Autoescalado y Balanceo de Carga**: Se implementa el Horizontal Pod Autoscaler para ajustar automáticamente el número de pods en función del uso de CPU.

- **Terminadores SSL**: Se utiliza AWS Elastic Load Balancer como terminador SSL.

- **Bases de Datos**: La base de datos PostgreSQL se despliega dentro del cluster de Kubernetes utilizando Persistent Volumes de Kubernetes.

- **Telemetría**: Cloudwatch de AWS para la recolección y almacenamiento de métricas, y Grafana para la visualización de las mismas.

Para obtener más detalles sobre la arquitectura, consulta la sección "Arquitectura de la Solución" en la memoria del proyecto.

## Ejecución del Entorno Local para Pruebas

Para lanzar el entorno de Kubernetes local para pruebas, utiliza el siguiente comando:

```bash
kubectl apply -f db-deployment.yaml,app-deployment.yaml,app-hpa.yaml,postgres-pvc.yaml
```

Una vez desplegado, puedes acceder a la aplicación en http://localhost:30007/data.

E interactuar con sus endpoints usando bien un navegador o una aplicación como Postman.

## Normas de Colaboración

- Crear un nuevo branch para cada desarrollo o bugfix.
- Modificar la línea 18 del fichero `app-deployment.yaml` con el nombre del contenedor Docker correspondiente al branch del desarrollador para realizar pruebas locales, sustituyendo la parte "kubectlbranch" con el nombre de tu propia rama:

```
image: gallasmur/mi-aplicacion-flask-kubectlbranch:latest
```

- Al finalizar el trabajo, crear una pull request a la rama `main`.
- Las pull requests serán revisadas por pares y aceptadas si superan la revisión.

Una vez se añada el código a rama main, nuestro pipeline Jenkins automáticamente creará una nueva imagen y la subirá al registro ECR de AWS en lugar de a Docker Hub, con lo que ésta podrá pasar a producción.

---

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

            // Verificar el despliegue
            sh "kubectl rollout status deployment/<nombre-de-tu-deployment>"
        }
    }
}

```

Además, en Terraform habrían quedado configurados servicios como CloudWatch y ELB, con lo que en esta pipeline solo nos ocupamríamos del despiegue al cluster EKS de la nueva versión de la aplicación.