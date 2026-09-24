# Execution tracing example

`examples/execution_tracing_example.py` shows a synthetic agent request moving
through the AI Shield pipeline: **policy evaluation** (`ShieldEngine.evaluate`),
the resulting **tool decision** (`PolicyResult`), and the tamper-evident
**audit/tracing output** (`ProvenanceGraph`). See `docs/AI_SHIELD.md` for the
full security model this pipeline enforces.

All data is synthetic, the pipeline is deterministic, and no network calls,
external MCP target, or credentials are involved.

## Run it

```bash
python -m examples.execution_tracing_example
```

## Scenarios and expected trace/audit events

| Scenario | Capability | Decision | Reason | Audit events |
| --- | --- | --- | --- | --- |
| Allowed read-only operation | `read_internal` | `allow` | `policy_satisfied` | 1 event, `decision=allow`, `previous_hash=None` (first event in the chain) |
| Consequential operation pending human review | `read_restricted` | `review` | `human_approval_required` | 1 event, `decision=review`, `previous_hash` links back to the prior event's hash |
| Unknown capability denied | `export_ledger` | `block` | `unknown_capability` | 1 event, `decision=block`, `previous_hash` links back to the prior event's hash |

Each audit event carries a SHA-256 `event_hash` over its canonicalized fields
and the `previous_hash` of the event before it, forming an append-only chain
(`ProvenanceGraph.verify_integrity()` recomputes and checks it). Running the
example prints, per scenario, the decision, reason, controls that fired, and
the resulting audit event id/hash pair.

`tests/test_execution_tracing_example.py` asserts the three decisions
(`allow`, `review`, `block`) and that every scenario produces exactly one
chained, hashed audit event.
