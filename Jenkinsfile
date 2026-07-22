pipeline {

    agent any

    environment {

        APP_NAME = "expense-tracker-enterprise"
        APP_VERSION = "1.0"
        DEPLOY_ENV = "DEV"

    }

    stages {

        stage('Workspace Verification') {

            steps {

                echo '========== Workspace =========='
                sh 'pwd'

                echo '========== Repository =========='
                sh 'ls -la'

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

        stage('Environment Variables') {

            steps {

                echo '========== Environment Variables =========='

                echo "Application Name : ${env.APP_NAME}"
                echo "Application Version : ${env.APP_VERSION}"
                echo "Deployment Environment : ${env.DEPLOY_ENV}"

            }

        }

        stage('Deploy') {

            when {
                branch 'main'
            }

            steps {

                echo "Deploying ${env.APP_NAME}"
                echo "Version : ${env.APP_VERSION}"
                echo "Environment : ${env.DEPLOY_ENV}"

                echo "Deploy Stage Executed"

            }

        }

    }

    post {

        always {

            echo "========== Pipeline Finished =========="

        }

        success {

            echo "Build Completed Successfully"

        }

        failure {

            echo "Pipeline Failed"

        }

    }

}