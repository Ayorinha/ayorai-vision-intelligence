from ai_shield.engine import ShieldEngine
from ai_shield.models import AgentRequest, Classification, Decision, Identity
from ai_shield.trust import AgentIdentityRecord, AgentTrustFabric


def test_shield_engine_can_compose_trust_fabric():
    fabric = AgentTrustFabric()
    fabric.register(
        AgentIdentityRecord(
            "agent-a", "team-a", 4, frozenset({"read_public"})
        )
    )
    engine = ShieldEngine(trust_fabric=fabric)
    request = AgentRequest(
        request_id="req-1",
        identity=Identity(subject="operator", role="analyst", assurance=3),
        agent_id="agent-a",
        capability="read_public",
        resource="ledger/demo",
        classification=Classification.PUBLIC,
    )
    assert engine.evaluate(request).decision == Decision.ALLOW


def test_shield_engine_blocks_unknown_agent_before_policy():
    fabric = AgentTrustFabric()
    engine = ShieldEngine(trust_fabric=fabric)
    request = AgentRequest(
        request_id="req-2",
        identity=Identity(subject="operator", role="analyst", assurance=3),
        agent_id="unknown",
        capability="read_public",
        resource="ledger/demo",
        classification=Classification.PUBLIC,
    )
    assert engine.evaluate(request).decision == Decision.BLOCK
