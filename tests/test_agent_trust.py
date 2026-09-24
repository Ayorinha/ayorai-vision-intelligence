from ai_shield.models import AgentRequest, Classification, Decision, Identity
from ai_shield.trust import AgentIdentityRecord, AgentTrustFabric, DelegationGrant


def request(agent_id: str, capability: str, resource: str = "ledger/demo") -> AgentRequest:
    return AgentRequest(
        request_id=f"req-{agent_id}-{capability}",
        identity=Identity(subject="operator", role="analyst", assurance=3),
        agent_id=agent_id,
        capability=capability,
        resource=resource,
        classification=Classification.PUBLIC,
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


def test_delegation_is_scoped_to_subject_capability_and_resource():
    fabric = AgentTrustFabric()
    fabric.register(
        AgentIdentityRecord(
            "agent-root", "team-a", 5, frozenset({"read_public"}), max_delegation_depth=1
        )
    )
    fabric.register(AgentIdentityRecord("agent-child", "team-a", 4, frozenset({"read_public"})))

    grant = DelegationGrant("grant-1", "agent-root", "agent-child", "read_public", "ledger/")
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW

    scoped = request("agent-child", "read_public", "ledger/demo")
    scoped = AgentRequest(**{**scoped.__dict__, "metadata": {"delegation_grant_id": "grant-1"}})
    assert fabric.authorize(scoped).decision == Decision.ALLOW

    outside = request("agent-child", "read_public", "customer/demo")
    outside = AgentRequest(**{**outside.__dict__, "metadata": {"delegation_grant_id": "grant-1"}})
    assert fabric.authorize(outside).decision == Decision.BLOCK



def test_delegation_scope_rejects_similar_prefixes():
    fabric = AgentTrustFabric()
    fabric.register(
        AgentIdentityRecord(
            "agent-root", "team-a", 5, frozenset({"read_public"}), max_delegation_depth=1
        )
    )
    fabric.register(AgentIdentityRecord("agent-child", "team-a", 4, frozenset({"read_public"})))

    grant = DelegationGrant(
        "grant-boundary",
        "agent-root",
        "agent-child",
        "read_public",
        "ledger/demo",
    )
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW

    allowed = request("agent-child", "read_public", "ledger/demo/item/123")
    allowed = AgentRequest(
        **{**allowed.__dict__, "metadata": {"delegation_grant_id": "grant-boundary"}}
    )
    assert fabric.authorize(allowed).decision == Decision.ALLOW

    exact = request("agent-child", "read_public", "ledger/demo")
    exact = AgentRequest(
        **{**exact.__dict__, "metadata": {"delegation_grant_id": "grant-boundary"}}
    )
    assert fabric.authorize(exact).decision == Decision.ALLOW

    attacker_controlled = request("agent-child", "read_public", "ledger/demo-secret")
    attacker_controlled = AgentRequest(
        **{
            **attacker_controlled.__dict__,
            "metadata": {"delegation_grant_id": "grant-boundary"},
        }
    )
    assert fabric.authorize(attacker_controlled).decision == Decision.BLOCK

def test_delegation_cannot_exceed_issuer_depth_or_capability():
    fabric = AgentTrustFabric()
    fabric.register(
        AgentIdentityRecord(
            "agent-root", "team-a", 5, frozenset({"read_public"}), max_delegation_depth=1
        )
    )
    fabric.register(AgentIdentityRecord("agent-child", "team-a", 4, frozenset({"read_public"})))

    too_deep = DelegationGrant(
        "grant-deep", "agent-root", "agent-child", "read_public", "ledger/", depth=2
    )
    assert fabric.issue_delegation(too_deep).decision == Decision.BLOCK

    invalid_capability = DelegationGrant(
        "grant-invalid", "agent-root", "agent-child", "execute_transaction", "ledger/"
    )
    assert fabric.issue_delegation(invalid_capability).decision == Decision.BLOCK


def test_revoked_delegation_is_denied():
    fabric = AgentTrustFabric()
    fabric.register(
        AgentIdentityRecord(
            "agent-root", "team-a", 5, frozenset({"read_public"}), max_delegation_depth=1
        )
    )
    fabric.register(AgentIdentityRecord("agent-child", "team-a", 4, frozenset({"read_public"})))
    grant = DelegationGrant("grant-1", "agent-root", "agent-child", "read_public", "ledger/")
    assert fabric.issue_delegation(grant).decision == Decision.ALLOW
    fabric.revoke_grant("grant-1")
    scoped = request("agent-child", "read_public", "ledger/demo")
    scoped = AgentRequest(**{**scoped.__dict__, "metadata": {"delegation_grant_id": "grant-1"}})
    assert fabric.authorize(scoped).decision == Decision.BLOCK
