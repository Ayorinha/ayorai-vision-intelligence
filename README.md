# AYORAI Vision Intelligence

> **Secure, evaluated agentic AI platform for computer vision, local RAG, controlled tools and Human-in-the-Loop workflows.**

**Author:** Anderson Leon Ayora · AI Engineer / Data Scientist  
**Brand:** AYORAI TECH

## Engineering thesis

**The model reasons. Deterministic policy authorizes. Humans approve consequential actions. Every important decision is traceable.**

This public-safe reference implementation combines computer vision, retrieval, agent orchestration, MCP, deterministic policy enforcement, RPA and auditable human review. It uses synthetic/public demonstration data only.

## Architecture

```text
VIDEO / RTSP
    │
    ▼
RPA INGESTION → JOB LIFECYCLE
    │
    ▼
COMPUTER VISION → TRACKING → CONFIDENCE
    │                         │
    │                         └── uncertain → HUMAN REVIEW
    ▼
EVENT STORE / SQLITE
    │
    ├── LOCAL RAG ──→ EVIDENCE
    │
    └── AGENT ORCHESTRATOR
                  │
                  ▼
             MCP / TOOL GATEWAY
                  │
                  ▼
          DETERMINISTIC POLICY
             │           │
             │           └── critical → HUMAN APPROVAL
             ▼
          READ-ONLY TOOLS
             │
             ▼
          AUDIT / EVENTS
```

## Security model

- Least-privilege MCP surface.
- Deterministic tool policy independent of model output.
- Critical review decisions require explicit human approval and reviewer identity.
- Evidence-first retrieval boundary.
- Public repository contains only synthetic/public demonstration data.
- Optional OpenAI-compatible LLM adapter; no provider call occurs unless credentials are explicitly configured.
- Security and dependency checks run in GitHub Actions.

See `docs/THREAT_MODEL.md` and `docs/EVALUATION.md`.

## Implemented capabilities

| Capability | Status |
|---|---|
| YOLO detection + tracking | ✅ |
| Confidence routing | ✅ |
| Human review queue | ✅ |
| SQLite persistence + event log | ✅ |
| Local-first RAG | ✅ |
| Agent orchestration boundary | ✅ |
| Deterministic tool policy | ✅ |
| OpenAI-compatible LLM adapter | ✅ optional |
| Protocol-compliant MCP server | ✅ |
| Streamable HTTP MCP transport | ✅ |
| FastAPI API | ✅ |
| Streamlit dashboard | ✅ |
| RPA input discovery | ✅ |
| Docker / Compose | ✅ |
| Functional tests | ✅ |
| Lint + CI | ✅ |
| Dependency audit + Bandit | ✅ |
| Threat model | ✅ |
| Evaluation plan | ✅ |

## MCP

The repository includes a protocol-compliant MCP server implemented with the official Python SDK. The exposed MCP surface is intentionally least-privilege and read-only by default. Consequential review operations remain behind the application policy boundary.

Run locally:

```bash
python -m src.mcp.server
```

For deployment, the server uses Streamable HTTP. The official MCP SDK documents Streamable HTTP as the current HTTP transport. citeturn0search6

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

## Docker

```bash
docker compose up --build
```

API: `http://localhost:8000`  
Dashboard: `http://localhost:8501`

## Quality gates

```bash
ruff check .
pytest -q
pip-audit
bandit -q -r src
```

CI runs these quality/security checks on pushes and pull requests.

## Documentation

- `docs/ARCHITECTURE.md` — system boundaries and data flow
- `docs/THREAT_MODEL.md` — threats, controls and residual risk
- `docs/EVALUATION.md` — safety and quality evaluation methodology
- `docs/mcp.md` — MCP/tool architecture
- `docs/agent.md` — evidence-first agent boundary
- `SECURITY.md` — public-repository security policy
- `CHANGELOG.md` — release history

## Demo data policy

Only public or synthetic material belongs in this repository. **Do not commit IEPTB confidential information, personal data, credentials, private videos or regulated documents.**

## Roadmap

Post-v1 engineering work is intentionally separated from the completed reference implementation:

1. Embedding/vector retrieval benchmark.
2. Durable distributed worker queue.
3. PostgreSQL/object storage deployment profile.
4. Enterprise identity/RBAC integration.
5. OpenTelemetry-compatible observability.
6. Reproducible adversarial benchmark corpus.

These are deployment and scale extensions, not claims of functionality that is not present.

## Portfolio positioning

**Python · Computer Vision · Agentic AI · RAG · MCP · AI Safety · FastAPI · RPA · Docker · CI/CD · Human-in-the-Loop · Data Engineering**

## License

MIT

## Author

**Anderson Leon Ayora**  
AI Engineer | Applied AI · Document Intelligence · Generative AI · Intelligent Automation

Part of the **AYORAI TECH** engineering portfolio.