pipeline {
    agent any // Jenkins master will orchestrate, but steps will run on the slave via SSH

    environment {
        // Define the environment variable for the slave server
        SLAVE_SERVER = 'ec2-user@172.31.2.97' // Your slave's IP
        // Define repository details (replace with your actual repo)
        GIT_REPO = 'https://github.com/anbalaganramu/flaskApp.git' // Replace this
        APP_NAME = 'my-flask-app' // Name for the Docker image/container
        APP_PORT = '8080' // Port your Flask app listens on inside the container
        HOST_PORT = '8080' // Port to expose on the slave host
    }

    stages {
        stage('Clone Repository on Slave') {
            steps {
                script {
                    sshagent(['flaskApp']) { // Use the SSH credential ID you configured
                        echo 'Cloning repository on Slave...'

                        // Step 1: Clone the repository directly on the slave
                        sh """
                            ssh -o StrictHostKeyChecking=no ${SLAVE_SERVER} '
                                # Remove any old clone directory
                                rm -rf ${APP_NAME}
                                # Clone the repository
                                git clone ${GIT_REPO} ${APP_NAME}
                            '
                        """
                    }
                }
            }
        }

        stage('Build Docker Image on Slave') {
            steps {
                script {
                    sshagent(['flaskApp']) {
                        echo 'Building Docker image on Slave...'

                        // Step 2: Navigate to the cloned repo and build the Docker image
                        sh """
                            ssh -o StrictHostKeyChecking=no ${SLAVE_SERVER} '
                                cd ${APP_NAME}
                                # Ensure Dockerfile exists
                                if [ ! -f Dockerfile ]; then
                                    echo "Error: Dockerfile not found in the cloned repository."
                                    exit 1
                                fi
                                # Build the image with a tag
                                docker build -t ${APP_NAME} .
                            '
                        """
                    }
                }
            }
        }

        // stage('Stop Previous Container (if any)') {
        //     steps {
        //         script {
        //             sshagent(['flaskApp']) {
        //                 echo 'Checking for and stopping any previous container...'
        //                 // Attempt to stop and remove a container with the same name, ignore errors if none exists
        //                 sh """
        //                     ssh -o StrictHostKeyChecking=no ${SLAVE_SERVER} '
        //                         docker stop ${APP_NAME} || true
        //                         docker rm ${APP_NAME} || true
        //                     '
        //                 """
        //             }
        //         }
        //     }
        // }

        // stage('Run Flask App Container on Slave') {
        //     steps {
        //         script {
        //             sshagent(['flaskApp']) {
        //                 echo 'Running Flask App container on Slave...'
        //                 // Run the built image, mapping the internal port (APP_PORT) to the host port (HOST_PORT)
        //                 // Use --rm to automatically remove the container when it stops
        //                 // Use -d to run in detached mode
        //                 sh """
        //                     ssh -o StrictHostKeyChecking=no ${SLAVE_SERVER} '
        //                         docker run -d --rm --name ${APP_NAME} -p ${HOST_PORT}:${APP_PORT} ${APP_NAME}
        //                     '
        //                 """
        //             }
        //         }
        //     }
        // }

        // stage('Verify Deployment') {
        //     steps {
        //         script {
        //             sshagent(['flaskApp']) {
        //                 echo 'Waiting for Flask app to start and verifying access...'
        //                 // Give the container a moment to start up
        //                 sh """
        //                     ssh -o StrictHostKeyChecking=no ${SLAVE_SERVER} '
        //                         sleep 10
        //                         # Check if the container is running
        //                         if [ \$(docker ps --filter "name=${APP_NAME}" --format "{{.Names}}") != "${APP_NAME}" ]; then
        //                             echo "Error: Container ${APP_NAME} is not running."
        //                             docker ps -a # Show all containers for debugging
        //                             exit 1
        //                         fi
        //                         # Optionally, check if the port is listening inside the container
        //                         docker exec ${APP_NAME} netstat -tuln | grep :${APP_PORT} || echo "Warning: Port ${APP_PORT} might not be listening inside the container."
        //                     '
        //                 """
        //             }
        //         }
        //     }
        // }
    }

    post {
        always {
            echo "Pipeline finished. Check the Slave machine's public IP on port ${params.HOST_PORT} for the Flask app."
            // Optional: Add a step to print the slave's IP address if needed
            // sh "echo 'Slave IP: 172.31.2.97'" // Hardcoded, get dynamically if needed
        }
        failure {
            script {
                sshagent(['flaskApp']) {
                    // Attempt to stop the container if the pipeline failed
                    sh """
                        ssh -o StrictHostKeyChecking=no ${SLAVE_SERVER} '
                            docker stop ${APP_NAME} || true
                            docker rm ${APP_NAME} || true
                        '
                    """
                }
            }
        }
    }
}
