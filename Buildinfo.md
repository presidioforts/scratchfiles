
Subject: RCA: build‑info.json StorageException due to oversized scopes field


---

Hi Team,

Summary:
During our Jenkins‑triggered Gradle build, the Artifactory publish step began failing with a StorageException complaining that the dependency_scopes column exceeded its 1 024‑character limit.


---

Impact:

All CI builds publishing build‑info to Artifactory aborted.

Automated promotion and traceability of artifacts was blocked until manual intervention.



---

Root Cause:
The JFrog Gradle plugin’s Build‑Info Extractor by default gathers every Gradle configuration name (e.g. compileClasspath, kaptDebugCompileClasspath, mockDebugRuntimeClasspath, etc.) into a single "scopes" array in build‑info.json. In our multi‑module project this list exceeded 1 024 characters, violating the Artifactory column size and triggering the exception.


---

Resolution:
We added a single line to our build.gradle to explicitly restrict the scopes emitted. This change ensures build‑info.json contains only the minimal required scope and stays well under the storage limit:

artifactory {
  publish {
    defaults {
      publishBuildInfo = true
      buildInfo {
        // limit emitted scopes to just compileClasspath
        scopes = ['compileClasspath']
      }
    }
  }
}

This update was validated on version 4.33.1 of com.jfrog.artifactory. After running ./gradlew clean artifactoryPublish, the resulting <buildDir>/build‑info/build‑info.json now includes only:

"scopes":["compileClasspath"]

and no longer exceeds 1 024 characters.


---

Next Steps:

1. Merge the above fragment into our shared build.gradle.


2. Allow Jenkins to supply Artifactory URL and credentials via existing pipeline parameters (ART_URL, ART_USER, ART_PWD).


3. Monitor the next few builds to confirm successful publication.



Please let me know if you have any questions or need further details.

Best regards,
[Your Name]
Platform Service Team Lead


