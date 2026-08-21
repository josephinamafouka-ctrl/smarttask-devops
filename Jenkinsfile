pipeline {
    agent any

    environment {
        // Remplacez par votre propre namespace Docker Hub
        DOCKERHUB_NAMESPACE = "mountou"
        IMAGE_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Récupération du code source depuis GitHub...'
                checkout scm
            }
        }

        stage('Build des images Docker') {
            steps {
                echo 'Construction des images Docker (frontend, backend, database)...'
                sh """
                    docker build -t ${DOCKERHUB_NAMESPACE}/smarttask-backend:${IMAGE_TAG} ./backend
                    docker build -t ${DOCKERHUB_NAMESPACE}/smarttask-frontend:${IMAGE_TAG} ./frontend
                    docker build -t ${DOCKERHUB_NAMESPACE}/smarttask-database:${IMAGE_TAG} ./database
                """
            }
        }

        stage('Tag latest') {
            steps {
                echo 'Attribution du tag latest en plus du tag de version...'
                sh """
                    docker tag ${DOCKERHUB_NAMESPACE}/smarttask-backend:${IMAGE_TAG} ${DOCKERHUB_NAMESPACE}/smarttask-backend:latest
                    docker tag ${DOCKERHUB_NAMESPACE}/smarttask-frontend:${IMAGE_TAG} ${DOCKERHUB_NAMESPACE}/smarttask-frontend:latest
                    docker tag ${DOCKERHUB_NAMESPACE}/smarttask-database:${IMAGE_TAG} ${DOCKERHUB_NAMESPACE}/smarttask-database:latest
                """
            }
        }

        stage('Connexion à Docker Hub') {
            steps {
                echo 'Authentification auprès du registre Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    sh 'echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin'
                }
            }
        }

        stage('Publication sur Docker Hub') {
            steps {
                echo 'Envoi des images vers Docker Hub...'
                sh """
                    docker push ${DOCKERHUB_NAMESPACE}/smarttask-backend:${IMAGE_TAG}
                    docker push ${DOCKERHUB_NAMESPACE}/smarttask-backend:latest
                    docker push ${DOCKERHUB_NAMESPACE}/smarttask-frontend:${IMAGE_TAG}
                    docker push ${DOCKERHUB_NAMESPACE}/smarttask-frontend:latest
                    docker push ${DOCKERHUB_NAMESPACE}/smarttask-database:${IMAGE_TAG}
                    docker push ${DOCKERHUB_NAMESPACE}/smarttask-database:latest
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline exécuté avec succès : images publiées avec le tag ${IMAGE_TAG} et latest."
        }
        failure {
            echo "Le pipeline a échoué. Consultez les journaux ci-dessus pour identifier l'étape en erreur."
        }
        always {
            echo 'Déconnexion de Docker Hub...'
            sh 'docker logout || true'
        }
    }
}
