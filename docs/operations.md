# Operations Runbook

## Start

```bash
docker compose up --build
```

Check:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

## Process

Use the dashboard at `http://localhost:8501` or call `POST /process-video`.

## Incident basics

1. Check `/health`.
2. Check container logs.
3. Check available disk space in `data/`.
4. Verify the model weight configured by `MODEL_PATH`.
5. Stop processing if outputs are corrupt or confidence quality degrades.
6. Preserve logs and metadata needed for audit.
7. Do not upload regulated data to GitHub.

## Model changes

Every model change should record:
- model name/version
- weights checksum
- dataset/version
- confidence thresholds
- validation metrics
- deployment date
- rollback target

## Data retention

Define retention by environment before accepting real operational video. Delete expired raw media and derived artifacts according to policy.
