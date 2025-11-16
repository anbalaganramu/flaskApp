pipeline {
    agent any
    environment {
        // Define the environment variable
        FLASK_SERVER = 'ec2-user@172.31.2.97' 
    }
    stages {
        stage('FlaskApp') {
            agent any
            steps {
                script {
                    sshagent(['flaskApp']) {
                        echo 'Flask Application'
                        // Create a folder "called test"
                        sh "ssh -o StrictHostKeyChecking=no ${FLASK_SERVER} 'mkdir test2'"
                    }
                }
            }
        }
    }
}