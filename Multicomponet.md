

Below is a revised version of the document with improved clarity, organization, and writing style. The technical details and original meaning have been preserved.


---

CMake Build Pack Overview

The CMake build pack generates three types of artifacts from a single source repository:

rh7: Produced as name-rh7-artifactversion.tar

rh8: Produced as name-rh8-artifactversion.tar

Windows: Produced as artifactname-windows-artifactversion.zip


Build Process

1. The main Jenkins pipeline checks out the source code from GitHub.


2. It then triggers two child pipeline jobs:

One job builds the rh7 artifact.

The other job builds the rh8 artifact.



3. The main pipeline itself builds the Windows artifact as a .zip file.



All three resulting artifacts are published to the generic-local repository in JFrog Artifactory.

Workspaces and Workers

Each artifact build (rh7, rh8, Windows) is performed in a separate workspace on its own dedicated Jenkins worker (agent).

Artifact Management

All artifacts are stored in the same Artifactory repository (generic-local). A YAML configuration file specifies include patterns for these artifacts:

**/name-rh7-*.tar

**/name-rh8-*.tar

**/artifactname-windows-*.zip


Deploy Stage

Currently, each CI job attempts to:

1. Make GET requests to Artifactory to download all three artifacts.


2. Push the artifacts to the UCD repository.



This happens independently in each job.


---

Issues

1. Independent GET Calls Cause Failures:
Because all three jobs run in parallel and attempt to download all artifacts, any job may fail if it tries to retrieve an artifact that isn’t yet published.


2. Unnecessary Duplication of Work:
Each job repeats the artifact retrieval and deployment steps, even though it only produced one artifact.


3. Reliability Concerns:
The current approach frequently leads to pipeline failures, requiring manual intervention or retries.




---

Proposed Solution

Centralize the artifact deployment stage in the main Jenkins pipeline job.

Updated Workflow

1. Child Jobs:
Each child job builds and publishes its own artifact (rh7, rh8, Windows) to Artifactory. They do not perform any deployment steps.


2. Main Job:
After confirming that all child jobs have completed successfully, the main job uses the YAML file’s include patterns to fetch all three artifacts from Artifactory. Once it verifies their availability, it pushes them to the UCD repository.




---

Benefits

No Premature Retrieval: By deferring the artifact GET steps until the main job, all artifacts are guaranteed to be available, preventing retrieval failures.

Reduced Duplication: Only one job handles artifact retrieval and deployment, reducing repetitive work.

Enhanced Reliability: The process is orchestrated in a single place, lowering the risk of errors and minimizing the need for manual intervention.


In summary, moving the deploy stage to the main pipeline simplifies the workflow and makes the CI/CD process more stable and maintainable.

