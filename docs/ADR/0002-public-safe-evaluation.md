# ADR-0002: Public-Safe Evaluation

- Status: Accepted
- Date: 2026-09-28

## Context

Security evaluation needs realistic failure modes, but a public portfolio must not expose credentials, private datasets or destructive targets.

## Decision

The public evaluation corpus uses synthetic identities, synthetic transactions and non-destructive scenarios. Public domain references may provide context, but no production account, private record or live financial action is exercised.

## Consequences

This makes evaluation reproducible and safe to publish. It also limits external validity: passing the corpus does not establish resistance to unknown attacks or production security.

## Evidence standard

Security and performance claims must come from executable tests or benchmarks. Narrative architecture claims are labeled as design intent unless executable evidence exists.
