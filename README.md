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

```text
                 AGENT / LLM
                     │
                     │ proposes action
                     ▼
            ┌───────────────────┐
            │   IDENTITY /      │
            │   TRUST CONTEXT   │
            └─────────┬─────────┘
                      ▼
            ┌───────────────────┐
            │   POLICY ENGINE   │
            └─────────┬─────────┘
                      ▼
            ┌───────────────────┐
            │ AUTHORIZATION +   │
            │ RISK GOVERNANCE   │
            └─────────┬─────────┘
                 ┌────┴────┐
                 │         │
               DENY      ALLOW
                 │         │
                 │         ▼
                 │   TOOL / MCP
                 │   EXECUTION
                 │         │
                 └────┬────┘
                      ▼
             AUDIT / PROVENANCE
```

### Core principle

**Reasoning ≠ Authorization ≠ Execution**

## What this project demonstrates

- deterministic tool authorization;
- least-privilege agent capabilities;
- identity and trust boundaries;
- transaction risk governance;
- default-deny egress controls;
- provenance and replay-aware execution;
- MCP/tool security boundaries;
- adversarial security evaluation;
- structured auditability;
- defensive isolation mechanisms.

The repository uses public or synthetic demonstration data. It does **not** connect to real financial infrastructure and does not provide offensive intrusion tooling.

## Threat Model

Potentially untrusted inputs include user instructions, retrieved documents, web content, tool outputs, MCP metadata, persistent memory and model-generated tool arguments.

Protected assets include credentials, sensitive data, external APIs, filesystem resources, high-impact transactions, agent identity/delegated authority and audit evidence.

**Security objective:** prevent an untrusted or compromised agent context from acquiring capabilities beyond the authority explicitly granted by policy.

See `docs/THREAT_MODEL.md`, `docs/ARCHITECTURE.md` and `docs/EVALUATION.md`.

## Security Controls

| Control | Purpose |
|---|---|
| Deterministic policy | Prevent model output from becoming implicit authority |
| Tool allowlisting | Restrict available capabilities |
| Least privilege | Minimize agent permissions |
| Transaction governance | Apply explicit rules to consequential actions |
| Egress control | Prevent uncontrolled external data transfer |
| Identity/trust context | Bind actions to explicit agent identity |
| Delegation limits | Control agent-to-agent authority propagation |
| Provenance | Preserve evidence about security decisions |
| Replay controls | Support detection and analysis of repeated actions |
| Isolation | Provide emergency containment |
| Adversarial tests | Validate security behavior against synthetic attacks |

## Evaluation

Security claims are treated as hypotheses that must be tested.

The evaluation layer covers controlled, non-destructive scenarios such as prompt injection, goal hijacking, tool abuse, privilege escalation, data exfiltration, malicious tool metadata and unsafe tool arguments.

Report at minimum: attack success rate, false-positive rate, false-negative rate, policy decision latency, throughput and regression status.

**Benchmark numbers are published only when produced by the repository’s reproducible benchmark harness.** No unsupported security or performance percentage is claimed here.

## Architecture

```text
Identity → Policy → Authorization → Risk → Tool/MCP Boundary → Execution → Audit
```

The separation is intentional: detection is not authorization, authorization is not execution.

## MCP Security Boundary

The repository includes a Python MCP implementation designed around a least-privilege security boundary.

The default design favors explicit tool exposure, read-only capabilities where possible, validation before consequential operations, policy enforcement before execution and structured security events.

Local development: `python -m src.mcp.server`

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

Future quality gates include SBOM generation, supply-chain verification and OpenTelemetry-compatible observability.

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
- adversarial evaluation harness
- sensitive-data controls
- policy-as-code
- observability

### v1.0 — Production Reference
- stable public API
- reproducible benchmark suite
- OpenTelemetry
- signed audit evidence
- deployment reference
- comprehensive security evaluation

## Contributing

Focused contributions are welcome in agent security, policy enforcement, MCP security, adversarial evaluation, testing, observability, documentation and performance engineering.

See `CONTRIBUTING.md` before opening a pull request. Security vulnerabilities should follow `SECURITY.md`.

## Scope and Disclaimer

AYORAI AI Shield is a defensive engineering and research reference implementation. It is **not** a certification, guarantee of agent safety, or substitute for an organization’s security architecture, risk management, compliance controls or professional security assessment.

## Author

**Anderson Leon Ayora**

AI Engineer · Applied AI · AI Safety

**AYORAI · Applied Intelligence**

## License

MIT