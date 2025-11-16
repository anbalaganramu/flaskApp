pipeline {
    agent any
    stages {
        stage('FlaskApp') {
            agent any
            steps {
                script {
                    sshagent(['flaskApp']) {
                        echo 'Flask Application'
                        // Create a folder "called test"
                        sh "ssh -o StrictHostKeyChecking=no ec2-user@172.31.2.97 'mkdir test'"
                    }
                }
            }
        }
    }
}