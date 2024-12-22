pipeline{
    
    // agent any
    agent {
        label 'docker'
    }
    
//

    stages {
        stage('Clean Workspace') {
            steps {
                script {
                    cleanWs()
                    echo "Workspace cleaned."
                    sh """
                    sudo docker rm -f $(sudo docker ps -a -q)
                    """
                }
                echo "Docker containers removed."
            }
        }


        stage('Clone repo') {
            steps {
                script {
                    git branch: 'main', url: 'https://github.com/yuribernstein/int0924.git'
                }
            }
        }
        stage('Docker build') {
            steps {
                dir('coding/flask_systeminfo'){
                    script {
                        sh """
                        sudo docker build -t flask_systeminfo:temp .
                        """
                    }
                }
            }
        }
        stage('Run container') {
            steps {
                script {
                    sh """
                    sudo docker run -p 8081:8081 -d flask_systeminfo:temp
                    """
                }
            }
        }
    }
    
}
