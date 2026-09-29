# ADR 0002 — Agent Runtime Control Plane

## Status
Accepted

## Context

Recent MCP security research and vendor incident analysis identify tool-definition poisoning, untrusted tool supply chains, missing per-call authorization, data exfiltration and runtime containment as material agent risks.

The existing Shield already provides deterministic policy, agent identity/delegation, isolation and tamper-evident provenance. The missing architectural seam is a single fail-closed boundary that composes those controls before consequential execution.

## Decision

Introduce AgentRuntimeControlPlane with four deterministic stages:

1. MCP tool integrity and poisoning assessment.
2. Runtime containment check.
3. Outbound data-flow policy.
4. Existing Shield identity/policy authorization.

No LLM is used as an authorization authority.

## Security properties

- Unpinned MCP tools are denied.
- Pinned tool-definition drift is denied.
- Known poisoning indicators are denied.
- Restricted data cannot leave to an unapproved destination.
- Containment suspends execution.
- Existing identity/delegation and policy controls remain authoritative.
- The components are independently testable.

## Non-goals

This ADR does not claim complete MCP security, complete prompt-injection detection, TEE support, or post-quantum cryptographic security. attestation.py and crypto.py provide integration and migration interfaces only.

## Evidence policy

Performance or security percentages must be produced by the repository benchmark harness before publication. Vendor-reported or academic benchmark results are not presented as AYORAI results.
