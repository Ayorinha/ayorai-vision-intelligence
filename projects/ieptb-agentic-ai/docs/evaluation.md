# Evaluation Strategy

## Quality dimensions

### Retrieval
- Recall@k
- Precision@k
- Context relevance

### Generation
- Faithfulness
- Answer relevance
- Citation/evidence correctness
- Structured output validity

### Safety
- Prompt-injection attack success rate
- PII leakage rate
- Unauthorized tool-call rate
- Policy bypass rate

### Reliability
- p50/p95 latency
- timeout rate
- retry rate
- deterministic-rule agreement

## Release gate
A candidate model/prompt/tool-policy configuration should only be promoted when it passes the configured quality and security thresholds.

Example:

```text
RAG groundedness       >= 0.90
Evidence relevance     >= 0.90
PII leakage             = 0
Unauthorized tools      = 0
Security regression     = 0 critical failures
Structured outputs     >= 0.99
```

These are proposed engineering gates for the prototype, not measured production results.

## Evaluation dataset
The public repository should contain only synthetic cases:
- valid remessas
- malformed files
- inconsistent totals
- missing fields
- ambiguous business rules
- malicious documents
- prompt-injection payloads

## Reproducibility
Every evaluation records:
- dataset version
- model
- prompt version
- retrieval parameters
- tool-policy version
- timestamp
