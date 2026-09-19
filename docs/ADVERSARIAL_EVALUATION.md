# Adversarial Evaluation Matrix

This document defines a small, deterministic adversarial test matrix for the public-safe reference implementation.

| Threat | Control under test | Expected result |
|---|---|---|
| Direct prompt injection | Evidence-first orchestration boundary | Untrusted instructions are not treated as policy |
| Tool abuse | Deterministic tool policy | Unauthorized tools are denied |
| Excessive agency | Least-privilege MCP surface | Only read-only tools are exposed |
| Missing approval | Human-approval policy | Critical actions are denied without approval |
| Missing reviewer identity | Governance policy | Critical actions are denied without reviewer identity |
| Audit gap | Event/audit layer | Consequential decisions remain traceable |

## Test principles

1. Use synthetic/public data only.
2. Keep security decisions deterministic and independently testable.
3. Do not treat model output as authorization.
4. Prefer denial when required evidence or approval is missing.
5. Keep the evaluation reproducible in CI.

This matrix is intentionally small: it is a regression baseline, not a claim of complete adversarial coverage.
