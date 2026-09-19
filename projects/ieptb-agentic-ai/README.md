# IEPTB Agentic AI Platform
### Secure, Evaluated Multi-Agent AI for Regulated Remessa Workflows

> **Research & engineering project by Anderson Leon Ayora (AyorAI).**
> A production-oriented reference architecture for applying Agentic AI, RAG, MCP-style tools, Document Intelligence and AI Safety to a regulated Central de Remessa de Arquivos (CRA) workflow.

**This is not an official IEPTB production system.** It is an independent portfolio/research implementation using synthetic data only.

## Engineering thesis
Enterprise AI is not just an LLM call. In regulated workflows, the system must prove **evidence, authorization, evaluation, traceability and safe failure**.

> **The model reasons. Deterministic policies authorize. Humans approve consequential actions. Every decision is traceable.**

## What this demonstrates
- Python/FastAPI production architecture
- Agentic orchestration + RAG
- MCP-style least-privilege tools
- Prompt-injection and data-leakage defenses
- LGPD-oriented controls
- Human-in-the-loop governance
- Automated evaluation and security gates
- Auditability and observability
- Enterprise integration patterns


## Secure RAG & Multi-Agent Research for Remessa de Arquivos

> Research and engineering prototype inspired by operational workflows in a regulated document-processing environment. This repository uses synthetic/anonymized data and does **not** contain IEPTB confidential information, credentials, production records, or personal data.

### Objective
Design an enterprise-grade AI platform for a Central de Remessa de Arquivos (CRA) workflow, combining:

- Python + FastAPI
- Agentic orchestration
- Retrieval-Augmented Generation (RAG)
- Document Intelligence/OCR
- MCP-style tool integration
- Security and prompt-injection defenses
- LGPD-oriented data controls
- Evaluation and quality gates
- Auditability and governance
- Enterprise integration patterns
- Docker + CI/CD

### Research question
**Can an agentic AI layer reduce manual effort in remessa validation while preserving traceability, access control, explainability and human approval?**

### Reference architecture

```text
                ┌─────────────────────────┐
                │     Enterprise User     │
                └────────────┬────────────┘
                             │
                    ┌────────▼────────┐
                    │ FastAPI Gateway │
                    └────────┬────────┘
                             │
             ┌───────────────▼────────────────┐
             │ Security & Policy Gateway      │
             │ PII • Injection • RBAC • Audit │
             └───────────────┬────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Agent Orchestrator│
                    └───┬────┬────┬────┘
                        │    │    │
              ┌─────────▼┐ ┌─▼──────┐ ┌──────▼─────┐
              │RAG Agent │ │Validator│ │Audit Agent │
              └────┬─────┘ └────┬────┘ └──────┬─────┘
                   │             │              │
             ┌─────▼─────┐ ┌────▼──────┐ ┌────▼──────┐
             │Vector DB  │ │Rules Engine│ │Audit Store │
             └───────────┘ └───────────┘ └───────────┘
                         │
                  ┌──────▼──────┐
                  │ CRA Adapter │
                  │ API / Files │
                  └─────────────┘
```

### Core workflow

1. Receive a synthetic remessa.
2. Validate schema and business rules.
3. Classify documents.
4. Retrieve relevant procedures/rules.
5. Ask specialized agents to analyze the case.
6. Run security and policy checks.
7. Produce a structured recommendation with evidence.
8. Require human approval for sensitive actions.
9. Write an immutable-style audit event.
10. Measure quality, latency and failure modes.

### Safety principle

**The model recommends; deterministic policy and human approval control consequential actions.**

The prototype deliberately separates:
- probabilistic reasoning (LLM/agents)
- deterministic validation (rules)
- authorization (RBAC/policy)
- evidence (retrieval)
- observability (traces/metrics)
- audit (events)

### Evaluation
The evaluation suite is designed around:
- retrieval relevance
- groundedness
- hallucination resistance
- structured-output validity
- prompt-injection resistance
- PII leakage
- unauthorized tool access
- latency
- reproducibility

See [docs/evaluation.md](docs/evaluation.md).

### Governance
See [docs/governance.md](docs/governance.md) and [docs/threat-model.md](docs/threat-model.md).

### Important scope note
This is an **independent research/portfolio implementation inspired by a regulated operational domain**. It is not presented as an official IEPTB production system and should never use real operational data in this public repository.

### Author
**Anderson Leon Ayora — AyorAI · Applied AI / AI Engineering**

