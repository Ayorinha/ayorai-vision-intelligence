from ai_shield.mcp_security import ToolDefinition, ToolIntegrityRegistry
from ai_shield.publisher_auth import ManifestSigner, PublisherKey


def unsigned_tool() -> ToolDefinition:
    return ToolDefinition(
        name="ledger.read",
        description="Read approved records.",
        input_schema='{"type":"object"}',
        publisher="synthetic",
        endpoint="https://example.invalid/mcp",
        version="1.0.0",
    )


def signed_tool(key: PublisherKey) -> ToolDefinition:
    base = unsigned_tool()
    signature = ManifestSigner(key).sign(base.canonical())
    return ToolDefinition(
        **{**base.__dict__, "publisher_key_id": key.key_id, "signature": signature}
    )


def test_authenticated_publisher_accepts_valid_manifest():
    key = PublisherKey("synthetic-v1", b"test-only-key")
    registry = ToolIntegrityRegistry(
        trusted_publishers={key.key_id: key},
        require_publisher_auth=True,
    )
    tool = signed_tool(key)
    registry.pin(tool)
    assert registry.assess(tool).allowed


def test_authenticated_publisher_rejects_missing_signature():
    key = PublisherKey("synthetic-v1", b"test-only-key")
    registry = ToolIntegrityRegistry(
        trusted_publishers={key.key_id: key},
        require_publisher_auth=True,
    )
    assert registry.assess(unsigned_tool()).reason == "publisher_auth_required"


def test_authenticated_publisher_rejects_tampered_manifest():
    key = PublisherKey("synthetic-v1", b"test-only-key")
    registry = ToolIntegrityRegistry(
        trusted_publishers={key.key_id: key},
        require_publisher_auth=True,
    )
    tool = signed_tool(key)
    registry.pin(tool)
    tampered = ToolDefinition(
        **{**tool.__dict__, "description": "Read approved records and secrets."}
    )
    assert registry.assess(tampered).reason == "publisher_signature_invalid"
