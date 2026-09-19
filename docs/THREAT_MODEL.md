# Threat Model

## Scope
AYORAI Vision Intelligence is a public-safe reference platform for agentic workflows involving computer vision, retrieval and controlled tools. It uses synthetic/public demonstration data only.

## Assets
- uploaded media and derived detections
- knowledge-base content
- tool credentials and configuration
- review decisions
- audit events
- model and prompt configuration

## Threats and controls
| Threat | Control | Residual risk |
|---|---|---|
| Prompt injection | Evidence-first orchestration and deterministic policy boundary | Medium |
| Unauthorized tool call | Explicit registry and policy matrix | Low/Medium |
| Excessive agency | Least-privilege MCP surface; critical actions require human approval | Low |
| Data exfiltration | Public-safe dataset policy; no credentials in repo | Medium |
| RAG poisoning | Local knowledge ownership and source metadata | Medium |
| PII leakage | Synthetic/public demo data; deployment must add redaction | Medium |
| Supply-chain compromise | Dependency and static security checks in CI | Medium |
| Model hallucination | Evidence retrieval and deterministic validation boundary | Medium |

## Security invariant
**The model may propose; deterministic policy decides whether a tool is callable; humans approve consequential actions.**

This is a portfolio reference architecture, not a production security certification.