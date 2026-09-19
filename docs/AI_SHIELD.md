# AYORAI AI Shield

## Objective
Reproducible defensive reference architecture for constraining autonomous AI in financial environments. Synthetic data only.

## Threat model
Safe synthetic Red Agent scenarios cover prompt injection, capability escalation, unauthorized restricted-data access, tool abuse, agent-to-agent manipulation, transaction abuse, network egress, replay, and audit-log tampering.

## Security invariants
1. Unknown capabilities are denied.
2. Role mismatch is denied.
3. Data classification cannot be exceeded.
4. External egress is default-deny.
5. Critical financial actions require scoped human approval.
6. Human approvals are bound to a stable request digest and may expire.
7. Consequential requests cannot be replayed within the same ShieldEngine instance.
8. Isolation revokes high-impact capabilities.
9. LLM output is never the authorization primitive.
10. Every decision is recorded in a tamper-evident hash chain.
11. Provenance integrity verification detects modification or chain reordering.

## Tamper-evident provenance
Each provenance event contains a UTC timestamp, the previous event hash, and a SHA-256 digest over canonicalized event fields. verify_integrity() recomputes the chain and detects modified events, deleted/reordered links, or inconsistent hashes.

This is tamper-evident, not tamper-proof. A production deployment should persist the audit stream in an append-only or externally anchored store and protect signing keys separately from the application process.

## Replay and approval binding
Consequential capabilities use request_id or an explicit idempotency_key as a replay key. Once a consequential request reaches ALLOW or REVIEW, repeating that key is blocked.

Human approval is not represented by a bare boolean alone. A HumanApproval carries an approval identifier, approver identity, timestamp, optional expiry, and the SHA-256 digest of the exact request being approved. Modifying the resource, amount, destination, identity, capability, or other bound fields invalidates the approval.

## Measurement
The defensive evaluation should track:
- approval-binding rejection rate;
- duplicate/replay rejection rate;
- provenance tamper-detection rate;
- deterministic decision reproducibility;
- isolation enforcement rate;
- time from detected invariant violation to containment.

The benchmark remains synthetic and non-destructive. Passing these tests does not establish security against unknown or future frontier systems.

## Agent Identity & Trust Fabric\n\nThe Shield can be composed with a deterministic trust fabric that registers agents, grants explicit capabilities, constrains agent-to-agent delegation, limits delegation depth, scopes delegated resources, and supports immediate revocation. See `docs/AGENT_IDENTITY_TRUST.md`.\n\n## Threat-model alignment
The design intentionally treats identity, tool authority, data access, transaction execution, egress, auditability, and containment as separate control-plane concerns. The model proposes; the Shield decides.