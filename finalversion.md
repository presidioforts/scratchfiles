**Vision**  Deliver an AI‑powered DevOps assistant that instantly diagnoses break‑fix issues and automates remediation, empowering engineers to focus on high‑value work rather than repetitive firefighting.

---

## Three Phases of Break‑Fix AI Assistant and Agentic Automation

### 1. Instant AI Break‑Fix Search

* **What it is:** An intelligent search interface where an engineer types a symptom (e.g., “EPL‑X python build workflow failed and here is the build error”) and instantly sees runbook steps detailing how to resolve the issue and any necessary configuration changes.
* **Why it matters:** Eliminates manual digging through logs and documentation.
* **Example:** Reduces lookup time from \~15 minutes to under 1 minute, streamlining problem diagnosis.
* **Result:** Directly returns the trained runbook steps that precisely solve the reported issue, without surfacing generic search lists.
  Directly returns the trained runbook steps that precisely solve the reported issue, without surfacing generic search lists.

### 2. Conversational AI Chat Assistant

* **What it is:** A friendly chat interface (Microsoft team or new a web chat interface) where engineers ask follow‑up questions — “What did we do last time to solve this EPL‑X python build workflow failed?” — and get clear, human‑style guidance.
* **Why it matters:** Reduces back‑and‑forth between teams, keeps engineers in context, and speeds resolution.
* **Result:** Provides precise, context‑aware guidance in a conversational format, enabling engineers to resolve follow‑up questions rapidly without leaving their workflow.

### 3. Agentic Automation

* **What it is:** AI agents that can not only recommend fixes but safely execute routine actions (e.g. restarting services, scaling up capacity) under lightweight approval controls.
* **Why it matters:** Frees engineers from repetitive “click‑and‑restart” tasks and ensures reliable, consistent incident handling.
* **Pilot Use Case:** Auto‑restart on HTTP 5xx error spikes—detect predefined error thresholds in Service X, generate a pod‑restart plan, seek one‑click approval, execute, and verify recovery.
* **How it works:** Agents sense alerts, use the break‑fix model to plan remediation steps, present action templates for quick approval, execute via orchestration tools (Kubernetes, GitHub Actions, JFrog Artifactory, Harness, Jenkins), and automatically confirm success with health checks.
* **Safety & Compliance:** Every action is gated by a human approval step, fully logged, and supports automated rollback to safeguard production systems.
* **Result:** Early trials indicate over 60% of routine incidents can be auto‑remediated, reducing Mean Time to Remediate (MTTR) by \~30%.

---

## Instant AI Break‑Fix Search- MVP

* **Status:** Completed low‑latency search prototype using your SentenceTransformer-based FastAPI implementation.
* **Highlights:**

  * Built a `/search` endpoint that loads embeddings from `index_pair.json` at startup.
  * Uses **all-MiniLM-L6-v2** to encode queries and precomputed embeddings, computing cosine similarity in < 200 ms.
  * Returns the precise runbook step(s) to resolve the reported issue

---

## Conversational AI Chat Assistant

* **Status:** In active testing – extending the search prototype with a conversational layer.
* **Highlights:**

  * Chat interface presents two buttons labeled **Search** and **Chat**; clicking the Chat button opens the conversational assistant, which invokes `/search` to gather context snippets and feeds them into the LLM for response generation.
  * Utilizes internally hosted **Llama‑3‑Instruct (3B)** for multi‑turn, contextually aware dialogue.
  * Aiming to allow engineers to ask follow‑up questions naturally and receive coherent, step‑by‑step guidance.

---

## Agentic Automation

* **Status:** Research & prototype phase – defining how chat and search models drive autonomous workflows.
* **Highlights:**

  * Leverage **Llama‑3‑Instruct (3B)** to interpret engineer intents and orchestrate multi-step remediation plans.
  * Utilize the **all-MiniLM-L6-v2** break‑fix search model as an action retriever, pulling the right knowledge snippets for each step.
  * Framework for safe, automated execution: generate action templates (e.g. restart service commands), require lightweight approval, then verify outcomes.

---

## Annual Time Savings (60 000 Tickets/Year)

| Phase       | Saved per Ticket        | Annual Tickets | Annual Hours Saved |
| ----------- | ----------------------- | -------------- | ------------------ |
| **Search**  | 15 min → 1 min = 14 min | 60 000         | 14 000 hrs         |
| **Chat**    | \~ 5 min                | 60 000         | 5 000 hrs          |
| **Agentic** | \~ 20 min               | 60 000         | 20 000 hrs         |
| **Total**   |                         | 60 000         | **39 000 hrs**     |

---

### Why This Matters for Management

* **39 000 hours saved annually** on break‑fix work — time our engineers can redirect toward innovation and strategic initiatives.

* **Rapid payback:** Phase 1 alone delivers measurable productivity gains within weeks.

* **Scalable impact:** As ticket volume grows, savings compound without proportional headcount increases.

* **Improved reliability & morale:** Faster resolutions reduce downtime, escalations, and engineer burnout.

* **Developer satisfaction:** Engineers gain confidence and autonomy, experiencing less frustration and higher engagement when resolving issues.

* This three‑phase roadmap gives us a clear path to unlock tens of thousands of engineering hours every year — driving both operational excellence and strategic growth.

**Conclusion:** By centering our AI assistant on operational efficiency and developer satisfaction, our platform service teams and developers can collaborate more effectively and deliver value faster than ever.
