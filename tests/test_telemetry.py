from ai_shield.engine import ShieldEngine
from ai_shield.models import AgentRequest, Classification, Decision, Identity
from ai_shield.telemetry import InMemoryTelemetry


def request() -> AgentRequest:
    return AgentRequest(
        request_id="req-telemetry",
        identity=Identity(subject="alice", role="analyst", assurance=3),
        agent_id="agent-1",
        capability="read_public",
        resource="report/1",
        classification=Classification.PUBLIC,
    )


def test_engine_emits_structured_policy_telemetry_without_affecting_decision() -> None:
    telemetry = InMemoryTelemetry()
    engine = ShieldEngine(telemetry=telemetry)

    result = engine.evaluate(request())

    assert result.decision == Decision.ALLOW
    assert len(telemetry.events) == 1
    event = telemetry.events[0]
    assert event.name == "ai_shield.policy.evaluate"
    assert event.attributes["decision"] == "allow"
    assert event.attributes["reason"] == "policy_satisfied"
    assert isinstance(event.attributes["duration_ms"], float)
    assert event.attributes["request_digest"] == engine.request_digest(request())


def test_telemetry_does_not_include_raw_resource_or_identity() -> None:
    telemetry = InMemoryTelemetry()
    engine = ShieldEngine(telemetry=telemetry)

    engine.evaluate(request())

    attributes = telemetry.events[0].attributes
    assert "resource" not in attributes
    assert "subject" not in attributes
    assert "agent_id" not in attributes
