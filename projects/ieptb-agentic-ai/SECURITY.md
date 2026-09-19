# Security Policy

## Scope
This repository is a public research/engineering prototype. It intentionally contains synthetic data only and is not an IEPTB production system.

## Security model
- deny-by-default tool authorization
- prompt-injection detection as a heuristic baseline
- PII redaction before retrieval
- tenant-bound authorization
- human approval for critical actions
- append-only audit events with a hash chain
- CI security and evaluation gates

## Reporting
Please do not publish sensitive information in issues. For a suspected vulnerability, provide a minimal reproducible description without personal or confidential data and contact the repository maintainer through GitHub.
