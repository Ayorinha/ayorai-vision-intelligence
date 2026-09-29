from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .models import Classification


class FlowDecision(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    REVIEW = "review"


@dataclass(frozen=True)
class DataFlowEvent:
    principal: str
    agent_id: str
    tool_name: str
    asset_id: str
    sensitivity: Classification
    destination: str
    bytes_out: int = 0


@dataclass(frozen=True)
class DataFlowResult:
    decision: FlowDecision
    reason: str


class DataFlowGuard:
    """Deterministic outbound-data policy; it does not inspect model intent."""

    def __init__(
        self,
        approved_destinations: set[str] | None = None,
        volume_limit: int = 1_000_000,
    ) -> None:
        self.approved_destinations = set(approved_destinations or set())
        self.volume_limit = volume_limit

    def evaluate(self, event: DataFlowEvent) -> DataFlowResult:
        if event.sensitivity == Classification.RESTRICTED:
            if event.destination not in self.approved_destinations:
                return DataFlowResult(
                    FlowDecision.BLOCK,
                    "restricted_data_external_destination",
                )
        if event.bytes_out < 0:
            return DataFlowResult(FlowDecision.BLOCK, "invalid_output_volume")
        if event.bytes_out > self.volume_limit:
            return DataFlowResult(FlowDecision.REVIEW, "output_volume_exceeds_profile")
        return DataFlowResult(FlowDecision.ALLOW, "data_flow_policy_satisfied")
