from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generic_mcp_gateway_allows_read_only_tool():
    response = client.post(
        "/mcp/call/search_knowledge",
        json={"query": "retention", "top_k": 1},
    )
    assert response.status_code == 200


def test_generic_mcp_gateway_blocks_critical_tool():
    response = client.post(
        "/mcp/call/approve_review",
        json={"review_id": 1, "reviewer": "human", "human_approved": True},
    )
    assert response.status_code == 403


def test_generic_mcp_gateway_never_trusts_human_approval_from_caller():
    response = client.post(
        "/mcp/call/reject_review",
        json={"review_id": 1, "reviewer": "attacker", "human_approved": True},
    )
    assert response.status_code == 403
