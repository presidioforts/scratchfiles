
Multi‑Model & Agentic DevOps Automation — High‑Level Design Document

1  Purpose

Provide a modular reference architecture that enables automated, policy‑controlled DevOps actions through multiple specialised language models and domain‑specific agents orchestrated by a central Model Context Protocol (MCP) server.

2  Scope

In scope: Prompt analysis, intent routing, agent dispatch, secure execution (MCP), audit/observability, PoC for Jenkins runner restart & log retrieval.

Out of scope: Full migration of all legacy scripts, enterprise‑wide RBAC rollout.


3  Goals & Success Metrics

4  Stakeholders

Platform Service Engineering (owners)

Dev & SRE teams (consumers)

Security GRC (policy reviewers)

Compliance / Audit (log consumers)


5  Architecture Overview

flowchart TD
    subgraph User Interfaces
        A1[Slack / Chat] --> R
        A2[CLI] --> R
        A3[Web UI] --> R
    end
    R[Prompt Router <br/> (Intent Classifier)] --> D[Agent Dispatcher / Planner]
    D -->|doc_lookup| Doc[Docs Agent <br/>(RAG)]
    D -->|ci_action| CI[CI Agent]
    D -->|infra_action| Infra[Infra Agent]
    D -->|monitor_query| Mon[Monitoring Agent]
    D -->|code_gen| Code[Code Agent]
    CI & Infra & Mon & Code --> MCP[MCP Server <br/>(Exec, Policy, Audit)]
    Doc --> RSP[LLM Summariser]
    MCP --> RSP
    RSP --> UI[(Response)]

6  Component Detail

6.1 Prompt Router / Intent Classifier

Model: Fine‑tuned all‑mpnet‑base‑v2 (≈80 ms)  → fallback LLaMA‑3‑8B when confidence < 0.8.

API: POST /route → {intent, confidence, entities}.

Retraining cadence: weekly on new chat logs.


6.2 Agent Dispatcher / Planner

Implements simple HTN‑style planner.

Chooses agent chain, supports parallel calls.

JSON schema: TaskPlan v0.3.


6.3 Tool‑Specific Agents

6.4 MCP Server

Transport: gRPC (internal) + REST (edge).

Plugins: Jenkins, Kubernetes, Linux SSH, MongoDB.

Policy Guard: OPA sidecar; deny‑by‑default.

Audit: OpenTelemetry → Loki & Grafana.


6.5 Observability

Distributed traces (OpenTelemetry)

Langfuse for LLM decisions.

Prometheus + Grafana dashboards.


7  Data Flow — Example "Runner Stuck"

1. User: "Runner is stuck again".


2. Router → infra_action (0.92).


3. Planner creates chain: CI‑Agent.getStatus → Infra‑Agent.restartService.


4. CI‑Agent GET /api/runner/42 (state = not‑responding).


5. MCP executes ssh restart_runner 42 via Infra plugin.


6. MCP logs action, returns JSON.


7. Summariser LLM produces RCA and resolution note.



8  Security & Compliance

RBAC: role tags (dev, on‑call, admin).

Secrets: HashiCorp Vault, short‑lived tokens.

Change Mgmt: every production‑impacting action requires Jira ticket ID in metadata.


9  Non‑Functional Requirements

10  Implementation Roadmap

11  Risks & Mitigations

LLM hallucination → wrong action – Strict schema validation, guarded execution.

Model drift – monthly offline eval & canary.

Credential sprawl – central vault + short‑lived certs.


12  Future Enhancements

Fine‑grained policy using semantic similarity ("restart prod" denial pattern).

Self‑healing action suggestions (planner loops until metrics green).

Cost optimiser to swap smaller models on low‑risk queues.



---

Author: <Your Name>  •  Version: 0.9‑draft  •  Date: 2025‑05‑21


