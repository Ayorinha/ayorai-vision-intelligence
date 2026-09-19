from ai_shield.evaluation_lab import EvaluationCase, Scenario, evaluate_case
from ai_shield.models import AgentRequest, Classification, Decision, Identity
from ai_shield.trust import AgentIdentityRecord, AgentTrustFabric


def test_delegation_abuse_is_blocked():
    fabric = AgentTrustFabric()
    fabric.register(AgentIdentityRecord("root", "team", 5, frozenset({"read_public"}), max_delegation_depth=1))
    fabric.register(AgentIdentityRecord("child", "team", 4, frozenset({"read_public"})))
    request = AgentRequest(
        request_id="delegation-abuse",
        identity=Identity(subject="synthetic", role="analyst", assurance=3),
        agent_id="child",
        capability="read_public",
        resource="outside/demo",
        classification=Classification.PUBLIC,
        metadata={"delegation_grant_id": "missing"},
    )
    case = EvaluationCase("delegation-abuse", Scenario.DELEGATION_ABUSE, request, Decision.BLOCK)
    assert evaluate_case(fabric, case).passed
