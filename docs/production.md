# Production deployment

This repository is production-oriented and deployable, but production operation still requires environment-specific infrastructure, secrets, model weights, observability and validation.

## Deployment

```bash
docker compose up --build
```

API: http://localhost:8000  
Dashboard: http://localhost:8501

## Production hardening

1. PostgreSQL for multi-worker persistence.
2. Object storage with signed URLs.
3. Authentication and RBAC.
4. Structured logs and OpenTelemetry.
5. Prometheus metrics.
6. Pinned model weights and checksums.
7. Representative validation dataset and calibrated thresholds.
8. Video retention/deletion policies.
9. Secret manager.
10. TLS/reverse proxy.
11. Rate limits and upload limits.
12. Backups/disaster recovery.
13. Model and dataset versioning.
14. No proprietary or regulated data in Git.
