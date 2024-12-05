### **2025 Resource Planning for EPL-X Product**

#### **Summary**
The EPL-X product 2025 resource planning focuses on addressing systemic platform issues, managing workflows, and supporting infrastructure services efficiently. The responsibilities are divided among three key teams: **Performance Engineering**, **Breakfix Incident**, and **Infrastructure Platform Service**. While automation and empowering app developers self-service aim to reduce SDLC/DevOps tickets, resource estimations highlight the need for 10–11 engineers in the Breakfix team by 2025 to handle the increased ticket volume. No additional resources are required for Performance Engineering or Infrastructure Platform Service teams.

---

#### **1. Responsibilities**

- **Performance Engineering Team**:
  - Address systemic platform and product issues.
  - Resolve EPL-X platform architecture challenges.
  - **Resource Note**: No additional resources are required. The PE and SME teams will continue to work on EPL-X similarly to EPL.

- **Breakfix Incident Team**:
  - Manage workflows for 9 buildpacks (Gradle-java, dotnet, npm, python) covering:
    - Checkout, Build, Test, Publish, Code Sign, Secrets, Sonar,Scan.
  - Support integrations with JFrog CLI, Redis, Object Store, HashiCorp Vault, and Artifactory.
  - Handle post migration/onboarding issues and infrastructure-specific workflows (GITSAS, SCP, GITACT).
  - Manage and resolve standard tickets, including scan/code coverage, Sonar, and tool configuration issues.
  - **Resource Needs**: To manage the projected ticket volume, the team will require 10–11 engineers by 2025.
  - - **Automation**:
    - Deploy self-service automation for workflow input variables to streamline ticket handling.
    - Empower **app developers** to manage configurations independently, enabling faster troubleshooting and reducing manual intervention.
    - Reduce **SDLC/DevOps tickets** by automating routine workflows and configuration processes.

- **Exclusion**:
  - Migration of EPL-X infrastructure from TKGI to OpenShift will be handled solely by the SME team and is not part of Breakfix team responsibilities.

- **Infrastructure Platform Service Team**:
  - Oversee EPL-X infrastructure, including automation and platform services.
  - Manage infrastructure tasks such as migrations from TKGI to OpenShift.
  - Support self-service automation tools for workflow input variables specific to infrastructure components.
  - **Resource Note**: Current SME team and infrastructure automation engineers will handle these tasks, requiring no additional resources.

---

#### **2. Breakfix Incident Team Ticket Management**
- **Standard Tickets**:
  - Issues related to scan/code coverage, Sonar, and other tool configurations.
- **Ticket Volume**:
  - Projected 2025 volume: ~10,000 tickets for ~10,000 components.
- **Ticket Handling Capacity**:
  - **Per Engineer**:
    - Capacity: 5 tickets/day × 22 working days = **1320 tickets/month**.
    - Adjusted for PTO/Training (17%): Remove 224 tickets, leaving **1096 tickets/month**.
  - **Resource Requirement**:
    - To handle 10,000 tickets, **10–11 engineers** will be required in 2025.

  Above estimation based on below 2025 EPL-X App Migration plan**
- **Timeline**:
  - **2024 Q3**: ~130 components migrated in non-production; <40 in production.
  - **2024 Q4–2025 Q1**: Target ~300 components.
  - **2025 Q2**: ~1,000–1,500 components.
  - **2025 Q3**: ~5,000 components.
  - **2025 End**: Target ~10,000 components migrated, marking a major milestone for EPL-X product and platform stabilization.
  

