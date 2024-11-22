
---

Proposed Temporary Workflow: Observability-Led Triage and Ticket Creation

Objective: Establish a clear interim process to ensure efficient incident management while automation for triage and ticket creation is developed and implemented.


---

Key Proposal

1. Responsibilities of the Observability Engineering Team

Until automated triage and ticket creation are operational, the Observability Engineering Team will undertake the following:

Triage Alerts:

Analyze Incoming Alerts: Assess all alerts to determine their validity and relevance.

Correlate Related Information: Aggregate data from various sources to identify patterns or recurring issues.

Filter Out Noise: Eliminate false positives and non-actionable alerts to focus on genuine incidents.

Assign Priorities: Classify each alert based on severity levels, such as:

P1: Critical incidents requiring immediate attention.

P2: High-priority issues needing prompt resolution.

P3: Medium-priority concerns to be addressed in due course.



Create Tickets:

Manual Ticket Creation: Open incident tickets in the designated ticketing system (e.g., Jira, ServiceNow).

Include Comprehensive Information:

Title: Craft a concise and descriptive summary of the issue.

Details: Provide logs, metrics, and any relevant contextual information from the alert analysis.

Priority Level: Clearly indicate the assigned priority (P1, P2, or P3).

Assignment: Route the ticket directly to the Platform Service Break-Fix Team for action.




---

2. Responsibilities of the Platform Service Break-Fix Team

Upon receipt of a ticket, the Platform Service Break-Fix Team will execute the following steps:

Acknowledge the Ticket:

Commit to Defined SLAs:

P1: Acknowledge within 5 minutes.

P2: Acknowledge within 15 minutes.

P3: Acknowledge within 1 hour.



Investigate and Resolve:

Analyze the Issue: Examine the details provided to understand the root cause.

Implement Solutions: Take necessary actions to resolve the incident efficiently.

Update the Ticket: Document all investigative steps and resolutions within the ticket for transparency and future reference.


Escalate If Necessary:

Request Additional Context: If more information is required, promptly reach out to the Observability Engineering Team.

Engage Additional Resources: Involve other teams or specialists if the issue extends beyond the team's scope.



---

Advantages

1. Clear Interim Ownership:

Dedicated Triage and Ticket Creation: The Observability Engineering Team's focus on these tasks reduces delays in incident response.

Efficient Resource Utilization: Allows the Platform Service Break-Fix Team to concentrate solely on resolving incidents.


2. Streamlined Workflow:

Effective Incident Handling: Ensures that all alerts are properly managed, minimizing the risk of critical alerts being overlooked.


3. Foundation for Automation:

Structured Process: Establishes a solid framework that can be seamlessly transitioned to an automated system upon completion of the BigPanda and ServiceNow integration.



---

Next Steps

1. Finalize the Workflow:

Confirm Roles and Responsibilities: Collaborate with both teams to ensure clarity and agreement on the interim process.

Align on SLAs: Establish mutual understanding and commitment to the defined service level agreements to ensure accountability.


2. Monitor and Iterate:

Track Performance Metrics: Monitor the manual process to identify any delays or inefficiencies.

Continuous Improvement: Use insights gained to refine the workflow and prepare for automation.


3. Automate the Workflow:

Initiate Integration Projects: Begin the integration of BigPanda with ServiceNow to automate triage and ticket creation processes.

Enhance Response Times: Leverage automation to improve efficiency and reduce manual workload, leading to faster incident resolution.



---

This temporary workflow provides a clear and professional framework for incident management during the transition period. By delineating specific responsibilities and establishing structured processes, the organization can maintain operational efficiency and prepare for a smooth implementation of automated systems.

