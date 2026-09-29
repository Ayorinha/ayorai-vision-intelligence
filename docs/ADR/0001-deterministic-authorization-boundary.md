# ADR-0001: Deterministic Authorization Boundary

- Status: Accepted
- Date: 2026-09-28

## Context

An LLM can generate plausible tool calls without possessing legitimate authority. Treating model output as authorization creates a confused-deputy boundary between reasoning and execution.

## Decision

Authorization is performed by deterministic Python policy and trust controls. The model may propose an action, but it cannot grant itself capabilities.

The execution path is:

`request -> identity/trust -> capability policy -> data boundary -> human approval -> transaction governance -> egress -> execution`

## Consequences

### Positive
- authorization is testable without an LLM;
- security regressions are deterministic;
- policy decisions are auditable;
- the system can run without an external model.

### Trade-offs
- policies must be explicitly maintained;
- dynamic context requires deliberate policy inputs;
- this does not eliminate model-level or infrastructure-level risk.

## Rejected alternative

Allowing the LLM to decide whether its own tool call is safe was rejected because the same component would be both requester and authority.

## Evidence

- `ai_shield/policy.py`
- `ai_shield/engine.py`
- `tests/test_adversarial_ai_shield.py`
- `benchmarks/shield_benchmark.py`
