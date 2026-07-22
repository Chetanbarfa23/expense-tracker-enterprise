pipeline {

    agent any

    environment {

        APP_NAME = "expense-tracker-enterprise"
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
                    pip3 --version
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

                sh '''
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                '''

            }

        }

        stage('Deploy Application') {

            when {

                branch 'main'

            }

            steps {

                echo '========== Deploying Application =========='

                sh '''
                    docker compose down || true
                    docker compose up -d --build
                '''

            }

        }

        stage('Health Check') {

            when {

                branch 'main'

            }

            steps {

                echo '========== Health Check =========='

                sh '''
                    docker ps
                '''

            }

        }

    }

    post {

        success {

            echo '========================================'
            echo ' Build Completed Successfully'
            echo ' Docker Image Built'
            echo ' Docker Image Pushed'
            echo ' Application Deployed'
            echo '========================================'

        }

        failure {

            echo '========================================'
            echo ' Pipeline Failed'
            echo ' Check Console Output'
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