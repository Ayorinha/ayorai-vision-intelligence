# Deployment Reference

AYORAI AI Shield is a reference security library, not a turnkey production appliance.

## Recommended boundary

    Ingress / API Gateway
            |
            v
    Authentication + workload identity
            |
            v
        Agent Runtime
            |
            v
      AYORAI AI Shield
       |     |      |
       |     |      +--> Provenance / audit sink
       |     +---------> Telemetry adapter
       +---------------> Policy / trust / containment
            |
            v
      Authorized tool or service

## Production responsibilities outside this repository

The deployment environment must provide:

- workload identity and credential lifecycle;
- secret storage and rotation;
- authenticated network transport;
- network allowlists and egress controls;
- centralized audit retention;
- incident response and isolation procedures;
- availability, rate limiting and resource quotas;
- environment-specific authorization policy;
- security testing against the deployed topology.

The library's deterministic controls do not replace those controls.

## Release gate

A production release should require:

1. CI and security workflows pass;
2. dependency audit and SBOM are generated;
3. the SBOM artifact is attested;
4. domain-specific evaluation evidence is reviewed;
5. deployment configuration is reviewed for identity, network and secret boundaries;
6. rollback and incident-isolation procedures are tested.

No step above is represented as a certification claim.
