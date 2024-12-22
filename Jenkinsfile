pipeline{
    
    // agent any
    agent {
        label 'docker'
    }
    
    stages {
        
        stage('Stage 1') {
            steps {
                script {
                    echo "Hello from stage1"
                    sh """
                    hostname
                    """
                }
            }
        }
        stage('Stage 2') {
            steps {
                script {
                    echo "Hello from stage2"
                    sh """
                    whoami
                    """
                }
            }
        }
        stage('Stage 3') {
            steps {
                script {
                    sh """
                    sudo docker images
                    """
                }
            }
        }
    }
    
}
