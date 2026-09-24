from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .models import AgentRequest, Decision, PolicyResult


@dataclass(frozen=True)
class AgentIdentityRecord:
    agent_id: str
    owner: str
    assurance: int
    capabilities: frozenset[str]
    active: bool = True
    max_delegation_depth: int = 0


@dataclass(frozen=True)
class DelegationGrant:
    grant_id: str
    issuer_agent_id: str
    subject_agent_id: str
    capability: str
    resource_prefix: str
    expires_at: str | None = None
    depth: int = 1


@dataclass
class AgentTrustFabric:
    """Deterministic identity, capability and delegation control plane."""

    identities: dict[str, AgentIdentityRecord] = field(default_factory=dict)
    grants: dict[str, DelegationGrant] = field(default_factory=dict)
    revoked_agents: set[str] = field(default_factory=set)
    revoked_grants: set[str] = field(default_factory=set)

    def register(self, identity: AgentIdentityRecord) -> None:
        self.identities[identity.agent_id] = identity

    def revoke_agent(self, agent_id: str) -> None:
        self.revoked_agents.add(agent_id)

    def revoke_grant(self, grant_id: str) -> None:
        self.revoked_grants.add(grant_id)

    def issue_delegation(self, grant: DelegationGrant) -> PolicyResult:
        issuer = self.identities.get(grant.issuer_agent_id)
        subject = self.identities.get(grant.subject_agent_id)
        if issuer is None or subject is None:
            return PolicyResult(Decision.BLOCK, "unknown_agent_identity", ("agent_identity",))
        if not issuer.active or issuer.agent_id in self.revoked_agents:
            return PolicyResult(Decision.BLOCK, "inactive_delegation_issuer", ("agent_identity",))
        if not subject.active or subject.agent_id in self.revoked_agents:
            return PolicyResult(Decision.BLOCK, "inactive_delegation_subject", ("agent_identity",))
        if grant.capability not in issuer.capabilities:
            return PolicyResult(Decision.BLOCK, "issuer_lacks_capability", ("delegation",))
        if grant.depth < 1 or grant.depth > issuer.max_delegation_depth:
            return PolicyResult(Decision.BLOCK, "delegation_depth_exceeded", ("delegation",))
        if grant.capability not in subject.capabilities:
            return PolicyResult(Decision.BLOCK, "subject_lacks_capability", ("least_privilege",))
        self.grants[grant.grant_id] = grant
        return PolicyResult(Decision.ALLOW, "delegation_issued", ("delegation",))

    @staticmethod
    def _resource_in_scope(resource: str, prefix: str) -> bool:
        """Return True only for the exact resource or a child resource."""
        resource = resource.rstrip("/")
        prefix = prefix.rstrip("/")
        return resource == prefix or resource.startswith(prefix + "/")

    def authorize(self, request: AgentRequest) -> PolicyResult:
        identity = self.identities.get(request.agent_id)
        if identity is None:
            return PolicyResult(Decision.BLOCK, "unknown_agent_identity", ("agent_identity",))
        if not identity.active or identity.agent_id in self.revoked_agents:
            return PolicyResult(Decision.BLOCK, "agent_identity_revoked", ("agent_identity",))
        if request.capability not in identity.capabilities:
            return PolicyResult(Decision.BLOCK, "agent_capability_not_granted", ("least_privilege",))

        grant_id = request.metadata.get("delegation_grant_id")
        if grant_id:
            grant = self.grants.get(str(grant_id))
            if grant is None or grant.grant_id in self.revoked_grants:
                return PolicyResult(Decision.BLOCK, "delegation_grant_invalid", ("delegation",))
            if grant.subject_agent_id != request.agent_id:
                return PolicyResult(Decision.BLOCK, "delegation_subject_mismatch", ("delegation",))
            if grant.capability != request.capability:
                return PolicyResult(Decision.BLOCK, "delegation_capability_mismatch", ("delegation",))
            if not self._resource_in_scope(request.resource, grant.resource_prefix):
                return PolicyResult(Decision.BLOCK, "delegation_scope_exceeded", ("delegation",))
            if grant.expires_at is not None:
                try:
                    if datetime.now(UTC) >= datetime.fromisoformat(grant.expires_at):
                        return PolicyResult(Decision.BLOCK, "delegation_expired", ("delegation",))
                except ValueError:
                    return PolicyResult(Decision.BLOCK, "delegation_expiry_invalid", ("delegation",))
        return PolicyResult(Decision.ALLOW, "agent_trust_satisfied", ("agent_identity", "least_privilege"))

    def snapshot(self) -> dict[str, int]:
        return {
            "registered_agents": len(self.identities),
            "active_agents": sum(
                identity.active and identity.agent_id not in self.revoked_agents
                for identity in self.identities.values()
            ),
            "delegations": len(self.grants),
            "revoked_delegations": len(self.revoked_grants),
        }
