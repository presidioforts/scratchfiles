
Here's the final draft of your document:


---

Subject: Request to Operationalize SDLC Breakfix Intake for EPL-X Product

Hi Paul,

As of March 31, we have successfully completed both phases of EPL-X onboarding for the Breakfix team:

Phase 1: Training on EPL-X Product, GitSaaS, GitHub Action CI architecture, and Runner Infrastructure.

Phase 2: Hands-on setup and validation of EPL-X CI workflows and Harness CD deployments across all active build packs.


The Breakfix team is now fully capable of independently managing builds and deployments of the reference application using the non-production GitSaaS organization. They have successfully configured EPL-X Action workflows and deployed them via Harness. Furthermore, the team is prepared to handle customer-reported incidents and service requests through SDLC DevOps tickets, covering both PCF/TAS and container-based builds within the EPL-X and Harness ecosystems.

Given this readiness, I propose transitioning the Breakfix team to become the primary intake point for GitSaaS, GitHub Action, and Harness deployment incidents and service requests. This would allow the SME team to shift focus to escalation support, aligning with our proven operating model for EPL and UCD.

Current Critical Issues Under Resolution:

EPL-X Workflow Execution Constraints:

Similar to EPL, we currently cannot directly execute customer-reported EPL-X workflows. Changes must be implemented and validated by customers themselves.

Action: SME team is collaborating with GitSaaS Engineering to enable this functionality for the entire Platform Service team.


Repository Forking and Troubleshooting:

As with EPL, we lack the ability to fork customer repositories to directly troubleshoot and validate fixes.

Action: SME team is actively coordinating with GitSaaS Engineering to provide this capability to the Platform Service team.


Support Organization Runner Configuration:

The dedicated eplx-support organization for Platform Service currently lacks runners, limiting our troubleshooting capabilities.

Action: We are working closely with the EPL-X Infrastructure team to provision runners for this organization.



These issues currently affect our ability to meet SLAs for SDLC DevOps tickets. Over the past six months, the SME team has managed these limitations effectively. Although customer satisfaction is not yet at optimal levels, operations have been maintained efficiently under existing constraints.

Ticket Volume:

EPL-X Workflow-related tickets: approximately 5-10 per week

GitSaaS-related tickets: approximately 10-15 per week


Please review and let me know your thoughts or if any further details are needed.

Best regards,
[Your Name]


