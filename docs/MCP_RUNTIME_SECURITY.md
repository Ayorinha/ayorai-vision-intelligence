# MCP Runtime Security

AYORAI treats MCP tool metadata as security-sensitive input rather than trusted configuration.

## Threat patterns covered

- tool-definition poisoning;
- definition drift / rug-pull style changes;
- unpinned tool discovery;
- revoked tools;
- authenticated publisher manifests;
- restricted-data egress;
- high-volume outbound flows;
- runtime containment.

## Control sequence

tool metadata -> integrity assessment -> containment -> data-flow policy -> identity/policy authorization -> execution -> provenance

## Trust model

A tool must be explicitly pinned before execution. A changed definition fails closed until it is reviewed and pinned again.

The registry is intentionally deterministic. It does not ask an LLM whether a tool is safe.

## Limits

Pattern-based poisoning detection is not a complete semantic detector. It is one layer in defense-in-depth. Deployments should add asymmetric publisher signatures, authenticated transport, server-side authorization, endpoint allowlists and independent security review. The included HMAC reference primitive is for controlled reference deployments; it is not non-repudiation and does not replace a production key-management system.

## Research directions

- asymmetric cryptographically signed tool manifests and key rotation;
- authenticated MCP server identity;
- semantic diffing of tool descriptions and schemas;
- policy enforcement at a gateway;
- response inspection for indirect prompt injection;
- replayable runtime telemetry.
