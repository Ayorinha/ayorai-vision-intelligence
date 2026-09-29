from datetime import UTC, datetime, timedelta

from ai_shield.models import AgentRequest, Classification, Decision, Identity
from ai_shield.trust import AgentIdentityRecord, AgentTrustFabric, DelegationGrant


def expiry(hours: float = 0.5) -> str:
    return (datetime.now(UTC) + timedelta(hours=hours)).isoformat()


def request(agent_id: str, capability: str, resource: str = "ledger/demo", metadata=None) -> AgentRequest:
    return AgentRequest(
        request_id=f"req-{agent_id}-{capability}",
        identity=Identity(subject="operator", role="analyst", assurance=3),
        agent_id=agent_id,
        capability=capability,
        resource=resource,
        classification=Classification.PUBLIC,
        metadata=metadata or {},
    )


def fabric_with_agents() -> AgentTrustFabric:
    fabric = AgentTrustFabric()
    fabric.register(
        AgentIdentityRecord(
            "agent-root", "team-a", 5, frozenset({"read_public"}), max_delegation_depth=1
        )
    )
    fabric.register(AgentIdentityRecord("agent-child", "team-a", 4, frozenset({"read_public"})))
    return fabric


def signed_request(agent_id: str, grant: DelegationGrant, resource="ledger/demo"):
    return request(
        agent_id,
        "read_public",
        resource,
        {"delegation_grant_id": grant.grant_id, "delegation_grant_digest": grant.digest()},
    )


def test_registered_agent_requires_explicit_capability():
    fabric = AgentTrustFabric()
    fabric.register(AgentIdentityRecord("agent-a", "team-a", 4, frozenset({"read_public"})))

    assert fabric.authorize(request("agent-a", "read_public")).decision == Decision.ALLOW
    assert fabric.authorize(request("agent-a", "read_internal")).decision == Decision.BLOCK


def test_unknown_or_revoked_agent_is_blocked():
    fabric = AgentTrustFabric()
    assert fabric.authorize(request("unknown", "read_public")).decision == Decision.BLOCK

    fabric.register(AgentIdentityRecord("agent-a", "team-a", 4, frozenset({"read_public"})))
    fabric.revoke_agent("agent-a")
    assert fabric.authorize(request("agent-a", "read_public")).decision == Decision.BLOCK


def test_delegation_is_short_lived_and_bound_to_subject_capability_and_resource():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-1", "agent-root", "agent-child", "read_public", "ledger/", expiry()
    )
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW
    assert fabric.authorize(signed_request("agent-child", grant)).decision == Decision.ALLOW
    assert fabric.authorize(signed_request("agent-child", grant, "customer/demo")).decision == Decision.BLOCK


def test_delegation_binding_rejects_tampered_metadata():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-binding", "agent-root", "agent-child", "read_public", "ledger/", expiry()
    )
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW

    tampered = request(
        "agent-child",
        "read_public",
        metadata={"delegation_grant_id": "grant-binding", "delegation_grant_digest": "tampered"},
    )
    assert fabric.authorize(tampered).reason == "delegation_binding_invalid"


def test_delegation_scope_rejects_similar_prefixes():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-boundary", "agent-root", "agent-child", "read_public", "ledger/demo", expiry()
    )
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW

    assert fabric.authorize(signed_request("agent-child", grant, "ledger/demo/item/123")).decision == Decision.ALLOW
    assert fabric.authorize(signed_request("agent-child", grant, "ledger/demo")).decision == Decision.ALLOW
    assert fabric.authorize(signed_request("agent-child", grant, "ledger/demo-secret")).decision == Decision.BLOCK


def test_delegation_cannot_exceed_issuer_depth_or_capability():
    fabric = fabric_with_agents()
    too_deep = DelegationGrant(
        "grant-deep", "agent-root", "agent-child", "read_public", "ledger/", expiry(), depth=2
    )
    assert fabric.issue_delegation(too_deep).decision == Decision.BLOCK

    invalid_capability = DelegationGrant(
        "grant-invalid", "agent-root", "agent-child", "execute_transaction", "ledger/", expiry()
    )
    assert fabric.issue_delegation(invalid_capability).decision == Decision.BLOCK


def test_expired_delegation_is_rejected():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-expired",
        "agent-root",
        "agent-child",
        "read_public",
        "ledger/",
        (datetime.now(UTC) - timedelta(seconds=1)).isoformat(),
    )
    assert fabric.issue_delegation(grant).reason == "delegation_expired"


def test_long_lived_delegation_is_rejected():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-long", "agent-root", "agent-child", "read_public", "ledger/", expiry(hours=2)
    )
    assert fabric.issue_delegation(grant).reason == "delegation_ttl_exceeded"


def test_missing_expiry_is_rejected():
    fabric = fabric_with_agents()
    grant = DelegationGrant("grant-no-expiry", "agent-root", "agent-child", "read_public", "ledger/")
    assert fabric.issue_delegation(grant).reason == "delegation_expiry_required"


def test_delegation_cannot_be_reused_for_another_payload():
    fabric = fabric_with_agents()
    original = DelegationGrant(
        "grant-reuse", "agent-root", "agent-child", "read_public", "ledger/", expiry()
    )
    assert fabric.issue_delegation(original).decision == Decision.ALLOW
    altered = DelegationGrant(
        "grant-reuse", "agent-root", "agent-child", "read_public", "customer/", expiry()
    )
    assert fabric.issue_delegation(altered).reason == "delegation_grant_id_reuse"


def test_self_delegation_is_denied():
    fabric = AgentTrustFabric()
    fabric.register(
        AgentIdentityRecord(
            "agent-root", "team-a", 5, frozenset({"read_public"}), max_delegation_depth=1
        )
    )
    grant = DelegationGrant(
        "grant-self", "agent-root", "agent-root", "read_public", "ledger/", expiry()
    )
    assert fabric.issue_delegation(grant).reason == "self_delegation_invalid"


def test_revoked_delegation_is_denied():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-revoked", "agent-root", "agent-child", "read_public", "ledger/", expiry()
    )
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW
    fabric.revoke_grant(grant.grant_id)
    assert fabric.authorize(signed_request("agent-child", grant)).decision == Decision.BLOCK


def test_delegation_cannot_be_used_by_another_subject():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-subject", "agent-root", "agent-child", "read_public", "ledger/", expiry()
    )
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW
    assert fabric.authorize(signed_request("agent-root", grant)).reason == "delegation_subject_mismatch"


def test_delegation_cannot_escalate_capability():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-cap", "agent-root", "agent-child", "read_public", "ledger/", expiry()
    )
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW
    escalated = request(
        "agent-child",
        "execute_transaction",
        metadata={"delegation_grant_id": grant.grant_id, "delegation_grant_digest": grant.digest()},
    )
    assert fabric.authorize(escalated).reason == "agent_capability_not_granted"


def test_delegation_scope_rejects_path_traversal():
    fabric = fabric_with_agents()
    grant = DelegationGrant(
        "grant-traversal", "agent-root", "agent-child", "read_public", "ledger/demo", expiry()
    )
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW
    escaped = signed_request("agent-child", grant, "ledger/demo/../secrets")
    assert fabric.authorize(escaped).reason == "delegation_scope_exceeded"
