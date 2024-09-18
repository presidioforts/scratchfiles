Certainly! Here is the updated API documentation with the missing details added to Table 1.

# Authentication Service API Documentation

## Introduction

Welcome to the **Authentication Service API** documentation. This API provides a secure and standardized method for authenticating users and client applications using OAuth 2.0. Clients can obtain access tokens to interact with protected resources securely. This document outlines the API endpoints, request and response details, error codes, and best practices to help you integrate smoothly.

---

## Table 1: API Overview

| **Field**               | **Description**                                                  | **Example**                                 |
|-------------------------|------------------------------------------------------------------|---------------------------------------------|
| **API Name**            | Name of the API                                                  | Authentication Service API                  |
| **Base URL**            | The root URL for API requests                                    | `https://api.example.com/v1/`               |
| **Supported Versions**  | API versioning and backward compatibility                        | `v1`, `v2`                                  |
| **Method**              | HTTP methods used by the API                                     | `POST`, `GET`                               |
| **Endpoint**            | Relative URL of the API endpoint                                 | `/oauth/token`                              |
| **Authentication**      | Method of authentication for API requests                        | OAuth 2.0 Bearer Token                      |
| **Rate Limiting**       | Maximum number of requests allowed per time interval             | 100 requests per minute                     |
| **GitHub Repository**   | Link to the GitHub repository where the API code is maintained   | `https://github.com/example/repo`           |
| **MongoDB Collections** | MongoDB collections related to the API for data storage          | `tokens`, `clients`, `device_registrations` |
| **Success Response**    | Example of a successful API response                             | `{ "access_token": "ABC123", "expires_in": 3600 }` |
| **Error Response**      | Example of an error response                                     | `{ "error": "invalid_request", "error_description": "Invalid credentials" }` |

### Endpoints and Methods

| **Endpoint**          | **Method** | **Description**                        |
|-----------------------|------------|----------------------------------------|
| `/oauth/token`        | `POST`     | Obtain an access token                 |
| `/oauth/revoke`       | `POST`     | Revoke an existing access token        |

### Versioning

Include the version number in the base URL:

- **Version 1**: `https://api.example.com/v1/`
- **Version 2**: `https://api.example.com/v2/`

### Authentication

All requests must be made over HTTPS. Include the access token in the `Authorization` header:

```
Authorization: Bearer {access_token}
```

### Rate Limiting

Exceeding the rate limit returns a `429 Too Many Requests` status code. Check the `Retry-After` header to know when to retry.

---

## Table 2: API Request and Response Details

### Service: Requesting an Access Token

#### Endpoint

`POST /oauth/token`

#### Required Headers

- `Content-Type: application/x-www-form-urlencoded`
- `Accept: application/json`

#### Parameters

| **Parameter**     | **Type** | **Required**                              | **Constraints**                                      | **Description**                                                    | **Example**                         |
|-------------------|----------|-------------------------------------------|------------------------------------------------------|--------------------------------------------------------------------|-------------------------------------|
| `grant_type`      | string   | Yes                                       | Must be one of: `password`, `client_credentials`     | Type of OAuth 2.0 flow                                             | `password`                          |
| `client_id`       | string   | Yes                                       | Max length: 50 characters                            | Unique identifier of the client application                        | `abc123`                            |
| `client_secret`   | string   | Required if client is confidential        | Max length: 50 characters                            | Client secret for confidential clients                             | `xyz456`                            |
| `username`        | string   | Required if `grant_type` is `password`    | Max length: 100 characters                           | The resource owner's username                                      | `user@example.com`                  |
| `password`        | string   | Required if `grant_type` is `password`    | Max length: 100 characters                           | The resource owner's password                                      | `password123`                       |
| `platform`        | string   | Yes                                       | Allowed values: `1`, `2`                             | Payment platform (`1` for CYBS, `2` for ANET)                      | `1`                                 |
| `device_id`       | string   | Required if client is a mobile application| 32-character hexadecimal string                      | Device ID for mobile clients                                       | `0e527cd6df507d99d595a0113b798f3e`  |
| `merchant_id`     | string   | Optional                                  | Max length: 50 characters                            | Merchant ID or `INTERNAL` for internal accounts                    | `merchant123`                       |

#### Example Request (cURL)

```bash
curl -X POST https://api.example.com/v1/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d "grant_type=password&client_id=abc123&client_secret=xyz456&username=user@example.com&password=password123&platform=1&device_id=0e527cd6df507d99d595a0113b798f3e"
```

#### Example Success Response

