# AYORAI AI Shield Benchmark

The benchmark is the executable evidence layer between the **Frontier Agent Evaluation Lab** and the deterministic **ShieldEngine**.

```text
B3 public-data reference / domain context
                    +
          synthetic operational scenarios
                    |
                    v
             Evaluation Lab
                    |
                    v
        ShieldEngine real decision path
                    |
                    v
        measured decisions + latency
                    |
                    v
          GitHub Actions gate
             |             |
        Step Summary     Artifact
```

## Data strategy for a B3 presentation

The benchmark deliberately separates **real public information** from **simulated operational events**:

- **Real-public-reference:** public B3 market-data pages and documented market-data concepts are used as domain context. The benchmark does not copy private records or connect to production systems.
- **Synthetic:** agent identities, requests, transaction amounts, destinations, approvals and adversarial conditions are generated locally and are non-destructive.
- **No fake benchmark claim:** synthetic results are measured by executing the real `ShieldEngine`; no performance or security number is manually entered.

B3 publishes public market-data resources including daily bulletins, historical series and public-data hubs. Its historical quotation material includes instrument identifiers, prices, trades and volume fields. citeturn0search0turn0search2turn0search5

For a real deployment, a B3-approved data adapter would replace the synthetic/context layer while keeping the deterministic authorization boundary. Market-data licensing, access controls and contractual permissions would remain separate concerns.

## What is measured

Each case declares an expected deterministic decision and is evaluated by the real `ShieldEngine`. The runner records:

- expected and observed decision
- pass/fail
- business context
- data mode and source
- per-case latency
- aggregate pass rate
- total runtime

Current scenarios cover least privilege, identity, data classification, human approval, egress control and transaction-risk governance. The transaction cases model low-risk, review-level and critical-risk settlement situations without contacting any real financial system.

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

Reports are generated under `benchmark-results/` and uploaded by CI as build evidence; generated numbers are not committed as source-of-truth data.

## Scope and limitations

A passing benchmark proves only that the modeled authority boundaries behave as specified for these scenarios. It does not establish security against unknown attacks, future models, production infrastructure, or real financial systems. A production B3 integration would require approved datasets, identity infrastructure, operational controls, observability, resilience testing and security review.
