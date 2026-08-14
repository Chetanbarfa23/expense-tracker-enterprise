pipeline {

    agent any

    environment {
        APP_NAME   = "expense-tracker-enterprise"
        IMAGE_NAME = "chetan8889/expense-tracker-enterprise"
        DEPLOY_ENV = "DEV"
    }

    stages {

        // =====================================================
        // WORKSPACE
        // =====================================================

        stage('Workspace Verification') {
            steps {

                echo '========== Workspace =========='

                sh '''
                    pwd
                    ls -la
                '''
            }
        }


        // =====================================================
        // BUILD INFORMATION
        // =====================================================

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


        // =====================================================
        // PYTHON
        // =====================================================

        stage('Verify Python') {
            steps {

                echo '========== Python Verification =========='

                sh '''
                    python3 --version
                '''
            }
        }


        // =====================================================
        // DOCKER
        // =====================================================

        stage('Verify Docker') {
            steps {

                echo '========== Docker Verification =========='

                sh '''
                    docker --version
                    docker compose version
                '''
            }
        }


        // =====================================================
        // BUILD DOCKER IMAGE
        // =====================================================

        stage('Build Docker Image') {
            steps {

                echo '========== Building Docker Image =========='

                sh '''
                    docker build \
                        -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                        .

                    docker tag \
                        ${IMAGE_NAME}:${BUILD_NUMBER} \
                        ${IMAGE_NAME}:latest
                '''
            }
        }


        // =====================================================
        // LIST IMAGES
        // =====================================================

        stage('List Docker Images') {
            steps {

                echo '========== Docker Images =========='

                sh '''
                    docker images | grep expense-tracker || true
                '''
            }
        }


        // =====================================================
        // DOCKER HUB LOGIN
        // =====================================================

        stage('Docker Hub Login') {
            steps {

                echo '========== Docker Hub Login =========='

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


        // =====================================================
        // PUSH DOCKER IMAGE
        // =====================================================

        stage('Push Docker Image') {
            steps {

                echo '========== Pushing Docker Image =========='

                sh '''
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }


        // =====================================================
        // DEPLOY TO AMAZON EKS
        // =====================================================

        stage('Deploy to Amazon EKS') {

            when {
                branch 'main'
            }

            steps {

                echo '========== Deploying to Amazon EKS =========='

                withCredentials([

                    string(
                        credentialsId: 'MYSQL_HOST',
                        variable: 'MYSQL_HOST'
                    ),

                    string(
                        credentialsId: 'MYSQL_USER',
                        variable: 'MYSQL_USER'
                    ),

                    string(
                        credentialsId: 'MYSQL_PASSWORD',
                        variable: 'MYSQL_PASSWORD'
                    ),

                    string(
                        credentialsId: 'MYSQL_DB',
                        variable: 'MYSQL_DB'
                    ),

                    string(
                        credentialsId: 'JWT_SECRET_KEY',
                        variable: 'JWT_SECRET_KEY'
                    )

                ]) {

                    sh '''
                        set -e

                        export HOME=/var/lib/jenkins
                        export KUBECONFIG=/var/lib/jenkins/.kube/config
                        export AWS_DEFAULT_REGION=ap-south-1

                        echo "========== AWS CHECK =========="

                        aws --version

                        aws sts get-caller-identity


                        echo "========== KUBERNETES CHECK =========="

                        kubectl config current-context

                        kubectl get nodes


                        echo "========== KUBERNETES SECRET =========="

                        echo "Deleting old Kubernetes Secret..."

                        kubectl delete secret expense-tracker-secret \
                            --ignore-not-found


                        echo "Creating Kubernetes Secret..."

                        kubectl create secret generic expense-tracker-secret \
                            --from-literal=MYSQL_HOST="$MYSQL_HOST" \
                            --from-literal=MYSQL_USER="$MYSQL_USER" \
                            --from-literal=MYSQL_PASSWORD="$MYSQL_PASSWORD" \
                            --from-literal=MYSQL_DB="$MYSQL_DB" \
                            --from-literal=JWT_SECRET_KEY="$JWT_SECRET_KEY"


                        echo "========== APPLYING KUBERNETES MANIFESTS =========="

                        kubectl apply -f kubernetes/


                        echo "========== RESTARTING DEPLOYMENT =========="

                        kubectl rollout restart deployment/expense-tracker


                        echo "========== WAITING FOR ROLLOUT =========="

                        kubectl rollout status \
                            deployment/expense-tracker \
                            --timeout=5m
                    '''
                }
            }
        }


        // =====================================================
        // HEALTH CHECK
        // =====================================================

        stage('Health Check') {

            when {
                branch 'main'
            }

            steps {

                echo '========== Kubernetes Health Check =========='

                sh '''
                    export HOME=/var/lib/jenkins
                    export KUBECONFIG=/var/lib/jenkins/.kube/config

                    echo "========== PODS =========="

                    kubectl get pods


                    echo "========== DEPLOYMENTS =========="

                    kubectl get deployments


                    echo "========== SERVICES =========="

                    kubectl get services


                    echo "========== HPA =========="

                    kubectl get hpa || true
                '''
            }
        }

    }


    // =========================================================
    // POST ACTIONS
    // =========================================================

    post {

        success {

            echo '''
========================================
       BUILD COMPLETED SUCCESSFULLY
========================================

Docker Image Built       : YES
Docker Image Pushed      : YES
Kubernetes Deployment    : YES
Amazon EKS               : YES
Health Check             : YES

========================================
'''
        }


        failure {

            echo '''
========================================
          PIPELINE FAILED
========================================

Check Jenkins Console Output
for the failed stage.

========================================
'''
        }


        always {

            echo '========== Docker Cleanup =========='

            sh '''
                docker image prune -f || true
            '''
        }
    }
}