# Architecture

## Security boundary

AYORAI separates model reasoning from authorization and consequential execution.

```text
AI Agent
   |
   v
Identity / Delegation
   |
   v
MCP Tool Integrity
   |
   v
Runtime Containment
   |
   v
Data-flow Guard
   |
   v
Deterministic Policy + Authorization
   |
   +---- deny ----> Blocked
   |
   v
Transaction / Egress Governance
   |
   v
Tool / MCP Execution
   |
   v
Provenance / Audit
```

## End-to-end application flow

```text
Client
  |
  v
FastAPI Gateway
  |
  +--> validation / security boundary
  |
  v
Agent Orchestrator ----> Local RAG
  |
  v
Tool Registry / MCP
  |
  v
Deterministic Policy Engine
  |                    \
  | read-only            \ critical
  v                       v
Tool execution       Human approval
  |                       |
  +-----------+-----------+
              v
         Audit / Events
```

## Responsibility boundaries

- **Computer Vision:** perception.
- **Tracking:** temporal identity.
- **Confidence engine:** deterministic routing.
- **Database:** durable state.
- **RAG:** contextual evidence.
- **Tool registry:** controlled actions.
- **Agent:** reasoning/orchestration boundary.
- **RPA:** process automation.
- **FastAPI:** service interface.
- **Dashboard:** human interaction.
- **Policy engine:** authorization independent of model output.
- **Audit/provenance:** evidence of security decisions and execution.

The reasoning layer is deliberately not presented as the detector, tracker, policy authority, or execution authority.

## Design principles

1. Retrieval provides evidence; it does not grant authority.
2. Tool permissions are deterministic and independent of model output.
3. Consequential operations require explicit human approval.
4. MCP exposes a least-privilege read-only surface by default.
5. Audit events remain part of the workflow.
6. Provider integration is optional; the platform can run without an external LLM.
7. Security failures fail closed rather than silently becoming authorization.

## Production boundary

PostgreSQL, object storage, distributed workers, enterprise identity and production observability remain deployment concerns. They are not simulated as if they already existed.
