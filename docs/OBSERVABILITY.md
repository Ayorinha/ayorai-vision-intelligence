# Observability Boundary

AYORAI AI Shield treats observability as a security boundary, not as an authorization mechanism.

## Runtime event contract

The engine emits one structured event after every policy evaluation:

- event name: `ai_shield.policy.evaluate`;
- decision and deterministic reason;
- control names returned by policy;
- request digest for correlation without exporting the raw request;
- decision duration in milliseconds;
- whether the trust fabric was active;
- whether the request was consequential.

The default sink is a no-op. Telemetry failure therefore cannot silently become authorization.

## OpenTelemetry integration

`ai_shield.telemetry.TelemetrySink` is the adapter seam for an OpenTelemetry exporter or another enterprise observability system. The repository deliberately keeps the core runtime free of a mandatory telemetry dependency.

An integration should map:

- event name to span/event name;
- attributes to typed telemetry attributes;
- request digest to a correlation attribute;
- decision, reason and controls to security dimensions.

Do not export raw prompts, retrieved documents, secrets, credentials, unrestricted tool arguments, or raw sensitive resources.

## Operational signals

A production deployment should monitor at least:

- decision count by decision type;
- policy evaluation latency percentiles;
- isolation activations;
- replay blocks;
- delegation failures and revocations;
- MCP integrity/drift failures;
- egress blocks;
- provenance-integrity failures;
- telemetry delivery health.

These are operational recommendations, not measured AYORAI performance claims.
