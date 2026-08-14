// ============================================================
// EXPENSE TRACKER ENTERPRISE
// CI/CD PIPELINE
//
// Flow:
//
// GitHub
//   ↓
// Jenkins
//   ↓
// Build Docker Image
//   ↓
// Login to AWS ECR
//   ↓
// Push Docker Image to ECR
//   ↓
// Deploy Image to Amazon EKS
//   ↓
// Kubernetes Secret + ConfigMap
//   ↓
// Rolling Deployment
//   ↓
// Health Check
//
// ============================================================


pipeline {

    // ========================================================
    // TASK 1: JENKINS AGENT
    // ========================================================

    agent any


    // ========================================================
    // TASK 2: GLOBAL ENVIRONMENT VARIABLES
    //
    // These values are available throughout the pipeline.
    // ========================================================

    environment {

        // Application name
        APP_NAME = "expense-tracker-enterprise"

        // AWS region where ECR and EKS are running
        AWS_REGION = "ap-south-1"

        // AWS ECR registry
        ECR_REGISTRY = "080019754331.dkr.ecr.ap-south-1.amazonaws.com"

        // Complete ECR repository
        IMAGE_NAME = "080019754331.dkr.ecr.ap-south-1.amazonaws.com/expense-tracker"

        // Deployment environment
        DEPLOY_ENV = "DEV"
    }


    // ========================================================
    // PIPELINE STAGES
    // ========================================================

    stages {


        // ====================================================
        // TASK 3: VERIFY JENKINS WORKSPACE
        //
        // Check where Jenkins is running and what files
        // Jenkins received from GitHub.
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
        // TASK 4: DISPLAY BUILD INFORMATION
        //
        // Useful for debugging and identifying builds.
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
        // TASK 5: VERIFY REQUIRED TOOLS
        //
        // Jenkins needs:
        //
        // Python
        // Docker
        // AWS CLI
        // kubectl
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
        // TASK 6: BUILD DOCKER IMAGE
        //
        // Application source code
        //        ↓
        // Dockerfile
        //        ↓
        // Docker Image
        //
        // Example:
        //
        // expense-tracker:25
        // expense-tracker:latest
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
        // TASK 7: VERIFY DOCKER IMAGE
        //
        // Display images created on Jenkins machine.
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
        // TASK 8: LOGIN TO AWS ECR
        //
        // Jenkins
        //    ↓
        // AWS ECR Authentication
        //
        // IMPORTANT:
        //
        // We are NOT using Docker Hub.
        //
        // We are using:
        //
        // AWS ECR
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
        // TASK 9: PUSH DOCKER IMAGE TO AWS ECR
        //
        // Docker Image
        //       ↓
        // AWS ECR
        //
        // Two tags are pushed:
        //
        // BUILD NUMBER
        // latest
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
        // TASK 10: DEPLOY APPLICATION TO AMAZON EKS
        //
        // Only deploy from main branch.
        //
        // Docker Image
        //       ↓
        // ECR
        //       ↓
        // EKS
        // ====================================================

        stage('Deploy to Amazon EKS') {

            when {

                branch 'main'
            }

            steps {

                echo '========== DEPLOYING TO AMAZON EKS =========='


                // =================================================
                // TASK 10A: LOAD DATABASE/JWT SECRETS
                //
                // Jenkins credentials are NOT written directly
                // inside Jenkinsfile.
                //
                // Jenkins injects them temporarily.
                // =================================================

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

                        // =================================================
                        // TASK 10B: CONFIGURE JENKINS KUBERNETES ACCESS
                        // =================================================

                        export HOME=/var/lib/jenkins

                        export KUBECONFIG=/var/lib/jenkins/.kube/config


                        // =================================================
                        // TASK 10C: VERIFY AWS IDENTITY
                        // =================================================

                        echo "========== AWS IDENTITY =========="

                        aws sts get-caller-identity


                        // =================================================
                        // TASK 10D: VERIFY EKS CONNECTION
                        // =================================================

                        echo "========== KUBERNETES CLUSTER =========="

                        kubectl config current-context

                        kubectl get nodes


                        // =================================================
                        // TASK 10E: UPDATE KUBERNETES SECRET
                        //
                        // Database password and JWT secret are stored
                        // in Kubernetes Secret.
                        // =================================================

                        echo "========== UPDATING KUBERNETES SECRET =========="

                        kubectl delete secret expense-tracker-secret \
                          --ignore-not-found


                        kubectl create secret generic expense-tracker-secret \
                          --from-literal=MYSQL_HOST="$MYSQL_HOST" \
                          --from-literal=MYSQL_USER="$MYSQL_USER" \
                          --from-literal=MYSQL_PASSWORD="$MYSQL_PASSWORD" \
                          --from-literal=MYSQL_DB="$MYSQL_DB" \
                          --from-literal=JWT_SECRET_KEY="$JWT_SECRET_KEY"


                        // =================================================
                        // TASK 10F: APPLY KUBERNETES CONFIGURATION
                        //
                        // Applies:
                        //
                        // deployment.yaml
                        // service.yaml
                        // configmap.yaml
                        // hpa.yaml
                        // etc.
                        // =================================================

                        echo "========== APPLYING KUBERNETES MANIFESTS =========="

                        kubectl apply -f kubernetes/


                        // =================================================
                        // TASK 10G: UPDATE APPLICATION IMAGE
                        //
                        // Tell Kubernetes:
                        //
                        // Use the newly built image from ECR.
                        //
                        // Example:
                        //
                        // ECR
                        //  ↓
                        // expense-tracker:26
                        //  ↓
                        // EKS Pod
                        // =================================================

                        echo "========== UPDATING DEPLOYMENT IMAGE =========="

                        kubectl set image deployment/expense-tracker \
                          expense-tracker=${IMAGE_NAME}:${BUILD_NUMBER}


                        // =================================================
                        // TASK 10H: WAIT FOR ROLLING UPDATE
                        //
                        // Kubernetes:
                        //
                        // Old Pod
                        //     +
                        // New Pod
                        //     ↓
                        // New Pod Ready
                        //     ↓
                        // Old Pod Removed
                        // =================================================

                        echo "========== WAITING FOR ROLLOUT =========="

                        kubectl rollout status \
                          deployment/expense-tracker \
                          --timeout=5m
                    '''
                }
            }
        }


        // ====================================================
        // TASK 11: KUBERNETES HEALTH CHECK
        //
        // Verify:
        //
        // Pods
        // Deployment
        // Service / Load Balancer
        // HPA
        // Running Docker image
        // ====================================================

        stage('Health Check') {

            when {

                branch 'main'
            }

            steps {

                echo '========== KUBERNETES HEALTH CHECK =========='

                sh '''

                    // =================================================
                    // TASK 11A: KUBERNETES CONFIG
                    // =================================================

                    export HOME=/var/lib/jenkins

                    export KUBECONFIG=/var/lib/jenkins/.kube/config


                    // =================================================
                    // TASK 11B: CHECK PODS
                    // =================================================

                    echo "========== PODS =========="

                    kubectl get pods


                    // =================================================
                    // TASK 11C: CHECK DEPLOYMENT
                    // =================================================

                    echo "========== DEPLOYMENT =========="

                    kubectl get deployment expense-tracker


                    // =================================================
                    // TASK 11D: CHECK SERVICE / LOAD BALANCER
                    // =================================================

                    echo "========== SERVICE =========="

                    kubectl get svc


                    // =================================================
                    // TASK 11E: CHECK HORIZONTAL POD AUTOSCALER
                    // =================================================

                    echo "========== HPA =========="

                    kubectl get hpa


                    // =================================================
                    // TASK 11F: VERIFY RUNNING IMAGE
                    //
                    // This confirms EKS is actually running the
                    // image that Jenkins just pushed.
                    // =================================================

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


        // ====================================================
        // TASK 12: SUCCESS MESSAGE
        // ====================================================

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


        // ====================================================
        // TASK 13: FAILURE MESSAGE
        // ====================================================

        failure {

            echo '========================================'
            echo '           PIPELINE FAILED'
            echo '========================================'

            echo 'Check Jenkins Console Output'

            echo '========================================'
        }


        // ====================================================
        // TASK 14: CLEANUP
        //
        // Remove unused Docker images from Jenkins.
        // ====================================================

        always {

            echo '========== DOCKER CLEANUP =========='

            sh '''
                docker image prune -f || true
            '''
        }
    }
}