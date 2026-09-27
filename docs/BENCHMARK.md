# AYORAI AI Shield Benchmark

The benchmark is the executable evidence layer between the **Frontier Agent Evaluation Lab** and the deterministic **ShieldEngine**.

```text
Synthetic scenarios
       |
       v
Evaluation Lab
       |
       v
ShieldEngine (real authorization path)
       |
       v
Measured decisions + latency
       |
       v
GitHub Actions security gate
       |
       +--> Step Summary
       +--> benchmark-results artifact
```

## What is measured

Each case declares an expected deterministic decision and is evaluated by the real `ShieldEngine`. The runner records:

- expected decision
- observed decision
- pass/fail
- per-case latency
- aggregate pass rate
- total runtime

The benchmark is synthetic-only and non-destructive.

## Security gate

The workflow fails when any benchmark case observes a decision different from its declared expected decision. This makes the benchmark a regression gate rather than a manually maintained scorecard.

Workflow: `.github/workflows/benchmark.yml`

Runner: `benchmarks/shield_benchmark.py`

Regression tests: `tests/test_shield_benchmark.py`

## Reproducibility

Run locally:

```bash
python -m pip install -e ".[dev]"
PYTHONPATH=. python -m benchmarks.shield_benchmark
PYTHONPATH=. python -m pytest -q tests/test_shield_benchmark.py
```

Reports are generated under `benchmark-results/` and are intentionally not committed as source-of-truth numbers. CI uploads them as build evidence.

## Scope and limitations

A passing benchmark proves only that the modeled authority boundaries behave as specified for these synthetic cases. It does not establish security against unknown attacks, future models, production infrastructure, or real financial systems.
