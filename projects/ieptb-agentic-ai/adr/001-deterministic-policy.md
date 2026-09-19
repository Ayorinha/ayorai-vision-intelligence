# ADR-001: Keep authorization outside the model

## Decision
The LLM/agent may propose actions, but deterministic policy code decides whether a tool can execute.

## Rationale
Authorization must be reproducible, testable, auditable and fail closed. Model output is treated as untrusted input.

## Consequence
Policy code becomes part of the security boundary and requires regression tests whenever tools or roles change.
