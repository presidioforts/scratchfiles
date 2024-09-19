

### 1. Validation Before Posting to Kafka
- I wanted to check if we’re performing any specific data validation before sending messages to Kafka. Are we ensuring that the message structure and required fields are in place?
- Are there any mechanisms in place to handle cases where the data might fail validation before posting to Kafka?

### 2. Debugging in Async Transactions (Logging Strategy)
- Are we currently using a transaction ID or correlation ID for better traceability across services, from the UI to Kafka and MongoDB? If not, do you think it would be helpful to implement?
- I think having clear log levels across the services (INFO, DEBUG, ERROR) could help with debugging. Is this something we’ve already set up?
- Do we have any logging in place for tracking errors, specifically around Kafka message consumption and MongoDB persistence? Just wondering if there’s more we can do here.

### 3. Handling Duplicates (Idempotency in Kafka)
- I wanted to ask if we’re assigning unique message keys for Kafka messages to avoid duplicates? It might help with idempotency.
- How are we managing Kafka offsets? Just wondering if we’re tracking them properly to avoid any issues with duplicate processing.
- Do you think enabling Kafka’s exactly-once semantics (EOS) would be useful in this case? I thought it might help with preventing duplicates.

### 4. Retry Logic
- I’m not sure how we’re handling retries if a message fails to persist in MongoDB. Do we have a retry mechanism in place?
- Is there a dead letter queue (DLQ) set up for failed messages, or do you think that would be something worth implementing?
- Are we monitoring for any failed transactions that aren’t being retried? I was thinking we might be able to set up alerts for that.
