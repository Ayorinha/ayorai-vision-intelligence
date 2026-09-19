# AYORAI AI Shield

**Advanced Defense Against Autonomous AI**

A defensive, deterministic containment reference architecture for protecting financial and other high-value systems from autonomous AI agents. Synthetic data only; no real financial infrastructure.

## Security thesis

> **Intelligence does not grant authority.**

Agents may analyze evidence and propose actions. Deterministic policy controls decide whether an action is allowed. Critical actions require human approval. A separate containment controller can revoke capabilities and mark the session isolated.

## Components

- Identity Guardian
- Capability Firewall
- Transaction Governor
- Data Broker
- Egress Controller
- Attack Provenance Graph
- Sovereign Isolator
- Safe adversarial evaluator

## Safety boundary

All attack scenarios are simulated against in-memory/synthetic resources. No credential theft, exploitation of real systems, real transaction execution, persistence, or network attack functionality is included.

## Run

    python -m pytest -q
    python -m ai_shield.demo

## Positioning

AI Engineering · Agentic Security · AI Safety · Financial Security · Zero Trust
