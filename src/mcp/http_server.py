from fastapi import FastAPI
from src.mcp.registry import ToolRegistry
from src.mcp.tools import build_registry
from src.vision.tracker import TrackStore

mcp_app = FastAPI(title="AYORAI MCP Tool Gateway")
registry: ToolRegistry = build_registry(TrackStore())

@mcp_app.get("/mcp/tools")
def tools():
    return {"tools": registry.names()}

@mcp_app.post("/mcp/call/{name}")
def call(name: str, arguments: dict | None = None):
    return {"result": registry.call(name, **(arguments or {}))}
