# Security Audit & Assurance Baseline

## Purpose
This document records the security-hardening baseline for the AYORAI AI Shield reference implementation. It is an engineering evidence document, not a production certification or independent third-party audit.

The baseline is informed by NIST AI RMF and its Generative AI Profile, NIST CSF 2.0, NIST SSDF 1.1, and OWASP GenAI and Agentic security guidance.

## Assurance model
Every material security claim should map through: Threat -> Security requirement -> Control -> Implementation -> Automated test -> CI evidence -> Documentation.

## Findings from repository review
### A-01 — Egress path was structurally unreachable
The policy layer rejected every external-network request before the dedicated egress allowlist could be evaluated.
**Hardening:** external access is now decided by the dedicated egress boundary. The default allowlist is empty.

### A-02 — Replay protection consumed REVIEW decisions
A consequential request receiving REVIEW was previously inserted into the replay set, preventing re-evaluation after human approval.
**Hardening:** only successfully ALLOWed consequential actions consume the replay key.

### A-03 — Transaction amount was not bound to the governed profile
The request amount and transaction governance profile could disagree.
**Hardening:** consequential transaction evaluation blocks on an amount mismatch.

### A-04 — Human approval validation was under-specified
Approval validation did not require valid approval identifiers, reviewer identity, timezone-aware timestamps, or coherent expiry.
**Hardening:** approval metadata is validated before authorization.

### A-05 — Provenance is tamper-evident in memory, not an immutable audit store
The hash chain detects event mutation while the process retains its sealed state, but it does not provide durable external immutability.
**Disposition:** documented residual limitation. Production deployments would require an append-only or independently protected audit sink.

### A-06 — MCP registry contains gated mutating functions
The registry contains approval/rejection functions, while the currently exposed MCP server surface is read-only.
**Disposition:** retain internal functions behind the application policy boundary and require explicit policy tests before exposing consequential MCP tools.

## Release gate
1. Security invariants have deterministic automated tests.
2. CI executes the relevant tests.
3. Dependency and static security checks remain green.
4. Threat model and residual risk are updated when the security boundary changes.
5. README claims remain consistent with executable behavior.

## Important limitation
AYORAI AI Shield is a defensive reference implementation. Automated tests do not establish production security, certification, compliance, or resistance to all attacks.