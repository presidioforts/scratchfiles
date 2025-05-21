
Multi-Model & Agentic DevOps Automation — High-Impact Design Document

1. Purpose

Design an intelligent, multi-agent DevOps system that automates root cause analysis and remediation actions using modular LLMs and agent pipelines. This system serves both developers and the platform support team, driving rapid incident resolution and controlled platform repair.

2. Scope

This system handles two primary DevOps flows:

Break-Fix Incident Resolution (Developer & Breakfix Ops)

Platform Remediation with Guardrails (Platform Service Team)


3. Business Use Cases

3.1 Developer-Focused Incident Assistant

Prompt Type: Natural language issue reports from developers

Detects failures (e.g., build errors, test timeouts, missing config)

Queries relevant runbooks, past incidents, and logs via vector search

Uses model reasoning to infer likely root causes

Summarizes findings + recommends next steps


3.2 Platform Service Automation with Guardrails

Prompt Type: Platform SRE request (e.g., restart runner, unblock deploy)

MCP server interprets structured actions (restart, kill process)

Enforces role and safety policies

Executes through verified plugin (SSH, REST, Jenkins, Kubernetes)

All actions logged, scoped, and revertible if needed


4. Architecture

flowchart TD
    subgraph User
        A1[Prompt from Dev or SRE]
    end
    A1 --> R[Prompt Analyzer]
    R --> D[Dispatcher / Planner]
    D -->|incident| Docs[Docs Agent (RAG + RCA)]
    D -->|ci_action| CI[CI Agent]
    D -->|infra_action| Infra[Infra Agent]
    Docs --> Resp[Response Builder]
    CI --> MCP[MCP Server]
    Infra --> MCP
    MCP --> Resp
    Resp --> A1

5. Core Components

5.1 Prompt Analyzer

Uses fast transformer-based model (e.g., all-mpnet) to classify:

incident, ci_action, infra_action, code_gen


Conf threshold fallback to LLaMA-3 for ambiguous prompts


5.2 Dispatcher / Planner

Converts prompt metadata into chainable task plan

Maps intent to agent endpoint (e.g., CI → Jenkins API)

Supports fallback + compound tasks


5.3 Tool-Specific Agents

5.4 MCP Server (Action Broker)

Trusted orchestrator between agents and real systems

Executes:

restart_service, get_logs, rerun_job, drain_node


Uses controlled plugins with minimal access scope

All actions auditable, policy-driven


6. Example Flows

6.1 Developer Prompt → RCA

Prompt: “Step 4 in my pipeline keeps failing”

Prompt Router → incident

Dispatcher → Docs Agent → Vector search (logs, past Jira tickets)

Docs Agent → model inference → summary + suggested fix


6.2 SRE Prompt → Platform Action

Prompt: “Restart jenkins-runner-42”

Router → infra_action

Dispatcher → Infra Agent → MCP

MCP validates permissions, executes SSH plugin

Returns: success/failure + log trace


7. Security & Trust Boundaries

Actions restricted by role (dev, on-call, admin)

All actions go through MCP checkpoint

Ticket ID or approval flag required for high-risk ops

Every prompt → traceable action → logged outcome


8. Design Strengths

Modular: swap in best model per task (LLaMA, Code Llama, ST)

Auditable: clear boundaries between reasoning and execution

Safe: no LLMs directly triggering production actions

Fast: small model handles 80–90% of routing cases


9. Build Plan (Initial Sprints)


---

Author: <Your Name>  •  Version: 1.1-Restored •  Date: 2025-05-21



The document has been fully restored and upgraded for expert-level clarity and strategic value. It now reflects your original architecture, clearly separates the two use cases (developer incident triage and platform remediation), and avoids unnecessary visibility/NFR clutter.

Ready for review — I’ll follow your lead on the next step.

