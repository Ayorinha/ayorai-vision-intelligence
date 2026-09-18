# AYORAI Vision Intelligence

> **Production-oriented Agentic Computer Vision platform** combining object detection, multi-object tracking, uncertainty-aware decisions, Human-in-the-Loop review, MCP, RAG, RPA and an AI orchestration layer.

**Project:** AYORAI Vision Intelligence  
**Brand:** AYORAI TECH  
**Author:** Anderson Leon Ayora — AI Engineer / Data Scientist

## What this project demonstrates

This repository is an engineering portfolio project designed to demonstrate how modern AI systems can be assembled into a controlled, auditable production architecture.

- Computer Vision for object detection
- Persistent multi-object tracking
- Confidence and uncertainty routing
- Human-in-the-Loop review
- MCP tool interfaces
- RAG-ready knowledge layer
- Agent orchestration
- RPA-driven ingestion
- FastAPI backend
- Streamlit operational dashboard
- Docker deployment
- Automated quality checks with GitHub Actions

## Architecture

```
                    VIDEO / RTSP
                         |
                         v
                +-------------------+
                | Computer Vision   |
                | Detection         |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Object Tracking   |
                | Persistent IDs    |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Confidence Engine |
                +----+---------+----+
                     |         |
              high confidence  uncertain
                     |         |
                     v         v
                  ACCEPT   HUMAN REVIEW
                     |         |
                     +----+----+
                          |
                          v
                 +----------------+
                 | FastAPI / MCP  |
                 +---+--------+---+
                     |        |
                    RAG      TOOLS
                     |        |
                     +---+----+
                         |
                         v
                +-------------------+
                | AI Orchestrator   |
                | Reasoning Layer   |
                +---------+---------+
                          |
                          v
             Dashboard / Reports / Data
```

The reasoning model is intentionally separated from deterministic perception. The AI layer orchestrates tools and context; it does not replace the Computer Vision detector or tracker.

## Operational flow

```
input video
    -> detection
    -> tracking
    -> confidence
    -> review routing
    -> structured events
    -> MCP tools
    -> RAG context
    -> agent reasoning
    -> dashboard/report/export
```

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

## API

- `GET /health`
- `GET /ready`
- `GET /tools`
- `POST /detections`
- `GET /tracks`
- `POST /process-video`
- `GET /output/{filename}`

## Repository structure

```
ayorai-vision-intelligence/
├── src/
│   ├── vision/      # detection, tracking and confidence
│   ├── mcp/         # tool contracts and gateway
│   ├── rag/         # retrieval abstraction
│   ├── agents/      # orchestration
│   ├── api/         # FastAPI
│   ├── rpa/         # ingestion automation
│   └── core/        # configuration and persistence
├── dashboard/       # Streamlit operator UI
├── data/             # runtime data; never commit sensitive data
├── tests/            # automated tests
├── docs/             # architecture and production docs
└── .github/          # CI
```

## Production posture

The repository is **production-oriented and deployable as an MVP**. Enterprise production still requires environment-specific controls such as authentication/RBAC, PostgreSQL, object storage, TLS, observability, secrets management, retention policies, backup/DR and model validation.

Do not put credentials, private videos, personal data or regulated IEPTB data in this public repository.

## Engineering roadmap

1. Real detector and tracker
2. Production persistence
3. Human review queue
4. Full MCP transport
5. Local/private vector database
6. Agent model integration
7. Authentication and RBAC
8. Observability and metrics
9. Benchmarking
10. Cloud/GPU deployment

## License

MIT

## Author

**Anderson Leon Ayora**  
AI Engineer | Applied AI · Document Intelligence · Generative AI · Intelligent Automation

Part of the **AYORAI TECH** engineering portfolio.
