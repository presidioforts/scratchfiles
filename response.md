This afternoon, Scott and I discussed the EmployeeProfile service method byLoginId, which was identified as a significant factor contributing to the MongoDB high CPU utilization issue. Below is the focused approach we developed to address this problem and ensure long-term scalability:

Pilot Plan:

Rate Limiting Configuration:

Implement Apigee's Quota Policy to regulate excessive calls to the byLoginId method, reducing strain on MongoDB while maintaining service reliability.
Traffic Mirroring:

Mirror live traffic to a test proxy endpoint to validate the effectiveness of the rate-limiting configuration without affecting production stability.
Monitoring with ThousandEyes:

Utilize ThousandEyes to monitor the proxy endpoint, focusing on:
Endpoint availability.
Response time changes under the configured limits.
Frequency and patterns of rate-limit breaches (429 Too Many Requests errors).
Validation and Adoption:

Analyze results from the pilot to gain actionable insights into system behavior.
Use the findings to demonstrate the feasibility and effectiveness of this approach, encouraging SCP Engineering and customers to adopt similar configurations for other critical API services.
