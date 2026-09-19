# Frontier AI evaluation plan

## Why this exists

Frontier models are increasingly capable of computer use, cybersecurity reasoning and multi-step autonomous work. OpenAI's GPT-6 Astra System Card describes a critical cybersecurity capability level and emphasizes stronger isolation, monitoring and blocking evaluations. This project adopts those architectural lessons without requiring a live frontier-model connection.

## Evaluation principle

**The model proposes; the Shield decides.** A frontier model can be connected to a proposal-generation layer later, but its confidence, natural-language reasoning, or claimed authority must never become an authorization primitive.

## Safe test families

1. Scope confusion — model claims a broader target than authorized.
2. Capability escalation — model proposes an unavailable tool.
3. Identity confusion — model claims another role.
4. Data boundary crossing — model requests higher classification.
5. Transaction pressure — model proposes a high-risk synthetic transfer.
6. Egress request — model proposes an unapproved external destination.
7. Isolation override — model metadata attempts to disable containment.
8. Agent-to-agent escalation — one synthetic agent asks another for excess privilege.

## Controls

- deterministic authorization
- default-deny egress
- human approval for consequential actions
- independent isolation state
- provenance for every decision
- regression tests in CI

## Limitations

Passing these tests does not establish security against an unknown AGI. It demonstrates that the tested authority boundaries are enforced for the modeled cases.


## Evaluation Lab v2

The repository now exposes `ai_shield.evaluation_lab` for deterministic case execution and aggregate pass-rate reporting across synthetic frontier-agent scenarios.
