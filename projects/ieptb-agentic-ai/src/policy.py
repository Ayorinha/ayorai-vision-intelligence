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

SAFE_ACTIONS = {"search_procedure", "validate_remessa", "create_review"}

def authorize(action: str, risk: Risk) -> Decision:
    """Deterministic authorization boundary. Model output is never the authority."""
    if risk is Risk.CRITICAL:
        return Decision(False, True, "Critical action requires human approval.")
    if action not in SAFE_ACTIONS:
        return Decision(False, True, "Action is not in the explicit public-prototype allow-list.")
    return Decision(True, False, "Action allowed by deterministic policy.")
