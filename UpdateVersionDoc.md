# CIWAT SCP API Platform – Platform Service Home

**Document Version:** 1.1  
**Last Updated:** YYYY-MM-DD  
**Owner:** Platform Service Team  

---

## Overview

The **CIWAT SCP API Platform** is a centralized microservices solution designed to unify API management and integration across our core DevOps products.

### Supported CI/CD Products
- **EPL:** A CI system powered by Cloudbee Jenkins.
- **EPL-X:** A CI system leveraging GitHub Actions.
- **Harness:** A deployment platform for OpenShift container environments.

### Team Structure
The platform is managed by the **Platform Service Team**, consisting of:
- **Performance Team**: Focuses on API response time and system throughput.
- **Observability Team**: Ensures logging, monitoring, and alerting best practices.
- **Infrastructure Team**: Manages cloud resources and platform scalability.
- **Breakfix Team**: Handles incident resolution and quick remediation.

This document serves as a **single source of truth** for API operations, integration checks, troubleshooting, and platform performance standards.

---

## API Integration Mapping to CI/CD Workflow

This section maps **API endpoints** to specific CI/CD workflow stages, showing when each API is called and its expected outcome.

| CI/CD Stage  | API Endpoint | Purpose | Expected Outcome |
|-------------|------------|---------|----------------|
| **EPL (Build)** | `/validate` | Runs validation checks | Returns validation status |
| **EPL-X (Testing)** | `/run-tests` | Executes integration tests | Test results returned |
| **Harness (Deployment)** | `/deploy` | Deploys artifacts to OpenShift | Deployment success/failure |
| **Post-Deployment** | `/health` | Checks system health | Returns API health status |

> **Action:** Fill in this table with actual API endpoints used in each CI/CD stage.

---

## API Call Sequence in CI/CD Workflow

Below is a step-by-step breakdown of API calls within the **CI/CD pipeline**:

1. **Code Commit → EPL Stage**
   - [API] `/validate` → Runs static validation
   - [API] `/dependency-check` → Checks for dependency issues

2. **EPL-X Stage (Extended Testing)**
   - [API] `/run-tests` → Executes unit & integration tests
   - [API] `/security-scan` → Runs security vulnerability scans

3. **Harness Stage (Deployment)**
   - [API] `/deploy` → Deploys artifacts
   - [API] `/config-sync` → Ensures configuration consistency

4. **Post-Deployment Health Check**
   - [API] `/health` → Validates service readiness

> **Action:** Update this section with the **actual sequence of API calls** used in your platform.

---

## Production Changes & Maintenance

### Daily Maintenance Tasks  
- Monitor system health and log errors.
- Verify successful backups and scheduled jobs.
- Manage disk space by pruning outdated logs and data.

### Monthly Maintenance Tasks  
- Archive old records and move logs to long-term storage.
- Apply security patches and updates to services.
- Review performance metrics and adjust scaling as needed.

### Yearly Maintenance Tasks  
- Perform full data archival for records beyond the retention policy.
- Audit infrastructure components and schedule necessary upgrades.
- Update maintenance documentation and refine escalation paths.

> **Action:** Specify the actual teams responsible for each task.

---

## API Enhancements & Change Management

All API updates follow a structured release process documented in:
- **[Release Cargo](#)**: High-level release summary.
- **[API Manifest](#)**: Detailed list of modified components.
- **[Post-Production Validation (PPV)](#)**: Outcome of deployment verification tests.

### Notification Process for Platform Team
- Engineers must document API changes in the Release Cargo and notify the Platform Team via **[Slack/#api-releases](#)**.
- Pre-deployment meetings are held to discuss upcoming changes.
- If CI/CD pipeline modifications are needed, the Platform Team collaborates with Engineering before deployment.

> **Action:** Add links to internal release documentation.

---

## API Performance Monitoring

### Key API Metrics
| Metric | Description | Target Value |
|--------|------------|-------------|
| **Response Time (p95)** | Time taken for 95% of requests | < 200ms |
| **Error Rate** | Percentage of failed API calls | < 1% |
| **Throughput** | Number of requests per second | > 100 rps |

### Monitoring & Alerting
- **Logging:** Logs are aggregated in **[Log Aggregator]**.
- **Alerting:** Notifications sent via **[PagerDuty/Slack]** if SLAs are violated.

> **Action:** Specify monitoring tools and alert conditions.

---

## Runbook for Production Incidents

### Incident Classification & Escalation
| Severity | Impact | Escalation |
|----------|--------|------------|
| **P1** | System-wide outage | Immediate team page & incident bridge |
| **P2** | Partial failure | Notify on-call engineer; escalate if unresolved in 1 hour |
| **P3** | Minor issue | Assigned during business hours |

### Incident Handling Process
1. **Acknowledge & Assign**: On-call engineer acknowledges alert.
2. **Triage**: Identify affected services and gather logs.
3. **Mitigation**: Apply quick fixes if possible.
4. **Resolution**: Fix root cause and validate recovery.
5. **Post-Incident Review**: Document findings and update procedures.

### Troubleshooting Template
- **Summary:** What is failing and how it was detected.
- **Logs & Metrics:** Gather error messages and performance data.
- **Recent Changes:** Identify deployments or config updates.
- **Mitigation Actions:** Rollbacks, scaling adjustments, failovers.
- **Escalation:** Contact the appropriate engineering teams.

> **Action:** Customize the runbook with real-world troubleshooting scenarios.

---

## SLA, SLO, and Operational Targets

### **Service Level Agreements (SLA)**
| Metric | Commitment |
|--------|-----------|
| **API Uptime** | 99.9% availability |
| **Response Time** | < 200ms per request |
| **Incident Resolution** | Critical issues resolved within 1 hour |

### **Service Level Objectives (SLO)**
- Maintain **99.99%** API reliability across all integrations.
- Ensure API **error rate stays below 0.5%**.

> **Action:** Define actual SLAs, SLOs, and OPT goals relevant to your platform.

---

## Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.1 | YYYY-MM-DD | Platform Service Team | Added maintenance, API enhancements, and incident runbook. |

---

_This document is a living resource and will be updated regularly to reflect process improvements, integration updates, and evolving operational standards._
