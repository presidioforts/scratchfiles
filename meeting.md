**SCP Microservice Platform Service Sync-Up Meeting - Follow-Up Discussion**

**Meeting Minutes**

1. **Template Microservice Observability Requirement**

   **Actions:**
   - **Meeting to Identify Requirements**: Bill, Dheeraj, Manda, Praveen, and Shaun will convene to discuss and compile a list of observability requirements.
   - **Feature Requests**: Separate feature requests will be created for:
     - SCP Microservice Platform Engineering
     - Observability Engineering

2. **Review and Prioritization of API Services**

   **Actions:**
   - **Working Session**: The platform service team will hold a working session to review all 55 API services and assign priorities—Critical, High, or Medium.
   - **Set SLAs**: Establish Service Level Agreements for each service based on its assigned priority.
   - **Configure Monitoring and Alerts**:
     - **Critical Services**: Set up monitoring and alerts using AppDynamics.
     - **High and Medium Priority Services**: Configure alerts within the Grafana dashboard for ongoing monitoring.

3. **Weekly SCP Platform Service Team Sync-Up Meeting**

   **Actions:**
   - **Issue Identification**: Detect issues such as service restarts and HTTP 500 error patterns.
     - Utilize Splunk logs and the PCF cloud service console for in-depth analysis.
     - Conduct Root Cause Analysis (RCA) for identified issues.
   - **Documentation and Backlog Creation**:
     - Document the findings from the RCA and log the efforts involved.
     - Create backlog items for SCP Engineering to address these issues.
     - The platform service team will manage an internal task ticket under the SCP Platform EPIC [Link].
   - **Scheduling**: Shaun will arrange the next sync-up meeting.

4. **CPU Spike and JVM Issues**

   **Actions:**
   - **Investigative Meeting**: Bill, Dheeraj, and Shaun will meet offline to delve into the CPU spike and JVM issues.
   - **Scheduling**: Shaun will set up this meeting for next week.

5. **Performance Analysis of Newly Onboarded GitSaaS Applications**

   **Context:**
   - Three SCP service applications have been onboarded into GitSaaS.
   - Satish seeks to understand the build performance differences between EPL and EPL-X.

   **Action:**
   - **Performance Comparison**: Shaun will analyze and compare the build times and performance metrics between EPL and EPL-X for the newly onboarded applications.
