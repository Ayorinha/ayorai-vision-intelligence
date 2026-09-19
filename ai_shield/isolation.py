from dataclasses import dataclass, field
from enum import Enum

class IsolationState(str, Enum):
    ACTIVE = "active"
    ISOLATING = "isolating"
    ISOLATED = "isolated"
    RECOVERING = "recovering"

@dataclass
class SovereignIsolator:
    state: IsolationState = IsolationState.ACTIVE
    revoked_capabilities: set[str] = field(default_factory=set)
    reason: str | None = None
    def isolate(self, reason: str) -> None:
        self.state = IsolationState.ISOLATING
        self.reason = reason
        self.revoked_capabilities.update({"network_egress", "financial_execution", "restricted_data"})
        self.state = IsolationState.ISOLATED
    def can_execute(self, capability: str) -> bool:
        return self.state != IsolationState.ISOLATED and capability not in self.revoked_capabilities
    def recover(self) -> None:
        if self.state == IsolationState.ISOLATED:
            self.state = IsolationState.RECOVERING
            self.revoked_capabilities.clear()
            self.reason = None
            self.state = IsolationState.ACTIVE
