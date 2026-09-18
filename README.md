# AYORAI Vision Intelligence

> **Agentic Computer Vision engineering platform** — detection, multi-object tracking, uncertainty routing, Human-in-the-Loop review, local-first RAG, tool orchestration, RPA and FastAPI.

**Author:** Anderson Leon Ayora · AI Engineer / Data Scientist  
**Brand:** AYORAI TECH

## Why this project exists

This portfolio project demonstrates how to compose modern AI engineering capabilities into one auditable workflow instead of isolated demos.

~~~text
VIDEO / RTSP
     │
     ▼
RPA INGESTION ──► JOB QUEUE / STATUS
     │
     ▼
COMPUTER VISION
Detection + Tracking + Persistent IDs
     │
     ▼
CONFIDENCE / UNCERTAINTY
     ├── high confidence ──► auto-accept
     └── uncertain ────────► HUMAN REVIEW
                                  │
                                  ▼
                         AUDITABLE DECISION
     │
     ▼
EVENT STORE + DATABASE
     │
     ├──────────────► TOOL GATEWAY
     │                         │
     └──────────────► LOCAL RAG
                               │
                               ▼
                         AGENT ORCHESTRATOR
                               │
                               ▼
                     DASHBOARD / REPORT / DATASET
~~~

### Engineering principles

- **Evidence first:** agent responses expose retrieved context instead of inventing facts.
- **Human oversight:** uncertain detections can enter a review queue.
- **Auditability:** jobs, detections, reviews and events are persisted.
- **Local first:** the demo RAG runs on SQLite without sending documents to a cloud API.
- **Separation of concerns:** perception, retrieval, tools, orchestration and UI are independent layers.
- **Production honesty:** the repository documents what is implemented and what still requires infrastructure hardening.

## Implemented capabilities

| Capability | Status |
|---|---|
| YOLO detection + tracking | Implemented |
| Persistent track summaries | Implemented |
| Confidence routing | Implemented |
| Human review queue | Implemented |
| Review audit fields | Implemented |
| Job lifecycle | Implemented |
| SQLite persistence | Implemented |
| Event log | Implemented |
| Local-first RAG | Implemented |
| Tool registry / HTTP gateway | Implemented |
| Agent orchestration boundary | Implemented |
| RPA input discovery | Implemented |
| FastAPI API | Implemented |
| Streamlit operator dashboard | Implemented |
| Docker / Compose | Implemented |
| CI / tests | Implemented |
| Full protocol-compliant MCP transport | Roadmap |
| LLM provider integration | Roadmap |
| Vector embeddings | Roadmap |
| Durable distributed worker queue | Roadmap |
| PostgreSQL / object storage | Roadmap |
| Authentication / RBAC | Roadmap |
| Production observability | Roadmap |

## API

- GET /health
- GET /ready
- GET /tools
- POST /jobs
- GET /jobs/{job_id}
- GET /jobs/{job_id}/detections
- GET /jobs/{job_id}/events
- GET /reviews
- POST /reviews/{review_id}
- POST /knowledge
- POST /agent/query
- POST /mcp/call/{name}
- GET /output/{filename}

## Run locally

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn src.api.main:app --reload
~~~

Dashboard:

~~~bash
streamlit run dashboard/app.py
~~~

## Docker

~~~bash
docker compose up --build
~~~

API: http://localhost:8000  
Dashboard: http://localhost:8501

## Demo data policy

Only public or synthetic material belongs in this repository. **Do not commit IEPTB confidential information, personal data, credentials, private videos or regulated documents.**

## Repository structure

~~~text
ayorai-vision-intelligence/
├── src/
│   ├── vision/       # detection, tracking, confidence
│   ├── core/         # settings, DB and persistence
│   ├── rag/          # local retrieval contract
│   ├── mcp/          # tool registry and gateway
│   ├── agents/       # evidence-first orchestration
│   ├── rpa/          # ingestion automation
│   └── api/          # FastAPI application
├── dashboard/         # operator UI
├── knowledge/         # synthetic demo knowledge
├── data/              # runtime data
├── tests/             # automated tests
├── docs/              # architecture and operations
└── .github/workflows/ # CI
~~~

## Production architecture

The current repository is a production-oriented MVP. A real enterprise deployment should add:

1. PostgreSQL or another managed relational database.
2. Object storage for large media.
3. Durable worker queue for long-running video jobs.
4. Authentication, RBAC and secrets management.
5. TLS and network isolation.
6. Metrics, traces and structured log aggregation.
7. Model/version registry and evaluation gates.
8. Retention, backup and disaster recovery policies.
9. A protocol-compliant MCP implementation when interoperability is required.
10. A local/private LLM and embedding provider where data residency is required.

## Portfolio positioning

**Python · Computer Vision · LLM/RAG · Agents · MCP · FastAPI · RPA · Docker · CI/CD · Human-in-the-Loop · AI Safety · Data Engineering**

## License

MIT

## Author

**Anderson Leon Ayora**  
AI Engineer | Applied AI · Document Intelligence · Generative AI · Intelligent Automation

Part of the **AYORAI TECH** engineering portfolio.
