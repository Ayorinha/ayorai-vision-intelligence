from src.core.policy import PolicyDenied, authorize_tool


def test_critical_tool_requires_human_approval():
    try:
        authorize_tool("approve_review", {})
    except PolicyDenied:
        return
    raise AssertionError("critical tool must be denied without approval")


def test_critical_tool_requires_reviewer_identity():
    try:
        authorize_tool("approve_review", {"human_approved": True})
    except PolicyDenied:
        return
    raise AssertionError("critical tool must be denied without reviewer identity")


def test_read_only_tool_is_allowed_without_approval():
    authorize_tool("get_track_summary", {})


def test_unknown_tool_is_denied():
    try:
        authorize_tool("unregistered_tool", {})
    except PolicyDenied:
        return
    raise AssertionError("unknown tool must be denied")
