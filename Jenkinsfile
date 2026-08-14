pipeline {

    agent any

    environment {
        APP_NAME   = "expense-tracker-enterprise"
        IMAGE_NAME = "chetan8889/expense-tracker-enterprise"
        DEPLOY_ENV = "DEV"
    }

    stages {

        stage('Workspace Verification') {
            steps {
                echo '========== Workspace =========='

                sh '''
                    pwd
                    ls -la
                '''
            }
        }

        stage('Build Information') {
            steps {
                echo '========== Build Information =========='

                echo "Build Number : ${env.BUILD_NUMBER}"
                echo "Job Name     : ${env.JOB_NAME}"
                echo "Branch Name  : ${env.BRANCH_NAME}"
                echo "Workspace    : ${env.WORKSPACE}"
                echo "Node Name    : ${env.NODE_NAME}"
            }
        }

        stage('Verify Python') {
            steps {
                echo '========== Python Verification =========='

                sh '''
                    python3 --version
                '''
            }
        }

        stage('Verify Docker') {
            steps {
                echo '========== Docker Verification =========='

                sh '''
                    docker --version
                    docker compose version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '========== Building Docker Image =========='

                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('List Docker Images') {
            steps {
                echo '========== Docker Images =========='

                sh '''
                    docker images | grep expense-tracker || true
                '''
            }
        }

        stage('Docker Hub Login') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                        -u "$DOCKER_USER" \
                        --password-stdin
                    '''

                }
            }
        }

        stage('Push Docker Image') {
            steps {

                echo '========== Pushing Docker Image =========='

                sh '''sed -i '' 's#080019754331.dkr.ecr.ap-south-1.amazonaws.com/expense-tracker:v1#chetan8889/expense-tracker-enterprise:latest#' kubernetes/deployment.yaml
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy to Amazon EKS') {

            when {
                branch 'main'
            }

            steps {

                echo '========== Deploying to Amazon EKS =========='

                withCredentials([

                    string(credentialsId: 'MYSQL_HOST', variable: 'MYSQL_HOST'),
                    string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
                    string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
                    string(credentialsId: 'MYSQL_DB', variable: 'MYSQL_DB'),
                    string(credentialsId: 'JWT_SECRET_KEY', variable: 'JWT_SECRET_KEY')

                ]) {

                    sh '''
                        export HOME=/var/lib/jenkins
                        export KUBECONFIG=/var/lib/jenkins/.kube/config
                        export AWS_DEFAULT_REGION=ap-south-1

                        echo "========== DEBUG =========="
                        whoami
                        echo "HOME=$HOME"
                        echo "KUBECONFIG=$KUBECONFIG"

                        aws --version
                        aws sts get-caller-identity

                        kubectl config current-context
                        kubectl get nodes

                        echo "Deleting old Kubernetes Secret..."

                        kubectl delete secret expense-tracker-secret --ignore-not-found

                        echo "Creating Kubernetes Secret..."

                        kubectl create secret generic expense-tracker-secret \
                          --from-literal=MYSQL_HOST="$MYSQL_HOST" \
                          --from-literal=MYSQL_USER="$MYSQL_USER" \
                          --from-literal=MYSQL_PASSWORD="$MYSQL_PASSWORD" \
                          --from-literal=MYSQL_DB="$MYSQL_DB" \
                          --from-literal=JWT_SECRET_KEY="$JWT_SECRET_KEY"

                        echo "Applying Kubernetes Manifests..."

                        kubectl apply -f kubernetes/

                        echo "Restarting Deployment..."

                        kubectl rollout restart deployment/expense-tracker

                        echo "Waiting for Rollout..."

                        kubectl rollout status deployment/expense-tracker
                    '''
                }
            }
        }

        stage('Health Check') {

            when {
                branch 'main'
            }

            steps {

                echo '========== Kubernetes Health Check =========='

                sh '''
                    export HOME=/var/lib/jenkins
                    export KUBECONFIG=/var/lib/jenkins/.kube/config

                    kubectl get pods
                    kubectl get deployments
                    kubectl get services
                '''
            }
        }

    }

    post {

        success {

            echo '========================================'
            echo 'Build Completed Successfully'
            echo 'Docker Image Built'
            echo 'Docker Image Pushed'
            echo 'Application Successfully Deployed to Amazon EKS'
            echo '========================================'

        }

        failure {

            echo '========================================'
            echo 'Pipeline Failed'
            echo 'Check Jenkins Console Output'
            echo '========================================'

        }

        always {

            echo '========== Cleanup =========='

            sh '''
                docker image prune -f || true
            '''

        }

    }

}