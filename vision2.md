**Vision**
Empower our platform‑service engineers with an AI‑driven DevOps assistant that transforms how we handle break‑fix tickets — going from manual search to conversational guidance, and finally to safe, automated remediation — so our teams can focus on high‑value work rather than repetitive firefighting.

---

## Three Phases of AI‑Driven DevOps

### 1. Instant Break‑Fix Search

* **What it is:** A ChatGPT‑style search interface where an engineer types a symptom (e.g., “EPL‑X python build workflow failed and here is the build error”) and instantly sees runbook steps detailing how to resolve the issue and any necessary configuration changes.
* **Why it matters:** Eliminates manual digging through logs and documentation.

### 2. Conversational Chat Assistant Conversational Chat Assistant

* **What it is:** A friendly chat interface (we have created chatGPT like UI for this) where engineers ask follow‑up questions — “What did we do last time?” — and get clear, human‑style guidance.
* **Why it matters:** Reduces back‑and‑forth between teams, keeps engineers in context, and speeds resolution.

### 3. Agentic Automation

* **What it is:** AI agents that can not only recommend fixes but safely execute routine actions (e.g. restarting services, scaling up capacity) under lightweight approval controls.
* **Why it matters:** Frees engineers from repetitive “click‑and‑restart” tasks and ensures reliable, consistent incident handling.

---

## MVP – Search

* **Status:** Completed low‑latency search prototype using your SentenceTransformer-based FastAPI implementation.
* **Highlights:**

  * Built a `/search` endpoint that loads embeddings from `index_pair.json` at startup.
  * Uses **all-MiniLM-L6-v2** to encode queries and precomputed embeddings, computing cosine similarity in < 200 ms.
  * Returns top 3 relevant break‑fix knowledge snippets per ticket, enabling engineers to find resolutions instantly.

---

## Chat AI Break‑Fix Assistance

* **Status:** In active testing – extending the search prototype with a conversational layer.
* **Highlights:**

  * Chat interface invokes `/search` to retrieve context and passes snippets to the LLM for response generation.
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
| **Chat**    | \~ 5 min overhead saved | 60 000         | 5 000 hrs          |
| **Agentic** | \~ 20 min automated     | 60 000         | 20 000 hrs         |
| **Total**   |                         | 60 000         | **39 000 hrs**     |

---

### Why This Matters for Management

* **39 000 hours saved annually** on break‑fix work — time our engineers can redirect toward innovation and strategic initiatives.
* **Rapid payback:** Phase 1 alone delivers measurable productivity gains within weeks.
* **Scalable impact:** As ticket volume grows, savings compound without proportional headcount increases.
* **Improved reliability & morale:** Faster resolutions reduce downtime, escalations, and engineer burnout.

This three‑phase roadmap gives us a clear path to unlock tens of thousands of engineering hours every year — driving both operational excellence and strategic growth.
