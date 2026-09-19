from dataclasses import dataclass
from enum import Enum


class Risk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Decision:
    allowed: bool
    requires_human: bool
    reason: str


def authorize(action: str, risk: Risk) -> Decision:
    """Deny-by-default policy boundary outside the LLM."""
    if risk is Risk.CRITICAL:
        return Decision(False, True, "Critical action requires human approval.")
    if action not in {"retrieve", "validate", "explain", "audit"}:
        return Decision(False, True, "Action is not in the public prototype allow-list.")
    return Decision(True, False, "Action allowed by deterministic policy.")
