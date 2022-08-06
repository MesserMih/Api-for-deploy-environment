pipeline {
    agent any

    environment {
        PROJECT_NAME = "API-Dev"
        OWNER_NAME = "Oznobikhin Mikhail"
    }
    stages {
        stage ("Build") {
            steps { 
                sh "docker compose up -d"
            }
        }
    }
}
