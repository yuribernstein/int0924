def commitId
def fullCommitId

pipeline {
    agent {
        label 'docker'
    }

    environment {
        DOCKER_CREDENTIALS_ID = 'docker'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/yuribernstein/int0924.git'
                script {
                    fullCommitId = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    commitId = fullCommitId.substring(0, 5)
                }
            }
        }

        stage('Build') {
            steps {
                dir('weatherapp') {
                    script {
                        echo "Commit ID is ${commitId}"
                    }
                    sh """
                    sed -i 's/API_KEY//g' configuration.json
                    sudo docker build -t weatherapp:${fullCommitId} . 1> /dev/null
                    sudo docker run --name weatherappci -p 8080:8080 -d weatherapp:${fullCommitId}
                    """
                }
            }
        }

        stage('Sleep') {
            steps {
                sleep time: 5, unit: 'SECONDS'
            }
        }

        stage('Test') {
            steps {
                dir('tests') {
                    sh """
                    sudo docker build -t weatherapp-test:${fullCommitId} . 1> /dev/null
                    sudo docker run --name weatherapp-testci --link weatherappci weatherapp-test:${fullCommitId} python3 testapp.py --zip 80905 --location 'Colorado Springs' --app_address 'http://weatherappci:8080'
                    sudo docker logs weatherapp-testci | grep pass
                    """
                }
            }
        }
    }


    post {
        success {
            echo 'Success - Build completed.'
            script {
                withCredentials([usernamePassword(credentialsId: 'docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                    echo ${DOCKER_PASS} | sudo docker login -u ${DOCKER_USER} --password-stdin
                    sudo docker tag weatherapp:${fullCommitId} yuribernstein/advisor:${fullCommitId}
                    sudo docker push yuribernstein/advisor:${fullCommitId}
                    """
                }
            }
        }
        failure {
            echo 'Error - Build failed.'
        }
        always {
            sh 'sudo docker rm -f $(sudo docker ps -aq)'
            echo 'This will always run after the stages, regardless of the result.'
        }
    }
}