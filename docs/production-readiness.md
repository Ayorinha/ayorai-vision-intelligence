# Production Readiness

This project follows the AYORAI engineering contract: deterministic boundaries, automated validation, security controls, observability, reproducible execution and evidence-backed releases.

## Definition of done
- [x] CI/security workflow exists or is established in the repository
- [x] Security/data-handling boundary documented
- [x] Architecture documented
- [x] Dependency audit and SBOM generation are automated
- [x] Runtime telemetry has a dependency-free adapter boundary
- [ ] Domain-specific evaluation evidence continuously expanded
- [ ] Release artifacts gated by CI

## Delivery pipeline
BRANCH → COMMIT → PR → REVIEW → MERGE → CI/CD → RELEASE

See `docs/OBSERVABILITY.md` for telemetry boundaries and `docs/DEPLOYMENT_REFERENCE.md` for production responsibilities.