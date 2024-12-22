pipeline {
    // Options for pipeline execution
    options {
        timeout(time: 1, unit: 'HOURS') // Timeout to prevent long-running jobs
        buildDiscarder(logRotator(numToKeepStr: '10')) // Limit build history
    }

    // Default agent
    agent none

    // Environment variables
    environment {
        SAMPLE_ENV = 'This is a sample environment variable'
        DOCKER_HUB_CREDENTIALS = credentials('DOCKER_HUB_CREDENTIALS')
    }

    // Parameters
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Branch to build')
    }

    stages {
        stage('Clean Workspace') {
            agent { label 'master-node' }
            steps {
                cleanWs()
                echo "Workspace cleaned."
            }
        }

        stage('Git Checkout') {
            agent { label 'git-node' }
            steps {
                checkout scm
                echo "Checked out repository."
            }
        }

        stage('Check Branch and Changes') {
            agent { label 'linux-builder' }
            steps {
                script {
                    echo "Current Branch: ${params.BRANCH_NAME}"
                    sh 'git diff --name-only HEAD~1 HEAD > changes.txt'
                    sh 'cat changes.txt'
                }
            }
        }

        stage('Get Commit ID') {
            agent { label 'linux-builder' }
            steps {
                script {
                    COMMIT_ID = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    echo "Commit ID: ${COMMIT_ID}"
                }
            }
        }

        stage('Run test.py') {
            agent { label 'linux-builder' }
            steps {
                script {
                    echo "Running test.py..."
                    sh 'python3 test.py'
                }
            }
        }

        stage('Build Docker Image') {
            agent { label 'docker-node' }
            steps {
                script {
                    sh "docker build -t myapp:${COMMIT_ID} ."
                    echo "Docker image built with tag: myapp:${COMMIT_ID}"
                }
            }
        }

        stage('Run Docker Container') {
            agent { label 'docker-node' }
            steps {
                script {
                    sh "docker run --name test-container -d myapp:${COMMIT_ID}"
                    echo "Docker container started with image: myapp:${COMMIT_ID}"
                }
            }
        }

        stage('Run full_test.py') {
            agent { label 'linux-builder' }
            steps {
                script {
                    echo "Running full_test.py..."
                    sh 'python3 full_test.py'
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            agent { label 'docker-node' }
            steps {
                withCredentials([usernamePassword(credentialsId: 'DOCKER_HUB_CREDENTIALS', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                        sh "docker push myapp:${COMMIT_ID}"
                        echo "Docker image pushed to Docker Hub with tag: myapp:${COMMIT_ID}"
                    }
                }
            }
        }

        stage('Send Completion Email') {
            agent { label 'master-node' }
            steps {
                script {
                    mail to: 'team@example.com', 
                         subject: "Pipeline Completed: ${env.JOB_NAME} #${env.BUILD_NUMBER}", 
                         body: "The pipeline has successfully completed.\n\nCommit ID: ${COMMIT_ID}" 
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs for details."
            error("Failing the build after recording logs.")
        }
        always {
            echo "Cleaning up..."
            cleanWs() // Clean workspace
        }
    }
}
