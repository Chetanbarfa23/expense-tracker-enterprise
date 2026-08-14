// ============================================================
// EXPENSE TRACKER ENTERPRISE - CI/CD PIPELINE
//
// GitHub
//   ↓
// Jenkins
//   ↓
// Docker Build
//   ↓
// AWS ECR
//   ↓
// Amazon EKS
//   ↓
// Kubernetes Secret + ConfigMap
//   ↓
// Rolling Deployment
//   ↓
// Health Check
// ============================================================

pipeline {

    // Jenkins agent
    agent any

    // Global variables
    environment {

        APP_NAME = "expense-tracker-enterprise"

        AWS_REGION = "ap-south-1"

        ECR_REGISTRY = "080019754331.dkr.ecr.ap-south-1.amazonaws.com"

        IMAGE_NAME = "080019754331.dkr.ecr.ap-south-1.amazonaws.com/expense-tracker"

        DEPLOY_ENV = "DEV"
    }

    stages {

        // ====================================================
        // TASK 1: WORKSPACE
        // ====================================================

        stage('Workspace Verification') {

            steps {

                echo '========== WORKSPACE VERIFICATION =========='

                sh '''
                    pwd
                    ls -la
                '''
            }
        }


        // ====================================================
        // TASK 2: BUILD INFORMATION
        // ====================================================

        stage('Build Information') {

            steps {

                echo '========== BUILD INFORMATION =========='

                echo "Build Number : ${env.BUILD_NUMBER}"
                echo "Job Name     : ${env.JOB_NAME}"
                echo "Branch Name  : ${env.BRANCH_NAME}"
                echo "Workspace    : ${env.WORKSPACE}"
                echo "Node Name    : ${env.NODE_NAME}"
            }
        }


        // ====================================================
        // TASK 3: VERIFY TOOLS
        // ====================================================

        stage('Verify Tools') {

            steps {

                echo '========== TOOL VERIFICATION =========='

                sh '''
                    python3 --version
                    docker --version
                    aws --version
                    kubectl version --client
                '''
            }
        }


        // ====================================================
        // TASK 4: BUILD DOCKER IMAGE
        // ====================================================

        stage('Build Docker Image') {

            steps {

                echo '========== BUILDING DOCKER IMAGE =========='

                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${BUILD_NUMBER} .

                    docker tag \
                      ${IMAGE_NAME}:${BUILD_NUMBER} \
                      ${IMAGE_NAME}:latest
                '''
            }
        }


        // ====================================================
        // TASK 5: VERIFY IMAGE
        // ====================================================

        stage('List Docker Images') {

            steps {

                echo '========== DOCKER IMAGES =========='

                sh '''
                    docker images | grep expense-tracker || true
                '''
            }
        }


        // ====================================================
        // TASK 6: LOGIN TO AWS ECR
        // ====================================================

        stage('ECR Login') {

            steps {

                echo '========== AWS ECR LOGIN =========='

                sh '''
                    aws ecr get-login-password \
                      --region ${AWS_REGION} | \
                    docker login \
                      --username AWS \
                      --password-stdin \
                      ${ECR_REGISTRY}
                '''
            }
        }


        // ====================================================
        // TASK 7: PUSH IMAGE TO ECR
        // ====================================================

        stage('Push Image to ECR') {

            steps {

                echo '========== PUSHING IMAGE TO AWS ECR =========='

                sh '''
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}

                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }


        // ====================================================
        // TASK 8: DEPLOY TO AMAZON EKS
        // ====================================================

        stage('Deploy to Amazon EKS') {

            when {
                branch 'main'
            }

            steps {

                echo '========== DEPLOYING TO AMAZON EKS =========='

                // Load secrets from Jenkins
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

                        # Configure Jenkins Kubernetes access

                        export HOME=/var/lib/jenkins
                        export KUBECONFIG=/var/lib/jenkins/.kube/config


                        # Verify AWS identity

                        echo "========== AWS IDENTITY =========="

                        aws sts get-caller-identity


                        # Verify EKS connection

                        echo "========== KUBERNETES CLUSTER =========="

                        kubectl config current-context
                        kubectl get nodes


                        # Create Kubernetes Secret

                        echo "========== UPDATING KUBERNETES SECRET =========="

                        kubectl delete secret expense-tracker-secret \
                          --ignore-not-found

                        kubectl create secret generic expense-tracker-secret \
                          --from-literal=MYSQL_HOST="$MYSQL_HOST" \
                          --from-literal=MYSQL_USER="$MYSQL_USER" \
                          --from-literal=MYSQL_PASSWORD="$MYSQL_PASSWORD" \
                          --from-literal=MYSQL_DB="$MYSQL_DB" \
                          --from-literal=JWT_SECRET_KEY="$JWT_SECRET_KEY"


                        # Apply Kubernetes manifests

                        echo "========== APPLYING KUBERNETES MANIFESTS =========="

                        kubectl apply -f kubernetes/


                        # Update deployment with new ECR image

                        echo "========== UPDATING DEPLOYMENT IMAGE =========="

                        kubectl set image deployment/expense-tracker \
                          expense-tracker=${IMAGE_NAME}:${BUILD_NUMBER}


                        # Wait for rolling deployment

                        echo "========== WAITING FOR ROLLOUT =========="

                        kubectl rollout status \
                          deployment/expense-tracker \
                          --timeout=5m
                    '''
                }
            }
        }


        // ====================================================
        // TASK 9: HEALTH CHECK
        // ====================================================

        stage('Health Check') {

            when {
                branch 'main'
            }

            steps {

                echo '========== KUBERNETES HEALTH CHECK =========='

                sh '''

                    # Kubernetes access

                    export HOME=/var/lib/jenkins
                    export KUBECONFIG=/var/lib/jenkins/.kube/config


                    # Pods

                    echo "========== PODS =========="

                    kubectl get pods


                    # Deployment

                    echo "========== DEPLOYMENT =========="

                    kubectl get deployment expense-tracker


                    # Service / Load Balancer

                    echo "========== SERVICE =========="

                    kubectl get svc


                    # Horizontal Pod Autoscaler

                    echo "========== HPA =========="

                    kubectl get hpa


                    # Verify running image

                    echo "========== CURRENT IMAGE =========="

                    kubectl get deployment expense-tracker \
                      -o jsonpath='{.spec.template.spec.containers[0].image}{"\\n"}'
                '''
            }
        }
    }


    // ========================================================
    // POST BUILD ACTIONS
    // ========================================================

    post {

        success {

            echo '========================================'
            echo '          BUILD SUCCESSFUL'
            echo '========================================'

            echo 'Docker Image Built'
            echo 'Image Pushed to AWS ECR'
            echo 'Application Deployed to Amazon EKS'
            echo 'Rollout Successful'
            echo 'Health Check Successful'

            echo '========================================'
        }


        failure {

            echo '========================================'
            echo '           PIPELINE FAILED'
            echo '========================================'

            echo 'Check Jenkins Console Output'

            echo '========================================'
        }


        always {

            echo '========== DOCKER CLEANUP =========='

            sh '''
                docker image prune -f || true
            '''
        }
    }
}