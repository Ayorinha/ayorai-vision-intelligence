# Production — AYORAI Vision Intelligence

This project is **production-oriented and deployable as an MVP**, not a claim of enterprise production certification.

## Runtime

- FastAPI API
- Streamlit operator dashboard
- Ultralytics-based vision pipeline
- Docker Compose
- SQLite single-node persistence
- MCP gateway
- RAG abstraction
- CI via GitHub Actions

## Local deployment

```bash
docker compose up --build
```

API: http://localhost:8000  
Dashboard: http://localhost:8501

## Enterprise hardening

Before handling sensitive or regulated workloads:

1. PostgreSQL for multi-worker persistence.
2. Object storage with signed URLs.
3. Authentication and RBAC.
4. Structured logs and OpenTelemetry.
5. Prometheus metrics and alerting.
6. Pinned model weights and checksums.
7. Representative validation dataset and calibrated thresholds.
8. Video retention/deletion policies.
9. Secret manager.
10. TLS/reverse proxy.
11. Rate limits and upload limits.
12. Backup and disaster recovery.
13. Model and dataset versioning.
14. Audit logs.
15. Security testing.
16. Keep proprietary and regulated data out of Git.
