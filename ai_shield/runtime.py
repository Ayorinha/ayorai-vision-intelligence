from __future__ import annotations

from dataclasses import dataclass

from .containment import ContainmentController
from .dataflow import DataFlowEvent, DataFlowGuard, FlowDecision
from .engine import ShieldEngine
from .mcp_security import ToolDefinition, ToolIntegrityRegistry
from .models import AgentRequest, Decision, PolicyResult


@dataclass(frozen=True)
class RuntimeRequest:
    request: AgentRequest
    tool: ToolDefinition
    data_flow: DataFlowEvent | None = None


class AgentRuntimeControlPlane:
    """Fail-closed control plane combining identity/policy, MCP integrity and data-flow controls."""

    def __init__(
        self,
        engine: ShieldEngine | None = None,
        tools: ToolIntegrityRegistry | None = None,
        dataflow: DataFlowGuard | None = None,
        containment: ContainmentController | None = None,
    ) -> None:
        self.engine = engine or ShieldEngine()
        self.tools = tools or ToolIntegrityRegistry()
        self.dataflow = dataflow or DataFlowGuard()
        self.containment = containment or ContainmentController()

    def evaluate(self, item: RuntimeRequest) -> PolicyResult:
        tool = self.tools.assess(item.tool)
        if not tool.allowed:
            self.containment.revoke_tool(item.tool.name)
            return PolicyResult(Decision.BLOCK, tool.reason, ("mcp_tool_integrity",))

        if not self.containment.can_execute(item.tool.name):
            return PolicyResult(Decision.ISOLATE, "runtime_containment_active", ("runtime_containment",))

        if item.data_flow is not None:
            flow = self.dataflow.evaluate(item.data_flow)
            if flow.decision == FlowDecision.BLOCK:
                return PolicyResult(Decision.BLOCK, flow.reason, ("data_flow_guard",))
            if flow.decision == FlowDecision.REVIEW:
                return PolicyResult(Decision.REVIEW, flow.reason, ("data_flow_guard",))

        return self.engine.evaluate(item.request)

    def contain(self, reason: str) -> None:
        self.containment.contain(reason)
        self.engine.emergency_isolate(reason)
