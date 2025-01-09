### **Sub-Catalog Items Under GitSaaS**

1. **Access or Login Issue**  
   - **Type**: Incident  
   - **Description**: Report problems signing in or accessing repositories in GitHub SaaS (GitHub.com). Include error messages, screenshots, and impacted usernames to expedite resolution.

2. **Request Default Branch Change**  
   - **Type**: Service Request  
   - **Description**: Request to change the default branch of a specific GitHub repository. Provide the repository name and the new default branch name.

3. **Request Repository Deletion or Archival**  
   - **Type**: Service Request  
   - **Description**: Request to delete or archive a GitHub repository. Include the repository name, justification (e.g., project completed), and any backup requirements.

4. **Request Removal of Branch Protection**  
   - **Type**: Service Request  
   - **Description**: Request to remove branch protection rules for urgent fixes or other changes. Specify the protected branch, the repository, and the reason for removal.

---

### **Sub-Catalog Items Under EPL-X (GitHub Actions Framework)**

1. **Configure Runner for System Upgrade**  
   - **Type**: Service Request  
   - **Description**: Request to install or upgrade system libraries, binaries, or allocate memory on an EPL-X GitHub Actions runner. Provide required tools, versions, and any compatibility constraints.

2. **Install New Software/Binary on Runner**  
   - **Type**: Service Request  
   - **Description**: Request to install or update a new build tool or software package on an EPL-X runner. Include version numbers, dependencies, and any relevant usage details.

3. **Runner Startup or Performance Issue**  
   - **Type**: Incident  
   - **Description**: Report issues such as runner startup failures, crashes, or resource constraints (e.g., out-of-memory). Provide runner logs, OS version, and pipeline context.

4. **Checkout Stage Failure**  
   - **Type**: Incident  
   - **Description**: Report problems during the code checkout step in an EPL-X workflow. Include repository/branch details, error messages, and logs for troubleshooting.

5. **Build Stage Failure**  
   - **Type**: Incident  
   - **Description**: Report compilation or build-related failures (e.g., missing dependencies, build script errors). Attach build logs, recent code changes, and environment details.

6. **Sonar Stage Failure**  
   - **Type**: Incident  
   - **Description**: Report issues or failures in the SonarQube code quality check stage. Provide relevant logs, screenshots, or error codes to speed up investigation.

7. **BlackDuck Stage Failure**  
   - **Type**: Incident  
   - **Description**: Report issues in the Black Duck security scan stage. Include scan logs, pipeline details, and any suspicious dependency changes.

8. **CheckMarx Stage Failure**  
   - **Type**: Incident  
   - **Description**: Report failures or errors in the Checkmarx vulnerability scanning stage. Provide scan reports, logs, or steps to reproduce the error.

9. **CodeSign Stage Failure**  
   - **Type**: Incident  
   - **Description**: Report problems with signing binaries or artifacts. Include logs, signing certificate details, and artifact references where possible.

10. **GTG (Good to Go) Stage Failure**  
    - **Type**: Incident  
    - **Description**: Report failures in the “Good to Go” stage, which validates readiness and approvals prior to publishing artifacts. Supply gating criteria and any relevant approval logs.

11. **SCM Tag Stage Failure**  
    - **Type**: Incident  
    - **Description**: Report issues applying version tags in the EPL-X workflow. Provide the repository name, commit hash, and any relevant error messages.

12. **Publish Artifact Failure**  
    - **Type**: Incident  
    - **Description**: Report failures when publishing artifacts to Artifactory. Include artifact names, logs, and HTTP errors (if any).

13. **Deploy Failure in Harness**  
    - **Type**: Incident  
    - **Description**: Report deployment failures in Harness.io triggered from an EPL-X workflow. Provide logs from Harness, environment details, and deployment IDs.

14. **Unexpected Tool Behavior**  
    - **Type**: Incident  
    - **Description**: Report odd or degraded performance from any tool integrated into EPL-X (Sonar, BlackDuck, Checkmarx, CodeSign, etc.). Describe the issue, steps to reproduce, and logs.
