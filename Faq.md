
Here’s both the email and the FAQ version for you:


---

Email:

Hello Arun/Vishal,

What Manda reported this morning, "Release Record Insert Failure," is similar to the incident Kishore reported this afternoon: <build URL link>.

<error log pasted here>I have reviewed the EPL code. Below, these two feature changes enforce case sensitivity and name matching between the Autodiscovery-identified names and the cicd.yml artifact section information. These changes were pushed 3 months ago, starting from the v2024.10.x tags and above.

<feature 1 link> and <feature 2 link>

This is an enterprise-wide change, and we will get more tickets when developers upgrade tags from v2024.09.x.

Fix resolution:
Updated the changes in cicd.yml, and after the update, the build was successful. <build URL>


---

FAQ: Didn't Find Any Artifact(s) to Insert into SCP, Please Validate the cicd.yml Configuration

Q1: What does the error "Didn't find any Artifact(s) to insert into SCP" mean?
A1: This error occurs when the system is unable to locate the specified artifacts in the repository, often due to mismatches or misconfigurations in the cicd.yml file. The issue is related to the enforcement of case sensitivity and name matching between the Autodiscovery-identified names and the artifact section in the cicd.yml file.

Q2: What recent changes might be causing this issue?
A2: The issue is linked to feature changes pushed three months ago, starting from the v2024.10.x tags and above. These changes enforce case sensitivity and name matching between Autodiscovery-identified names and the cicd.yml artifact section.

Q3: What should I check in the cicd.yml file to resolve this error?
A3: Ensure that the names in the cicd.yml file exactly match the names identified by Autodiscovery, considering case sensitivity. You can verify the details of the changes in the following links:

[Feature 1 link]

[Feature 2 link]


Q5: How was the issue fixed?
A5: The issue was resolved by updating the cicd.yml file with the correct artifact names. After making the necessary updates, the build was successful. [<Build URL link>]


---

Let me know if you need anything else!

