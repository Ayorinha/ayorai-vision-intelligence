# Threat Model Summary

| Threat | Boundary | Control | Residual risk |
|---|---|---|---|
| Prompt injection | User/retrieved text | heuristic detection + untrusted-content rule | detector evasion |
| PII leakage | Input/retrieval | redaction + synthetic dataset | heuristic false negatives |
| Tool abuse | Agent/tool boundary | RBAC + deny-by-default + risk policy | implementation bugs |
| Cross-tenant access | Tool boundary | tenant equality check | identity provider not integrated |
| Retrieval poisoning | Knowledge boundary | evidence treated as untrusted | source integrity not cryptographically verified |
| Critical side effect | Decision boundary | deterministic policy + human approval | approval UX not integrated |
| Audit tampering | Audit store | append-only JSONL + hash chain | local filesystem trust |
