Hi [Name],

Jones, Bill E, and I discussed this, and your RCA is correct. The high CPU utilization issue has been ongoing for over a year, but we only recently caught it through our new observability alerts and incidents.

Our recommendations:

1. Fix the indexing as soon as possible.


2. Create a new endpoint (as you suggested) to fetch employees inactive in the past three months, and implement pagination for this new endpoint to manage large datasets effectively.


3. Have DSOP consume this new paginated endpoint for all internal processing.



Let me know if you have any questions.

Best regards,
[Your Name]

