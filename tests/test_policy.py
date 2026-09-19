import pytest

from src.core.policy import PolicyDenied, authorize_tool

def test_read_only_tool_is_allowed():
    policy = authorize_tool("search_knowledge", {"query": "retention"})
    assert policy.read_only is True
    assert policy.requires_human_approval is False

def test_critical_tool_requires_human_approval():
    with pytest.raises(PolicyDenied):
        authorize_tool("approve_review", {"review_id": 1, "reviewer": "human"})

    policy = authorize_tool("approve_review", {"review_id": 1, "reviewer": "human", "human_approved": True})
    assert policy.risk == "critical"