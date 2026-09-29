# Engineering Evidence

This repository is designed to make senior-level engineering claims inspectable rather than promotional.

## Evidence layers

| Layer | Evidence | Repository location |
|---|---|---|
| Architecture | ADRs and system diagrams | `docs/ADR/`, `docs/ARCHITECTURE.md` |
| Threat modeling | Assets, threats, controls and residual risk | `docs/THREAT_MODEL.md` |
| Deterministic enforcement | Executable policy and trust boundary | `ai_shield/` |
| Adversarial evaluation | Synthetic regression corpus | `tests/test_prompt_injection.py`, `tests/test_adversarial_*.py` |
| Benchmarking | Real ShieldEngine execution | `benchmarks/shield_benchmark.py` |
| Observability | Dependency-free telemetry adapter and security boundary | `ai_shield/telemetry.py`, `docs/OBSERVABILITY.md` |
| CI quality | Tests, lint, security and benchmark gates | `.github/workflows/` |
| Supply chain | Dependency audit, dependency review, SBOM and SBOM attestation | `.github/workflows/security.yml`, `dependency-review.yml`, `sbom.yml` |
| Static analysis | CodeQL and Bandit | `.github/workflows/codeql.yml`, `security.yml` |

## Claim discipline

A metric is published only when it is produced by the repository's executable harness or a GitHub Actions artifact. No benchmark number is manually inserted into the README.

## Current limitations

- The public corpus is synthetic and intentionally non-destructive.
- Benchmark latency is environment-dependent.
- A passing regression suite is not a security certification.
- Production deployments require environment-specific identity, secrets, network, observability, resilience and incident-response controls.
- The telemetry adapter is OpenTelemetry-compatible by contract but does not itself provide an OpenTelemetry backend.
- SBOM attestation depends on GitHub Actions trust and repository permissions; it is not a software supply-chain certification.