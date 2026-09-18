# Development — AYORAI Vision Intelligence

## Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## API

```bash
uvicorn src.api.main:app --reload
```

## Dashboard

```bash
streamlit run dashboard/app.py
```

## Tests

```pytest```

## Lint

```ruff check .```

## Engineering sequence

1. Validate deterministic contracts.
2. Run unit tests.
3. Test video processing on a public/synthetic sample.
4. Validate model thresholds against a representative dataset.
5. Review uncertain events.
6. Benchmark throughput and review rate.
7. Containerize.
8. Run CI.
9. Deploy only after environment-specific security controls are configured.
