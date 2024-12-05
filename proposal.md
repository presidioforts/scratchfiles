**2025 Platform Service Team Resource Planning for EPL-X Product**  

**Summary**  
In 2025, the EPL-X Resource Planning strategy is focused on managing a projected ~10,000 annual tickets supporting ~10,000 migrated components, stabilizing the platform, and enabling efficient developer self-service. This approach anticipates the evolving complexity of the EPL-X(GITSAS, GITACT) product and Infrastructure environment. Three teams will continue to handle the EPL-X Platform Services - Infrastructure and Operation:

- **Performance Engineering (PE)**: Address systemic platform and product issues with existing headcount.
- **Breakfix Incident Team**: Scale to 10–11 engineers to handle standard incident tickets and workflow challenges. Introduce self-service automation to reduce manual intervention and enable developer self-service.
- **Infrastructure Platform Service Team (SME/Automation Engineers)**: Oversee infrastructure migrations and services without additional resources, ensuring the underlying platform supports growth and stability.

---

### 1. Team Responsibilities & Scope

**1.1 Performance Engineering Team**  
- **Primary Responsibilities:**
  - Address systemic platform and product issues impacting EPL-X.
  - Collaborate with Workflow SME and Infra SME teams to resolve architectural challenges.
- **Resource Note:**  
  - No additional resources needed for 2025.  
  - The existing PE and SME teams will continue supporting EPL-X similarly to EPL, ensuring platform optimizations and reducing recurring incidents.

**1.2 Breakfix Incident Team**  
- **Primary Responsibilities:**
  - Manage and resolve standard workflow tickets across 9 buildpacks (e.g., Gradle-java, dotnet, npm, python), including:  
    - Checkout, Build, Test, Publish, Code Sign, Secrets Management, Sonar Scanning, and Security Scan.
  - Support integrations with JFrog CLI, Redis, Object Store, HashiCorp Vault, and Artifactory.
  - Triage and resolve post-migration/onboarding issues specific to EPL-X infrastructure, including GITSAS, SCP, and GITACT workflows.
  - Handle standard tickets (e.g., scan/code coverage, Sonar, and tool configuration issues) to maintain developer velocity.
  
- **Automation & Self-Service Initiatives:**
  - Deploy self-service automation tools for workflow input variables, enabling developers to configure and troubleshoot their EPL-X workflow pipeline independently.
  - Track adoption metrics (e.g., % of tickets resolved via self-service) to measure success.

- **Exclusion:**
  - Migration of EPL-X infrastructure from TKGI to OpenShift is out of scope for this team and will be led by the SME/Infrastructure team.

- **Resource Requirements:**
  - Current projections estimate ~10,000 standard tickets in 2025.
  - Each engineer can effectively handle ~1,096 tickets/month after accounting for PTO/training.
  - Based on projected volume, 10–11 engineers will be required by the end of 2025.

- **Ramp-Up Plan:**
  - **2024 Q4–2025 Q1:** Incrementally add engineers (3–4 engineers) as components grow to ~300.  
  - **2025 Q2:** Reach ~7–8 engineers to handle ~1,000–1,500 components.  
  - **2025 Q3:** Scale up to 10–11 engineers as we approach ~5,000 components.  
  - **End of 2025:** Final team size at 10–11 engineers to support ~10,000 components, achieving a major EPL-X milestone.

**1.3 Infrastructure Platform Service Team**  
- **Primary Responsibilities:**
  - Oversee EPL-X infrastructure services, including the TKGI to OpenShift migration.
  - Maintain platform-level automation and ensure stable foundational services.
  - Provide and enhance infrastructure-level self-service tools.
  
- **Resource Note:**
  - No additional resources required. The current SME team and infrastructure automation engineers will handle tasks associated with platform migrations and ongoing support.

---

### 2. Breakfix team Capacity Planning

**Per Engineer Per Month:**  
  - 5 tickets/day × 22 working days ≈ 110 tickets/month per engineer.
  - With process improvements, each engineer can escalate to handle approximately 60 tickets/week (≈ 240 tickets/month).
  - After accounting for PTO/training (~17%), a safe estimate is ~1,096 tickets/engineer/year (adjusting the monthly figure to align with annual totals and training assumptions).
  
- **Total Resource Requirement:**
  - To handle 10,000 tickets annually: ~10–11 engineers.

---

### 3. Migration & Growth Milestones

**App Component Migration Schedule**  
- **2024 Q3:** ~130 components migrated in non-production, <40 in production.
- **2024 Q4–2025 Q1:** Migrate ~300 components.
- **2025 Q2:** Migrate ~1,000–1,500 components, triggering a higher ticket load.
- **2025 Q3:** Scale up to ~5,000 components.
- **By End of 2025:** Achieve the major milestone of migrating ~10,000 components.

