Authentication Service API Documentation

Introduction

Welcome to the Authentication Service API documentation. This API provides a secure and standardized method for authenticating users and client applications using OAuth 2.0. Clients can obtain access tokens to interact with protected resources securely. This document outlines the API endpoints, request and response details, error codes, infrastructure details, and best practices to help you integrate smoothly.


---

Table 1: API Overview

Endpoints and Methods

Versioning

Include the version number in the base URL:

Version 1: https://api.example.com/v1/

Version 2: https://api.example.com/v2/


Authentication

All requests must be made over HTTPS. Include the access token in the Authorization header:

Authorization: Bearer {access_token}

Rate Limiting

Exceeding the rate limit returns a 429 Too Many Requests status code. Check the Retry-After header to know when to retry.


---

Table 2: API Request and Response Details

Service: Requesting an Access Token

Endpoint

POST /oauth/token

Required Headers

Content-Type: application/x-www-form-urlencoded

Accept: application/json


Parameters

Example Request (cURL)

curl -X POST https://api.example.com/v1/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d "grant_type=password&client_id=abc123&client_secret=xyz456&username=user@example.com&password=password123&platform=1&device_id=0e527cd6df507d99d595a0113b798f3e"

Example Success Response

{
  "access_token": "ABC12345ABCDE6789TOKEN",
  "token_type": "Bearer",
  "expires_in": 14400,
  "client_status": "active",
  "scope": "PaymentVerificationPermission PaymentDebitPermission"
}

Example Error Response

{
  "error": "invalid_request",
  "error_description": "Device ID format is invalid."
}


---

Service: Revoking an Access Token

Endpoint

POST /oauth/revoke

Required Headers

Content-Type: application/x-www-form-urlencoded

Accept: application/json


Parameters

Example Request (cURL)

curl -X POST https://api.example.com/v1/oauth/revoke \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d "token=ABC12345ABCDE6789TOKEN&client_id=abc123&client_secret=xyz456&device_id=0e527cd6df507d99d595a0113b798f3e"

Example Success Response

{
  "result": "Token revoked successfully."
}

Example Error Response

{
  "error": "invalid_request",
  "error_description": "The token provided is invalid or has already been revoked."
}


---

Table 3: Error Codes and Troubleshooting

Common Error Codes

Troubleshooting Tips

Invalid Credentials: Double-check the client_id, client_secret, username, and password.

Invalid Device ID: Ensure device_id is a valid 32-character hexadecimal string.

Rate Limit Exceeded: Monitor your request rates and implement backoff strategies.

Unsupported Grant Type: Confirm that the grant_type is among the supported types.



---

Table 4: Infrastructure Details

Deployment Environments

The Authentication Service API is hosted on Pivotal Cloud Foundry (PCF) and is available in the following environments:

Kafka Integration

The API interacts with Apache Kafka for event streaming and message queuing.

Kafka Topics Used

Kafka Configuration

Bootstrap Servers: kafka1.example.com:9092, kafka2.example.com:9092

Security Protocol: SSL

Consumer Group ID: auth-service-group


Hosting Platform

Platform: Pivotal Cloud Foundry (PCF)

Regions: (Specify regions if applicable, e.g., US-East, EU-West)

Scaling: Auto-scaling enabled based on load


MongoDB Collections

Database: auth_db

Collections:

tokens: Stores access and refresh tokens

clients: Contains client application details

device_registrations: Holds mobile device registrations


Replica Set: (Provide details if applicable)



---

Security Considerations

HTTPS Required: All requests must use HTTPS to protect data in transit.

Secure Token Storage: Store access tokens securely; do not expose them in client-side code or logs.

Token Expiration: Tokens expire as indicated by expires_in. Obtain new tokens as needed.

Sensitive Data Handling: Do not transmit sensitive data like passwords over insecure channels.

Access Control: Ensure proper access controls are in place for different environments.



---

Glossary of Terms

OAuth 2.0: An authorization framework enabling applications to obtain limited access to user accounts.

Access Token: A token that grants access to protected resources.

Client Application: The application making requests to the API.

CYBS: CyberSource payment platform.

ANET: Authorize.Net payment platform.

INTERNAL: Denotes internal accounts within the system.

PCF: Pivotal Cloud Foundry, a cloud platform for deploying applications.

Kafka: A distributed streaming platform used for building real-time data pipelines and streaming apps.



---

Contact and Support

For assistance or to report issues, contact our support team:

Email: support@example.com

Documentation: API Docs

Developer Portal: Developer Site

GitHub Repository: API Repository



---

Thank you for using the Authentication Service API. We strive to provide a seamless integration experience. If you have any feedback or need further assistance, please reach out to our support team.


---

Appendix: Additional Information

Environment Configuration Details

Development Environment

Purpose: Internal development and testing

Access: Restricted to internal IPs or VPN

Data: Uses test data; no real user information


UAT Environment

Purpose: Testing by QA and stakeholders before production release

Access: Controlled access, possibly extended to key clients

Data: Staging data that simulates production


Production Environment

Purpose: Live environment serving end-users

Access: Publicly accessible over the internet

Data: Real user data; complies with all data protection regulations


Monitoring and Logging

Monitoring Tools: (Specify tools, e.g., Prometheus, New Relic)

Logging: Centralized logging using Kafka topic auth-service-logs

Access to Logs: Logs are accessible to authorized personnel for troubleshooting


Deployment Pipeline

CI/CD Tools: (Specify tools, e.g., Jenkins, GitLab CI/CD)

Deployment Frequency: Regular deployments in dev and UAT; scheduled releases to production


How to Use This Information

Developers: Use the appropriate environment URLs for development and testing.

DevOps Engineers: Reference the Kafka topics and infrastructure details for setup and maintenance.

Security Teams: Review the hosting and infrastructure details to ensure compliance with security policies.



---

By including this Infrastructure Details section, we've provided comprehensive information to assist developers, DevOps engineers, and other stakeholders in understanding the API's operational context and integration points. This addition enhances transparency and facilitates smoother collaboration across teams.


---

If you have any further questions or need additional details, please don't hesitate to contact our support team.

