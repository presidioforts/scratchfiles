Below is a more technical deep-dive into the root cause, query mechanics, and recommended optimizations for your MongoDB performance issue. This analysis assumes familiarity with MongoDB indexing, Spring Data repository methods, and REST API architecture.


---

1. Problem Overview

High Throughput on /ByLandID
The EmployeeProfileService endpoint /ByLandID was invoked ~495+ times per minute by a single consumer (or multiple consumers). This rate is abnormally high for a single API, suggesting either a bug or misuse on the client side.

MongoDB Node CPU Spiking to 100%
A large volume of requests led to stress on the primary MongoDB node. Profiling the database or examining the logs revealed that CPU usage correlated to a single expensive query.



---

2. Primary Query Causing the Issue

Query in Repository

@QueryValue = "{ 
   'sourceSystem': ?0, 
   'employeeStatus': 'A', 
   '$or': [
     { 'employeeLogin': { '$regex': ?1, '$options': 'i' } },
     { 'samAccountName': { '$regex': ?1, '$options': 'i' } }
   ]
}"
EmployeeProfile findByLandId(String sourceSystem, String employeeLogin);

Why This Query is Problematic

1. Use of $regex on Unindexed Fields

Regular-expression queries typically require scanning the entire collection when used on fields that are not indexed with a compatible pattern. This yields high CPU utilization and slow performance.

Even if you have an index on these fields, $regex queries starting with wildcards (/.*.../) cannot fully leverage the index.



2. Compound $or Condition

The query checks two separate fields (employeeLogin and samAccountName) with regex. This amplifies the scanning problem because MongoDB must evaluate both conditions.



3. High Call Volume

A single expensive query is multiplied by 495+ calls/minute, compounding load on the database.





---

3. Technical Root Cause

Core Issue: Unbounded $regex queries on two fields, triggered at a high request rate, causing full collection scans on the EmployeeProfile collection. The cluster’s CPU usage spiked due to the volume of regex evaluations, which are CPU-intensive.


---

4. Recommendations and Optimizations

1. Add Appropriate Indexes

Compound or Single-Field Index: If you need partial text search and you know that employeeLogin or samAccountName typically matches from the start of the string, consider creating a compound index that includes sourceSystem, employeeStatus, and one of these fields.

Prefix-Based Regex: If your search is anchored at the beginning (e.g. '^somePrefix'), MongoDB can leverage the index. If you truly need substring matches anywhere in the string, a normal B-Tree index helps less, so consider a text index or a specialized approach.



2. Query Restructuring

Split the OR Logic: If typically one field is used more frequently than the other, query that field first with a standard or anchored lookup. Only resort to a broader $regex if that yields no results. This reduces the overhead of evaluating both conditions each time.

Parameterized Search: Depending on your business logic, you might not need a full substring search. Try exact matches first or partial matches on indexed fields.



3. Reduce Call Frequency

Rate Limiting / Throttling: Implement API-level throttles (e.g., in Apigee or the service layer). This helps protect the database from unintentional or malicious call patterns.

Caching: If the same data is requested repeatedly, consider caching frequently accessed results (in-memory cache like Redis, or a dedicated caching mechanism).



4. Consumer-Side Fix

The API consumer may be misconfigured or calling /ByLandID in a loop. Investigate and correct that usage to prevent excessive requests.



5. Performance Testing & Monitoring

Load Testing: Recreate the call pattern in a test environment to ensure the new indexing/queries handle the anticipated load.

Observability: Set up alerting (e.g., CPU usage alerts, slow query logs) so you can act on abnormal spikes more quickly.





---

5. Step-by-Step Mitigation Plan

1. Immediate

Add Index on (sourceSystem, employeeStatus, employeeLogin) or (sourceSystem, employeeStatus, samAccountName) as needed.

Lock Down the consumer’s call rate. Temporarily limit the TPS (transactions per second) via gateway or service-level controls.



2. Short-Term

Refactor the Query to remove or reduce unbounded $regex.

Batch or Cache: If the consumer is loading data for multiple employees, consider a batched endpoint instead of repeated single lookups.



3. Long-Term

Investigate Client Logic: Identify the root cause of the 495+ calls/min (infinite loops, poor scheduling, etc.).

Implement Observability (logging, metrics, dashboards) for early detection of spikes.

Revisit Search Requirements: If advanced partial matching is truly needed at high scale, consider using a specialized search engine (e.g., Elasticsearch).





---

6. Conclusion

The technical bottleneck lies primarily in high-volume regex queries on unindexed fields. By adding indexes, optimizing the query, and throttling or caching at the API layer, the MongoDB cluster load should stabilize. Collaboration with the API consumer is essential to prevent excessive or repetitive calls. Once these steps are implemented and tested, you should see a significant reduction in CPU usage and improved overall response times.


---

Note: Always validate index effectiveness by analyzing your MongoDB query plan (db.<collection>.explain()) to confirm that your newly added indexes are being used as expected.


