import pytest

from src.core.policy import PolicyDenied
from src.mcp.registry import ToolRegistry


def test_registry_denies_unknown_tool():
    registry = ToolRegistry()
    with pytest.raises(KeyError):
        registry.call("not_registered")


def test_registry_requires_approval_for_critical_tool():
    registry = ToolRegistry()
    registry.register("approve_review", lambda review_id, reviewer="human": {"approved": review_id})

    with pytest.raises(PolicyDenied):
        registry.call("approve_review", review_id=1, reviewer="reviewer")

    result = registry.call(
        "approve_review",
        review_id=1,
        reviewer="reviewer",
        human_approved=True,
    )
    assert result == {"approved": 1}


def test_registry_does_not_forward_control_metadata():
    received = {}

    def handler(**kwargs):
        received.update(kwargs)
        return kwargs

    registry = ToolRegistry()
    registry.register("search_knowledge", handler)

    registry.call("search_knowledge", query="policy", human_approved=True)

    assert received == {"query": "policy"}
