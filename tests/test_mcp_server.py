from src.mcp.server import mcp

def test_mcp_server_exposes_least_privilege_tools():
    names = {tool.name for tool in mcp._tool_manager.list_tools()}
    assert {"get_track_summary", "get_review_queue", "search_knowledge"} <= names
    assert "approve_review" not in names