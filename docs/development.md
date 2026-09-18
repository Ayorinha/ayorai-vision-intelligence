# Development workflow

## 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 2. Run

```uvicorn src.api.main:app --reload```

## 3. Test

```pytest```

## 4. Quality

```ruff check .```

## Next implementation milestones

1. Plug in a production detector.
2. Plug in a multi-object tracker.
3. Persist tracks in PostgreSQL/Parquet.
4. Implement MCP transport.
5. Add local embeddings/vector store.
6. Connect an approved reasoning model.
7. Build the review dashboard.
8. Add Docker and CI/CD deployment.
9. Benchmark annotation throughput and review rate.
