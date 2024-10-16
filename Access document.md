Certainly! Here's the document with properly formatted section headings:


---

Access to Enterprise GIT Cloud for Platform Services Engineers

Summary

Platform Services Engineers need to be added to specific Active Directory (AD) groups to gain the necessary access to GitHub and related repositories. Below are the details on the AD groups required, their purpose, and how to verify access.

AD Groups Required

The following three LDAP-based AD groups are essential for access to GitHub and the repositories:

1. AD-ENT-GROUP1 – Provides access to log in to GitHub.com.


2. AD-ENT-GROUP2 – Grants standard repository access, including the ability to execute GitHub Actions workflows.


3. AD-ENT-GROUP3 – Provides access to the repositories under the CTO organization within GitHub.



Why These AD Groups Are Required

1. AD-ENT-GROUP1

This group allows engineers to log in to GitHub.com with their enterprise credentials. Without this, engineers cannot access GitHub or any related repositories.

2. AD-ENT-GROUP2

This group provides standard access to GitHub repositories, including the ability to execute GitHub Actions workflows. Engineers will need this to trigger and manage automation workflows within the platform.

3. AD-ENT-GROUP3

Engineers in this group will have access to the CTO organization’s repositories, enabling them to work on critical projects, manage settings, and collaborate with the broader CTO team.

Verifying Access

1. GitHub Login (AD-ENT-GROUP1): Log in to GitHub.com using your enterprise credentials.


2. Repository Access (AD-ENT-GROUP2): Confirm that you can execute GitHub Actions workflows by triggering a workflow run in the repositories.


3. CTO Organization Access (AD-ENT-GROUP3): Ensure you have access to the CTO organization repositories and the projects you are assigned to.



Contact Information

For any issues with access, please reach out to Sarada (Admin), Vishal, or Shaun for standard support.


---

Let me know if this meets your requirements or if you need any further adjustments!


