**Subject:** Follow-Up: EmployeeProfile Service Method `byLoginId` Discussion  

Hi [Recipient],  

This afternoon, Scott and I discussed the `EmployeeProfile` service method `byLoginId`, which was identified as a significant factor contributing to the MongoDB high CPU utilization issue. Below is the focused approach we are proposing as the next step:  

**Proposed Approach:**  
We are proposing to configure **Rate Limiting** for the `byLoginId` method to control excessive requests and mitigate the impact on MongoDB performance.  

**Steps for the Pilot:**  
1. **Rate Limiting Configuration:**  
   - Implement Apigee's Quota Policy for the `byLoginId` method to limit request volume and reduce database load while maintaining operational reliability.  

2. **Traffic Mirroring:**  
   - Use Apigee to mirror live traffic to a test proxy endpoint to validate the rate-limiting configuration without impacting production stability.  

3. **Monitoring with ThousandEyes:**  
   - Deploy ThousandEyes to monitor the proxy endpoint for:  
     - Availability and uptime.  
     - Response time variations under rate limits.  
     - Frequency of rate-limit violations (`429 Too Many Requests` errors).  

4. **Validation and Demonstration:**  
   - Evaluate pilot results to validate the effectiveness of rate limiting in mitigating CPU issues.  
   - Present findings to SCP Engineering and customers to encourage adopting this method for other high-traffic API services.  

This approach is designed to address the immediate issue while providing a scalable framework for broader adoption. Please let us know if you have any feedback or suggestions to refine this plan further.  

Best regards,  
[Your Name]  