```json
{
  "access_token": "ABC12345ABCDE6789TOKEN",
  "token_type": "Bearer",
  "expires_in": 14400,
  "client_status": "active",
  "scope": "PaymentVerificationPermission PaymentDebitPermission"
}
```

#### Example Error Response

```json
{
  "error": "invalid_request",
  "error_description": "Device ID format is invalid."
}
```

---

### Service: Revoking an Access Token

#### Endpoint

`POST /oauth/revoke`

#### Required Headers

- `Content-Type: application/x-www-form-urlencoded`
- `Accept: application/json`

#### Parameters

| **Parameter**     | **Type** | **Required**                              | **Constraints**                                      | **Description**                                                    | **Example**                         |
|-------------------|----------|-------------------------------------------|------------------------------------------------------|--------------------------------------------------------------------|-------------------------------------|
| `token`           | string   | Yes                                       | Max length: 255 characters                           | The access token to revoke                                         | `ABC12345ABCDE6789TOKEN`            |
| `client_id`       | string   | Yes                                       | Max length: 50 characters                            | Unique identifier of the client application                        | `abc123`                            |
| `client_secret`   | string   | Required if client is confidential        | Max length: 50 characters                            | Client secret for confidential clients                             | `xyz456`                            |
| `device_id`       | string   | Required if client is a mobile application| 32-character hexadecimal string                      | Device ID for mobile clients                                       | `0e527cd6df507d99d595a0113b798f3e`  |

#### Example Request (cURL)

```bash
curl -X POST https://api.example.com/v1/oauth/revoke \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d "token=ABC12345ABCDE6789TOKEN&client_id=abc123&client_secret=xyz456&device_id=0e527cd6df507d99d595a0113b798f3e"
```

#### Example Success Response

```json
{
  "result": "Token revoked successfully."
}
```

#### Example Error Response

```json
{
  "error": "invalid_request",
  "error_description": "The token provided is invalid or has already been revoked."
}
```

---

## Table 3: Error Codes and Troubleshooting

### Common Error Codes

| **HTTP Status Code** | **Error Code**           | **Description**                                         | **Suggested Fix**                                         |
|----------------------|--------------------------|---------------------------------------------------------|-----------------------------------------------------------|
| 400                  | `invalid_request`        | Missing or invalid request parameters                   | Ensure all required parameters are included and valid.    |
| 401                  | `invalid_client`         | Invalid client credentials                              | Verify the `client_id` and `client_secret`.               |
| 401                  | `invalid_grant`          | Invalid user credentials or grant type                  | Check `username`, `password`, and `grant_type`.           |
| 400                  | `unsupported_grant_type` | The `grant_type` is not supported                       | Use a supported `grant_type` (e.g., `password`).          |
| 403                  | `unauthorized_client`    | Client not authorized for this grant type               | Confirm client permissions and allowed grant types.       |
| 429                  | `rate_limit_exceeded`    | Too many requests in a given time frame                 | Wait for the rate limit to reset (see `Retry-After` header). |
| 500                  | `server_error`           | Internal server error                                   | Retry later or contact support if the issue persists.     |

### Troubleshooting Tips

- **Invalid Credentials**: Double-check the `client_id`, `client_secret`, `username`, and `password`.
- **Invalid Device ID**: Ensure `device_id` is a valid 32-character hexadecimal string.
- **Rate Limit Exceeded**: Monitor your request rates and implement backoff strategies.
- **Unsupported Grant Type**: Confirm that the `grant_type` is among the supported types.

---

## Security Considerations

- **HTTPS Required**: All requests must use HTTPS to protect data in transit.
- **Secure Token Storage**: Store access tokens securely; do not expose them in client-side code or logs.
- **Token Expiration**: Tokens expire as indicated by `expires_in`. Obtain new tokens as needed.
- **Sensitive Data Handling**: Do not transmit sensitive data like passwords over insecure channels.

---

## Glossary of Terms

- **OAuth 2.0**: An authorization framework enabling applications to obtain limited access to user accounts.
- **Access Token**: A token that grants access to protected resources.
- **Client Application**: The application making requests to the API.
- **CYBS**: CyberSource payment platform.
- **ANET**: Authorize.Net payment platform.
- **INTERNAL**: Denotes internal accounts within the system.

---

## Contact and Support

For assistance or to report issues, contact our support team:

- **Email**: support@example.com
- **Documentation**: [API Docs](https://api.example.com/docs)
- **Developer Portal**: [Developer Site](https://developer.example.com)
- **GitHub Repository**: [API Repository](https://github.com/example/repo)

---

Thank you for using the Authentication Service API. We strive to provide a seamless integration experience. If you have any feedback or need further assistance, please reach out to our support team.
