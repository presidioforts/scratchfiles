Here is the consolidated document with all seven feedback items:


---

Breakfix Customer Forum Dated September 20, 2024


---

1. Problem Reported By: App team

Reported Problem Description: The app team raised concerns about the support model involving multiple tools and different support teams. For example, in the case of Threadfix upload-related issues, they were directed to contact different teams. They inquired if there is a support contact and JIRA URL mapping available for different tool chains.

Internal Discussion Outcome: This issue is related to the need for a consolidated product home landing page where all the necessary support details, including contacts and JIRA URLs, are available in one place.

Next Step: Breakfix leads and SMEs will brainstorm how to design the product home landing page, focusing on making it easier for teams to find support contacts and JIRA URLs for different tools in one place. The goal is to simplify navigation and provide all relevant information clearly and efficiently.


---

2. Problem Reported By: App team

Reported Problem Description: The app team reported that the npm and Gradle caches are being cleared by the infrastructure team during their builds. Since these caches are global, it is impacting their builds. They asked if there is a better way to handle this issue.

Response/Comments: The Breakfix team has delivered and tested a branch-specific npm cache configuration and documented the solution. The document has been published for the app team to reference. However, the branch-specific cache solution for Gradle is still being worked on.

Next Step: Continue working on the Gradle branch-specific cache solution and update the app team once it is ready.


---

3. Problem Reported By: Harlow, John from YOM app team

Reported Problem Description: John from the YOM app team requested a discussion regarding BD scan issues and repeated build issues.

Next Step: John from the YOM app team is requested to schedule a meeting with Dan (SCAN SME), Shaun (CI SME), and the Breakfix team leads to address the BD scan and build issues.


---

4. Problem Reported By: App team

Reported Problem Description: The app team raised an issue where Ops engineers are not following the RCA process. Some engineers are closing tickets without RCA details when help from the Jenkins Infra team is required. The app team suggested that instead of closing the ticket and asking them to open a new one, the ticket should be reassigned to the infra breakfix team.

Next Step: Madhu and David will schedule a training session to address this gap and ensure proper ticket handling and reassignment to the infra breakfix team when needed.


---

5. Problem Reported By: App team

Reported Problem Description: The app team requested access to old tickets so they can review solutions from other app teams who faced similar issues. This would allow them to adopt working resolutions instead of creating new tickets.

Next Step: Rajesh Vasan is working with Matthew to explore possible solutions for providing access to old tickets.


---

6. Problem Reported By: App team

Reported Problem Description: The app team raised concerns about Jenkins build timeouts, specifically pointing out that builds 23 and 15 are running significantly slower than expected.

Next Step: The app team will submit a Jenkins Infra issue through an SDLC ticket, after which the relevant team will investigate the cause of the slow builds and provide a resolution.


---

7. Problem Reported By: App team

Reported Problem Description: The app team suggested displaying critical system outages or service disruptions as a banner on the Jenkins build homepage to keep users informed in real-time.

Next Step: David and Shaun will work with Paul and Satish to explore how this notification method can be implemented on the Jenkins build homepage.


---

Let me know if you need any further adjustments!

