# AYORAI AI Shield

[![CI](https://github.com/Ayorinha/ayorai-vision-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/Ayorinha/ayorai-vision-intelligence/actions/workflows/ci.yml)
[![Security](https://github.com/Ayorinha/ayorai-vision-intelligence/actions/workflows/security.yml/badge.svg)](https://github.com/Ayorinha/ayorai-vision-intelligence/actions/workflows/security.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Deterministic runtime security and policy enforcement for autonomous AI agents.**

## Security thesis

> **Intelligence does not grant authority.**

LLMs and autonomous agents can propose actions, but model output should not automatically become execution authority.

AYORAI AI Shield is a defensive reference implementation that places explicit security and authorization controls between **agent reasoning** and **consequential tool execution**.

## Runtime control plane

The current security boundary composes four deterministic stages before execution:

```text
Agent
  |
  v
Agent Identity / Delegation
  |
  v
MCP Tool Integrity
  |  pinned metadata / drift / poisoning signals
  v
Runtime Containment
  |
  v
Data-flow Guard
  |  sensitivity / destination / volume
  v
Deterministic Policy + Authorization
  |
  v
Transaction / Egress Governance
  |
  v
Tool / MCP Execution
  |
  v
Tamper-evident Provenance
```

The separation is intentional:

**Reasoning ≠ Authorization ≠ Execution**

## Architecture diagram

~~~mermaid
flowchart LR
    A[AI Agent] --> I[Identity / Delegation]
    I --> M[MCP Tool Integrity]
    M --> C[Runtime Containment]
    C --> D[Data-flow Guard]
    D --> P[Deterministic Policy]
    P --> T[Transaction / Egress Governance]
    T --> X[Tool / MCP Execution]
    X --> E[Provenance / Audit]
    P -. deny .-> Z[Blocked]
    D -. sensitive egress .-> Z
    M -. drift / poisoning .-> Z
~~~

> **Security boundary:** reasoning is separated from authorization and consequential execution.

## What this project demonstrates

- deterministic tool authorization;
- scoped agent identity and delegation;
- MCP tool-definition integrity and drift detection;
- fail-closed runtime containment;
- restricted-data egress controls;
- transaction risk governance;
- provenance and replay-aware execution;
- crypto-agility inventory and migration interfaces;
- runtime-attestation integration interface;
- dependency-free runtime telemetry with an OpenTelemetry adapter seam;
- adversarial security evaluation;
- structured auditability.

The repository uses public or synthetic demonstration data. It does **not** connect to real financial infrastructure and does not provide offensive intrusion tooling.

## Threat Model

Potentially untrusted inputs include user instructions, retrieved documents, web content, tool outputs, MCP metadata, persistent memory and model-generated tool arguments.

Protected assets include credentials, sensitive data, external APIs, filesystem resources, high-impact transactions, agent identity/delegated authority and audit evidence.

**Security objective:** prevent an untrusted or compromised agent context from acquiring capabilities beyond the authority explicitly granted by policy.

See `docs/THREAT_MODEL.md`, `docs/architecture.md`, `docs/MCP_RUNTIME_SECURITY.md`, `docs/EVALUATION.md`, `docs/OBSERVABILITY.md` and `docs/DEPLOYMENT_REFERENCE.md`.

## Security Controls

| Control | Purpose |
|---|---|
| Deterministic policy | Prevent model output from becoming implicit authority |
| Agent identity/delegation | Bind actions to explicit principals and scoped authority |
| MCP integrity registry | Pin tool metadata, verify trusted publishers and fail closed on drift |
| Tool poisoning detection | Detect known malicious instruction patterns before execution |
| Data-flow guard | Restrict sensitive outbound data by destination and volume |
| Runtime containment | Suspend sessions and revoke execution/egress |
| Least privilege | Minimize agent permissions |
| Transaction governance | Apply explicit rules to consequential actions |
| Provenance | Preserve evidence about security decisions |
| Replay controls | Support detection and analysis of repeated actions |
| Crypto inventory | Track algorithms for migration planning |
| Runtime attestation interface | Provide a seam for trusted execution environments |
| Adversarial tests | Validate security behavior against synthetic attacks |

## MCP Security Boundary

MCP tool metadata is treated as security-sensitive input. Tools must be explicitly pinned before execution; changed definitions fail closed until reviewed and pinned again.

The implementation is intentionally deterministic and does not ask an LLM whether a tool is safe.

See `docs/MCP_RUNTIME_SECURITY.md`.

## Evaluation

Security claims are treated as hypotheses that must be tested.

The evaluation layer covers controlled, non-destructive scenarios such as prompt injection, goal hijacking, tool abuse, privilege escalation, data exfiltration, malicious tool metadata, unsafe tool arguments, tool-definition drift and runtime containment.

Report at minimum: attack success rate, false-positive rate, false-negative rate, policy decision latency, throughput and regression status.

**Benchmark numbers are published only when produced by the repository’s reproducible benchmark harness.** No unsupported security or performance percentage is claimed here.

## Local Development

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
```

Quality/security checks:

```bash
ruff check .
pytest -q
pip-audit
bandit -q -r src
```

Docker: `docker compose up --build`

## Engineering Quality Gates

- automated tests and coverage reporting;
- Ruff linting;
- static security analysis;
- dependency auditing;
- GitHub Actions CI;
- security regression tests;
- reproducible evaluation;
- documented security assumptions.

Current quality gates include automated SBOM generation and attestation plus a dependency-free OpenTelemetry-compatible telemetry boundary. Future work includes asymmetric supply-chain signatures/key rotation and production provider integrations.

## Design Principles

### Default Deny
Capabilities are not granted merely because an agent requested them.

### Least Privilege
An agent receives only the minimum authority necessary for its task.

### Explicit Trust Boundaries
User input, retrieved content, memory, tools and model output are not implicitly trusted.

### Evidence Before Claims
Security and performance claims require reproducible tests or benchmarks.

### Fail Closed
Security failures must not silently become authorization.

### Public-Safe Research
Examples use synthetic/public data and non-destructive scenarios.

## Roadmap

### v0.1 — Policy Enforcement Foundation
- deterministic policy engine
- tool authorization
- audit events
- threat model
- regression tests

### v0.5 — Agent Security Runtime
- MCP security boundary
- agent identity/delegation
- tool-definition integrity
- data-flow controls
- runtime containment
- adversarial evaluation harness
- sensitive-data controls
- policy-as-code
- observability

### v1.0 — Production Reference
- stable public API
- reproducible benchmark suite
- OpenTelemetry provider integration
- signed audit evidence
- deployment reference
- comprehensive security evaluation
- authenticated tool/server provenance
- confidential-computing provider integration
- post-quantum migration guidance

## Research boundaries

The new controls are deliberately scoped to evidence-backed engineering directions. They do not claim complete MCP security, complete prompt-injection detection, confidential-computing guarantees, or post-quantum security.

Performance and security percentages are not inferred from vendor or academic results. They must be generated by the repository benchmark harness before being presented as AYORAI measurements.

## Contributing

Focused contributions are welcome in agent security, policy enforcement, MCP security, adversarial evaluation, testing, observability and performance engineering.

See `CONTRIBUTING.md` before opening a pull request. Security vulnerabilities should follow `SECURITY.md`.

## Scope and Disclaimer

AYORAI AI Shield is a defensive engineering and research reference implementation. It is **not** a certification, guarantee of agent safety, or substitute for an organization’s security architecture, risk management, compliance controls or professional security assessment.

## Author

**Anderson Leon Ayora**

AI Engineer · Applied AI · AI Safety

**AYORAI · Applied Intelligence**

## License

MIT

## Operational reference

- `docs/OBSERVABILITY.md` — telemetry contract, privacy boundary and operational signals.
- `docs/DEPLOYMENT_REFERENCE.md` — production topology and responsibilities.
- `docs/POST_QUANTUM_MIGRATION.md` — migration planning without claiming post-quantum security.
