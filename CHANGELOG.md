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


## Unreleased — Security hardening baseline

- hardened human-approval validation;
- made egress allowlisting reachable while retaining default deny;
- prevented REVIEW outcomes from consuming consequential replay keys;
- bound transaction requests to their governed amount;
- added regression tests for these security invariants;
- documented audit findings, residual risks, and assurance gates.
