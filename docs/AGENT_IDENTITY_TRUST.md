# AYORAI Agent Identity & Trust Fabric

## Purpose

The Trust Fabric is the identity and delegation control plane that sits before the existing deterministic AI Shield policy. It answers a different question from the Shield:

- Trust Fabric: who is this agent, what capability was granted, and under whose authority?
- AI Shield: given that identity and capability context, should this specific action execute?

The model never becomes an authorization primitive.

## Controls

- Explicit agent registration with assurance metadata.
- Capability allowlists per agent identity.
- Immediate agent revocation.
- Scoped agent-to-agent delegation.
- Delegation subject, issuer and capability binding.
- Resource-prefix scoping for delegated authority.
- Delegation depth limits.
- Mandatory short-lived delegation grants.
- Deterministic grant digests bound to the presented request.
- Grant-ID reuse protection against payload substitution.
- Explicit grant revocation.
- Deterministic decisions suitable for regression testing.

## Delegation invariant

A child agent cannot gain authority that the issuer does not already possess. Delegation is additionally constrained by:

1. issuer identity being active;
2. subject identity being active;
3. issuer holding the delegated capability;
4. subject holding the delegated capability;
5. configured delegation depth;
6. exact issuer/subject/capability binding;
7. resource scope;
8. mandatory expiry;
9. maximum delegation lifetime (one hour by default);
10. request-to-grant digest binding;
11. explicit revocation state.

A delegation presented to the policy engine must include both its grant identifier and the SHA-256 digest of the exact grant payload. This is an integrity/binding control; it is not a substitute for asymmetric credentials or proof-of-possession.

## Integration boundary

AgentTrustFabric.authorize() can be composed with ShieldEngine before the existing policy decision. The repository keeps this control plane explicit rather than silently changing the behavior of existing demonstrations.

For a production deployment, identity and delegation state should be backed by a durable trust service, cryptographic credentials, asymmetric signatures or workload identity, key rotation, and transactional revocation propagation.

## Safety boundary

This is a defensive reference implementation. It uses synthetic identities and does not implement credential theft, real-world intrusion, persistence, or unauthorized access.
