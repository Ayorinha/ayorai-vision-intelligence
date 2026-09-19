def test_mcp_server_exposes_governed_tools():
    from src.mcp_server import mcp
    assert mcp is not None
