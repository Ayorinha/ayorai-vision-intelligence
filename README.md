# AYORAI AI Shield

[![CI](https://github.com/Ayorinha/ayorai-vision-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/Ayorinha/ayorai-vision-intelligence/actions/workflows/ci.yml) [![Security](https://github.com/Ayorinha/ayorai-vision-intelligence/actions/workflows/security.yml/badge.svg)](https://github.com/Ayorinha/ayorai-vision-intelligence/actions/workflows/security.yml)

![AYORAI AI Shield](assets/ayorai-shield-hero.jpg)

> **Deterministic runtime defense for autonomous AI agents in regulated environments.**

**Author:** Anderson Leon Ayora · AI Engineer / Data Scientist  
**Brand:** AYORAI TECH

**Current release:** 3.0.0

## Security thesis

> **Intelligence does not grant authority.**

**The model proposes. The Shield decides.**

AYORAI AI Shield is a public-safe defensive reference architecture for autonomous agents operating around high-value or regulated workflows. It separates model reasoning from deterministic authorization and keeps consequential actions behind explicit policy, transaction governance, egress controls, provenance and isolation boundaries.

The repository uses synthetic/public demonstration data only. It does not connect to real financial infrastructure and does not implement real-world intrusion capabilities.

## Three security pillars

### 1. AYORAI AI Shield
Runtime defense for autonomous agents:
- deterministic capability authorization
- transaction risk governance
- default-deny egress
- data classification
- emergency isolation
- tamper-evident provenance and replay controls
- synthetic adversarial evaluation

### 2. Agent Identity & Trust Fabric
Identity and delegation controls for agentic systems:
- scoped agent identity
- capability and trust boundaries
- agent-to-agent delegation
- delegation depth controls
- revocation
- policy-driven authorization

### 3. Frontier Agent Evaluation Lab
A defensive evaluation layer for advanced agents:
- adversarial scenarios
- frontier-agent regression tests
- security evaluation matrix
- deterministic safety assertions
- machine-readable evaluation coverage

## Architecture

```text
             AUTONOMOUS AGENT
                    │
                    ▼
             IDENTITY & TRUST
                    │
                    ▼
             POLICY ENGINE
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   TRANSACTION           TOOL / MCP
    GOVERNOR              FIREWALL
          │                   │
          └─────────┬─────────┘
                    ▼
             EGRESS CONTROL
                    │
                    ▼
          PROVENANCE / REPLAY
                    │
                    ▼
              ISOLATION
                    │
                    ▼
          SYNTHETIC EVALUATION
```

The original computer-vision / RAG / human-review platform remains part of the repository as the application layer and demonstration environment.

## Implemented capabilities

| Capability | Status |
|---|---|
| Deterministic tool policy | ✅ |
| AI Shield runtime defense | ✅ |
| Agent identity & trust fabric | ✅ |
| Agent-to-agent delegation controls | ✅ |
| Transaction risk governance | ✅ |
| Default-deny egress | ✅ |
| Emergency isolation | ✅ |
| Attack provenance / replay defense | ✅ |
| Frontier-agent evaluation lab | ✅ |
| Adversarial regression tests | ✅ |
| Least-privilege MCP server | ✅ |
| Streamable HTTP MCP transport | ✅ |
| Local-first RAG | ✅ |
| Computer vision + tracking | ✅ |
| Human review queue | ✅ |
| FastAPI API | ✅ |
| Streamlit dashboard | ✅ |
| RPA input discovery | ✅ |
| Docker / Compose | ✅ |
| Pytest + Ruff | ✅ |
| Dependency audit + Bandit | ✅ |
| GitHub Actions CI/security | ✅ |
| Threat model + evaluation docs | ✅ |

## MCP security boundary

The repository includes a protocol-compliant MCP server using the official Python SDK. The exposed MCP surface is intentionally least-privilege and read-only by default. Consequential review operations remain behind the application policy boundary.

Run locally:

```bash
python -m src.mcp.server
```

## API

- `GET /health`
- `GET /ready`
- `GET /tools`
- `GET /metrics`
- `POST /jobs`
- `GET /jobs/{job_id}`
- `GET /jobs/{job_id}/detections`
- `GET /jobs/{job_id}/events`
- `GET /reviews`
- `POST /reviews/{review_id}`
- `POST /knowledge`
- `POST /agent/query`
- `POST /mcp/call/{name}`

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn src.api.main:app --reload
```

Dashboard:

```bash
streamlit run dashboard/app.py
```

Docker:

```bash
docker compose up --build
```

API: `http://localhost:8000`  
Dashboard: `http://localhost:8501`

## Quality and security gates

```bash
ruff check .
pytest -q
pip-audit
bandit -q -r src
```

GitHub Actions runs CI and security checks on repository changes.

## 🤝 Contribute

**You do not need to understand the entire architecture to contribute.**

AYORAI AI Shield is open to focused contributions in AI safety, agent security, MCP/tool security, deterministic policy enforcement, evaluation, testing, documentation, observability, and developer experience.

### Start here

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Browse open issues labeled **good first issue** or **help wanted**.
3. Pick one small, clearly scoped task.
4. Add tests or evaluation evidence where applicable.
5. Open a focused pull request.

### Good first contributions

- documentation and examples
- synthetic adversarial evaluation cases
- regression tests
- MCP/tool security cases
- authorization and policy tests
- execution tracing examples
- performance fixtures
- local setup improvements
- CI/developer tooling

**Contribution principle:** small, reproducible, evidence-driven changes are preferred over large rewrites.

## Documentation

- `docs/ARCHITECTURE.md` — system boundaries and data flow
- `docs/THREAT_MODEL.md` — threats, controls and residual risk
- `docs/EVALUATION.md` — safety and quality evaluation methodology
- `docs/FRONTIER_AI_EVALUATION.md` — frontier-agent evaluation lab
- `docs/AGENT_IDENTITY_TRUST.md` — agent identity and delegation model
- `docs/mcp.md` — MCP/tool architecture
- `docs/AI_SHIELD.md` — AI Shield architecture
- `docs/agent.md` — evidence-first agent boundary
- `SECURITY.md` — public-repository security policy
- `CHANGELOG.md` — release history

## Demo data and safety scope

Only public or synthetic material belongs in this repository.

**Do not commit confidential information, personal data, credentials, private videos or regulated documents.**

All adversarial scenarios are synthetic and non-destructive. This project is a defensive research and portfolio reference implementation, not a production financial security system.

## Roadmap

The core reference implementation is complete. Future work is intentionally limited to deployment and evaluation extensions:

1. Reproducible adversarial benchmark corpus.
2. Embedding/vector retrieval benchmark.
3. Durable distributed worker queue.
4. PostgreSQL/object-storage deployment profile.
5. Enterprise identity/RBAC integration.
6. OpenTelemetry-compatible observability.

These are extensions, not claims of functionality already present.

## Portfolio positioning

**AI Safety · AI Engineering · Agentic AI · LLM Security · MCP · RAG · Python · Computer Vision · FastAPI · RPA · Docker · CI/CD · Human-in-the-Loop**

## License

MIT

## Author

**Anderson Leon Ayora**  
AI Engineer | Applied AI · Document Intelligence · Generative AI · Intelligent Automation

Part of the **AYORAI TECH** engineering portfolio.
