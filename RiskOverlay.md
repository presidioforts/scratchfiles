Incident Response and Risk Management: Artifactory Upgrade Case

Current Situation: A significant incident occurred, which was escalated to senior management. The root cause, identified during the Root Cause Analysis (RCA), was linked to an Artifactory infrastructure upgrade. The upgrade caused failures in the Conda Python buildpack because the Anaconda client binary version in use was outdated and incompatible with the upgraded Artifactory environment, which required the latest 2024 version.

Risk Overlay Expectation: We have a well-established upgrade process that includes EPL product regression testing, Operations UAT acceptance, and customer UAT sign-off before any upgrade is implemented. Unfortunately, this process was not followed. The Artifactory infrastructure and operations teams proceeded with the upgrade without adhering to the required validation and testing steps.

Remediation: To resolve the issue, we updated the older Anaconda client library to a compatible version and deployed a fix to production, stabilizing the platform. Immediate corrective action minimized further customer impact.

Next Steps: We are currently upgrading the lower production environments while ensuring strict compliance with the validation process for future upgrades. Additionally, the Infra engineering team has been formally reminded to rigorously follow the established testing and approval process to prevent similar oversights in the future.
