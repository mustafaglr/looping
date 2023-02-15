def appName = ""

pipeline {
  agent {
    kubernetes {
        yaml """\
        metadata:
          labels:
            app: jenkins-agent
        spec:
          serviceAccountName: jenkins
          volumes:
            - name: docker-socket
              emptyDir: {}
          containers:
            - name: jnlp
              env:
                - name: CONTAINER_ENV_VAR
                  value: jnlp
            - name: docker
              image: docker:19.03.1
              command:
                - sleep
              args:
                - 99d
              volumeMounts:
                - name: docker-socket
                  mountPath: /var/run
            - name: docker-daemon
              args: [--insecure-registry=registry.kubernetes.local:80]
              image: docker:19.03.1-dind
              securityContext:
                privileged: true
              volumeMounts:
                - name: docker-socket
                  mountPath: /var/run
            - name: argo
              image: argoproj/argocd:v2.6.1
              command:
                - cat
              tty: true
              securityContext:
                runAsUser: 0
      """.stripIndent()
    }
  }
  environment {
        REGISTRY_URL = "registry.kubernetes.local:80"
        ARGO_URL = "argocd-server.argocd.svc.cluster.local:80"
        VERSION = "${BRANCH_NAME}-${BUILD_ID}"
  }
  stages {
    stage ('Commit')
    {
        steps {
            script {
                appName = env.JOB_NAME.split('/')[0];
                echo "appName: ${appName}"
            }
        }
    }
    stage('Image Build & Push') {
      steps {
        container('docker') {
            sh """
              echo '172.18.8.101 registry.kubernetes.local' >> /etc/hosts
              echo '172.18.8.102 registry.kubernetes.local' >> /etc/hosts
              echo '172.18.8.103 registry.kubernetes.local' >> /etc/hosts
              echo '172.18.8.104 registry.kubernetes.local' >> /etc/hosts
            """
          withCredentials([usernamePassword(credentialsId: 'harbor-admin-credential', passwordVariable: 'HARBOR_PASS', usernameVariable: 'HARBOR_USER')]) {
            sh "docker build -t ${env.REGISTRY_URL}/${BRANCH_NAME}/${appName}:${env.VERSION} ."
            sh "docker login -u $HARBOR_USER -p $HARBOR_PASS ${env.REGISTRY_URL}"
            sh "docker push ${env.REGISTRY_URL}/${BRANCH_NAME}/${appName}:${env.VERSION}"
          }
        }
      }
    }
    stage('Deploy to DEV') {
      steps {
        container('argo') {
          withCredentials([usernamePassword(credentialsId: 'argo-admin-credential', passwordVariable: 'ARGO_PASS', usernameVariable: 'ARGO_USER')]) {
            sh "yes | argocd login ${ARGO_URL} --username ${ARGO_USER} --password ${ARGO_PASS}"
            sh "argocd app set ${appName}-${BRANCH_NAME} -p app.deployment.image=${env.REGISTRY_URL}/${BRANCH_NAME}/${appName}:${env.VERSION}"
            sh "argocd app sync ${appName}-${BRANCH_NAME}"
          }
        }
      }
    }

  }
}
