
Here is the consolidated document titled "Breakfix Customer Forum Dated October 4, 2024":


---

Breakfix Customer Forum Dated October 4, 2024

1. Problem Reported By: Bob from 2FSN app team (Rizzo Robert)
Reported Problem Description: It is hard to find the product feature documentation, specifically on how to configure dependency component builds. The app team needs to build multiple dependency components in a specific order and is struggling to find clear guidance. Bob mentioned needing direct help from the product developer and inquired about the best channel to reach out for support. They also expressed a desire for ongoing developer assistance as needed.
Next Action/Comments: Explore ways to make product documentation more accessible and clear, especially for configuring dependency component builds. Identify and recommend the best communication channel for app teams to reach out to product developers, potentially setting up a dedicated support line for ongoing developer assistance.
Next Step: The app team will draft a specification for the dependency build order requirement, with a focus on making it generic so that other app teams can adopt it. Engineering will not build features that are specific to an individual app team.


---

2. Problem Reported By: Bob from 2FSN app team
Reported Problem Description: Bob mentioned that the app team has moved all their scan builds to PR (Pull Request) builds only, as having scans on every build was too costly.
Response/Comments: Dan (Scan SME) responded that reducing scan build volume may lead to a better experience, especially if there is a high volume of builds. The app team agreed with this response and is on board with the approach.
Next Step: No further action needed. The app team is aligned with the solution.


---

3. Problem Reported By: Hester Kenneth from Capital Market - 1MCR
Reported Problem Description: Hester raised a concern that the product is getting so many features added that the app team has no visibility into them. They would like to understand what EPL engineering/developers think about the features, especially ones that the app team is not using at all. Additionally, Hester expressed a desire to split long-running builds into smaller ones by creating more repositories to reduce build time, but implementing a dependency build model is challenging. They want the product engineering team to focus more on what the app team needs rather than continuing to add more features. Hester also requested ideas from product engineering on how to achieve a smaller build time model.
Next Action/Comments: Both this problem and Problem 1 reflect similar concerns regarding product feature overload and the challenge of configuring dependency builds. The app team is looking for better alignment between product features and their actual needs, particularly for reducing build times and improving the dependency model. Product engineering should prioritize visibility, documentation, and a feature set that addresses the app team's specific requirements.
Next Step: Product engineering will provide suggestions on how to reduce build time by splitting builds into smaller components. A follow-up session may be scheduled to review the features and understand the app team's priorities.


---

4. Problem Reported By: Hester Kenneth from Capital Market - 1MCR
Reported Problem Description: Hester asked about the best approach for GitHub repository branch hygiene and how to manage unnecessary branches.
Response/Comments: Madhu responded by suggesting that the app team create a Service Request to temporarily remove the branch protection rule, allowing them to delete unwanted branches from the repository. Madhu emphasized that this is an important step that the app team should perform regularly with every release. Additionally, Bob demonstrated how to avoid tagging certain branches by adjusting the cicd.yml configuration.
Next Step: The app team should implement a process for regular branch cleanup by submitting Service Requests as needed. Bob's method for excluding certain branches from tagging via cicd.yml should also be documented and shared with other teams.


---

5. Problem Reported By: Reynold Teresa
Reported Problem Description: Reynold requested a flowchart that provides an overview of the entire EPL feature set on one page, extending from SDLC start to finish. Given that 10 unique roles are involved in production, they want the product’s landing page to include a visual flow with all the steps in the CI/CD product workflow. At each stage, it should identify the responsible support team and specify what JIRA requests to raise. Additionally, Reynold suggested linking relevant Confluence knowledge pages to the main product landing page and embedding them in the flowchart or diagram.
Response/Comments: Manda responded by providing a conceptual overview link for EPL. This feedback needs further analysis to better understand the app team's request and determine how best to provide the detailed flowchart and related documentation they are seeking.
Next Step: The product team should analyze the app team's request to determine how to present the EPL workflow in a comprehensive flowchart, including support teams, JIRA request processes, and links to knowledge resources. A follow-up discussion may be needed to clarify expectations and deliver the requested flow.


---

6. Problem Reported By: Bulson Laura and Bon from 2FSN app team
Reported Problem Description: Laura and Bon reported issues related to the TruffleHog scan. They inquired why a failed TruffleHog scan build cannot be rebuilt and shared a common experience where PR builds are not reporting correctly.
Response/Comments: Bob responded, explaining that when the TruffleHog scan fails, it should immediately break the build instead of waiting for the build to run for 2 hours and then fail at the publish/GTG stage. The internal Breakfix team discussed that the TruffleHog scan should stop the build for release builds but allow it to continue for snapshot and PR builds since these build types do not execute the GTG stage.
Proposed Solution: Introduce a feature flag to break the build immediately upon TruffleHog scan failure for release builds, while allowing snapshot and PR builds to continue.
Next Step: The Breakfix team will work with product engineering to consider implementing the proposed flag to stop the build for release builds upon TruffleHog scan failure while allowing snapshot and PR builds to proceed. Further testing and validation of this behavior may be required before rollout.


---

Let me know if you'd like any additional changes!

