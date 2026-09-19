from src.core.tools import call_tool

def test_unknown_tool_is_denied():
    result=call_tool("dump_database", {})
    assert result.allowed is False

def test_release_requires_human():
    result=call_tool("release_remessa", {"remessa_id":"R-001"})
    assert result.allowed is False
    assert result.requires_human is True
