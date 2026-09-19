from src.mcp.server import mcp


def test_mcp_server_exposes_least_privilege_tools():
    names = {tool.name for tool in mcp._tool_manager.list_tools()}
    expected = {
        "get_track_summary",
        "get_low_confidence_events",
        "get_review_queue",
        "get_events",
        "search_knowledge",
    }
    assert expected <= names
    assert "approve_review" not in names
    assert "reject_review" not in names
