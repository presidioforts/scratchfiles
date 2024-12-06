## **Observability Status**

| **Task**                                                         | **Description**                                                               | **Status**             | **Notes**                                                                                                                                                                | **Owner**                 |
|------------------------------------------------------------------|-------------------------------------------------------------------------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| **Endpoints Availability Health Check Monitoring (ThousandEyes)** | Monitor endpoint availability and health using ThousandEyes.                 | In Progress            | Out of 23 services, 6 have been implemented. Approximately 30+ services are not ready for healthcheck integration. Engineering is actively fixing the endpoints. Observability team is working on the remaining integrations. | Observability Engineering |
| **External Resource Monitoring (Kafka)**                         | Monitor Kafka external resources to ensure seamless operations.               | Drafting Requirement   | Requirements are being drafted to effectively monitor Kafka external resources.                                                                                            | Platform Services Team    |
| **AppDynamics**                                                  | Implement AppDynamics for comprehensive application performance monitoring.  | Completed              | Fully operational, providing real-time insights into application performance and facilitating proactive issue resolution.                                                 | Platform Services Team    |

---

## **NFR Implementation Status**

| **Task**                                                 | **Description**                                                                 | **Status**                        | **Owner**                          |
|----------------------------------------------------------|---------------------------------------------------------------------------------|-----------------------------------|------------------------------------|
| **Slow Query Mongo DB (NFR)**                            | Optimize MongoDB queries to reduce latency and improve performance.             | In Progress, JIRA created         | Platform Service + SCP Engineering |
| **Standardization of API Response for Observability**     | Standardize API responses to enhance observability and consistency.              | Planned                           | Platform Services Team             |
| **Kafka Bad Message Handling**                           | Develop and implement mechanisms to handle and log bad messages in Kafka streams. | In Progress, JIRA created         | SCP Engineering                    |

---

