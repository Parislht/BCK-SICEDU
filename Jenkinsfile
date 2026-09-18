// Pipeline de BCK-HUASCARAN (Jenkins multibranch del curso).
//
//   development → despliega el entorno dev
//   qa          → SonarQube, despliega qa
//   uat         → despliega uat (presentaciones semanales)
//   main        → todavía no despliega
//
// El .env de cada entorno está en Jenkins como credencial "Secret file":
// HUASCARAN_SECRETS_BACKEND_DEV, _QA y _UAT. Nunca se imprime en el log.
//
// Todavía no hay tests: cuando existan (pytest), van en un stage antes de
// SonarQube, igual que en el Jenkinsfile del frontend.

pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }

    environment {
        ENTORNO  = "${env.BRANCH_NAME == 'development' ? 'dev' : env.BRANCH_NAME}"
        PROYECTO = "huascaran_bck_${env.BRANCH_NAME == 'development' ? 'dev' : env.BRANCH_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube') {
            when {
                branch 'qa'
            }
            agent {
                docker {
                    image 'maven:3.9.8-eclipse-temurin-21-alpine'
                    reuseNode true
                }
            }
            steps {
                // Si SonarQube aún no está configurado para el proyecto, el build
                // queda UNSTABLE pero el despliegue de qa sigue.
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        withSonarQubeEnv('SonarQube-Server') {
                            sh """
                                export SONAR_USER_HOME="\${WORKSPACE}/.sonar"
                                mkdir -p "\${SONAR_USER_HOME}"
                                ${scannerHome}/bin/sonar-scanner
                            """
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'development'
                    branch 'qa'
                    branch 'uat'
                }
            }
            steps {
                withCredentials([
                    file(credentialsId: "HUASCARAN_SECRETS_BACKEND_${env.ENTORNO.toUpperCase()}", variable: 'ENV_FILE')
                ]) {
                    sh '''
                        rm -f .env
                        cp "$ENV_FILE" .env
                        docker compose -p "$PROYECTO" up -d --build --remove-orphans
                    '''
                }
            }
        }

        stage('Verificar despliegue') {
            when {
                anyOf {
                    branch 'development'
                    branch 'qa'
                    branch 'uat'
                }
            }
            steps {
                // Al arrancar, el contenedor migra la base y (si se pide) carga los
                // usuarios de prueba; recién después responde la API.
                sh '''
                    set +e
                    CONTENEDOR=$(docker compose -p "$PROYECTO" ps -aq backend)
                    RESPONDE=no

                    echo "Esperando hasta 120 s a que la API responda en / ..."
                    for i in $(seq 1 24); do
                        if docker compose -p "$PROYECTO" exec -T backend python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=3)" >/dev/null 2>&1; then
                            RESPONDE=si
                            break
                        fi
                        CORRIENDO=$(docker inspect -f '{{.State.Running}}' "$CONTENEDOR" 2>/dev/null)
                        echo "  intento $i/24 -> Running=$CORRIENDO"
                        # Si el contenedor ya se detuvo (migración fallida, .env incompleto), no tiene sentido esperar.
                        if [ "$CORRIENDO" != "true" ]; then break; fi
                        sleep 5
                    done

                    docker compose -p "$PROYECTO" ps -a
                    docker compose -p "$PROYECTO" logs --tail=80 --no-color

                    if [ "$RESPONDE" != "si" ]; then
                        echo "ERROR: la API no responde. Revisar los logs de arriba (DATABASE_URL, migraciones)."
                        exit 1
                    fi
                    echo "OK: la API responde."
                '''
            }
        }

        stage('Quality Gate') {
            when {
                branch 'qa'
            }
            steps {
                // Va después del despliegue para no retrasarlo esperando a SonarQube.
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    timeout(time: 5, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: false
                    }
                }
            }
        }
    }

    post {
        always {
            // El .env solo hace falta para levantar el contenedor.
            sh 'rm -f .env'
        }
    }
}
