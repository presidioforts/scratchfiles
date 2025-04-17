
Subject: Quick fix: build‑info publish failure

Hi team,

RCA
com.jfrog.artifactory wrote every Gradle configuration to scopes in build‑info.json. In a multi‑module build this string broke Artifactory’s 1 024‑char limit and threw StorageException.

Fix – add one line:

artifactory {
  publish {
    defaults {
      buildInfo {
        scopes = ['compileClasspath']   // keep it short
      }
    }
  }
}

Run ./gradlew clean artifactoryPublish; build-info.json now shows only "scopes":["compileClasspath"], and the publish succeeds.

Please commit, rerun Jenkins, and let me know if it’s green.

Thanks,
<your name>

