
Below is a revised Non-Functional Requirement (NFR) user story that specifically references your Kafka payload-signing Bash script. This version includes sample code snippets from the current implementation to illustrate how Bash-based complexity could become a liability in a growing enterprise environment. The overall goal remains the same: transitioning to a JavaScript-based GitHub Action for greater maintainability, observability, and future-proofing.


---

NFR User Story: Migrate Kafka Payload-Signing Logic to JavaScript Action

Title:
Adopt a JavaScript-Based Action for Kafka Payload Signing & Deployment

As a DevOps Engineer (responsible for enterprise CI/CD pipelines),
I want to replace the Bash-based Kafka payload-signing script with a Node.js/JavaScript GitHub Action,
so that the system remains maintainable, secure, and scalable while meeting our event-driven (Kafka) deployment requirements.


---

Description

We currently use a Bash script to construct, sign, and publish deployment payloads to Kafka (“EVENT_BASED” integration). The script depends on commands like sed, awk, openssl, and manual environment checks. As the product grows, maintaining and extending these shell-based steps introduces several risks:

1. Complex, Hard-to-Read Logic

The script constructs JSON with awk/sed, for example:

IMG_NAME="$(echo ${{ env.IMAGE_NAME }} | awk -F ':' '{print $1}')"
IMG_TAG="$(echo ${{ env.IMAGE_NAME }} | awk -F ':' '{print $2}')"

This is concise but fragile if IMAGE_NAME is missing or malformed.

Large blocks of inline logic complicate debugging:

if [ "${{ env.WORKFLOW_TYPE }}" == "snapshot" ]; then
  stageId="dev"
else
  stageId="dev,test"
fi

Repeated conditionals expand quickly as new environment variables or integration points are added.



2. OpenSSL Reliance & Silent Failures

The script signs payloads using:

openssl dgst -sha256 \
  -sigopt rsa_padding_mode:pss \
  -sigopt rsa_pss_saltlen:-1 \
  -sign "$GITHUB_WORKSPACE/jwt-certs/jwt.key" \
  -out signature.bin

However, there is no strict exit-code check; if this fails, the script may continue, producing an empty or invalid signature without a clear error message.



3. Limited Observability & Logging

The script uses a handful of echo statements, e.g.:

echo "Raw kafka_payload => $kafka_payload"

But no structured logging or try/catch mechanism. In an enterprise setting, diagnosing issues from minimal console output is time-consuming.



4. Kubernetes, Yet Still Bash

Even though we run on Linux-based self-hosted Kubernetes runners, the shell script remains prone to environment drift (like missing dependencies or changes in package versions). A JavaScript action using Node’s built-in libraries avoids these pitfalls.




A JavaScript-based GitHub Action that replicates (and enhances) this functionality will enable cleaner error handling, easier versioning, and smoother collaboration across teams.


---

Acceptance Criteria

1. JavaScript Action for Kafka Deployment

The existing Bash script (referenced above) is refactored into a Node.js-based GitHub Action.

Payload construction, signing (RSA-PSS), and Kafka publishing must be encapsulated in modular JS functions (@actions/core or a well-known Kafka library as needed).



2. Structured Error & Logging

Critical steps (e.g., signing the payload) should be wrapped in try/catch blocks with descriptive error messages.

Use core.info, core.warning, and core.error to provide clarity on process stages and failures.



3. Security & Compliance

Sensitive data such as private keys or signatures must never be logged in plaintext.

If using the Node crypto module, ensure it matches enterprise standards for RSA-PSS, SHA-256 hashing, and salt length.

Incorporate any relevant Snyk or Dependabot scans for the new Action repository.



4. Kubernetes Integration Validation

The new JavaScript Action must run smoothly on the existing Linux K8s runners, but must not rely on OS-specific commands like sed, awk, or shell-based openssl.

At least one integration test confirms a successful end-to-end Kafka deployment event in a K8s-based pipeline.



5. Documentation & Onboarding

Provide a detailed README explaining how to use the new Action, including required inputs (env.IMAGE_NAME, env.UNIQUE_ID, etc.) and outputs (final signed payload).

Offer a migration guide for any teams currently relying on the Bash script, outlining minimal steps to adopt the new JavaScript Action.





---

Value & Rationale

Maintainability: JavaScript code can be tested with frameworks (Jest, Mocha) and easily updated. Meanwhile, large Bash scripts become notoriously unmanageable as product requirements grow.

Robust Error Handling: With Node’s try/catch and GitHub’s Actions Toolkit, we eliminate silent or cryptic Bash failures.

Enhanced Logging & Observability: Centralized logs, standardized messages, and immediate job failure on critical errors mean quicker resolution times and fewer release delays.

Future-Proofing: Even though we’re currently on Linux K8s runners, a JavaScript Action remains portable if we expand to other OSes or ephemeral container setups.

Enterprise Security: Node’s crypto module (or a similar library) is well-maintained, frequently patched, and easier to audit than a system-level openssl installation.


By adopting a JavaScript-based solution for Kafka payload signing and publication now, we proactively protect our enterprise CI/CD product from the creeping complexity and technical debt inherent in extended Bash scripting—ensuring we stay ready for future expansion and maintain best-in-class reliability.

