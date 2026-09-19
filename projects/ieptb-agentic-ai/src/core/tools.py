from dataclasses import dataclass
from src.policy import Risk, authorize
from src.core.authz import Principal, Role, can_call
from src.core.validation import validate_remessa

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

def call_tool(tool: str, payload: dict, principal: Principal | None = None, target_tenant: str = "synthetic") -> ToolResult:
    principal = principal or Principal(tenant_id=target_tenant, role=Role.ANALYST)
    risk = TOOL_RISK.get(tool, Risk.HIGH)
    if not can_call(principal, tool, target_tenant):
        return ToolResult(tool, False, "Denied by tenant/role authorization.", False)
    decision = authorize(tool, risk)
    if not decision.allowed:
        return ToolResult(tool, False, decision.reason, decision.requires_human)
    if tool == "validate_remessa":
        return ToolResult(tool, True, str({"issues": validate_remessa(payload)}), False)
    return ToolResult(tool, True, f"synthetic:{tool}", decision.requires_human)
