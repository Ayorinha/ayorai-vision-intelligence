# Changelog

## 3.0.0 — 2026-09-19

### AYORAI AI Shield
- Promoted the project from an application-centric reference implementation to a defensive autonomous-agent security architecture.
- Added deterministic runtime defense for agent capabilities and consequential actions.
- Added transaction risk governance and default-deny egress controls.
- Added emergency isolation and attack provenance / replay-defense mechanisms.
- Added synthetic adversarial evaluation coverage.

### Agent Identity & Trust Fabric
- Added scoped agent identity and trust boundaries.
- Added agent-to-agent delegation controls.
- Added delegation depth and revocation controls.
- Integrated trust decisions with the Shield authorization boundary.

### Frontier Agent Evaluation Lab
- Added a dedicated evaluation layer for advanced autonomous-agent behavior.
- Added adversarial regression coverage and deterministic safety assertions.
- Expanded the CI security matrix to execute the evaluation lab.

### MCP and platform security
- Hardened the MCP surface around least privilege and read-only operations.
- Kept consequential review operations behind the application policy boundary.
- Maintained GitHub Actions CI/security gates, dependency auditing and Bandit checks.

### Documentation
- Reframed the README around the three AYORAI security pillars.
- Documented the defensive scope, synthetic-data policy and non-production boundaries.
- Updated portfolio positioning and release metadata.

## 2.1.0
- Aligned package and portfolio release metadata.
- Strengthened MCP least-privilege regression tests.
- Added deterministic tool-registry authorization tests.
- Added CI and Security status badges to the README.

## 2.0.0
- Agentic computer vision platform with local-first RAG, tool orchestration, RPA and human review.

## Unreleased — 2026-09-29

### Agent Runtime Security
- Added a fail-closed runtime control plane combining MCP integrity, containment, data-flow controls and existing deterministic authorization.
- Added TOFU-pinned MCP tool definitions with drift and poisoning-signal detection.
- Added authenticated MCP publisher manifests for controlled reference deployments.
- Added restricted-data egress and output-volume controls.
- Added explicit session containment and tool revocation primitives.
- Added cryptographic algorithm inventory for migration planning.
- Added runtime-attestation integration interface without claiming TEE security.
- Added mandatory short-lived agent delegation with issuer/subject/capability/resource constraints.
- Added SHA-256 grant binding, grant-ID reuse protection, expiry/TTL enforcement and explicit revocation tests.
- Added regression tests for tool poisoning, drift, restricted-data egress, containment and delegation abuse.
- Added ADR 0002 and MCP runtime-security documentation.
- Added no unsupported security or performance claims.
