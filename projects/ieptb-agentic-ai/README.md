# IEPTB Agentic AI Platform
### Secure, Evaluated Agentic AI for Regulated Remessa Workflows

**AyorAI · Applied AI / AI Engineering / AI Safety**

> Research & engineering project by Anderson Leon Ayora.
> A public-safe reference implementation for secure agentic systems in a regulated CRA/remessa research scenario.

> **Important:** This is **not an official IEPTB production system**. It uses synthetic data only and contains no production records, credentials, private endpoints or personal data.

## Why this project exists

Enterprise AI needs more than a model call. The hard engineering problem is controlling what an agent can see, retrieve, call and change — while preserving evidence and auditability.

**Engineering invariant:** the model reasons; retrieval is untrusted; deterministic policy authorizes; tools are least-privilege; humans approve consequential actions; every decision is auditable.

## Architecture

Client → FastAPI Gateway → Security Gate → Agent Orchestrator → Retrieval + Validation → Tool Gateway → Policy Engine → Human Approval for critical actions → Audit Store.

The orchestrator uses an explicit typed state machine so security and policy stages cannot be silently skipped.

## Security controls

- Prompt-injection detection at the trust boundary.
- PII redaction before retrieval.
- Retrieved text treated as data, never as authorization.
- Explicit roles: viewer, analyst, reviewer, admin.
- Tenant isolation checks on every tool call.
- Deny-by-default tool permissions.
- Risk classification for tool operations.
- Critical operations fail closed and require human approval.
- Typed orchestration state machine prevents unsafe stage skipping.
- Append-only audit persistence with chained SHA-256 hashes.
- Correlation IDs for request-level traceability.
- Synthetic adversarial regression tests in CI.

## MCP integration

The project includes a real MCP server boundary using the official Python MCP SDK v2. It exposes only governed synthetic tools and keeps authorization in deterministic application code rather than delegating permission decisions to a model.

Run locally:

    cd projects/ieptb-agentic-ai
    make install
    make mcp

The MCP server uses Streamable HTTP.

## Evaluation

The repository contains executable synthetic cases covering evidence retrieval, prompt injection, governance and human approval, cross-tenant authorization, role-based tool access, state-machine safety and MCP server availability.

Run:

    make evaluate

The command generates evaluation/report.json from the actual execution. **No benchmark result is hard-coded or claimed before the code produces it.**

## Developer workflow

    make install
    make lint
    make test
    make security
    make compile
    make evaluate
    make run

API docs: /docs
Health: /health
Analysis: POST /analyze

## Docker

    docker compose up --build

The image runs as a non-root user, includes a healthcheck, and persists the synthetic audit log through a local volume.

## Repository structure

    src/
      api/              FastAPI boundary
      core/             security, retrieval, tools, policy, state, audit
      mcp_server.py     MCP tool boundary
    evaluation/         executable benchmark + generated report
    tests/              unit, API, security and governance tests
    adr/                architecture decisions
    docs/               architecture, governance, threat model and demo

## Current limitations — intentionally explicit

This is a reference platform, not a claim of production readiness. The retriever is deterministic keyword retrieval rather than a vector database; prompt-injection and PII detection are heuristic baselines; the audit store is local JSONL; the identity layer is synthetic; there is no external LLM provider in the public demo; and the human-approval UX is represented as a policy boundary rather than a real approval system.

These limitations are documented so future work can be measured instead of hidden behind marketing language.

## Roadmap

1. Embedding/vector retrieval with retrieval-quality evaluation.
2. Adversarial prompt-injection and tool-abuse corpus.
3. Persistent observability with OpenTelemetry-compatible traces.
4. Production identity integration and stronger tenant isolation.
5. Policy-as-code test matrix and signed tool manifests.
6. MCP client integration and end-to-end agent interoperability tests.
7. Model adapters with offline/local inference options.
8. Reproducible benchmark reports and latency/error budgets.

## Public-safety scope

Do not add confidential IEPTB information or personal data.

**Author:** Anderson Leon Ayora — AyorAI
