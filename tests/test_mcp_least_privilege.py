"""Regression tests for the MCP tool registry's least-privilege boundary.

Covers the suggested cases from issue #18: an allowed read-only operation,
a denied consequential operation, an unknown tool, and an unauthorized
capability (a tool registered without a matching policy entry). Everything
here runs against the in-process registry/policy layer only -- no real
external MCP target is contacted.
"""
import pytest

from src.core.policy import POLICIES, PolicyDenied
from src.mcp.registry import ToolRegistry
from src.mcp.tools import build_registry


def _echo(**kwargs):
    return kwargs


def test_allowed_read_only_operation_executes():
    registry = ToolRegistry()
    registry.register("search_knowledge", _echo)

    result = registry.call("search_knowledge", query="retention")

    assert result == {"query": "retention"}


def test_denied_consequential_operation_without_approval():
    registry = ToolRegistry()
    registry.register("approve_review", _echo)

    with pytest.raises(PolicyDenied):
        registry.call("approve_review", review_id=1, reviewer="human")


def test_unknown_tool_is_rejected_before_policy_check():
    registry = ToolRegistry()

    with pytest.raises(KeyError):
        registry.call("delete_everything")


def test_unauthorized_capability_without_policy_entry_is_denied():
    # Simulates a capability that was registered as a callable tool but
    # never given a least-privilege policy entry.
    registry = ToolRegistry()
    registry.register("run_shell_command", _echo)
    assert "run_shell_command" not in POLICIES

    with pytest.raises(PolicyDenied):
        registry.call("run_shell_command", command="rm -rf /")


def test_every_registered_capability_has_an_explicit_policy():
    # Guards against shipping a new MCP tool that silently has no
    # least-privilege policy entry.
    registry = build_registry()
    for name in registry.names():
        assert name in POLICIES, f"{name} is missing a least-privilege policy entry"
