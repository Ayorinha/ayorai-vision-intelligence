from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ToolPolicy:
    risk: str
    read_only: bool
    requires_human_approval: bool

POLICIES: dict[str, ToolPolicy] = {
    "get_track_history": ToolPolicy("low", True, False),
    "get_track_summary": ToolPolicy("low", True, False),
    "get_low_confidence_events": ToolPolicy("low", True, False),
    "get_review_queue": ToolPolicy("low", True, False),
    "get_events": ToolPolicy("low", True, False),
    "search_knowledge": ToolPolicy("low", True, False),
    "export_annotations": ToolPolicy("medium", True, False),
    "approve_review": ToolPolicy("critical", False, True),
    "reject_review": ToolPolicy("critical", False, True),
}

class PolicyDenied(PermissionError):
    """Raised when a tool call violates the deterministic safety policy."""

def authorize_tool(name: str, arguments: dict[str, Any]) -> ToolPolicy:
    policy = POLICIES.get(name)
    if policy is None:
        raise PolicyDenied(f"Tool '{name}' is not registered in the policy matrix")
    if policy.requires_human_approval and arguments.get("human_approved") is not True:
        raise PolicyDenied(f"Tool '{name}' requires explicit human approval")
    if policy.requires_human_approval and not arguments.get("reviewer"):
        raise PolicyDenied(f"Tool '{name}' requires a reviewer identity")
    return policy