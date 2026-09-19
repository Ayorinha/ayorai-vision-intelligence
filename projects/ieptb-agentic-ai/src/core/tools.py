from dataclasses import dataclass
from src.policy import Risk, authorize

@dataclass(frozen=True)
class ToolResult:
    tool: str
    allowed: bool
    output: str
    requires_human: bool

TOOL_RISK = {
    "search_procedure": Risk.LOW,
    "validate_remessa": Risk.MEDIUM,
    "create_review": Risk.HIGH,
    "release_remessa": Risk.CRITICAL,
}

def call_tool(tool: str, payload: dict) -> ToolResult:
    risk=TOOL_RISK.get(tool, Risk.HIGH)
    decision=authorize(tool, risk)
    if not decision.allowed:
        return ToolResult(tool, False, decision.reason, decision.requires_human)
    return ToolResult(tool, True, f"synthetic:{tool}:{payload}", decision.requires_human)
