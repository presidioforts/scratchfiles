
Hi [Name],

Bill and I discussed this, and your RCA is correct. The high CPU utilization issue has been ongoing for over a year, but we only recently detected it via our new observability alerts and incidents. Additionally, we agree with the fix you proposed, and we would like to add a few more recommendations:

1. Fix the indexing as soon as possible.


2. Create a new endpoint (as you suggested) to fetch employees inactive in the past three months, and implement pagination to handle large datasets efficiently.


3. Have DSOP consume this new paginated endpoint for all internal processing.



Please let me know if you have any questions or need further clarification.

Best regards,
[Your Name]

