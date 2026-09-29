from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ContainmentController:
    """Explicit runtime containment state for integrations above the policy engine."""

    session_suspended: bool = False
    network_egress_blocked: bool = False
    tool_access_revoked: set[str] = field(default_factory=set)
    subagents_denied: bool = False
    reason: str | None = None

    def contain(self, reason: str) -> None:
        self.session_suspended = True
        self.network_egress_blocked = True
        self.subagents_denied = True
        self.reason = reason

    def revoke_tool(self, tool_name: str) -> None:
        self.tool_access_revoked.add(tool_name)

    def can_execute(self, tool_name: str) -> bool:
        return not self.session_suspended and tool_name not in self.tool_access_revoked

    def release(self) -> None:
        self.session_suspended = False
        self.network_egress_blocked = False
        self.subagents_denied = False
        self.reason = None
