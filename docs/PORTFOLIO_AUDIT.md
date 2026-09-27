# Portfolio Audit — AYORAI AI Shield

## Purpose

This document records the current engineering and portfolio posture of the AYORAI AI Shield repository. It is intended to make claims about the project traceable to executable tests, CI workflows and documented limitations.

## Verified scope

- Defensive reference architecture for autonomous AI agents.
- Deterministic authorization is separated from model reasoning.
- Identity, capability, policy, transaction, egress, provenance, replay and isolation controls are represented in the architecture.
- Synthetic, non-destructive scenarios are used for adversarial evaluation.
- GitHub Actions automates CI, security checks and benchmark execution.

## Evidence standard

A claim should be supported by one of:

1. an executable test;
2. an executable benchmark;
3. a CI workflow result or artifact;
4. a versioned design document.

Narrative claims without one of these forms should be treated as design intent rather than measured evidence.

## Current benchmark evidence

The benchmark executes the real ShieldEngine authorization path against synthetic scenarios. The latest recorded successful execution passed 10/10 scenarios. This demonstrates reproducible enforcement for the scenarios represented in the benchmark; it does not establish production security or resistance to unknown attacks.

## Security boundary

The core invariant is:

> The model may propose; deterministic policy decides whether the requested capability is callable.

Human approval is required where the configured policy marks an action as consequential. External egress defaults to deny, and isolation can revoke high-impact capabilities.

## Limitations

- Synthetic evaluation is not equivalent to a real-world authorized red-team engagement.
- Tamper-evident provenance is not the same as tamper-proof storage.
- Current Shield controls do not constitute post-quantum cryptography.
- Production deployments require environment-specific identity, secrets, network, observability, durable audit and incident-response controls.

## Interview-safe description

> AYORAI AI Shield is a public-safe reference architecture I built to separate AI reasoning from system authority. The model can propose an action, but deterministic policy, identity, capability and transaction controls decide whether that action is allowed. I validate those controls with executable synthetic benchmarks in GitHub Actions, rather than claiming that synthetic tests are real-world attacks or a production certification.
