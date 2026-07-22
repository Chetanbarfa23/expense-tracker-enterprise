pipeline {

    agent any

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

                echo "Build Number : ${env.BUILD_NUMBER}"
                echo "Job Name     : ${env.JOB_NAME}"
                echo "Branch Name  : ${env.BRANCH_NAME}"
                echo "Workspace    : ${env.WORKSPACE}"
                echo "Node Name    : ${env.NODE_NAME}"

            }

        }

        stage('Deploy') {

            when {
                branch 'main'
            }

            steps {

                echo "Deploy Stage Executed"

            }

        }

    }

    post {

        always {

            echo "Pipeline Finished"

        }

        success {

            echo "Build Completed Successfully"

        }

        failure {

            echo "Pipeline Failed"

        }

    }

}