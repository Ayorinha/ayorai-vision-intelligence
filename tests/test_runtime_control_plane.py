from ai_shield.dataflow import DataFlowEvent, DataFlowGuard
from ai_shield.mcp_security import ToolDefinition, ToolIntegrityRegistry
from ai_shield.models import AgentRequest, Classification, Decision, Identity
from ai_shield.runtime import AgentRuntimeControlPlane, RuntimeRequest


def make_request() -> AgentRequest:
    return AgentRequest(
        request_id="runtime-1",
        identity=Identity(subject="operator", role="analyst", assurance=3),
        agent_id="agent-a",
        capability="read_public",
        resource="ledger/demo",
        classification=Classification.PUBLIC,
    )


def make_tool(description: str = "Read approved records.") -> ToolDefinition:
    return ToolDefinition(
        name="ledger.read",
        description=description,
        input_schema='{"type":"object"}',
        publisher="synthetic",
        endpoint="https://example.invalid/mcp",
    )


def test_control_plane_requires_pinned_tool():
    tools = ToolIntegrityRegistry()
    control = AgentRuntimeControlPlane(tools=tools)
    result = control.evaluate(RuntimeRequest(make_request(), make_tool()))
    assert result.decision == Decision.BLOCK
    assert result.reason == "tool_not_pinned"


def test_control_plane_runs_policy_after_tool_integrity():
    tools = ToolIntegrityRegistry()
    tools.pin(make_tool())
    control = AgentRuntimeControlPlane(tools=tools)
    result = control.evaluate(RuntimeRequest(make_request(), make_tool()))
    assert result.decision == Decision.ALLOW


def test_control_plane_blocks_restricted_external_flow():
    tools = ToolIntegrityRegistry()
    tools.pin(make_tool())
    flow = DataFlowEvent(
        "operator",
        "agent-a",
        "ledger.read",
        "ledger/1",
        Classification.RESTRICTED,
        "https://attacker.invalid",
        10,
    )
    control = AgentRuntimeControlPlane(
        tools=tools,
        dataflow=DataFlowGuard(approved_destinations={"https://approved.invalid"}),
    )
    request = AgentRequest(
        **{
            **make_request().__dict__,
            "classification": Classification.RESTRICTED,
            "capability": "read_restricted",
        }
    )
    result = control.evaluate(RuntimeRequest(request, make_tool(), flow))
    assert result.decision == Decision.BLOCK
    assert result.reason == "restricted_data_external_destination"


def test_control_plane_containment_is_fail_closed():
    tools = ToolIntegrityRegistry()
    tools.pin(make_tool())
    control = AgentRuntimeControlPlane(tools=tools)
    control.contain("subagent_escape_attempt")
    result = control.evaluate(RuntimeRequest(make_request(), make_tool()))
    assert result.decision in {Decision.BLOCK, Decision.ISOLATE}
