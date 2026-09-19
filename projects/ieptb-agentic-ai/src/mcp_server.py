"""Public-safe MCP server exposing governed synthetic remessa tools.

Uses the official MCP Python SDK v2. The MCP boundary delegates authorization to
our deterministic policy layer; the model/client never receives unrestricted tools.
"""
from typing import Any
from mcp.server import MCPServer

from src.core.validation import validate_remessa

mcp = MCPServer("ieptb-agentic-ai")

@mcp.tool()
def validate_synthetic_remessa(remessa_id: str, quantidade_titulos: int, valor_total: float, arquivo: str) -> dict[str, Any]:
    """Validate a synthetic remessa without performing a side effect."""
    issues = validate_remessa({"remessa_id": remessa_id, "quantidade_titulos": quantidade_titulos, "valor_total": valor_total, "arquivo": arquivo})
    return {"remessa_id": remessa_id, "valid": not issues, "issues": issues, "synthetic": True}

@mcp.tool()
def explain_safety_boundary() -> str:
    """Explain why consequential operations require deterministic policy and human approval."""
    return "LLM reasoning is advisory; authorization is deterministic; critical actions require human approval."

if __name__ == "__main__":
    mcp.run(transport="streamable-http", json_response=True)
