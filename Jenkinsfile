
pipeline{
  agent any
    stages {
        stage('Building Docker Container') {
            steps {
                script {
                  sh '''
                  docker build -t mustfaglr/looping:${currentBuild.number} .
                  '''
                }
            }
        }
        stage('Deploying to Cluster') {
            steps {
              echo "Deploy is started!"
              script {
                sh '''
                docker login -u mustafaglr -p dckr_pat_Papu7myfbjEprjs3FrNK3xyyOYg
                docker push mustfaglr/looping:${currentBuild.number}
                '''
              }
        }
        stage('Helm') {
            steps {
                script {
                  helm repo update
                  helm upgrade -i app harbor/app
                  --set image 
               }
            }
        }

        
              
        // post { 
        //     success { 
        //         script {
        //             if (env.BUILD_NUMBER != '1') {
        //                notifySuccessful(repoName,branchName)
        //             }
        //         }
        //     }
        //      failure { 
        //         script {
        //             if (env.BUILD_NUMBER != '1') {
        //                notifyFailed(repoName,branchName)
        //            }
        //         }
        //     }
        // }
      }
    }

}


// def notifyStarted(String repoName,String branchName) {
//   emailext body: "STARTED",
//         mimeType: 'text/html',
//         subject: "[Jenkins] ${repoName}-${branchName}-${currentBuild.number} - STARTED",
//         to: "",
//         replyTo: "",
//         recipientProviders: [[$class: 'CulpritsRecipientProvider']]
// }
  
// def notifySuccessful(String repoName,String branchName) {
//   emailext body: '''${SCRIPT, template="groovy-html.template"}''',
//         mimeType: 'text/html',
//         subject: "[Jenkins] ${repoName}-${branchName}-${currentBuild.number} - SUCCEED",
//         to: "",
//         replyTo: "",
//         recipientProviders: [[$class: 'CulpritsRecipientProvider']]
// }
  
// def notifyFailed(String repoName,String branchName) {
//   emailext body: '''${SCRIPT, template="groovy-html.template"}''',
//         mimeType: 'text/html',
//         subject: "[Jenkins] ${repoName}-${branchName}-${currentBuild.number} - FAILED",
//         to: "",
//         replyTo: "",
//         recipientProviders: [[$class: 'CulpritsRecipientProvider']]
// }
