# AYORAI AI Shield

## Objective

Reproducible defensive reference architecture for constraining autonomous AI in financial environments. Synthetic data only.

## Threat model

Safe synthetic Red Agent scenarios cover prompt injection, capability escalation, unauthorized restricted-data access, tool abuse, agent-to-agent manipulation, transaction abuse, and network egress.

## Security invariants

1. Unknown capabilities are denied.
2. Role mismatch is denied.
3. Data classification cannot be exceeded.
4. External egress is default-deny.
5. Critical financial actions require human approval.
6. Isolation revokes high-impact capabilities.
7. LLM output is never the authorization primitive.
8. Every decision is recorded in provenance.

No software can honestly guarantee perfect security against an unknown future AGI. This project therefore uses measurable invariants, adversarial regression tests, and containment behavior rather than claiming invulnerability.
