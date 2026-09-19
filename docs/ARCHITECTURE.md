# Architecture

## End-to-end flow

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

## Design principles
1. Retrieval provides evidence; it does not grant authority.
2. Tool permissions are deterministic and independent of model output.
3. Consequential operations require explicit human approval.
4. MCP exposes a least-privilege read-only surface by default.
5. Audit events remain part of the workflow.
6. Provider integration is optional; the platform can run without an external LLM.

## Production boundary
PostgreSQL, object storage, distributed workers, enterprise identity and production observability remain deployment concerns. They are not simulated as if they already existed.