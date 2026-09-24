from fastapi import FastAPI, HTTPException
from src.core.policy import POLICIES, PolicyDenied
from src.mcp.registry import ToolRegistry
from src.mcp.tools import build_registry

mcp_app = FastAPI(title="AYORAI Tool Gateway")
registry: ToolRegistry = build_registry()


@mcp_app.get("/mcp/tools")
def tools():
    return {"transport": "HTTP tool gateway", "tools": registry.names()}


@mcp_app.post("/mcp/call/{name}")
def call(name: str, arguments: dict | None = None):
    """Expose read-only tools only through the legacy internal HTTP gateway."""
    policy = POLICIES.get(name)
    if policy is None:
        raise HTTPException(404, "Tool not found")
    if not policy.read_only or policy.requires_human_approval:
        raise HTTPException(
            403,
            "Critical or state-changing tools must use the dedicated review workflow",
        )
    try:
        return {"result": registry.call(name, **(arguments or {}))}
    except PolicyDenied as exc:
        raise HTTPException(403, str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
